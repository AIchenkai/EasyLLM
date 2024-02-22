"""本文件中声明了一些常用的函数与全局变量，供其他模块使用。"""
from json import load
from enum import Enum
import os

try:
    with open('config.json') as f:
        Configs = load(f)
except FileNotFoundError:
    raise FileNotFoundError(
        "Config file not found! Please make sure you have a 'config.json' file in {}.".format(os.getcwd()))


def getAvatars():
    """
    返回用户头像和bot头像的url链接
    """
    return (
        "/root/projects/gpt2_cn/EasyLLM/assets/pic/user.png",
        "/root/projects/gpt2_cn/EasyLLM/assets/pic/bot.png"
    )


class NLGEnum(Enum):
    """聊天机器人类型枚举"""
    Azure = 0
    ChatGLM = 1  # 原始ChatGLM模型





if __name__ == '__main__':
    raise RuntimeError("This module is not executable!")
