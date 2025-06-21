from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import get_db
from models import Users
from dependencies import get_user_from_jwt_token
from .project_crud import get_project_details,get_project_list,create_project
from .project_schemas import ProjectDetails,AddProject
from typing import List
import uuid


router = APIRouter(prefix="/projects",tags=["Projects"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

@router.get("/project_list")
def project_listing(db: Session = Depends(get_db),user: Users = Depends(get_user_from_jwt_token))-> List[ProjectDetails]:
    return get_project_list(db=db,user=user)

@router.post("/projects_creation")
def project_creation( data: AddProject,db: Session = Depends(get_db),user: Users = Depends(get_user_from_jwt_token)):
    return create_project(data=data,db=db,user=user)

@router.get("/projects_details/{id}")
def project_details(project_id:uuid.UUID,db: Session = Depends(get_db),user: Users = Depends(get_user_from_jwt_token))->ProjectDetails:
    return get_project_details(project_id=project_id,db=db,user=user)