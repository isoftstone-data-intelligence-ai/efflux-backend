from sqlalchemy.future import select
from sqlalchemy import update, delete
from model.llm_config import LlmConfig
from typing import Optional, List, Dict, Any
from datetime import datetime

class LlmConfigDAO:
    def __init__(self, session_factory):
        self._session_factory = session_factory
        print('llm config dao init')

    async def get_all_configs(self) -> List[LlmConfig]:
        """获取所有 LLM 配置"""
        async with self._session_factory() as session:
            result = await session.execute(select(LlmConfig))
            return result.scalars().all()

    async def get_config_by_id(self, id: int) -> Optional[LlmConfig]:
        """根据配置ID获取 LLM 配置"""
        async with self._session_factory() as session:
            result = await session.execute(
                select(LlmConfig).where(LlmConfig.id == id)
            )
            return result.scalar_one_or_none()

    async def get_configs_by_user_id(self, user_id: int) -> List[LlmConfig]:
        """根据用户ID获取该用户的所有 LLM 配置"""
        async with self._session_factory() as session:
            result = await session.execute(
                select(LlmConfig).where(LlmConfig.user_id == user_id)
            )
            return result.scalars().all()

    async def create_config(self,
                          user_id: int,
                          template_id: int,
                          provider: str,
                          api_key: str,
                          base_url: str,
                          model: str,
                          extra_config: Optional[Dict[str, Any]] = None) -> LlmConfig:
        """创建新的 LLM 配置
        
        Args:
            user_id: 用户ID
            template_id: 模板ID
            provider: 模型提供商名称
            api_key: API密钥
            base_url: API基础URL
            model: 模型名称
            extra_config: 额外配置参数
        """
        async with self._session_factory() as session:
            new_config = LlmConfig(
                user_id=user_id,
                template_id=template_id,
                provider=provider,
                api_key=api_key,
                base_url=base_url,
                model=model,
                extra_config=extra_config,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(new_config)
            await session.commit()
            return new_config

    async def update_config(self,
                          id: int,
                          template_id: Optional[int] = None,
                          provider: Optional[str] = None,
                          api_key: Optional[str] = None,
                          base_url: Optional[str] = None,
                          model: Optional[str] = None,
                          extra_config: Optional[Dict[str, Any]] = None) -> Optional[LlmConfig]:
        """更新 LLM 配置信息"""
        async with self._session_factory() as session:
            update_data = {}
            if template_id is not None:
                update_data['template_id'] = template_id
            if provider is not None:
                update_data['provider'] = provider
            if api_key is not None:
                update_data['api_key'] = api_key
            if base_url is not None:
                update_data['base_url'] = base_url
            if model is not None:
                update_data['model'] = model
            if extra_config is not None:
                update_data['extra_config'] = extra_config
            
            if update_data:
                update_data['updated_at'] = datetime.now()
                result = await session.execute(
                    update(LlmConfig)
                    .where(LlmConfig.id == id)
                    .values(**update_data)
                    .returning(LlmConfig)
                )
                await session.commit()
                return result.scalar_one_or_none()
            return None

    async def delete_config(self, id: int) -> bool:
        """删除 LLM 配置"""
        async with self._session_factory() as session:
            result = await session.execute(
                delete(LlmConfig).where(LlmConfig.id == id)
            )
            await session.commit()
            return result.rowcount > 0 