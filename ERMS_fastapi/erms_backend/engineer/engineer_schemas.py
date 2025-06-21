from typing import  List
from pydantic import BaseModel
from auth.auth_schemas import UserProfile



class Engineers(BaseModel):
    engineer: List[UserProfile]

class EngineerCapacity(UserProfile):
    allocated_percentage: int
    available_capacity: int