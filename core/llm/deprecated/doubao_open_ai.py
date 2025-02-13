import os
from langchain_core.language_models import LanguageModelLike
from core.llm.llm_chat import LLMChat
from langchain_openai import ChatOpenAI
from typing import Union
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class DoubaoLlm(LLMChat):
    """
    DoubaoLlm 类 - 封装豆包自研语言模型

    该类继承自 LLMChat，提供了与豆包自研语言模型（Doubao LLM）的集成实现。
    它通过环境变量加载配置信息，并创建对应的语言模型实例。
    """
    ENABLED = True  # 指定该模型是否启用

    def is_enable(self) -> bool:
        """
        检查当前模型是否启用

        Returns:
            bool: 返回 True 表示模型启用
        """
        return True

    def name(self) -> Union[str, None]:
        """
        获取模型的名称

        Returns:
            Union[str, None]: 模型名称，返回 "DoubaoLlm" 表示当前模型。
        """
        return "DoubaoLlm"

    def get_llm_model(self) -> Union[LanguageModelLike, None]:
        """
        获取豆包语言模型实例

        通过环境变量加载豆包语言模型的配置，创建一个 ChatOpenAI 实例。

        Returns:
            Union[LanguageModelLike, None]: 返回一个 ChatOpenAI 实例，用于流式生成响应。
        """
        return ChatOpenAI(
            api_key=os.environ['DOUBAO_API_KEY'],      # 豆包 API 密钥
            base_url=os.environ['DOUBAO_BASE_URL'],    # 豆包服务的基础 URL
            model=os.environ['DOUBAO_MODEL'],          # 使用的模型名称
            streaming=True,                            # 启用流式响应
        )
