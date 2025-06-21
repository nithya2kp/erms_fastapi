from datetime import datetime, timedelta
from typing import Optional
import config
from jose import jwt, JWTError

from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from db import get_db
from models import Users,UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_jwt(
    email: str,
    user_id: Optional[str] = None,
    username: Optional[str] = None,
) -> str:
    expire = datetime.utcnow() + timedelta(days=2)
    payload = {
        "sub": email,
        "exp": expire,
        "user_id": user_id,
        "username": username,
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)

def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        return decoded, None
    except JWTError as e:
        return None, str(e)


def get_user_from_jwt_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Users:
    decoded, error = decode_jwt(token)

    if error:
        detail = "Token expired!" if "expired" in error.lower() else "Invalid token!"
        raise HTTPException(status_code=401, detail=detail)

    user = db.query(Users).filter(Users.id == decoded.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    if user.email != decoded.get("sub"):
        raise HTTPException(status_code=422, detail="Email mismatch!")

    return user

def require_manager(user: Users = Depends(get_user_from_jwt_token)) -> Users:
    if user.role != UserRole.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can perform this action."
        )
    return user 