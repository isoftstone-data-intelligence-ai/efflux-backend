from sqlalchemy.future import select
from sqlalchemy import update, delete
from model.mcp_app import MCPApp
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import func


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
                        app_name: str,
                        description: str,
                        source_link: str,
                        icon_url: str,
                        server_name: str,
                        command: str,
                        args: List[str],
                        env: Optional[Dict[str, Any]] = None) -> MCPApp:
        """创建新的 MCP 应用"""
        async with self._session_factory() as session:
            new_app = MCPApp(
                app_name=app_name,
                description=description,
                source_link=source_link,
                icon_url=icon_url,
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
                        app_name: Optional[str] = None,
                        description: Optional[str] = None,
                        source_link: Optional[str] = None,
                        icon_url: Optional[str] = None,
                        server_name: Optional[str] = None,
                        command: Optional[str] = None,
                        args: Optional[List[str]] = None,
                        env: Optional[Dict[str, Any]] = None) -> Optional[MCPApp]:
        """更新 MCP 应用信息"""
        async with self._session_factory() as session:
            update_data = {}
            if app_name is not None:
                update_data['app_name'] = app_name
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

    async def get_app_page(self, page: int = 1, page_size: int = 10) -> Tuple[List[MCPApp], int]:
        """获取应用分页列表
        
        Args:
            page: 页码，从1开始
            page_size: 每页数量
            
        Returns:
            Tuple[List[MCPApp], int]: 返回分页数据和总记录数
        """
        async with self._session_factory() as session:
            # 查询总记录数
            count_query = select(func.count()).select_from(MCPApp)
            total = await session.scalar(count_query)
            
            # 查询分页数据
            offset = (page - 1) * page_size
            query = select(MCPApp).offset(offset).limit(page_size)
            result = await session.execute(query)
            
            return result.scalars().all(), total