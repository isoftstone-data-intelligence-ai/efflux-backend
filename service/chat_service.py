from core.llm.llm_manager import LLMChat, LLMManager
from typing import AsyncGenerator, List, Optional
from core.mcp.convert_mcp_tools import convert_mcp_to_langchain_tools
from dao.artifacts_template_dao import ArtifactsTemplateDAO
from dao.chat_window_dao import ChatWindowDAO
from dao.llm_config_dao import LlmConfigDAO
from dto.artifacts_schema import ArtifactsSchema
from dto.chat_dto import ChatDTO
from dto.chat_window_dto import ContentDTO, ChatMessageDTO
from model.artifacts_template import ArtifactsTemplate
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
                 llm_config_dao: LlmConfigDAO, artifacts_template_dao: ArtifactsTemplateDAO, llm_manager: LLMManager):
        """
        初始化 ChatService

        Args:
            mcp_config_service (MCPConfigService): MCP 配置服务，用于获取 MCP-Server 的相关配置。
            chat_window_dao (ChatWindowDAO): 会话记录DAO，用于持久化会话及对话历史。
            llm_config_dao (LlmConfigDAO): LLM配置DAO，用于管理和获取用户的LLM配置信息。
            llm_manager (LLMManager): LLM管理器，用于管理不同的语言模型实例。

        Attributes:
            chat_window_dao: 会话窗口数据访问对象
            llm_config_dao: LLM配置数据访问对象
            mcp_config_service: MCP配置服务
            llm_manager: LLM管理器
            user_history_dict (dict): 用于存储每个用户的历史会话记录
        """
        self.chat_window_dao = chat_window_dao
        self.llm_config_dao = llm_config_dao
        self.artifacts_template_dao = artifacts_template_dao
        self.mcp_config_service = mcp_config_service
        self.llm_manager = llm_manager
        self.user_history_dict = {}  # 用于存储每个用户的历史会话记录

    async def _validate_llm_config(self, user_id: int, llm_config_id: int) -> LlmConfig:
        """
        验证 LLM 配置是否属于指定用户。

        Args:
            user_id (int): 用户ID
            llm_config_id (int): LLM配置ID

        Returns:
            LlmConfig: 验证通过的 LLM 配置

        Raises:
            PermissionError: 当用户尝试访问不属于自己的 LLM 配置时抛出
        """
        user_llm_config: LlmConfig = await self.llm_config_dao.get_config_by_id(llm_config_id=llm_config_id)
        if user_llm_config.user_id != user_id:
            raise PermissionError("您没有权限使用此 LLM 配置")
        return user_llm_config

    async def agent_stream(self, chat_dto: ChatDTO) -> AsyncGenerator[str, None]:
        """
        langchain 流式代理方法

        动态加载 MCP-Server 的标准化工具，通过语言模型提供流式会话功能。

        Args:
            chat_dto (ChatDTO): 会话请求数据传输对象，包含用户 ID、问题、提示词等。
        Yields:
            str: 模型返回的流式会话响应，每次生成一个 JSON 格式的消息块。
        """
        # 判断是否需要创建会话
        if not chat_dto.chat_id:
            chat_dto.chat_id = await self.create_chat_window(chat_dto.user_id, chat_dto.query)
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

                # 使用user_id和chat_id组合创建唯一键
                combined_id = f"{chat_dto.user_id}_{chat_dto.chat_id}"

                # 初始化或更新用户的历史记录
                if combined_id not in self.user_history_dict:
                    self.user_history_dict[combined_id] = []
                self.user_history_dict[combined_id].append({
                    "user": user_query,
                    "assistant": assistant_reply
                })
                # 保留最近3条历史记录
                self.user_history_dict[combined_id] = self.user_history_dict[combined_id][-3:]

                # 更新会话历史记录
                await self.update_chat_window(chat_dto.chat_id, user_query, assistant_reply)
            for tool_call in collected_data["tool_calls"]:
                print("--->tool_call:", tool_call)

        # 构造模型的输入内容
        # inputs = await self.load_inputs(chat_dto)

        # 模型选择
        user_llm_config = await self._validate_llm_config(chat_dto.user_id, chat_dto.llm_config_id)
        llm_provider = user_llm_config.provider
        llm_chat = self.llm_manager.get_llm(llm_provider)

        # 构造模型的输入内容
        # chat / artifacts 分流
        if chat_dto.code:
            # 走 artifacts 流程
            inputs = await self.load_artifacts_inputs(chat_dto)
        else:
            # 标准流式 chat 流程
            inputs = await self.load_inputs(chat_dto)

        async for chunk in llm_chat.stream_chat(inputs=inputs, tools=tools, callback=data_callback,
                                                api_key=user_llm_config.api_key,
                                                base_url=user_llm_config.base_url,
                                                model=user_llm_config.model,
                                                code=chat_dto.code):
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

    async def load_artifacts_inputs(self, chat_dto: ChatDTO) -> dict:
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
        prompt = """{
            "You are a skilled software engineer.\nYou do not make mistakes.\nGenerate an fragment.\nYou can install additional dependencies.\nDo not touch project dependencies files like package.json, package-lock.json, requirements.txt, etc.\nYou can use one of the following templates:\n1. code-interpreter-v1: \"Runs code as a Jupyter notebook cell. Strong data analysis angle. Can use complex visualisation to explain results.\". File: script.py. Dependencies installed: python, jupyter, numpy, pandas, matplotlib, seaborn, plotly. Port: none.\n2. nextjs-developer: \"A Next.js 13+ app that reloads automatically. Using the pages router.\". File: pages/index.tsx. Dependencies installed: nextjs@14.2.5, typescript, @types/node, @types/react, @types/react-dom, postcss, tailwindcss, shadcn. Port: 3000.\n3. vue-developer: \"A Vue.js 3+ app that reloads automatically. Only when asked specifically for a Vue app.\". File: app.vue. Dependencies installed: vue@latest, nuxt@3.13.0, tailwindcss. Port: 3000.\n4. streamlit-developer: \"A streamlit app that reloads automatically.\". File: app.py. Dependencies installed: streamlit, pandas, numpy, matplotlib, request, seaborn, plotly. Port: 8501.\n5. gradio-developer: \"A gradio app. Gradio Blocks/Interface should be called demo.\". File: app.py. Dependencies installed: gradio, pandas, numpy, matplotlib, request, seaborn, plotly. Port: 7860.",
            
        }

        就像网络接口的数据格式json字符串,去掉你的提示语，以及json数据结构外的内容 如下，代码部分放在code字段，其余字段看能否回填

        {
            "commentary": "I will generate a simple 'Hello World' application using the Next.js template. This will include a basic page that displays 'Hello World' when accessed.",
            "template": "nextjs-developer",
            "title": "Hello World",
            "description": "A simple Next.js app that displays 'Hello World'.",
            "additional_dependencies": [],
            "has_additional_dependencies": false,
            "install_dependencies_command": "",
            "port": 3000,
            "file_path": "pages/index.tsx",
            "code": ""
        }"""
        messages.append(("system", prompt))

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

    async def create_chat_window(self, user_id: int, query: str, chat_messages: Optional[List[str]] = None) -> int:
        # 会话概要
        # summary_prompt = "根据会话记录总结出本次会话的概要"
        # summary_query = query + reply
        # summary = self.normal_chat(ChatDTO(prompt=summary_prompt, query=summary_query))
        summary = query[:10]
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

    async def build_artifacts_inputs(self, chat_dto: ChatDTO) -> dict:
        """
        字典结构
        inputs:
            system : str        # 系统提示词
            messages: [
                {user : str}          # 用户query
                {assistant : str}     # AI的回答
            ]

        :param chat_dto:
        :return:
        """

        artifacts_templates = []
        if chat_dto.artifacts_template_id != 0:
            # artifacts_template_id非0表示选择某一个模板，根据id从DB获取模板
            artifacts_template = await self.artifacts_template_dao.get_artifact_template_by_id(
                chat_dto.artifacts_template_id)
            artifacts_templates.append(artifacts_template)
        else:
            # artifacts_template_id为0表示AUTO模式，从DB获取全部模板
            artifacts_templates = await self.artifacts_template_dao.get_all_artifact_templates()
        # 提示词
        system_prompt = self.templates_to_prompt(artifacts_templates)

        messages = []
        # 根据chat_id查询历史记录
        if chat_dto.chat_id:
            chat_window = await self.chat_window_dao.get_chat_window_by_id(chat_dto.chat_window_id)
            if chat_window.content:
                # 方案一：直接将历史记录构建为inputs字典，追加最后一次用户的query
                messages.append(chat_window.content)
        # 此次对话query
        query = chat_dto.query
        # 拼接最后一次query
        messages.append(("user", query))
        # 方案二：将历史记录拼接到system prompt ,并固定提示词 ex: 参考下面的对话历史记录，完成query的内容
        return {
            "system": system_prompt,
            "messages": messages
        }

    @staticmethod
    def templates_to_prompt(templates: List[ArtifactsTemplate]) -> str:
        # 系统提示词
        system_prompt = """
                You are a skilled software engineer.
                You do not make mistakes.
                Generate an fragment.
                You can install additional dependencies.
                Do not touch project dependencies files like package.json, package-lock.json, requirements.txt, etc.
                You can use one of the following templates:{templates_list}.
                And please provide your response in JSON format without any additional explanations or comments.
                The response must follow this schema structure, with the code placed in the code field:
                schema:{json_schema}
                """
        prompt_lines = []
        for index, template in enumerate(templates, 1):
            file_info = template.file or 'none'
            libs = ', '.join(template.lib or [])
            port = template.port or 'none'

            prompt_line = f"{index}. {template.name}: \"{template.instructions}\". File: {file_info}. Dependencies installed: {libs}. Port: {port}."
            prompt_lines.append(prompt_line)

        # 模板字符串    
        templates_str = '\n'.join(prompt_lines)

        # 获取 ArtifactsTemplateDTO 的 JSON Schema
        json_schema = ArtifactsSchema.model_json_schema()

        # 构建最终的系统提示词，替换两个占位符
        return system_prompt.format(
            templates_list=templates_str,
            json_schema=json.dumps(json_schema, indent=2, ensure_ascii=False)
        )

    async def normal_chat(self, chat_dto: ChatDTO) -> str:
        """
        普通的聊天方法，不使用流式响应。

        Args:
            chat_dto (ChatDTO): 会话请求数据传输对象。

        Returns:
            str: 模型的响应内容

        Raises:
            PermissionError: 当用户尝试访问不属于自己的 LLM 配置时抛出
        """
        # 获取用户的 LLM 配置
        user_llm_config = await self._validate_llm_config(chat_dto.user_id, chat_dto.llm_config_id)
        llm_provider = user_llm_config.provider
        llm_chat = self.llm_manager.get_llm(llm_provider)

        return await llm_chat.normal_chat(
            inputs=chat_dto.query,
            api_key=user_llm_config.api_key,
            base_url=user_llm_config.base_url,
            model=user_llm_config.model
        )
