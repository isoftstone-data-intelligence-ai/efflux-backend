import os
from langchain_core.language_models import LanguageModelLike
from core.llm.llm_chat import LLMChat
from langchain_openai import ChatOpenAI
from typing import Union
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class QwenLlm(LLMChat):
    """
    实现了LLMChat接口的具体语言模型类，用于与名为'Qwen'的语言模型交互。

    Attributes:
        ENABLED (bool): 表示该模型是否启用的常量。
    """

    ENABLED = True

    def is_enable(self) -> bool:
        """
        检查QwenLlm是否已启用。

        Returns:
            bool: 总是返回True，表示此实现总是启用的。
        """
        return True

    def name(self) -> Union[str, None]:
        """
        获取此语言模型的名称。

        Returns:
            str: 返回代表语言模型名称的字符串 "QwenLlm"。
        """
        return "QwenLlm"

    def get_llm_model(self) -> Union[LanguageModelLike, None]:
        """
        获取配置好的Qwen语言模型实例。

        该方法从环境变量中读取必要的配置信息（如API密钥、基础URL和模型名称），
        并创建一个启用了流式传输的ChatOpenAI实例来作为语言模型。

        Returns:
            LanguageModelLike: 配置好的语言模型实例，或None如果创建失败。
        """
        return ChatOpenAI(
            api_key=os.environ['DASHSCOPE_API_KEY'],
            base_url=os.environ['QWEN_BASE_URL'],
            model=os.environ['QWEN_MODEL'],
            streaming=True,
        )

