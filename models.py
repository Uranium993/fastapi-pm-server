from email.policy import default
from unittest.mock import DEFAULT
from uuid import uuid4
from sqlalchemy import BigInteger, Column, Enum, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
from database import Base

class User (Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4(), unique=True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    password = Column(String, unique=True, nullable=False)
    role = (String(6))


class ProjectStatus(str, enum.Enum):
    DEFAULT = 'INIT'
    IN_PREPARATION = 'IN_PREPARATION'
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    REJECTED = 'REJECTED'
    RETRY = 'RETRY'

class ProjectPhase(Base):
    __tablename__ = "phases"
    id = Column(BigInteger, primary_key=True)
    #id_project = Column(ForeignKey("project.id"), index=True)
    status = Column(Integer, nullable = False)
    dt_updated = Column(DateTime, nullable=True)

class Project(Base):
    __tablename__ = "project"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    inactive = Column(Boolean, default=False)
    year = Column(String)
    user = Column(UUID, ForeignKey('user.id'))
    codename = Column(String(50), nullable=False, unique=True)
    creator_name = Column(String(50), nullable=False)
    client_name = Column(String(50), nullable=False)
    client_email = Column(String(64), unique=True  )
    client_number = Column(Integer)
    estimated_worth = Column(Integer)
    final_worth = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    IDR = Column(ForeignKey(ProjectPhase.id), nullable=False, index=True)
    IDP = Column(ForeignKey(ProjectPhase.id), nullable=False, index=True)
    PGD = Column(ForeignKey(ProjectPhase.id), nullable=False, index=True)
    PZI = Column(ForeignKey(ProjectPhase.id), nullable=False, index=True)
    PIO = Column(ForeignKey(ProjectPhase.id), nullable=False, index=True)



