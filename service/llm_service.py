from core.common.logger import get_logger
from typing import List, Optional
from dao.llm_config_dao import LlmConfigDAO
from dao.llm_template_dao import LlmTemplateDAO
from exception.exception import BaseAPIException
from model.llm_config import LlmConfig
from model.llm_template import LlmTemplate
from exception.exception_dict import ExceptionType
from dto.llm_config_dto import LLMConfigDTO, CreateLLMConfigDTO
from dto.llm_template_dto import LLMTemplateDTO

logger = get_logger(__name__)


class LLMService:
    """LLM服务管理类，负责处理LLM相关的所有业务逻辑，包括配置和模板管理"""

    def __init__(self, llm_config_dao: LlmConfigDAO, llm_template_dao: LlmTemplateDAO):
        self.llm_config_dao = llm_config_dao
        self.llm_template_dao = llm_template_dao

    # Config 相关方法
    def to_config_dto(self, config: Optional[LlmConfig]) -> Optional[LLMConfigDTO]:
        """将 LlmConfig 模型转换为 DTO"""
        if not config:
            return None
        return LLMConfigDTO(**config.model_dump())

    # Template 相关方法
    def to_template_dto(self, template: Optional[LlmTemplate]) -> Optional[LLMTemplateDTO]:
        """将 LlmTemplate 模型转换为 DTO"""
        if not template:
            return None
        return LLMTemplateDTO(**template.model_dump())

    # 配置管理相关方法
    async def get_user_configs(self, user_id: int) -> List[LLMConfigDTO]:
        """获取用户的所有 LLM 配置"""
        configs = await self.llm_config_dao.get_configs_by_user_id(user_id)
        return [self.to_config_dto(config) for config in configs]

    async def get_config(self, config_id: int, user_id: int) -> Optional[LLMConfigDTO]:
        """获取单个 LLM 配置，并验证是否属于当前用户"""
        config = await self.llm_config_dao.get_config_by_id(config_id)
        if config is None:
            raise BaseAPIException(
                status_code=ExceptionType.RESOURCE_NOT_FOUND.code,
                detail=ExceptionType.RESOURCE_NOT_FOUND.message
            )
        # 验证配置是否属于当前用户
        if config.user_id != user_id:
            raise BaseAPIException(
                status_code=ExceptionType.PERMISSION_DENIED.code,
                detail=ExceptionType.PERMISSION_DENIED.message
            )
        return self.to_config_dto(config)

    async def add_config(self, llm_config: CreateLLMConfigDTO) -> LLMConfigDTO:
        """新增一个 LLM 配置"""
        # 验证关键字段不能为空
        if not llm_config.api_key.strip():
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="API key 不能为空"
            )
        if not llm_config.base_url.strip():
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="Base URL 不能为空"
            )
        if not llm_config.model.strip():
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="Model 不能为空"
            )

        new_config = await self.llm_config_dao.create_config(
            user_id=llm_config.user_id,
            template_id=llm_config.template_id,
            provider=llm_config.provider,
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
            model=llm_config.model,
            model_nickname=llm_config.model_nickname,
            extra_config=llm_config.extra_config
        )
        return self.to_config_dto(new_config)

    async def update_config(self, llm_config: LLMConfigDTO) -> Optional[LLMConfigDTO]:
        """更新 LLM 配置"""
        # 验证关键字段不能为空
        if not llm_config.api_key.strip():
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="API key 不能为空"
            )
        if not llm_config.base_url.strip():
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="Base URL 不能为空"
            )
        if not llm_config.model.strip():
            raise BaseAPIException(
                status_code=ExceptionType.INVALID_PARAM.code,
                detail="Model 不能为空"
            )

        # 获取当前配置信息并验证所有权
        current_config = await self.llm_config_dao.get_config_by_id(llm_config.id)
        if not current_config:
            raise BaseAPIException(
                status_code=ExceptionType.RESOURCE_NOT_FOUND.code,
                detail=ExceptionType.RESOURCE_NOT_FOUND.message
            )
        
        # 验证配置是否属于当前用户
        if current_config.user_id != llm_config.user_id:
            raise BaseAPIException(
                status_code=ExceptionType.PERMISSION_DENIED.code,
                detail=ExceptionType.PERMISSION_DENIED.message
            )

        updated_config = await self.llm_config_dao.update_config(
            id=llm_config.id,
            template_id=llm_config.template_id,
            provider=llm_config.provider,
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
            model=llm_config.model,
            model_nickname=llm_config.model_nickname,
            extra_config=llm_config.extra_config
        )
        if not updated_config:
            raise BaseAPIException(
                status_code=ExceptionType.CONFIG_UPDATE_FAILED.code,
                detail="配置更新失败"
            )
        return self.to_config_dto(updated_config)

    async def delete_config(self, config_id: int, user_id: int) -> bool:
        """删除 LLM 配置"""
        # 确保配置存在并验证所有权
        config = await self.llm_config_dao.get_config_by_id(config_id)
        if not config:
            raise BaseAPIException(
                status_code=ExceptionType.RESOURCE_NOT_FOUND.code,
                detail=ExceptionType.RESOURCE_NOT_FOUND.message
            )
            
        # 验证配置是否属于当前用户
        if config.user_id != user_id:
            raise BaseAPIException(
                status_code=ExceptionType.PERMISSION_DENIED.code,
                detail=ExceptionType.PERMISSION_DENIED.message
            )

        success = await self.llm_config_dao.delete_config(config_id)
        if not success:
            raise BaseAPIException(
                status_code=ExceptionType.CONFIG_DELETE_FAILED.code,
                detail="配置删除失败"
            )
        return success

    # 模板管理相关方法
    async def get_all_templates(self) -> List[LLMTemplateDTO]:
        """获取所有 LLM 模板"""
        templates = await self.llm_template_dao.get_all_templates()
        return [self.to_template_dto(template) for template in templates] 