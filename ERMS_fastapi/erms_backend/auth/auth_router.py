from fastapi import FastAPI,HTTPException,APIRouter,Depends
from fastapi import  File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db import get_db
from .auth_schemas import UserLogin,UserProfile
from .auth_crud import authenticate_user,get_profile
from models import Users
from dependencies import get_user_from_jwt_token,create_jwt

router = APIRouter(prefix="/auth",tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

"""
Login
Permission: Public level
"""
@router.post("/login")
def login(
    db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()
)->UserLogin:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt(email=user.email, user_id=str(user.id), username=user.username)
    user_response = UserLogin(
        email=user.email,
        name=user.name,
        access_token=token
    )
    return user_response

"""
View Profile
Permission: Engineer,Manager level
"""
@router.get("/profile")
def profile(db: Session = Depends(get_db),user: Users = Depends(get_user_from_jwt_token)) -> UserProfile:
    return get_profile(user,db)

