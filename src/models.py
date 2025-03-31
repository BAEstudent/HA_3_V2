from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, MetaData, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship #, declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=True, nullable=False)

# class Links(Base):
#     __tablename__ = "links"
#     id = Column(Integer, primary_key=True, index=True)
#     long_url = Column(String, nullable=False)
#     short_code = Column(String, nullable=False)
#     create_dt = Column(TIMESTAMP, nullable=False)
#     expire_dt = Column(TIMESTAMP, nullable=False)
#     user_id = Column(String, nullable=False)
