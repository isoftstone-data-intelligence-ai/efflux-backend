from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP
from extensions.ext_database import Base

class User(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    create_time = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now)

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, create_time={self.create_time})"

    def __repr__(self):
        return str(self)