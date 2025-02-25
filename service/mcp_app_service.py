from typing import List, Optional, Tuple
from dao.mcp_app_dao import MCPAppDAO
from dto.mcp_app_dto import MCPAppDTO
from dto.mcp_server_dto import MCPServerDTO, CreateMCPServerDTO
from model.mcp_app import MCPApp
from exception.exception import BaseAPIException
from exception.exception_dict import ExceptionType
from service.mcp_config_service import MCPConfigService


class MCPAppService:
    def __init__(self, mcp_app_dao: MCPAppDAO, mcp_config_service: MCPConfigService):
        self.mcp_app_dao = mcp_app_dao
        self.mcp_config_service = mcp_config_service

    def to_dto(self, app: Optional[MCPApp]) -> Optional[MCPAppDTO]:
        """将 MCPApp 模型转换为 DTO"""
        if not app:
            return None
        return MCPAppDTO(
            id=app.id,
            name=app.name,
            description=app.description,
            icon_url=app.icon_url,
            requires_configuration=app.requires_configuration,
            desktop_app=app.desktop_app,  # 新增字段
            github_repo_id=app.github_repo_id,
            github_repo_name=app.github_repo_name,
            github_repo_full_name=app.github_repo_full_name,
            github_html_url=app.github_html_url,
            github_url=app.github_url,
            github_created_at=app.github_created_at,
            github_updated_at=app.github_updated_at,
            github_pushed_at=app.github_pushed_at,
            server_name=app.server_name,
            command=app.command,
            args=app.args,
            env=app.env,
            
            # 通用字段
            created_at=app.created_at,
            updated_at=app.updated_at
        )

    async def get_app_page(self, page: int = 1, page_size: int = 10) -> Tuple[List[MCPAppDTO], int]:
        """获取应用列表，支持分页"""
        apps, total = await self.mcp_app_dao.get_app_page(page, page_size)
        return [self.to_dto(app) for app in apps], total

    async def get_app(self, app_id: int) -> Optional[MCPAppDTO]:
        """获取单个应用"""
        app = await self.mcp_app_dao.get_app_by_id(app_id)
        if app is None:
            raise BaseAPIException(
                status_code=ExceptionType.RESOURCE_NOT_FOUND.code,
                detail=ExceptionType.RESOURCE_NOT_FOUND.message
            )
        return self.to_dto(app)
    
    async def import_server(self, app_id: int, user_id: int) -> MCPServerDTO:
        """根据MCP应用信息创建一个新的MCP服务器
        
        Args:
            app_id: MCP应用ID
            user_id: 用户ID
            
        Returns:
            MCPServerDTO: 新创建的MCP服务器DTO对象
            
        Raises:
            BaseAPIException: 当应用不存在或服务器名称重复时抛出异常
        """
        mcp_app = await self.get_app(app_id)
        if not mcp_app:
            raise BaseAPIException(
                status_code=ExceptionType.RESOURCE_NOT_FOUND.code,
                detail="MCP应用不存在"
            )
            
        mcp_server = CreateMCPServerDTO(
            user_id = user_id,
            server_name=mcp_app.server_name,
            command=mcp_app.command,
            args=mcp_app.args,
            env=mcp_app.env
        )
        
        # 调用config service创建服务器
        return await self.mcp_config_service.add_server(mcp_server)
