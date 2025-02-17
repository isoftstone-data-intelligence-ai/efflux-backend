from fastapi import APIRouter, Depends
from core.common.container import Container
from core.security.middleware import request_token_context
from dto.global_response import GlobalResponse
from service.artifacts_template_service import ArtifactsService
from utils import result_utils

router = APIRouter(prefix="/artifacts", tags=["Artifacts"])


def get_artifacts_service() -> ArtifactsService:
    return Container.artifacts_service()


@router.get("/template_list", summary="获取制品模板列表")
async def get_template_list(artifacts_service: ArtifactsService = Depends(get_artifacts_service)) \
        -> GlobalResponse:
    result = await artifacts_service.get_artifacts_templates()
    return result_utils.build_response(result)



