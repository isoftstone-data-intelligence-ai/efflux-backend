from fastapi import APIRouter, Depends

from dto.global_response import GlobalResponse
from dto.user_dto import UserResult, UserInit
from core.common.container import Container
from service.user_service import UserService
from typing import List
from core.common.logger import get_logger
from model.user import User
from core.security.middleware import request_token_context
from utils import result_utils

router = APIRouter(prefix="/user", tags=["Users"])

logger = get_logger(__name__)


def get_user_service() -> UserService:
    return Container.user_service()  # 直接获取已注册的测试服务


def convert_to_user_result(users: List[User]) -> List[UserResult]:
    return [UserResult(id=user.id, name=user.name, email=user.email) for user in users]


@router.get("/list", summary="用户列表", response_model=List[UserResult])
async def list_users(user_service: UserService = Depends(get_user_service)):
    """
    List all users 用户列表
    """
    users: List[User] = await user_service.get_users()
    user_result = convert_to_user_result(users)
    return result_utils.build_response(user_result)


@router.post("/user", summary="用户注册", response_model=UserResult)
async def create_user(user: UserInit, user_service: UserService = Depends(get_user_service)) -> GlobalResponse:
    """
    创建用户
    :user: 用户初始信息
    """
    rs = await user_service.create_user(user.name, user.email, user.password)
    logger.error(rs)
    return result_utils.build_response(rs)

@router.get("/tokeninfo", summary="用户token信息", response_model=UserResult)
async def read_user_token_info():
    # 获取当前线程/协程内的token信息
    user_info = request_token_context.get()
    return user_info