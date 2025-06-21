from pydantic import BaseModel
from datetime import datetime
import uuid

class AssignmentDetails(BaseModel):
    assignment_name: str|None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    engineer_name: str | None = None
    allocation_percentage: int|None = None
    role:str|None = None

    class Config:
        from_attributes = True

class CreateAssignment(BaseModel):
    assignment_id: uuid.UUID|None = None
    assignment_name: str|None = None
    engineer_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None
    allocation_percentage: int |None = None
    start_date: datetime|None = None
    end_date: datetime|None = None
    role: str|None = None