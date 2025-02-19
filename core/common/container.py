from dependency_injector import containers, providers
from core.llm.claude import ClaudeLlm
from core.llm.llm_manager import LLMManager
from core.llm.ollama import OllamaLlm
from core.llm.open_ai import OpenAILlm
from dao.llm_config_dao import LlmConfigDAO
from dao.llm_template_dao import LlmTemplateDAO
from extensions.ext_database import DatabaseProvider
from dao.user_dao import UserDAO
from dao.chat_window_dao import ChatWindowDAO
from dao.mcp_server_dao import MCPServerDAO
from service.chat_service import ChatService
from service.chat_window_service import ChatWindowService
from service.file_service import FileService
from service.mcp_config_service import MCPConfigService
from service.storage_strategy import OSSStorageStrategy, LocalStorageStrategy
from service.user_service import UserService
from core.llm.azure_open_ai import AzureLlm
from service.llm_service import LLMService
from dotenv import load_dotenv
import os

class Container(containers.DeclarativeContainer):
    # 注册数据库会话提供器
    database_provider = providers.Singleton(DatabaseProvider)

    # 注册 user DAO
    user_dao = providers.Singleton(UserDAO, session_factory=database_provider.provided.session_factory)
    # 注册 user Service
    user_service = providers.Singleton(UserService, user_dao=user_dao)

    # 注册 MCPServer DAO
    mcp_server_dao = providers.Singleton(MCPServerDAO, session_factory=database_provider.provided.session_factory)
    # 注册 MCP Config Service
    mcp_config_service = providers.Singleton(MCPConfigService, mcp_server_dao=mcp_server_dao)

    # 注册chat_window DAO
    chat_window_dao = providers.Singleton(ChatWindowDAO, session_factory=database_provider.provided.session_factory)
    # 注册chat_window Service
    chat_window_service = providers.Singleton(ChatWindowService, chat_window_dao=chat_window_dao)

    # 注册llm_config DAO
    llm_config_dao = providers.Singleton(LlmConfigDAO, session_factory=database_provider.provided.session_factory)
    # 注册llm_template DAO
    llm_template_dao = providers.Singleton(LlmTemplateDAO, session_factory=database_provider.provided.session_factory)
    # 注册 LLM Service
    llm_service = providers.Singleton(LLMService,
                                      llm_config_dao=llm_config_dao,
                                      llm_template_dao=llm_template_dao)
    # 注入支持的LLMChat，根据提供商和风格分类
    azure = AzureLlm()
    claude = ClaudeLlm()
    ollama = OllamaLlm()
    open_ai = OpenAILlm()
    # llm chat集合
    llm_map = {
        azure.name(): azure,
        claude.name(): claude,
        ollama.name(): ollama,
        "default": open_ai # 默认使用open ai风格的LLMChat
    }
    # 注册LLM Manager
    llm_manager = providers.Singleton(LLMManager, llm_map)

    # 注册 chat Service
    chat_service = providers.Singleton(ChatService,
                                       mcp_config_service=mcp_config_service,
                                       chat_window_dao=chat_window_dao,
                                       llm_config_dao=llm_config_dao,
                                       llm_manager=llm_manager)

    load_dotenv()
    ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    ACCESS_KEY_SECRET = os.getenv('ACCESS_KEY_SECRET')
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    ENDPOINT = os.getenv('ENDPOINT')

    # 创建OSS存储策略工厂
    oss_strategy_factory = providers.Factory(
        OSSStorageStrategy,
        access_key_id=ACCESS_KEY_ID,
        access_key_secret=ACCESS_KEY_SECRET,
        bucket_name=BUCKET_NAME,
        endpoint=ENDPOINT
    )

    # 创建本地存储策略工厂
    local_strategy_factory = providers.Factory(LocalStorageStrategy)

    # 默认使用本地存储策略的实际实例
    strategy = providers.Singleton(local_strategy_factory)

    file_service = providers.Factory(
        FileService,
        strategy=strategy
    )

    @classmethod
    def switch_to_oss(cls, oss_strategy_factory=None):
        # 切换到OSS策略
        global strategy
        strategy = providers.Singleton(oss_strategy_factory)

    @classmethod
    def switch_to_local(cls, local_strategy_factory=None):
        # 切换回本地策略
        global strategy
        strategy = providers.Singleton(local_strategy_factory)
