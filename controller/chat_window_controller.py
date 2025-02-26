from fastapi import APIRouter, Depends
from core.common.container import Container
from core.security.middleware import request_token_context
from dto.global_response import GlobalResponse
from service.chat_window_service import ChatWindowService
from utils import result_utils

router = APIRouter(prefix="/api/chat_window", tags=["ChatWindow"])


def get_chat_window_service():
    return Container.chat_window_service()


@router.get("/chat_window_list", summary="用户会话列表")
async def get_chat_window_list(chat_window_service: ChatWindowService = Depends(get_chat_window_service)) \
        -> GlobalResponse:
    user_id = request_token_context.get().get("id")
    result = await chat_window_service.get_user_chat_windows(user_id)
    return result_utils.build_response(result)

@router.get("/detail/{chat_window_id}", summary="获取会话详情")
async def get_chat_window_detail(
    chat_window_id: int,
    chat_window_service: ChatWindowService = Depends(get_chat_window_service)
) -> GlobalResponse:
    result = await chat_window_service.get_chat_window_by_id(chat_window_id)
    return result_utils.build_response(result)
