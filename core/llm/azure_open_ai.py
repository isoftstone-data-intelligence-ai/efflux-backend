from langchain_core.language_models import LanguageModelLike
from core.llm.llm_chat import LLMChat
from langchain_openai import AzureChatOpenAI
from typing import Optional


class AzureLlm(LLMChat):
    """
    AzureLlm 类 - 封装 Azure OpenAI 服务作为语言模型

    该类继承自 LLMChat，提供了与 Azure OpenAI 集成的具体实现。
    它通过读取环境变量获取 Azure OpenAI 服务的配置信息，并创建语言模型实例。
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
        return "Azure"

    def get_llm_model(self, api_key: str, base_url: str, model: str) -> Optional[LanguageModelLike]:
        """
        获取 Azure OpenAI 服务的语言模型实例

        Args:
            api_key (str): API 密钥
            base_url (str): API Base URL
            model (str): 使用的模型名称

        Returns:
            Optional[LanguageModelLike]: 返回一个 AzureChatOpenAI 实例，用于流式生成响应。
            如果创建实例失败，返回 None。

        Raises:
            Exception: 当创建 AzureChatOpenAI 实例时发生错误
        """
        try:
            return AzureChatOpenAI(
                openai_api_key=api_key,     # Azure OpenAI API 密钥
                azure_endpoint=base_url,    # Azure 服务端点
                openai_api_version=model,   # Azure OpenAI API 版本
                streaming=True,             # 启用流式响应
            )
        except Exception as e:
            # 这里可以添加日志记录
            raise Exception(f"Failed to create AzureChatOpenAI instance: {str(e)}")