from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dependencies import get_db,get_user_from_jwt_token,require_manager
from models import Users
import uuid
from.engineer_crud import get_engineers,get_engineer_capacity
from .engineer_schemas import Engineers,EngineerCapacity
from auth.auth_schemas import UserProfile


router = APIRouter(prefix="/engineers",tags=["Engineers"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

"""
Listing Engineers
Permission: Manager level
"""
@router.get("/engineer_count")
def listing_engineers(db: Session = Depends(get_db),user: Users = Depends(require_manager))->Engineers:
    return get_engineers(db=db)


"""
Details of Engineer capacity
Permission: Manager level
"""
@router.get("/{engineer_id}/capacity")
def engineer_capacity( engineer_id: uuid.UUID,db: Session = Depends(get_db),user: Users = Depends(require_manager))-> EngineerCapacity:
    return get_engineer_capacity(engineer_id=engineer_id,db=db)
