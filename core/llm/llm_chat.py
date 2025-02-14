from abc import ABC, abstractmethod
from typing import Union, AsyncGenerator, Any, List, Optional
from langchain_core.language_models import LanguageModelLike
from core.llm.llm_message import LLMMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage
from core.common.logger import get_logger

logger = get_logger(__name__)


class LLMChat(ABC):
    """
    抽象类用于定义与语言模型进行对话的基础接口。
    """

    def __init__(self):
        """
        初始化
        """

    @abstractmethod
    def is_enable(self) -> bool:
        """
        检查是否启用了LLMChat服务。

        Returns:
            bool: 如果服务可用则返回True，否则返回False。
        """

    @abstractmethod
    def name(self) -> Optional[str]:
        """
        获取聊天模块的名称。

        Returns:
            Optional[str]: 聊天模块的名称或None如果未指定。
        """

    @abstractmethod
    def get_llm_model(self, api_key: str, base_url: str, model: str) -> Optional[LanguageModelLike]:
        """
        获取当前使用的语言模型。

        Args:
            api_key (str): API密钥
            base_url (str): API Base URL
            model (str): 模型名称

        Returns:
            Optional[LanguageModelLike]: 语言模型实例或None如果未指定。
        """

    async def stream_chat(self, inputs: Union[dict[str, Any], Any], tools: List[BaseTool],
                          api_key: str, base_url: str, model: str,
                          callback=None) -> \
            AsyncGenerator[LLMMessage, None]:
        """
        异步流式处理用户输入并与语言模型交互。

        Args:
            inputs (Union[dict[str, Any], Any]): 用户输入的数据。
            tools (List[BaseTool]): 工具列表，可以被语言模型使用。
            callback (callable, optional): 完成后的回调函数。
            api_key : 模型api_key
            base_url : 模型官网访问地址
            model : 模型名称 & 版本号
        Yields:
            LLMMessage: 包含从语言模型获得的消息或工具调用信息。
        """
        # 收集流数据的容器
        collected_data = {
            "messages": [],  # 存储接收到的消息内容
            "tool_calls": [],  # 存储工具调用记录
            "tool_errors": []  # 存储工具调用错误
        }

        # llm_model (LanguageModelLike): 语言模型实例
        llm_model = self.get_llm_model(api_key,base_url,model)

        graph = create_react_agent(model=llm_model, tools=tools)

        async for chunk in graph.astream(inputs, stream_mode=["messages", "values"]):
            # chat消息获取
            if isinstance(chunk, tuple) and chunk[0] == "messages":
                message_chunk = chunk[1][0]  # Get the message content
                if isinstance(message_chunk, AIMessageChunk):
                    if message_chunk.content != '':
                        # chat结果收集
                        collected_data["messages"].append(message_chunk.content)
                        yield LLMMessage(content=message_chunk.content, type="message")
            elif isinstance(chunk, dict) and "messages" in chunk:
                # Print a newline after the complete message
                print("newline\n", flush=True)
            # tools调用消息获取
            elif isinstance(chunk, tuple) and chunk[0] == "values":
                message = chunk[1]['messages'][-1]
                if isinstance(message, AIMessage) and message.tool_calls:
                    # 工具调用 标题话术
                    yield LLMMessage(content="Tool Calls: ", type="tool_call")
                    for tc in message.tool_calls:
                        # 工具调用收集
                        collected_data["tool_calls"].append(tc)
                        # 工具调用 名称
                        yield LLMMessage(content=tc.get('name', 'Tool'), type="tool_call")
                        if tc.get("error"):
                            # 工具调用错误收集
                            collected_data["tool_errors"].append(tc.get("error"))
                            yield LLMMessage(content=tc.get('error'), type="tool_call")
                        # 工具调用 参数
                        yield LLMMessage(content=' Args:', type="tool_call")
                        args = tc.get("args")
                        if isinstance(args, str):
                            yield LLMMessage(content=f' {args}', type="tool_call")
                        elif isinstance(args, dict):
                            for arg, value in args.items():
                                yield LLMMessage(content=f' {arg}: {value}', type="tool_call")

        # 返回最终 collected_data
        if callback:
            await callback(collected_data)

    async def normal_chat(self, inputs: str, api_key: str, base_url: str, model: str) -> str:
        """
        普通的聊天方法，不使用流式响应。

        Args:
            inputs (str): 用户输入的消息
            api_key (str): API密钥
            base_url (str): API Base URL
            model (str): 模型名称

        Returns:
            str: 模型的响应内容
        """
        llm_model = self.get_llm_model(api_key, base_url, model)
        result = llm_model.invoke([HumanMessage(content=inputs)])
        return result.content
