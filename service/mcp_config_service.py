import json
from core.common.logger import get_logger
from core.mcp.server.server_loader import StdioServerParameters
from dto.mcp_server_dto import MCPServerDTO, CreateMCPServerDTO
from typing import List, Optional
from dao.mcp_server_dao import MCPServerDAO
from exception.exception import BaseAPIException
from model.mcp_server import McpServer
from exception.exception_dict import ExceptionType

logger = get_logger(__name__)


class MCPConfigService:

    def __init__(self, mcp_server_dao: MCPServerDAO):
        self.mcp_server_dao = mcp_server_dao

    # 不设置为静态方法，因为config service已经在container注册过了，一定有实例
    def to_dto(self, server: Optional[McpServer]) -> Optional[MCPServerDTO]:
        """将 McpServer 模型转换为 DTO
        
        Args:
            server: McpServer 实例或 None
            
        Returns:
            McPServerDTO 实例或 None
        """
        if not server:
            return None
        return MCPServerDTO(**server.model_dump())  # ** 解包操作：将 model_dump() 返回的字典进行解包，展开为关键字参数（键值对）传递给 DTO

    # 获取用户的所有servers
    async def get_user_servers(self, user_id: int) -> List[MCPServerDTO]:
        servers = await self.mcp_server_dao.get_servers_by_user_id(user_id)
        return [self.to_dto(server) for server in servers]

    # 获取单个server
    async def get_server(self, server_id: int) -> Optional[MCPServerDTO]:
        server = await self.mcp_server_dao.get_server_by_id(server_id)
        if server is None:
            raise BaseAPIException(
                status_code=ExceptionType.RESOURCE_NOT_FOUND.code,
                detail=ExceptionType.RESOURCE_NOT_FOUND.message
            )
        return self.to_dto(server)

    # 新增一个server
    async def add_server(self, mcp_server: CreateMCPServerDTO) -> MCPServerDTO:
        # 验证服务器名称和命令不能为空字符串
        if not mcp_server.server_name.strip():  # 除字符串两端的空白字符（包括空格、制表符、换行符等）
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="MCP server name 不能为空"
            )
        if not mcp_server.command.strip():
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="MCP server command 不能为空"
            )

        # 检查同一用户下是否存在同名服务器
        existing_servers = await self.get_user_servers(mcp_server.user_id)
        if any(server.server_name == mcp_server.server_name for server in existing_servers):
            raise BaseAPIException(
                status_code=ExceptionType.DUPLICATE_SERVER_NAME.code,
                detail=ExceptionType.DUPLICATE_SERVER_NAME.message
            )

        new_server = await self.mcp_server_dao.create_server(
            user_id=mcp_server.user_id,
            server_name=mcp_server.server_name,
            command=mcp_server.command,
            args=mcp_server.args,
            env=mcp_server.env
        )
        return self.to_dto(new_server)

    # 编辑server
    async def update_server(self, mcp_server: MCPServerDTO) -> Optional[MCPServerDTO]:
        # 验证服务器名称和命令不能为空字符串
        if not mcp_server.server_name.strip():
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="MCP server name 不能为空"
            )
        if not mcp_server.command.strip():
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="MCP server command 不能为空"
            )

        # 获取当前服务器信息
        current_server = await self.get_server(mcp_server.id)
        if not current_server:
            raise BaseAPIException(
                status_code=ExceptionType.RESOURCE_NOT_FOUND.code,
                detail=ExceptionType.RESOURCE_NOT_FOUND.message
            )

        # 如果服务器名称发生变化，检查新名称是否与其他服务器冲突
        if current_server.server_name != mcp_server.server_name:
            existing_servers = await self.get_user_servers(mcp_server.user_id)
            if any(server.server_name == mcp_server.server_name for server in existing_servers):
                raise BaseAPIException(
                    status_code=ExceptionType.DUPLICATE_SERVER_NAME.code,
                    detail=ExceptionType.DUPLICATE_SERVER_NAME.message
                )

        updated_server = await self.mcp_server_dao.update_server(
            id=mcp_server.id,
            server_name=mcp_server.server_name,
            command=mcp_server.command,
            args=mcp_server.args,
            env=mcp_server.env
        )
        if not updated_server:
            raise BaseAPIException(
                status_code=ExceptionType.SERVER_UPDATE_FAILED.code,
                detail=ExceptionType.SERVER_UPDATE_FAILED.message
            )
        return self.to_dto(updated_server)

    # 删除server
    async def delete_server(self, server_id: int) -> bool:
        # 确保服务器存在
        server = await self.get_server(server_id)
        if not server:
            raise BaseAPIException(
                status_code=ExceptionType.RESOURCE_NOT_FOUND.code,
                detail=ExceptionType.RESOURCE_NOT_FOUND.message
            )

        success = await self.mcp_server_dao.delete_server(server_id)
        if not success:
            raise BaseAPIException(
                status_code=ExceptionType.SERVER_DELETE_FAILED.code,
                detail=ExceptionType.SERVER_DELETE_FAILED.message
            )
        return success

    # 加载mcp_server_config
    async def load_mcp_server_config(self, server_id: int) -> StdioServerParameters:
        """ Load the server configuration from DB """
        try:
            mcp_sever = await self.get_server(server_id)

            # Construct the server parameters
            result = StdioServerParameters(
                command=mcp_sever.command,
                args=mcp_sever.args,
                env=mcp_sever.env if mcp_sever.env else None,  # 这是额外的一层保护，以免数据库有env={}的情况
            )

            # debug
            logger.debug(f"Loaded config from DB: command='{result.command}', args={result.args}, env={result.env}")

            # return result
            return result
        except Exception as e:
            # error
            logger.error(str(e))
            raise
