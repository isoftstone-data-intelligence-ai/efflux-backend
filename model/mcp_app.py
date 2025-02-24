from datetime import datetime

from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ARRAY, TEXT, JSON

from extensions.ext_database import Base


class MCPApp(Base):
    __tablename__ = 'mcp_app'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    app_name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    source_link =Column(String(100), nullable=False)
    icon_url = Column(String(100), nullable=False)

    # mcp sever config
    server_name = Column(String(100), nullable=False)
    command = Column(String(100), nullable=False)
    args = Column(ARRAY(TEXT), nullable=False)
    env = Column(JSON, nullable=True)

    # common
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now, onupdate=datetime.now)

