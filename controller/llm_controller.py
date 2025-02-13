from fastapi import APIRouter, Depends
from core.common.container import Container
from core.security.middleware import request_token_context
from dto.global_response import GlobalResponse
from dto.llm_config_dto import LLMConfigDTO, CreateLLMConfigDTO
from dto.llm_template_dto import LLMTemplateDTO
from service.llm_service import LLMService
from utils import result_utils

router = APIRouter(prefix="/llm", tags=["LLM"])


def get_llm_service() -> LLMService:
    llm_service = Container.llm_service()  # 直接获取已注册的服务
    return llm_service


@router.get("/templates")
async def get_templates(
    llm_service: LLMService = Depends(get_llm_service)
) -> GlobalResponse:
    """获取所有可用的 LLM 模板"""
    templates = await llm_service.get_all_templates()
    return result_utils.build_response(templates)


@router.get("/configs")
async def get_configs(
    llm_service: LLMService = Depends(get_llm_service)
) -> GlobalResponse:
    """获取当前用户的所有 LLM 配置"""
    user_id = request_token_context.get().get("user_id")
    configs = await llm_service.get_user_configs(user_id)
    return result_utils.build_response(configs)


@router.get("/config/{_id}")
async def get_config(
    _id: int,
    llm_service: LLMService = Depends(get_llm_service)
) -> GlobalResponse:
    """获取指定的 LLM 配置"""
    config = await llm_service.get_config(_id)
    return result_utils.build_response(config)


@router.post("/config")
async def add_config(
    config: CreateLLMConfigDTO,
    llm_service: LLMService = Depends(get_llm_service)
) -> GlobalResponse:
    """添加新的 LLM 配置"""
    user_id = request_token_context.get().get("user_id")
    config.user_id = user_id
    new_config = await llm_service.add_config(config)
    return result_utils.build_response(new_config)


@router.put("/config")
async def update_config(
    config: LLMConfigDTO,
    llm_service: LLMService = Depends(get_llm_service)
) -> GlobalResponse:
    """更新 LLM 配置"""
    user_id = request_token_context.get().get("user_id")
    config.user_id = user_id
    updated_config = await llm_service.update_config(config)
    return result_utils.build_response(updated_config)


# @router.delete("/config/{_id}")
# async def delete_config(
#     _id: int,
#     llm_service: LLMService = Depends(get_llm_service)
# ) -> GlobalResponse:
#     """删除 LLM 配置"""
#     await llm_service.delete_config(_id)
#     return result_utils.build_response(None)



