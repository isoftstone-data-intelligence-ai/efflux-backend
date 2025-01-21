import asyncio
from extensions.ext_database import engine, Base

class DatabaseProvider:
    @classmethod
    async def init_db(cls):
        # 延迟导入，避免循环依赖
        from model.user import User  
        async with engine.begin() as conn:
            # 打印 metadata 的所有表
            print(Base.metadata.tables.keys())
            # 创建所有未存在的表
            await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(DatabaseProvider.init_db())
