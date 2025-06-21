from sqlalchemy.orm import Session
import models
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from models import Users

def authenticate_user(email: str, password: str, db: Session):
    """
    Login function
     Parameters:
     - email: User email
     - password: User password
     - db (Session): Database session

    Returns:
        User details Response
    """
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Try again with a valid Email!!")
    else:
        if user.password_hash == password:
            return user
        else:
            raise HTTPException(status_code=401, detail="Invalid Password!!")


def get_profile(user:Users,db: Session):
    """
    Creating  assignments
     Parameters:
     - user: User Object
     - db: DB Session

    Returns:
        User instance
    """
    if user.email is not None:
        user = db.query(models.Users).filter(models.Users.email == user.email).first()
        return user
