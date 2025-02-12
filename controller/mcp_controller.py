from fastapi import APIRouter, Depends
from core.common.container import Container
from core.security.middleware import request_token_context
from dto.global_response import GlobalResponse
from dto.mcp_server_dto import MCPServerDTO, CreateMCPServerDTO
from service.mcp_config_service import MCPConfigService
from utils import result_utils

router = APIRouter(prefix="/mcp", tags=["MCPServer"])


def get_mcp_config_service() -> MCPConfigService:
    mcp_config_service = Container.mcp_config_service()  # 直接获取已注册的服务
    return mcp_config_service


@router.get("/mcp_server_list")
async def mcp_server_list(mcp_config_service: MCPConfigService = Depends(get_mcp_config_service)) \
        -> GlobalResponse:
    # token中获取user_id
    user_id = request_token_context.get().get("user_id")
    mcp_servers = await mcp_config_service.get_user_servers(user_id)
    return result_utils.build_response(mcp_servers)


@router.get("/mcp_server/{_id}")
async def get_server(
        _id: int,
        mcp_config_service: MCPConfigService = Depends(get_mcp_config_service)
) -> GlobalResponse:
    server = await mcp_config_service.get_server(_id)
    return result_utils.build_response(server)


@router.post("/mcp_server")
async def add_server(
        server: CreateMCPServerDTO,
        mcp_config_service: MCPConfigService = Depends(get_mcp_config_service)
) -> GlobalResponse:
    # token中获取user_id
    user_id = request_token_context.get().get("user_id")
    server.user_id = user_id
    new_server = await mcp_config_service.add_server(server)
    return result_utils.build_response(new_server)


@router.put("/mcp_server")
async def update_server(
        server: MCPServerDTO,
        mcp_config_service: MCPConfigService = Depends(get_mcp_config_service)
) -> GlobalResponse:
    user_id = request_token_context.get().get("user_id")
    server.user_id = user_id
    updated_server = await mcp_config_service.update_server(server)
    return result_utils.build_response(updated_server)


@router.delete("/mcp_server/{_id}")
async def delete_server(
        _id: int,
        mcp_config_service: MCPConfigService = Depends(get_mcp_config_service)
) -> GlobalResponse:
    await mcp_config_service.delete_server(_id)
    return result_utils.build_response(None)
