from extensions.ext_database import Base
from sqlalchemy import Column, BigInteger, String, Integer, ARRAY


class ArtifactsTemplate(Base):
    __tablename__ = 'artifacts_template'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    template_name = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    lib = Column(ARRAY(String), nullable=False)
    file = Column(String(100), nullable=False)
    instructions = Column(String(255), nullable=False)
    port = Column(Integer, nullable=True)



