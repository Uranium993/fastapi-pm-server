from dataclasses import asdict
import database as _database 
import models as _models
import schemas as _schemas
from typing import TYPE_CHECKING, List
from fastapi.encoders import jsonable_encoder

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_user(user: _schemas.CreateUser, db: "Session") -> _schemas.User:
    user = _models.User( **user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return _schemas.User.from_orm(user)

async def create_project(project: _schemas.Project, db: "Session") -> _schemas.Project:
    
    project = _models.Project(**project.dict())
    print(project)
    db.add(project)
    db.commit()
    db.refresh(project)
    return _schemas.Project.from_orm(project)

async def get_all_projects(db: "Session") -> List[_schemas.Project]:
    projects = db.query(_models.Project).all()
    return list(map(_schemas.Project.from_orm, projects))

async def get_project(project_id: str, db: "Session") -> List[_schemas.Project]:
    project = db.query(_models.Project).filter(_models.Project.id == project_id).first()
    return project

async def update_project(project_data: _schemas.updateProject, project: _models.Project, db: "Session") -> _schemas.Project:
    projectData = _models.Project(**project_data.dict(exclude_unset=True))
    db.commit()
    db.refresh(projectData)

    return _schemas.Project.from_orm(projectData)


async def delete_project(project: _models.Project, db: "Session"):
    db.delete(project)
    db.commit()

