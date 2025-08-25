from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from libs.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
