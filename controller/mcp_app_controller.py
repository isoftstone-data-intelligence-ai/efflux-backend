from fastapi import APIRouter, Depends, Query
from core.common.container import Container
from core.security.middleware import request_token_context
from dto.global_response import GlobalResponse
from service.mcp_app_service import MCPAppService
from utils import result_utils

router = APIRouter(prefix="/mcp_app", tags=["MCPApp"])

def get_mcp_app_service() -> MCPAppService:
    return Container.mcp_app_service()

@router.get("/page", summary="mcp应用列表")
async def get_app_page(
    page: int = Query(1, description="页码，从1开始"),
    page_size: int = Query(10, description="每页数量"),
    mcp_app_service: MCPAppService = Depends(get_mcp_app_service)
) -> GlobalResponse:
    apps, total = await mcp_app_service.get_app_page(page, page_size)
    return result_utils.build_page_response(apps, page, page_size, total)

@router.get("/{app_id}", summary="mcp应用详情")
async def get_app(
    app_id: int,
    mcp_app_service: MCPAppService = Depends(get_mcp_app_service)
) -> GlobalResponse:
    app = await mcp_app_service.get_app(app_id)
    return result_utils.build_response(app)

@router.post("/import/{app_id}", summary="为当前用户一键添加MCP配置")
async def import_server(
    app_id: int,
    mcp_app_service: MCPAppService = Depends(get_mcp_app_service)
) -> GlobalResponse:
    # token中获取user_id
    user_id = request_token_context.get().get("id")
    new_server = await mcp_app_service.import_server(app_id, user_id)
    return result_utils.build_response(new_server)