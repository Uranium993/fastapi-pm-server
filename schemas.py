import datetime as _dt
from enum import Enum
from typing import Optional
from unicodedata import name
from pydantic import BaseModel, validator
from sqlalchemy import table
from models import ProjectStatus

class ProjectPhase(BaseModel):
    status: int = 0

    # @validator('status')
    # def status_match(cls, v):
    #     if not v in ['possible_value_1', 'possible_value_2']:
    #         raise ValueError('c must be in [possible_value_1, possible_value_2]')
    #     return v

    class Config:
        orm_mode: True

     

class _BaseUser(BaseModel):
    name: str
    email: str
    password: str
    role: str

class User(_BaseUser):
    pass

    class Config:
        orm_mode = True

class CreateUser(_BaseUser):
    pass

class _BaseProject(BaseModel):
    inactive: Optional[bool] = None
    year: Optional[str] = None
    user: Optional[str] = None
    codename: Optional[str] = None
    creator_name: Optional[str] = None
    client_name: Optional[str] = None
    client_email:Optional[ str] = None
    client_number: Optional[int] = None
    estimated_worth: Optional[int] = None
    final_worth: Optional[int] = None

    IDR: ProjectPhase
    IDP: ProjectPhase
    PGD: ProjectPhase
    PZI: ProjectPhase
    PIO: ProjectPhase

class Project (_BaseProject):

    class Config:
        orm_mode = True



class createProject(_BaseProject):
    codename: str
    client_name: str

class updateProject(_BaseProject):
    pass
    

    