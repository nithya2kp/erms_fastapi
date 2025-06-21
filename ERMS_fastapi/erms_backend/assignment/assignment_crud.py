
from models import Users,Assignments
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from .assignment_schemas import AssignmentDetails
from models import UserRole

def get_assignment_list(user: Users, db: Session) -> List[AssignmentDetails]:
    """
    Listing assignments
     Parameters:
     - user: User Object
     - db: DB Session

    Returns:
        Custom AssignmentDetails response
    """
    db_user = db.query(Users).filter(Users.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist!!")

    assignments = db.query(Assignments).all()

    results = []
    for a in assignments:
        engineer = db.query(Users).filter(Users.id == a.engineer_id).first()
        results.append(
            AssignmentDetails(
                assignment_name=a.assignment_name,
                start_date=a.start_date,
                end_date=a.end_date,
                engineer_name=engineer.name if engineer else None,
                allocation_percentage=a.allocation_percentage,
                role=a.role,
            )
        )

    return results


def create_assignment(data,db:Session):
    """
    Creating  assignments
     Parameters:
     -  data: request body
     - db: DB Session

    Returns:
        JSON response
    """
    assignment = Assignments(
        engineer_id=data.engineer_id,
        project_id=data.project_id,
        allocation_percentage=data.allocation_percentage,
        start_date=data.start_date,
        end_date=data.end_date,
        role=data.role,
        assignment_name=data.assignment_name
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return {"message": "Engineer assigned successfully", "assignment_id": str(assignment.id)}


def update_assignment(data,db:Session):
    """
    Updating particular assignment
     Parameters:
     - data: request body
     - db: DB Session

    Returns:
        JSON response
    """
    assignment = db.query(Assignments).filter(Assignments.id == data.assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    if data.engineer_id is not None:
        assignment.engineer_id = data.engineer_id
    if data.project_id is not None:
        assignment.project_id = data.project_id
    if data.allocation_percentage is not None: 
        assignment.allocation_percentage = data.allocation_percentage
    if data.start_date is not None:
        assignment.start_date = data.start_date
    if data.end_date is not None:
        assignment.end_date = data.end_date
    if data.role is not None:
        assignment.role = data.role
    if data.assignment_name is not None:
        assignment.assignment_name = data.assignment_name
    db.commit()
    db.refresh(assignment)

    return {"message": "Assignment updated successfully"}


def assignment_delete(id,db:Session):
    """
    Removing particular assignment
     Parameters:
     - id: assignment_id
     - db: DB Session

    Returns:
        JSON response
    """
    assignment = db.query(Assignments).filter(Assignments.id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    db.delete(assignment)
    db.commit()

    return {"message": "Assignment deleted successfully"}