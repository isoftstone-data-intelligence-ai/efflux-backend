from langchain_core.language_models import LanguageModelLike
from core.llm.llm_chat import LLMChat
from langchain_openai import ChatOpenAI
from typing import Optional


class OpenAILlm(LLMChat):

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
        return "OpenAILlm"

    def get_llm_model(self, api_key: str, base_url: str, model: str) -> Optional[LanguageModelLike]:
        """
        获取 OpenAI SDK 兼容的 LLM 实例

        Args:
            api_key (str): API 密钥
            base_url (str): API Base URL
            model (str): 使用的模型名称

        Returns:
            Optional[LanguageModelLike]: 返回一个 ChatOpenAI 实例，用于流式生成响应。
            如果创建实例失败，返回 None。

        Raises:
            Exception: 当创建 ChatOpenAI 实例时发生错误
        """
        try:
            return ChatOpenAI(
                api_key=api_key,      # API 密钥
                base_url=base_url,    # API Base URL
                model=model,          # 使用的模型名称
                streaming=True,       # 启用流式响应
            )
        except Exception as e:
            # 这里可以添加日志记录
            raise Exception(f"Failed to create ChatOpenAI instance: {str(e)}")