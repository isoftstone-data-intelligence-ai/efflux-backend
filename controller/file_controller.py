from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from core.common.container import Container
from dto.global_response import GlobalResponse
from service.file_service import FileService
from utils import result_utils
import os


router = APIRouter(prefix="/file", tags=["OSS"])
# 加载临时文件目录配置
TEMP_DIR = os.getenv('TEMP_DIR')

def get_file_service() -> FileService:
    file_service = Container.file_service()  # 直接获取已注册的服务
    return file_service


@router.post("/upload/")
async def upload(file: UploadFile = File(...), file_service: FileService = Depends(get_file_service)) \
        -> GlobalResponse:
    temp_file_path = os.path.join(TEMP_DIR, file.filename)
    try:
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)

        file_service.upload_file(temp_file_path, file.filename)
        return result_utils.build_response({"filename": file.filename})
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)  # 删除临时文件


@router.get("/download/{file_name}")
async def download(file_name: str, file_service: FileService = Depends(get_file_service)):
    temp_download_path = os.path.join(TEMP_DIR, f"downloaded_{file_name}")
    try:
        file_service.download_file(file_name, temp_download_path)
        return FileResponse(path=temp_download_path, filename=file_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))



# 切换为OSS上传下载文件
@router.post("/switch-to-oss")
def switch_to_oss():
    Container.switch_to_oss()
    return result_utils.build_response({"message": "Switched to OSS"})


# 切换为本地上传下载文件
@router.post("/switch-to-local")
def switch_to_local():
    Container.switch_to_local()
    return result_utils.build_response({"message": "Switched to local"})
