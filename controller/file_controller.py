from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from core.common.logger import get_logger
from core.common.container import Container
from dto.global_response import GlobalResponse
from service.file_service import FileService
from utils import result_utils
import os

router = APIRouter(prefix="/file", tags=["OSS"])
# 显示创建日志
logger = get_logger(__name__)

# 确定项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 定义TEMP_DIR为项目根目录下的临时文件夹
TEMP_DIR = os.path.join(BASE_DIR, 'tmp')
os.makedirs(TEMP_DIR, exist_ok=True)

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
async def download(file_name: str, background_tasks: BackgroundTasks, file_service: FileService = Depends(get_file_service)):
    temp_file_path = os.path.join(TEMP_DIR, f"downloaded_{file_name}")
    try:
        file_service.download_file(file_name, temp_file_path)
        # 添加任务，在响应返回后删除临时文件
        background_tasks.add_task(os.remove, temp_file_path)
        return FileResponse(path=temp_file_path, filename=file_name, media_type='application/octet-stream')
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# 切换为OSS上传下载文件
@router.post("/switch-to-oss")
def switch_to_oss() \
        -> GlobalResponse:
    Container.switch_to_oss()
    logger.info("File upload and download Switched to OSS.")
    return result_utils.build_response({"message": "Switched to OSS"})


# 切换为本地上传下载文件
@router.post("/switch-to-local")
def switch_to_local() \
        -> GlobalResponse:
    Container.switch_to_local()
    logger.info("File upload and download Switched to local.")
    return result_utils.build_response({"message": "Switched to local"})
