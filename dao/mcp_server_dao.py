from sqlalchemy.future import select
from sqlalchemy import update, delete
from model.mcp_server import McpServer
from typing import Optional, List, Dict, Any
from datetime import datetime

class MCPServerDAO:
    def __init__(self, session_factory):
        self._session_factory = session_factory
        print('mcp server dao init')

    async def get_all_servers(self) -> List[McpServer]:
        """获取所有 MCP 服务器"""
        async with self._session_factory() as session:
            result = await session.execute(select(McpServer))
            return result.scalars().all()

    async def get_server_by_id(self, id: int) -> Optional[McpServer]:
        """根据服务器ID获取 MCP 服务器"""
        async with self._session_factory() as session:
            result = await session.execute(
                select(McpServer).where(McpServer.id == id)
            )
            return result.scalar_one_or_none()

    async def get_servers_by_user_id(self, user_id: int) -> List[McpServer]:
        """根据用户ID获取该用户的所有 MCP 服务器"""
        async with self._session_factory() as session:
            result = await session.execute(
                select(McpServer).where(McpServer.user_id == user_id)
            )
            return result.scalars().all()

    async def create_server(self, 
                          user_id: int,
                          server_name: str, 
                          command: str, 
                          args: List[str], 
                          env: Optional[Dict[str, Any]] = None) -> McpServer:
        """创建新的 MCP 服务器"""
        async with self._session_factory() as session:
            new_server = McpServer(
                user_id=user_id,
                server_name=server_name,
                command=command,
                args=args,
                env=env,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(new_server)
            await session.commit()
            return new_server

    async def update_server(self,
                          id: int,
                          server_name: Optional[str] = None,
                          command: Optional[str] = None,
                          args: Optional[List[str]] = None,
                          env: Optional[Dict[str, Any]] = None) -> Optional[McpServer]:
        """更新 MCP 服务器信息"""
        async with self._session_factory() as session:
            update_data = {}
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
                    update(McpServer)
                    .where(McpServer.id == id)
                    .values(**update_data)
                    .returning(McpServer)
                )
                await session.commit()
                return result.scalar_one_or_none()
            return None

    async def delete_server(self, id: int) -> bool:
        """删除 MCP 服务器"""
        async with self._session_factory() as session:
            result = await session.execute(
                delete(McpServer).where(McpServer.id == id)
            )
            await session.commit()
            return result.rowcount > 0
