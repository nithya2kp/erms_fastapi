from pydantic import BaseModel
import uuid
from models import ProjectStatus
from datetime import datetime

class ProjectDetails(BaseModel):
    id: uuid.UUID | None = None
    project_status: ProjectStatus
    name: str
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    manager_id: uuid.UUID | None = None
    required_skills: list[str]
    team_size: int | None = None

    class Config:
        from_attributes = True


class AddProject(BaseModel):
    id: uuid.UUID|None = None
    project_status: ProjectStatus|None =None
    name: str|None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    required_skills: list[str|None] = None
    team_size: int | None = None


