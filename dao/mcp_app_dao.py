from sqlalchemy.future import select
from sqlalchemy import update, delete
from model.mcp_app import MCPApp
from typing import Optional, List, Dict, Any
from datetime import datetime


class MCPAppDAO:
    def __init__(self, session_factory):
        self._session_factory = session_factory
        print('mcp app dao init')

    async def get_all_apps(self) -> List[MCPApp]:
        """获取所有 MCP 应用"""
        async with self._session_factory() as session:
            result = await session.execute(select(MCPApp))
            return result.scalars().all()

    async def get_app_by_id(self, id: int) -> Optional[MCPApp]:
        """根据应用ID获取 MCP 应用"""
        async with self._session_factory() as session:
            result = await session.execute(
                select(MCPApp).where(MCPApp.id == id)
            )
            return result.scalar_one_or_none()

    async def create_app(self,
                        name: str,
                        description: str,
                        icon_url: str,
                        requires_configuration: bool,
                        # GitHub 仓库信息
                        github_repo_id: int,
                        github_repo_name: str,
                        github_repo_full_name: str,
                        github_html_url: str,
                        github_url: str,
                        github_created_at: datetime,
                        github_updated_at: datetime,
                        github_pushed_at: datetime,
                        # MCP 服务器配置
                        server_name: str,
                        command: str,
                        args: List[str],
                        env: Optional[Dict[str, Any]] = None) -> MCPApp:
        """创建新的 MCP 应用"""
        async with self._session_factory() as session:
            new_app = MCPApp(
                name=name,
                description=description,
                icon_url=icon_url,
                requires_configuration=requires_configuration,
                github_repo_id=github_repo_id,
                github_repo_name=github_repo_name,
                github_repo_full_name=github_repo_full_name,
                github_html_url=github_html_url,
                github_url=github_url,
                github_created_at=github_created_at,
                github_updated_at=github_updated_at,
                github_pushed_at=github_pushed_at,
                server_name=server_name,
                command=command,
                args=args,
                env=env,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(new_app)
            await session.commit()
            return new_app

    async def update_app(self,
                        id: int,
                        name: Optional[str] = None,
                        description: Optional[str] = None,
                        source_link: Optional[str] = None,
                        icon_url: Optional[str] = None,
                        server_name: Optional[str] = None,
                        command: Optional[str] = None,
                        args: Optional[List[str]] = None,
                        env: Optional[Dict[str, Any]] = None,
                        requires_configuration: Optional[bool] = None) -> Optional[MCPApp]:
        """更新 MCP 应用信息"""
        async with self._session_factory() as session:
            update_data = {}
            if name is not None:
                update_data['name'] = name
            if description is not None:
                update_data['description'] = description
            if source_link is not None:
                update_data['source_link'] = source_link
            if icon_url is not None:
                update_data['icon_url'] = icon_url
            if server_name is not None:
                update_data['server_name'] = server_name
            if command is not None:
                update_data['command'] = command
            if args is not None:
                update_data['args'] = args
            if env is not None:
                update_data['env'] = env
            if requires_configuration is not None:
                update_data['requires_configuration'] = requires_configuration

            if update_data:
                update_data['updated_at'] = datetime.now()
                result = await session.execute(
                    update(MCPApp)
                    .where(MCPApp.id == id)
                    .values(**update_data)
                    .returning(MCPApp)
                )
                await session.commit()
                return result.scalar_one_or_none()
            return None

    async def delete_app(self, id: int) -> bool:
        """删除 MCP 应用"""
        async with self._session_factory() as session:
            result = await session.execute(
                delete(MCPApp).where(MCPApp.id == id)
            )
            await session.commit()
            return result.rowcount > 0