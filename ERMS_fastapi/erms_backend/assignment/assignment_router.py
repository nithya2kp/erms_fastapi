from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordBearer
from .assignment_crud import get_assignment_list,create_assignment,update_assignment,assignment_delete
from sqlalchemy.orm import Session
from db import get_db
from models import Users
from dependencies import get_user_from_jwt_token,require_manager
from typing import List
import uuid
from.assignment_schemas import AssignmentDetails,CreateAssignment

router = APIRouter(prefix="/assignments",tags=["Assignments"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


"""
Listing complete assignments 
Permission: Manager level
"""
@router.get("/assignment_list")
def assignment_list(db: Session = Depends(get_db),user: Users = Depends(get_user_from_jwt_token))-> List[AssignmentDetails]:
    return get_assignment_list(db=db,user=user)

"""
Creating assignments assigning engineers
Permission: Manager level
"""
@router.post("/assignment_details")
def assign_engineer(
    request:CreateAssignment,
    db: Session = Depends(get_db),
    user: Users = Depends(require_manager)
):
    return create_assignment(data=request,db=db)

"""
Updating existing assignment
Permission: Manager level
"""
@router.put("/assignment/{id}")
def assignment_update(
    data: CreateAssignment,
    db: Session = Depends(get_db),
    user: Users = Depends(require_manager)
):
    return update_assignment(data=data,db=db)


"""
Delete existing assignments
Permission: Manager level
"""
@router.delete("/assignment_delete/{id}")
def delete_assignment(
    assignment_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: Users = Depends(require_manager)
):
    return assignment_delete(id=assignment_id,db=db)
