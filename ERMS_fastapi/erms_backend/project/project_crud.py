from models import Users,Projects
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .project_schemas import ProjectDetails,AddProject
from typing import List
from models import UserRole

def get_project_list(user:Users,db:Session)-> List[ProjectDetails]:
    db_user = db.query(Users).filter(Users.id == user.id).first()
    if db_user:
        projects = db.query(Projects).all()
        return [ProjectDetails.model_validate(p, from_attributes=True) for p in projects]
    else:
        raise HTTPException(status_code=404,detail="User doesnot exists!!")
    

def get_project_details(project_id, user: Users, db: Session) -> ProjectDetails:
    db_user = db.query(Users).filter(Users.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    db_project = db.query(Projects).filter(Projects.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found!")

    return ProjectDetails.model_validate(db_project, from_attributes=True)
    

def create_project(data,user:Users,db:Session):
    if user.role!=UserRole.MANAGER:
        raise HTTPException(status_code=403, detail="Only managers can assign engineers.")
    new_project = Projects(
        project_status=data.project_status,
        name=data.name,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
        manager_id=user.id,
        required_skills=data.required_skills,
        team_size=data.team_size,
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {"message": "Project Created successfully", "project_id": str(new_project.id)}
