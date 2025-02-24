from typing import List, Optional, Tuple
from dao.mcp_app_dao import MCPAppDAO
from dto.mcp_app_dto import MCPAppDTO
from model.mcp_app import MCPApp
from exception.exception import BaseAPIException
from exception.exception_dict import ExceptionType

class MCPAppService:
    def __init__(self, mcp_app_dao: MCPAppDAO):
        self.mcp_app_dao = mcp_app_dao

    def to_dto(self, app: Optional[MCPApp]) -> Optional[MCPAppDTO]:
        """将 MCPApp 模型转换为 DTO"""
        if not app:
            return None
        return MCPAppDTO(
            id=app.id,
            app_name=app.app_name,
            description=app.description,
            source_link=app.source_link,
            icon_url=app.icon_url,
            server_name=app.server_name,
            command=app.command,
            args=app.args,
            env=app.env
        )

    async def get_app_list(self, page: int = 1, page_size: int = 10) -> Tuple[List[MCPAppDTO], int]:
        """获取应用列表，支持分页"""
        apps = await self.mcp_app_dao.get_all_apps()
        total = len(apps)
        
        # 计算分页
        start = (page - 1) * page_size
        end = start + page_size
        paginated_apps = apps[start:end]
        
        return [self.to_dto(app) for app in paginated_apps], total

    async def get_app(self, app_id: int) -> Optional[MCPAppDTO]:
        """获取单个应用"""
        app = await self.mcp_app_dao.get_app_by_id(app_id)
        if app is None:
            raise BaseAPIException(
                status_code=ExceptionType.RESOURCE_NOT_FOUND.code,
                detail=ExceptionType.RESOURCE_NOT_FOUND.message
            )
        return self.to_dto(app)