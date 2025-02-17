
from sqlalchemy import Column, BigInteger, String, Integer


class ArtifactsTemplate:
    __tablename__ = 'artifacts_template'

    id = Column(BigInteger, primary_key=True)
    template_name = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    lib = Column(String(500), nullable=False)
    file = Column(String(100), nullable=False)
    instructions = Column(String(255), nullable=False)
    port = Column(Integer)



