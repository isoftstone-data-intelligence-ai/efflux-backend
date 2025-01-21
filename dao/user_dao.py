from sqlalchemy.future import select
from model.user import User
from typing import List

class UserDAO:
    def __init__(self, session_factory):
        self._session_factory = session_factory
        print('user dao init')

    async def get_all_users(self) -> List[User]:
        async with self._session_factory() as session:  # 获取会话
            result = await session.execute(select(User)) # 得到Result对象
            return result.scalars().all() # 使用Result.scalars将元组列表转为List[User]


    async def create_user(self, name: str, email: str, password: str):
        async with self._session_factory() as session:
            new_user = User(name=name, email=email, password=password)
            session.add(new_user)
            await session.commit()
            return new_user

    async def get_user_by_name(self, user_name: str) -> User:
        async with self._session_factory() as session:
            result = await session.execute(select(User).where(User.name == user_name))
            return result.scalars().first()