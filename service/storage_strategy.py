from abc import ABC, abstractmethod
import os
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
    def upload(self, file_path: str, target_name: str):
        os.makedirs(os.path.dirname(target_name), exist_ok=True)
        os.rename(file_path, target_name)

    def download(self, file_name: str, save_as: str):
        os.makedirs(os.path.dirname(save_as), exist_ok=True)
        os.rename(file_name, save_as)