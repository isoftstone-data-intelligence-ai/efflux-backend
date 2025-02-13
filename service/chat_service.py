from core.llm.llm_manager import LLMChat, LLMManager
from typing import AsyncGenerator, List, Optional
from core.mcp.convert_mcp_tools import convert_mcp_to_langchain_tools
from dao.chat_window_dao import ChatWindowDAO
from dao.llm_config_dao import LlmConfigDAO
from dto.chat_dto import ChatDTO
from dto.chat_window_dto import ContentDTO, ChatMessageDTO
from model.chat_window import ChatWindow
from model.llm_config import LlmConfig
from service.mcp_config_service import MCPConfigService
import json


class ChatService:
    """
    ChatService 类 - 提供与模型会话相关的服务

    该类负责与语言模型 (LLM) 进行交互，动态加载工具并支持流式会话。
    同时维护用户的历史会话记录，以实现更自然的上下文会话效果。
    """

    def __init__(self, mcp_config_service: MCPConfigService, chat_window_dao: ChatWindowDAO,
                 llm_config_dao: LlmConfigDAO):
        """
        初始化 ChatService

        Args:
            llm (LLMChat): 语言模型管理器，用于处理会话逻辑。
            mcp_config_service (MCPConfigService): MCP 配置服务，用于获取 MCP-Server 的相关配置。
            chat_window_dao: 会话记录DAO，用于持久化会话及对话历史
        """
        # self.llm = llm
        self.chat_window_dao = chat_window_dao
        self.llm_config_dao = llm_config_dao
        self.mcp_config_service = mcp_config_service
        self.user_history_dict = {}  # 用于存储每个用户的历史会话记录

    async def agent_stream(self, chat_dto: ChatDTO, user_id: int) -> AsyncGenerator[str, None]:
        """
        langchain 流式代理方法

        动态加载 MCP-Server 的标准化工具，通过语言模型提供流式会话功能。

        Args:
            chat_dto (ChatDTO): 会话请求数据传输对象，包含用户 ID、问题、提示词等。
            user_id : 用户id，从token中获取
        Yields:
            str: 模型返回的流式会话响应，每次生成一个 JSON 格式的消息块。
        """
        # 判断是否需要创建会话
        if not chat_dto.chat_id:
            new_chat_window_id = await self.create_chat(user_id, chat_dto.query)
        # 初始化 langchain agent 工具列表
        tools = []
        if chat_dto.server_id:
            # 通过json文件获取mcp-server配置，这个需要保留
            # server_params = await load_config_from_file(chat_dto.server_name)

            # 通过数据库获取mcp-server配置
            server_params = await self.mcp_config_service.load_mcp_server_config(chat_dto.server_id)

            # 获取mcp-server的所有tools并转换为langchain agent tools
            tools = await convert_mcp_to_langchain_tools([server_params])

        # 定义回调方法，用于收集模型返回的数据
        async def data_callback(collected_data):
            user_query = chat_dto.query
            print("--->messages:", ''.join(collected_data["messages"]))
            if "messages" in collected_data and collected_data["messages"]:
                assistant_reply = ''.join(collected_data["messages"])

                # 初始化或更新用户的历史记录
                if user_id not in self.user_history_dict:
                    self.user_history_dict[user_id] = []
                self.user_history_dict[user_id].append({
                    "user": chat_dto.query,
                    "assistant": assistant_reply
                })
                # 保留最近 3 条历史记录
                self.user_history_dict[user_id] = self.user_history_dict[user_id][-3:]
                # 更新会话历史记录
                if chat_dto.chat_id is None:
                    chat_window_id = new_chat_window_id
                else:
                    chat_window_id = chat_dto.chat_id
                await self.update_chat_window(chat_window_id, user_query, assistant_reply)
            for tool_call in collected_data["tool_calls"]:
                print("--->tool_call:", tool_call)

        # 构造模型的输入内容
        inputs = await self.load_inputs(chat_dto)

        user_llm_config_id = 1
        user_llm_config: LlmConfig = await self.llm_config_dao.get_config_by_id(user_llm_config_id)
        llm_nick_name = user_llm_config.nick_name
        llm_original = LLMManager.get_llm(name=llm_nick_name)
        llm = llm_original.get_llm_model(user_llm_config.api_key,user_llm_config.base_url,user_llm_config.model)


        # 调用语言模型的流式接口，生成响应
        async for chunk in llm.stream_chat(inputs=inputs, tools=tools, callback=data_callback):
            yield json.dumps(chunk.model_dump()) + "\n"

    async def load_inputs(self, chat_dto: ChatDTO) -> dict:
        """
        加载模型输入内容

        根据用户请求，拼接提示词、历史记录和当前问题，构造模型的输入。

        Args:
            chat_dto (ChatDTO): 会话请求数据传输对象。

        Returns:
            dict: 拼装好的模型输入，包含消息列表。
        """
        # 初始化一个空的消息列表，用于存储所有要发送给模型的消息
        messages = []
        # 检查是否有系统提示词（prompt）
        # 如果有，将其作为 system 角色的消息添加到列表中
        if chat_dto.prompt:
            messages.append(("system", chat_dto.prompt))

        # 添加最近 3 条用户历史记录
        if chat_dto.user_id in self.user_history_dict:
            for record in self.user_history_dict[chat_dto.user_id][-3:]:
                # 每条历史记录都包含用户的问题和 AI 的回答
                # 按照时间顺序添加到消息列表中
                messages.append(("user", record["user"]))  # 用户的历史问题
                messages.append(("assistant", record["assistant"]))  # AI 的历史回答

        # 将当前用户的新问题添加到消息列表的最后
        messages.append(("user", chat_dto.query))

        # 调试用：打印所有将要发送给模型的消息
        print(">>> 模型输入 messages：")
        for role, content in messages:
            print(f"{role}: {content}")

        # 返回一个包含所有消息的字典
        # 这个格式是 LLM API 所需的标准格式
        return {"messages": messages}

    async def create_chat(self, user_id: int, query: str, chat_messages: Optional[List[str]] = None) -> int:
        # 会话概要
        # summary_prompt = "根据会话记录总结出本次会话的概要"
        # summary_query = query + reply
        # summary = self.normal_chat(ChatDTO(prompt=summary_prompt, query=summary_query))
        summary = query
        # 创建新的会话
        new_chat_window = await self.chat_window_dao.create_chat_window(user_id=user_id, summary=summary)
        return new_chat_window.id

    async def get_chat_by_id(self, chat_window_id: int) -> ChatWindow:
        return await self.chat_window_dao.get_chat_window_by_id(chat_window_id)

    async def update_chat_window(self, chat_window_id: int, query: str, reply: Optional[str] = None):
        # 旧会话
        old_chat_window: ChatWindow = await self.chat_window_dao.get_chat_window_by_id(chat_window_id)

        # 构建新会话 content
        content_user = ContentDTO(type="text", text=query)
        content_assistant = ContentDTO(type="text", text=reply)
        
        # 创建消息，注意 content 需要是列表
        chat_message_user = ChatMessageDTO(
            role="user",
            content=[content_user]
        )
        chat_message_assistant = ChatMessageDTO(
            role="assistant",
            content=[content_assistant]
        )

        # 构建新的内容列表并转换为可序列化的字典
        new_content = [
            chat_message_user.model_dump(),
            chat_message_assistant.model_dump()
        ]

        # 最终更新内容
        if old_chat_window.content is None:
            update_content = new_content
        else:
            old_content = old_chat_window.content
            old_content.extend(new_content)
            update_content = old_content

        # 更新会话窗口
        await self.chat_window_dao.update_chat_window(
            chat_window_id=chat_window_id,
            summary=None,
            content=update_content
        )

    async def normal_chat(self, chat_dto: ChatDTO) -> str:
        return await self.llm.normal_chat(1, chat_dto.query)
