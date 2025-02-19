from typing import List, Optional

from pydantic import BaseModel


class ArtifactsTemplateDTO(BaseModel):
    id: int
    template_name: str
    name: str
    lib: List[str]
    file: str
    instructions: str
    port: Optional[int] = None

    def to_dict(self) -> dict:
        """将对象转换为字典格式，方便序列化为 JSON"""
        return {
            "id": self.id,
            "template_name": self.template_name,
            "name": self.name,
            "lib": self.lib,
            "file": self.file,
            "instructions": self.instructions,
            "port": self.port
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ArtifactsTemplateDTO":
        """从字典格式创建对象，方便反序列化"""
        return cls(
            id=data["id"],
            template_name=data["template_name"],
            name=data["name"],
            lib=data["lib"],
            file=data["file"],
            instructions=data["instructions"],
            port=data.get("port")  # port 是可选的，使用 .get() 避免 KeyError
        )