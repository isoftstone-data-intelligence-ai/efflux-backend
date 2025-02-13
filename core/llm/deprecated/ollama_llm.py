import os
from langchain_core.language_models import LanguageModelLike
from core.llm.llm_chat import LLMChat
from langchain_ollama import ChatOllama
from typing import Union
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class OllamaLlm(LLMChat):
    """
    OllamaLlm 类 - 封装 Ollama 本地模型服务
    
    该类继承自 LLMChat，提供了与 Ollama 模型服务的集成实现。
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
            Union[str, None]: 模型名称，返回 "OllamaLlm" 表示当前模型。
        """
        return "OllamaLlm"

    def get_llm_model(self) -> Union[LanguageModelLike, None]:
        """
        获取 Ollama 语言模型实例
        
        通过环境变量加载 Ollama 配置，创建一个 ChatOllama 实例。
        
        Returns:
            Union[LanguageModelLike, None]: 返回一个 ChatOllama 实例，用于流式生成响应。
        """
        return ChatOllama(
            model=os.environ['OLLAMA_MODEL'],
            base_url=os.environ['OLLAMA_BASE_URL'],
            temperature=0.6,
            streaming=True,
        ) 