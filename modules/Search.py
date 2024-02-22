import requests

from loguru import logger

from fastapi import HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse


class Search:

    def __init__(self, Bing_config: dict):

        self.subscription_key = Bing_config.get("subscription_key", None)


        # Search engine related. You don't really need to change this.
        self.BING_SEARCH_V7_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
        self.BING_MKT = "en-US"

        # Specify the number of references from the search engine you want to use.
        # 8 is usually a good number.
        self.REFERENCE_COUNT = 8

        # Specify the default timeout for the search engine. If the search engine
        # does not respond within this time, we will return an error.
        self.DEFAULT_SEARCH_ENGINE_TIMEOUT = 5

        # If the user did not provide a query, we will use this default query.
        self._default_query = "Who said 'live long and prosper'?"

        # This is really the most important part of the rag model. It gives instructions
        # to the model on how to generate the answer. Of course, different models may
        # behave differently, and we haven't tuned the prompt to make it optimal - this
        # is left to you, application creators, as an open problem.
        self._rag_query_text = """
        你是大型语言人工智能助手。你将接收到一个用户问题，请针对该问题提供清晰、简洁且准确的答案。你将获得一系列与问题相关的上下文信息，如果适用，请使用上下文信息。

        你的答案必须正确、准确，并且以专家的角度用客观、专业的语气撰写。请将回答限制在1024个字符内。不要提供与问题无关的信息，也不要重复。如果给定的上下文没有提供足够的信息，请在相关主题后注明“信息缺失”。
        
        除了代码、特定的名称和引用外，你的答案必须使用与问题相同的语言撰写，一定要用中文回答中文问题。
        
        以下是上下文信息集：
        
        {context}
        
        请记住，不要盲目地逐字重复上下文内容。以下是用户的问题：
        """



    def search_with_bing(self, query: str):
        """
        Search with bing and return the contexts.
        """


        params = {"q": query, "mkt": self.BING_MKT}


        response = requests.get(
            self.BING_SEARCH_V7_ENDPOINT,
            headers={"Ocp-Apim-Subscription-Key": self.subscription_key},
            params=params,
            timeout=self.DEFAULT_SEARCH_ENGINE_TIMEOUT,
        )
        if not response.ok:
            logger.error(f"{response.status_code} {response.text}")
            raise HTTPException(response.status_code, "Search engine error.")
        json_content = response.json()
        try:
            contexts = json_content["webPages"]["value"][:self.REFERENCE_COUNT]
            prompt = self.search_prompt(contexts) + query
            print("prompt:", prompt)
        except KeyError:
            logger.error(f"Error encountered: {json_content}")
            return []
        return prompt

    def search_prompt(self, contexts: list[dict[str, any]]):
        system_prompt = self._rag_query_text.format(
            context="\n\n".join(
                [f"[[{i + 1}]] {c['snippet']}" for i, c in enumerate(contexts)]
            )
        )
        return system_prompt





if __name__ == '__main__':
    raise NotImplementedError("This module is not runnable!")