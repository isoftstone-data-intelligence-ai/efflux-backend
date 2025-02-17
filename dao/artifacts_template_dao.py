from typing import List

from sqlalchemy.future import select

from model.artifacts_template import ArtifactsTemplate


class ArtifactsTemplateDAO:
    def __init__(self, session_factory):
        self._session_factory = session_factory


    async def create_artifact_template(self, artifact_template: ArtifactsTemplate):
        async with self._session_factory() as session:
            session.add(artifact_template)
            await session.commit()
            return artifact_template

    async def get_all_artifact_templates(self) -> List[ArtifactsTemplate]:
        async with self._session_factory() as session:
            result = await session.execute(select(ArtifactsTemplate))
            return result.scalars().all()
