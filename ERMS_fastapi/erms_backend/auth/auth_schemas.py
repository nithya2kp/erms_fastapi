from typing import Annotated, List, Optional
import enum
from pydantic import BaseModel, StringConstraints, constr
import uuid
from models import SeniorityLevel,UserRole

class UserLogin(BaseModel):
    """ User Login response model """
    email: str | None = None
    name: str | None = None
    access_token: str | None = None

class UserProfile(BaseModel):
    username: str | None = None
    email: str | None = None
    name: str | None = None
    seniority_level: SeniorityLevel = SeniorityLevel.JUNIOR
    role: UserRole = UserRole.ENGINEER
    skills: list[str] | None = []
    max_capacity : int|None = None
    department: str|None = None

    class Config:
        from_attributes = True  