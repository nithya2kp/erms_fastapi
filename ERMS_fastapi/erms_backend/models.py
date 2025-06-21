import enum
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID, VARCHAR
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

class UserRole(enum.Enum):
    ENGINEER = "engineer"
    MANAGER = "manager"

class SeniorityLevel(enum.Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"

class ProjectStatus(enum.Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"

class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )


class Users(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str | None] = mapped_column(VARCHAR(100), nullable=True)
    password_hash: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(VARCHAR(100))
    name: Mapped[str | None] = mapped_column(VARCHAR(50), nullable=True)
    seniority_level: Mapped[SeniorityLevel] = mapped_column(
        Enum(SeniorityLevel), nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False
    )
    skills: Mapped[list[str]] = mapped_column(ARRAY(String))
    max_capacity : Mapped[int|None] = mapped_column(Integer, nullable=True) # 100 for full-time, 50 for part-time

    password_updated_at: Mapped[TIMESTAMP | None] = mapped_column(
        TIMESTAMP(timezone=True), onupdate=func.now(), nullable=True
    )
    department: Mapped[str|None] = mapped_column(nullable=True)

    managed_projects: Mapped[list["Projects"]] = relationship(
    back_populates="manager", foreign_keys="Projects.manager_id"
    )
    assignments: Mapped[list["Assignments"]] = relationship(
    back_populates="engineer", foreign_keys="Assignments.engineer_id"
    )


class Projects(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), nullable=False
    )
    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(nullable=True)
    
    start_date: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    end_date: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    manager_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    required_skills: Mapped[list[str]] = mapped_column(ARRAY(String))
    team_size: Mapped[int] = mapped_column(Integer, nullable=True)

    manager: Mapped["Users"] = relationship(back_populates="managed_projects")
    assignments: Mapped[list["Assignments"]] = relationship(back_populates="project")

class Assignments(Base,TimestampMixin):
    __tablename__ = "assignments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id")
    )
    assignment_name: Mapped[str] = mapped_column()
    start_date: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    end_date: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    engineer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    allocation_percentage: Mapped[int] = mapped_column(Integer, nullable=True)
    role: Mapped[str] = mapped_column()

    project: Mapped["Projects"] = relationship(back_populates="assignments")
    engineer: Mapped["Users"] = relationship(back_populates="assignments")