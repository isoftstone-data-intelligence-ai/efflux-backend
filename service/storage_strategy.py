from abc import ABC, abstractmethod
import os
import shutil
import oss2

# 定义策略接口
class StorageStrategy(ABC):
    @abstractmethod
    def upload(self, file_path: str, target_name: str):
        pass

    @abstractmethod
    def download(self, file_name: str, save_as: str):
        pass

# 阿里云OSS策略
class OSSStorageStrategy(StorageStrategy):
    def __init__(self, access_key_id, access_key_secret, bucket_name, endpoint):
        auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)

    def upload(self, file_path: str, target_name: str):
        with open(file_path, 'rb') as fileobj:
            self.bucket.put_object(target_name, fileobj)

    def download(self, file_name: str, save_as: str):
        result = self.bucket.get_object_to_file(file_name, save_as)
        if result.status != 200:
            raise Exception("Download failed")

# 本地存储策略
class LocalStorageStrategy(StorageStrategy):
    tempdir = 'local_oss';
    def __init__(self, base_dir=None):
        # 如果base_dir没有指定，则尝试自动发现项目根目录。
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir

    def upload(self, file_path: str, target_name: str):
        # 定义保存文件的基础目录
        save_dir = os.path.join(self.base_dir, self.tempdir)

        # 确保目标目录存在
        target_dir = os.path.join(save_dir)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)

        # 使用shutil.move以支持跨文件系统移动
        try:
            shutil.move(file_path, target_dir)
        except OSError as e:
            raise Exception(f"Failed to move file from {file_path} to {target_name}: {e}")

    def download(self, file_name: str, save_as: str):
        local_oss_dir = os.path.join(self.base_dir, self.tempdir)
        source_path = os.path.join(local_oss_dir, file_name)

        if not os.path.exists(source_path):
            raise FileNotFoundError(f"File {file_name} does not exist in local storage.")

        os.makedirs(os.path.dirname(save_as), exist_ok=True)
        shutil.copy(source_path, save_as)  # 使用copy而不是move，以便保留原始文件