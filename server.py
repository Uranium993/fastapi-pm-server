from fastapi import FastAPI, encoders, HTTPException, status, Path
from typing import TYPE_CHECKING, List
import fastapi
import sqlalchemy.orm as orm
import uvicorn
import services as _services
from models import Base
import schemas as _schemas
from database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

inventory = {1: {"name": "djoko", "brand": "smartass"}}



@app.get("/")
def home():
    return {"data": "Working..."}


@app.post("/api/users", response_model=_schemas.User)
async def create_user(
    user: _schemas.CreateUser, db: orm.Session = fastapi.Depends(_services.get_db)
):
    return await _services.create_user(user=user, db=db)


@app.post("/api/projects", response_model=_schemas.Project)
async def create_project(
    project: _schemas.createProject, db: orm.Session = fastapi.Depends(_services.get_db)
):
    return await _services.create_project(project=project, db=db)


@app.get("/api/projects", response_model=List[_schemas.Project])
async def get_projects(db: orm.Session = fastapi.Depends(_services.get_db)):
    return await _services.get_all_projects(db=db)

@app.get("/api/projects/{project_id}", response_model=_schemas.Project)
async def get_single_project(project_id: str, db: orm.Session = fastapi.Depends(_services.get_db)):
    return await _services.get_project(project_id=project_id, db=db)


@app.patch("/api/projects/{project_id}", response_model=_schemas.Project)
async def update_project_partial(project_id: str, project: _schemas.updateProject, db: orm.Session = fastapi.Depends(_services.get_db)):
    
    db_project = await _services.get_project(project_id=project_id, db=db)
    if db_project is None:
        raise fastapi.HTTPException(status_code=404, detail="Project not found")
    
    project_data = project.__dict__
    for key, value in project_data.items():
        if value is not None:
            setattr(db_project, key, value) 
            print(value)

    db.commit()
    db.refresh(db_project)
    # project_data = encoders.jsonable_encoder(update_data)
    #return await _services.update_project(project_data=project_data, project=project, db=db)
    return db_project

@app.put("/api/projects/{project_id}/{foreign_key}", response_model=_schemas.ProjectPhase)
async def update_phase(project_id: str, foreign_key: int, project_phase: _schemas.ProjectPhase, db: orm.Session = fastapi.Depends(_services.get_db)):
    db_project = await _services.get_project(project_id=project_id, db=db)





@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str, db: orm.Session = fastapi.Depends(_services.get_db)):
    project = await _services.get_project(project_id=project_id, db=db)
    if project is None:
        raise fastapi.HTTPException(status_code=404, detail="Project doesn't exist")

    await _services.delete_project(project, db=db)

    return "Project deleted successfuly!"


if __name__ == '__main__':
    uvicorn.run("server:app",
                host='0.0.0.0',
                port=8001,
                debug=True,
                reload=True)