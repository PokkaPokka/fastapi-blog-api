from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True, nullable = False, index = True)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = "True", nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), server_default = text('NOW()'), nullable = False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)

    owner = relationship("User") # The User here refferes to the class User below

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False, index = True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), server_default = text('NOW()'), nullable = False)

