"""该文件定义了聊天机器人的后端类"""
from abc import abstractmethod
from urllib.parse import urljoin

import requests
import openai

from modules.utils import NLGEnum


class NLGBase:
    """聊天机器人基类，建议在进行聊天机器人开发时继承该类"""

    def __init__(self, botType: NLGEnum, model: str, prompt: str = None):
        self.type = botType  # 机器人类型
        self.model = model  # 机器人模型
        self.prompt = prompt  # 默认提示语(用于指定机器人的身份，有助于提高针对特定领域问题的效果)，优先级低于查询时传入的prompt

    @abstractmethod
    def singleQuery(self, message: str, prompt: str = None) -> str:
        """
        简单地进行单次查询，详细文档请参考各子类的实现

        :param message: str 用户输入的消息
        :param prompt: str 提示语(用于指定机器人的身份，有助于提高针对特定领域问题的效果)
        :return: 响应结果
        """
        pass

    @abstractmethod
    def continuedQuery(self, message, history: [[str, str]], prompt: str = None):
        """
        进行带有历史记录的查询，详细文档请参考各子类的实现

        :param message: str 用户输入的消息
        :param history: [[str, str]...] 分别为用户输入和机器人回复(先前的)
        :param prompt: str 提示语(用于指定机器人的身份，有助于提高针对特定领域问题的效果)
        """
        pass

    def historyConverter(self, history: [[str, str]], prompt: str = None):
        """
        将[[str, str]...]形式的历史记录转换为[{"role": "user", "content": ""}, {"role": "assistant", "message": ""}...]的格式，
        使用场景是将gradio的Chatbot聊天记录格式转换为ChatGPT/ChatGLM3的聊天记录格式
        :param history: [[str, str]...] 分别为用户输入和机器人回复(先前的)
        :param prompt: str 提示语(用于指定机器人的身份，有助于提高针对特定领域问题的效果，允许为空)
        :return: [{"role": "user", "content": ""}, {"role": "assistant", "message": ""}...]的格式的历史记录，注意，该结果不包括
        本次的用户输入
        """
        sessionPrompt = prompt if prompt else self.prompt
        sessionHistory = [{"role": "system", "content": sessionPrompt}] if sessionPrompt else []
        for chat in history:
            sessionHistory.append({"role": "user", "content": chat[0]})
            sessionHistory.append({"role": "assistant", "content": chat[1]})
        return sessionHistory


class ChatGLM(NLGBase):
    """
    调用远端ChatGLM进行问答

    目标项目来自：https://github.com/THUDM/ChatGLM3
    """

    def __init__(self, ChatGLM_config: dict, prompt: str = None):
        super().__init__(NLGEnum.ChatGLM, ChatGLM_config.get("model", "NLG/ChatGLM2"), prompt)
        self.host, self.secret = None, None
        self.mode = ChatGLM_config.get("mode", "remote")
        if self.mode == "remote":
            self.host = ChatGLM_config.get("host", None)
            self.secret = ChatGLM_config.get("secret", None)
            if not self.host:
                raise ValueError("ChatGLM host is not set! Please check your 'config.json' file.")
            self.checkConnection()
        else:
            raise NotImplementedError("ChatGLM local mode is not implemented yet!")

    def singleQuery(self, message: str, prompt: str = None) -> str:
        """
        简单地进行单次查询

        在单次查询中也可以传入先前的历史记录，作为单次查询的辅助信息，但该历史记录并不会被记录和更新，在单词查询中仅被用作辅助机器人决策。
        :param message: str 本次用户输入
        :param prompt: str 提示语(用于指定机器人的身份，有助于提高针对特定领域问题的效果)
        :return: str 对本次聊天的回复内容
        """
        sessionPrompt = prompt if prompt else self.prompt
        try:
            response = requests.post(
                url=urljoin(self.host, 'singleQuery'),
                params={"secret": self.secret},
                json={"prompt": sessionPrompt, "message": message},
                timeout=20
            )
        except requests.exceptions.Timeout:
            raise TimeoutError("Connection to ChatGLM timed out, please check your network status.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection to ChatGLM failed, please check your host and secret.")
        return response.json().get("content", "")

    def continuedQuery(self, message: str, history: [[str, str]], prompt: str = None) -> str:
        """
        进行带有历史记录的查询

        按照gradio官方demo chatbot_simple的开发示例，若是想实现带有历史记录的对话，无需在BotBase中自行实现历史记录的保留，建议的做法
        是在gradio中更新历史记录，每次查询时只需要调用更新后的history即可。该方法只需按照OpenAI API的要求，将[[str, str]...]形式的
        历史记录转换为[{"role": "user", "content": ""}, {"role": "assistant", "message": ""}...]的格式即可。
        :param message: str 本次用户输入
        :param history: [[str, str]...] 分别为用户输入和机器人回复(先前的)
        :param prompt: str 提示语(用于指定机器人的身份，有助于提高针对特定领域问题的效果)
        """
        sessionHistory = self.historyConverter(history, prompt)
        print("message:", message)
        print("history:", history)
        print("prompt:", prompt)
        print("sessionHistory:", sessionHistory)
        try:
            response = requests.post(
                url=urljoin(self.host, 'continuedQuery'),
                params={"secret": self.secret},
                json={"history": sessionHistory, "message": message},
                timeout=100
            )
            print("NLG-response:", response.json())
        except requests.exceptions.Timeout:
            raise TimeoutError("Connection to ChatGLM timed out, please check your network status.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection to ChatGLM failed, please check your host and secret.")
        return response.json().get("content", "")

    def checkConnection(self):
        """
        检查与远端ChatGLM的连接状态
        :return: bool 是否连接成功
        """
        try:
            response = requests.get(
                url=self.host,
                params={"secret": self.secret},
                timeout=10
            )
            if not response.status_code == 200:
                raise ConnectionError(f"Connection to {self.model} failed, please check your host and secret.")
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Connection to {self.model} timed out, please check your network status.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Connection to {self.model} failed, please check your host and secret.")
        finally:
            print("ChatGLM remote mode connection check finished.")



