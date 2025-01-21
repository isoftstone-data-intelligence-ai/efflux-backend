import os
from langchain_core.language_models import LanguageModelLike
from core.llm.llm_chat import LLMChat
from langchain_openai import AzureChatOpenAI
from typing import Union
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


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
        return True

    def name(self) -> Union[str, None]:
        """
        获取模型的名称

        Returns:
            Union[str, None]: 模型名称，返回 "AzureLlm" 表示当前模型。
        """
        return "AzureLlm"

    def get_llm_model(self) -> Union[LanguageModelLike, None]:
        """
        获取 Azure OpenAI 服务的语言模型实例

        通过环境变量加载 Azure OpenAI 服务的配置，创建一个 AzureChatOpenAI 实例。

        Returns:
            Union[LanguageModelLike, None]: 返回一个 AzureChatOpenAI 实例，用于流式生成响应。
        """
        return AzureChatOpenAI(
            deployment_name=os.environ['DEPLOYMENT_NAME'],  # Azure 部署名称
            openai_api_key=os.environ['AZURE_API_KEY'],      # Azure OpenAI API 密钥
            azure_endpoint=os.environ['AZURE_ENDPOINT'],     # Azure 服务端点
            openai_api_version=os.environ['AZURE_API_VERSION'],  # Azure OpenAI API 版本
            temperature=0.7,  # 模型生成文本的随机性参数
            streaming=True,   # 启用流式响应
        )
