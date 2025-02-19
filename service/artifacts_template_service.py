from typing import List

from dao.artifacts_template_dao import ArtifactsTemplateDAO
from dto.artifacts_template_dto import ArtifactsTemplateDTO
from model.artifacts_template import ArtifactsTemplate


class ArtifactsService:
    def __init__(self, artifacts_template_dao: ArtifactsTemplateDAO):
        self.artifacts_template_dao = artifacts_template_dao


    async def get_artifacts_templates(self) -> List[ArtifactsTemplateDTO]:
        """
        获取所有artifacts模板并转换为 DTO

        Returns:
            List[ArtifactsTemplateDTO]: 制品模板 DTO 列表
        """
        artifacts: List[ArtifactsTemplate] = await self.artifacts_template_dao.get_all_artifact_templates()
        return [self.convert_template_model_to_template_dto(artifact) for artifact in artifacts]


    @staticmethod
    def convert_template_model_to_template_dto(model: ArtifactsTemplate) -> ArtifactsTemplateDTO:
        """
        将数据库模型转换为 DTO

        Args:
            model (ArtifactsTemplate): 数据库模型对象

        Returns:
            ArtifactsTemplateDTO: 转换后的 DTO 对象
        """
        # 将 lib 字符串转换为列表
        # lib_list = model.lib.split(',') if model.lib else []
        
        return ArtifactsTemplateDTO(
            template_name=model.template_name,
            name=model.name,
            lib=model.lib,
            file=model.file,
            instructions=model.instructions,
            port=model.port
        )