class Azure(NLGBase):
    """
    通过API调用Azure OpenAI进行问答

    API文档参考：
    """

    def __init__(self, Azure_config: dict, prompt: str = None):
        super().__init__(NLGEnum.Azure, Azure_config.get("azure_model", "gpt-4"), prompt)
        self.api_key = Azure_config.get("api_key", None)
        if not self.api_key:
            raise ValueError("Azure OpenAI api_key is not set! Please check your 'config.json' file.")
        self.api_base = Azure_config.get("api_base", None)
        if not self.api_base:
            raise ValueError("Azure OpenAI api_base is not set! Please check your 'config.json' file.")
        self.api_version = Azure_config.get("api_version", None)
        if not self.api_version:
            raise ValueError("Azure OpenAI api_version is not set! Please check your 'config.json' file.")
        self.api_type = Azure_config.get("api_type", None)
        if not self.api_type:
            raise ValueError("Azure OpenAI api_type is not set! Please check your 'config.json' file.")

        self.engine = Azure_config.get("engine", "gpt4test")  # 引擎名称
        self.host = openai
        self.host.api_type = self.api_type
        self.host.api_base = self.api_base
        self.host.api_version = self.api_version
        self.host.api_key = self.api_key

    def singleQuery(self, message: str, prompt: str = None) -> str:
        """
        简单地进行单次查询

        在单次查询中也可以传入先前的历史记录，作为单次查询的辅助信息，但该历史记录并不会被记录和更新，在单词查询中仅被用作辅助机器人决策。
        :param message: str 本次用户输入
        :param prompt: str 提示语(用于指定机器人的身份，有助于提高针对特定领域问题的效果)
        :return str 对本次聊天的回复内容
        """
        sessionPrompt = prompt if prompt else self.prompt
        sessionMessage = [
            {"role": "system", "content": sessionPrompt},
            {"role": "user", "content": message}
        ] if sessionPrompt else [
            {"role": "user", "content": message}
        ]
        session = self.host.ChatCompletion.create(
            engine=self.engine,  # 使用设定的引擎名称
            messages=sessionMessage,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return session.choices[0].message.content

    def continuedQuery(self, message, history: [[str, str]], prompt: str = None):
        """
        进行带有历史记录的查询

        按照gradio官方demo chatbot_simple的开发示例，若是想实现带有历史记录的对话，无需在BotBase中自行实现历史记录的保留，建议的做法
        是在gradio中更新历史记录，每次查询时只需要调用更新后的history即可。该方法只需按照OpenAI API的要求，将[[str, str]...]形式的
        历史记录转换为[{"role": "user", "content": ""}, {"role": "assistant", "message": ""}...]的格式即可。
        :param message: str 本次用户输入
        :param history: [[str, str]...] 分别为用户输入和机器人回复(先前的)
        :param prompt: str 提示语(用于指定机器人的身份，有助于提高针对特定领域问题的效果)
        """
        sessionHistory = self.historyConverter(history, prompt)
        sessionHistory.append({"role": "user", "content": message})
        session = self.host.ChatCompletion.create(
            engine=self.engine,
            messages=sessionHistory,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return session.choices[0].message.content

    def checkConnection(self):
        """
        检查与Azure OpenAI的连接状态(通过测试Chat API)
        :return: bool 是否连接成功
        """
        try:
            response = requests.post(
                url=f"{self.api_base}/v1/engines/{self.engine}/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": self.engine,
                    "messages": [{"role": "user", "content": "Say this is a test!"}]
                },
                timeout=10
            )
            if not response.status_code == 200:
                raise ConnectionError(f"Connection to {self.engine} failed, please check your host and secret.")
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Connection to {self.engine} timed out, please check your network status.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Connection to {self.engine} failed, please check your host and secret.")
        finally:
            print("Azure OpenAI connection check finished.")




if __name__ == '__main__':
    raise NotImplementedError("This module is not runnable!")
