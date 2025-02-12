from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from core.common.container import Container
from core.security.middleware import request_token_context
from dto.chat_dto import ChatDTO
from service.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


# 从容器中获取注册在容器中的 ChatService 实例
def get_chat_service() -> ChatService:
    """
    获取 ChatService 实例

    通过依赖注入，从容器中获取注册的 ChatService 实例。

    Returns:
        ChatService: 用于处理会话的服务实例
    """
    return Container.chat_service()


@router.post("/stream_agent", summary="流式返回会话")
async def stream_response(chat_dto: ChatDTO, chat_service: ChatService = Depends(get_chat_service)):
    """
    模型会话接口 - 返回流式响应

    接收用户请求数据并通过 ChatService 处理会话逻辑，返回流式响应。

    Args:
        chat_dto (ChatDTO): 包含会话请求数据的对象
        chat_service (ChatService): 会话服务实例（通过依赖注入获取）

    Returns:
        StreamingResponse: 流式响应对象，媒体类型为 text/event-stream
    """
    # token中获取user_id
    user_id = request_token_context.get().get("user_id")
    return StreamingResponse(
        chat_service.agent_stream(chat_dto, user_id),
        media_type="text/event-stream"
    )


@router.post("/normal_chat", summary="普通会话")
async def normal_chat(chat_dto: ChatDTO, chat_service: ChatService = Depends(get_chat_service)):
    # token中获取user_id
    user_id = request_token_context.get().get("user_id")
    return await chat_service.normal_chat(chat_dto)
