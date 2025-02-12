import os
from langchain_core.language_models import LanguageModelLike
from core.llm.llm_chat import LLMChat
from langchain_openai import ChatOpenAI
from typing import Union, Optional


class OpenAILlm(LLMChat):

    ENABLED = True  # 指定该模型是否启用

    def is_enable(self) -> bool:
        """
        检查当前模型是否启用

        Returns:
            bool: 返回 True 表示模型启用
        """
        return self.ENABLED

    def name(self) -> Union[str, None]:
        """
        获取模型的名称

        Returns:
            Union[str, None]: 模型名称，返回 "DoubaoLlm" 表示当前模型。
        """
        return self.name

    def get_llm_model(self, api_key, base_url, model) -> Optional[LanguageModelLike]:
        """
        获取 OpenAI SDK 兼容的 LLM 实例

        Returns:
            Optional[LanguageModelLike]: 返回一个 ChatOpenAI 实例，用于流式生成响应。
        """
        return ChatOpenAI(
            api_key=api_key,      # 豆包 API 密钥
            base_url=base_url,    # 豆包服务的基础 URL
            model=model,          # 使用的模型名称
            streaming=True,                            # 启用流式响应
        )