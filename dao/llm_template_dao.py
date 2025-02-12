from sqlalchemy.future import select
from sqlalchemy import update, delete
from model.llm_template import LlmTemplate
from typing import Optional, List

class LlmTemplateDAO:
    """LLM模板数据访问对象，用于管理LLM模板的数据库操作"""
    
    def __init__(self, session_factory):
        self._session_factory = session_factory
        
    async def get_all_templates(self) -> List[LlmTemplate]:
        """获取所有LLM模板
        
        Returns:
            List[LlmTemplate]: LLM模板列表
        """
        async with self._session_factory() as session:
            result = await session.execute(select(LlmTemplate))
            return result.scalars().all()
            
    async def get_template_by_id(self, id: int) -> Optional[LlmTemplate]:
        """根据ID获取LLM模板
        
        Args:
            id (int): 模板ID
            
        Returns:
            Optional[LlmTemplate]: 找到的模板对象，未找到则返回None
        """
        async with self._session_factory() as session:
            result = await session.execute(
                select(LlmTemplate).where(LlmTemplate.id == id)
            )
            return result.scalar_one_or_none()
            
    async def get_templates_by_provider(self, provider: str) -> List[LlmTemplate]:
        """根据提供商获取LLM模板
        
        Args:
            provider (str): 模型提供商名称
            
        Returns:
            List[LlmTemplate]: 该提供商的所有模板列表
        """
        async with self._session_factory() as session:
            result = await session.execute(
                select(LlmTemplate).where(LlmTemplate.provider == provider)
            )
            return result.scalars().all()
            
    async def create_template(self,
                            provider: str,
                            model_display_name: str,
                            api_key_variable: Optional[str] = 'API Key',
                            base_url_variable: Optional[str] = 'Base URL',
                            model_variable: Optional[str] = 'Model') -> LlmTemplate:
        """创建新的LLM模板
        
        Args:
            provider (str): 模型提供商名称
            model_display_name (str): 展示给用户的模型名称
            api_key_variable (str, optional): API密钥变量名
            base_url_variable (str, optional): 基础URL变量名
            model_variable (str, optional): 模型变量名
            
        Returns:
            LlmTemplate: 创建的模板对象
        """
        async with self._session_factory() as session:
            new_template = LlmTemplate(
                provider=provider,
                model_display_name=model_display_name,
                api_key_variable=api_key_variable,
                base_url_variable=base_url_variable,
                model_variable=model_variable
            )
            session.add(new_template)
            await session.commit()
            return new_template
            
    async def update_template(self,
                            id: int,
                            provider: Optional[str] = None,
                            model_display_name: Optional[str] = None,
                            api_key_variable: Optional[str] = None,
                            base_url_variable: Optional[str] = None,
                            model_variable: Optional[str] = None) -> Optional[LlmTemplate]:
        """更新LLM模板信息
        
        Args:
            id (int): 模板ID
            provider (str, optional): 模型提供商名称
            model_display_name (str, optional): 展示给用户的模型名称
            api_key_variable (str, optional): API密钥变量名
            base_url_variable (str, optional): 基础URL变量名
            model_variable (str, optional): 模型变量名
            
        Returns:
            Optional[LlmTemplate]: 更新后的模板对象，如果没有更新则返回None
        """
        async with self._session_factory() as session:
            update_data = {}
            if provider is not None:
                update_data['provider'] = provider
            if model_display_name is not None:
                update_data['model_display_name'] = model_display_name
            if api_key_variable is not None:
                update_data['api_key_variable'] = api_key_variable
            if base_url_variable is not None:
                update_data['base_url_variable'] = base_url_variable
            if model_variable is not None:
                update_data['model_variable'] = model_variable
                
            if update_data:
                result = await session.execute(
                    update(LlmTemplate)
                    .where(LlmTemplate.id == id)
                    .values(**update_data)
                    .returning(LlmTemplate)
                )
                await session.commit()
                return result.scalar_one_or_none()
            return None
            
    async def delete_template(self, id: int) -> bool:
        """删除LLM模板
        
        Args:
            id (int): 要删除的模板ID
            
        Returns:
            bool: 删除成功返回True，否则返回False
        """
        async with self._session_factory() as session:
            result = await session.execute(
                delete(LlmTemplate).where(LlmTemplate.id == id)
            )
            await session.commit()
            return result.rowcount > 0 