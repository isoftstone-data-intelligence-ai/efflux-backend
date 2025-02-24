from typing import TypeVar, Generic, List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

T = TypeVar('T')

class Pagination(Generic[T]):
    """分页查询工具类
    
    提供统一的分页查询接口，支持任意 SQLAlchemy 模型的分页操作。
    
    Example:
        async def get_app_page(self, page: int = 1, page_size: int = 10) -> Tuple[List[MCPApp], int]:
            async with self._session_factory() as session:
                return await Pagination.paginate(
                    session=session,
                    query=select(MCPApp),
                    page=page,
                    page_size=page_size
                )
    """
    
    @staticmethod
    async def paginate(
        session: AsyncSession,
        query: Select,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[T], int]:
        """执行分页查询
        
        Args:
            session: SQLAlchemy 异步会话
            query: 查询语句
            page: 页码，从1开始
            page_size: 每页数量
            
        Returns:
            Tuple[List[T], int]: 返回分页数据和总记录数
        """
        # 查询总记录数
        count_query = select(func.count()).select_from(query.subquery())
        total = await session.scalar(count_query)
        
        # 查询分页数据
        offset = (page - 1) * page_size
        result = await session.execute(
            query.offset(offset).limit(page_size)
        )
        
        return result.scalars().all(), total