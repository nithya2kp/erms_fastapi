from sqlalchemy.orm import Session
from models import Users,UserRole,Assignments
from fastapi import HTTPException
from .engineer_schemas import Engineers,EngineerCapacity
from auth.auth_schemas import UserProfile
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


def get_engineers(db:Session)->Engineers:
    """
    Listing out engineers
     Parameters:
     - db (Session): Database session

    Returns:
        Custom Engineer response
    """
    engineers = db.query(Users).filter(Users.role == UserRole.ENGINEER).all()
    profiles = [UserProfile.model_validate(e, from_attributes=True) for e in engineers]
    return Engineers(engineer=profiles)

def get_engineer_capacity(engineer_id:UUID,db:Session)->EngineerCapacity:
    """
    Calculate engineer capacity
     Parameters:
     - id: Engineer id
     - db (Session): Database session

    Returns:
        Custom EngineerCapacity response
    """
    engineer = db.query(Users).filter(Users.id == engineer_id).first()
    if not engineer:
        raise HTTPException(status_code=404, detail="Engineer not found")

    if engineer.role != UserRole.ENGINEER:
        raise HTTPException(status_code=400, detail="User is not an engineer")
    
    now = datetime.utcnow()
    active_assignments = db.query(Assignments).filter(
        Assignments.engineer_id == engineer.id,
        Assignments.start_date <= now,
        Assignments.end_date >= now
    ).all()

    total_allocated = sum(a.allocation_percentage for a in active_assignments)

    available_capacity = engineer.max_capacity - total_allocated
    available_capacity = max(available_capacity, 0)

    return EngineerCapacity(
    id=engineer.id,
    name=engineer.name,
    email=engineer.email,
    role=engineer.role,
    allocated_percentage=total_allocated,
    available_capacity=available_capacity
)