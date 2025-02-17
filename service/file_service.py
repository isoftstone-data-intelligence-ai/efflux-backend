from service.storage_strategy import StorageStrategy


class FileService:
    def __init__(self, strategy: StorageStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: StorageStrategy):
        self.strategy = strategy

    def upload_file(self, file_path: str, target_name: str):
        self.strategy.upload(file_path, target_name)
        # 记录到数据库的逻辑可以放在这里

    def download_file(self, file_name: str, save_as: str):
        self.strategy.download(file_name, save_as)
        # 记录到数据库的逻辑可以放在这里
