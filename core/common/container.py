from dependency_injector import containers, providers

from extensions.ext_database import DatabaseProvider
from dao.user_dao import UserDAO
from dao.chat_window_dao import ChatWindowDAO
from dao.mcp_server_dao import MCPServerDAO
from service.chat_service import ChatService
from service.chat_window_service import ChatWindowService
from service.mcp_config_service import MCPConfigService
from service.user_service import UserService
from core.llm.qwen_open_ai import QwenLlm


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

    # 注册模型
    llm = providers.Singleton(QwenLlm)

    # 注册 chat Service
    chat_service = providers.Singleton(ChatService, llm=llm, mcp_config_service=mcp_config_service, chat_window_dao=chat_window_dao)


