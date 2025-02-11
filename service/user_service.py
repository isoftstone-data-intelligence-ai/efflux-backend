from dao.user_dao import UserDAO
from core.common.logger import logger
from passlib.hash import bcrypt
from model.user import User
from typing import List
from exception.exception import BaseAPIException
from exception.exception_dict import ExceptionType


@logger
class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    async def get_users(self) -> List[User]:
        print("enter user service")
        users: List[User] = await self.user_dao.get_all_users()
        print("enter user service done")
        return users

    async def create_user(self, name: str, email: str, password: str):
        user = await self.get_user_by_name(name)
        if user:
            raise BaseAPIException(
                status_code=ExceptionType.DUPLICATE_USER_NAME.code,
                detail=ExceptionType.DUPLICATE_USER_NAME.message
            )
        user = await self.get_user_by_email(email)
        if user:
            raise BaseAPIException(
                status_code=ExceptionType.DUPLICATE_EMAIL.code,
                detail=ExceptionType.DUPLICATE_EMAIL.message
            )
        hashed_password = bcrypt.hash(password)
        return await self.user_dao.create_user(name, email, hashed_password)

    async def get_user_by_name(self, user_name) -> User:
        return await self.user_dao.get_user_by_name(user_name)

    async def get_user_by_email(self, email) -> User:
        return await self.user_dao.get_user_by_email(email)
