from langchain_core.language_models import LanguageModelLike
from core.llm.llm_chat import LLMChat
from langchain_ollama import ChatOllama
from typing import Optional


class OllamaLlm(LLMChat):
    """
    OllamaLlm 类 - 封装 Ollama 本地模型服务

    该类继承自 LLMChat，提供了与 Ollama 模型服务的集成实现。
    它通过变量加载配置信息，并创建对应的语言模型实例。
    """
    ENABLED = True  # 指定该模型是否启用

    def is_enable(self) -> bool:
        """
        检查当前模型是否启用

        Returns:
            bool: 返回 True 表示模型启用
        """
        return self.ENABLED

    def name(self) -> Optional[str]:
        """
        获取模型的名称

        Returns:
            Optional[str]: 模型名称
        """
        return "Ollama"

    def get_llm_model(self, api_key: str, base_url: str, model: str) -> Optional[LanguageModelLike]:
        """
        获取 Ollama 语言模型实例

        Args:
            api_key (str): API密钥（Ollama本地运行不需要此参数）
            base_url (str): API Base URL
            model (str): 使用的模型名称

        Returns:
            Optional[LanguageModelLike]: 返回一个 ChatOllama 实例，用于流式生成响应。
            如果创建实例失败，返回 None。

        Raises:
            Exception: 当创建 ChatOllama 实例时发生错误
        """
        try:
            return ChatOllama(
                model=model,          # 使用的模型名称
                base_url=base_url,    # API Base URL
                temperature=0.6,
                streaming=True,       # 启用流式响应
            )
        except Exception as e:
            # 这里可以添加日志记录
            raise Exception(f"Failed to create ChatOllama instance: {str(e)}")