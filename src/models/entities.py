"""
Pydantic models for Asana entities.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from uuid import uuid4


def generate_uuid() -> str:
    """Generate UUID for Asana GID simulation."""
    return str(uuid4())


class Organization(BaseModel):
    organization_id: str = Field(default_factory=generate_uuid)
    name: str
    domain: str
    is_organization: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class Team(BaseModel):
    team_id: str = Field(default_factory=generate_uuid)
    organization_id: str
    name: str
    description: Optional[str] = None
    team_type: str
    created_at: datetime = Field(default_factory=datetime.now)


class User(BaseModel):
    user_id: str = Field(default_factory=generate_uuid)
    organization_id: str
    email: str
    first_name: str
    last_name: str
    role: str = 'member'
    job_title: Optional[str] = None
    department: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    last_active_at: Optional[datetime] = None


class TeamMembership(BaseModel):
    membership_id: str = Field(default_factory=generate_uuid)
    team_id: str
    user_id: str
    is_team_lead: bool = False
    joined_at: datetime = Field(default_factory=datetime.now)


class Project(BaseModel):
    project_id: str = Field(default_factory=generate_uuid)
    organization_id: str
    team_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    project_type: str
    workflow_type: str
    status: str = 'active'
    owner_id: Optional[str] = None
    is_public: bool = True
    color: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    due_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None


class Section(BaseModel):
    section_id: str = Field(default_factory=generate_uuid)
    project_id: str
    name: str
    position: int
    created_at: datetime = Field(default_factory=datetime.now)


class Task(BaseModel):
    task_id: str = Field(default_factory=generate_uuid)
    project_id: Optional[str] = None
    section_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    assignee_id: Optional[str] = None
    created_by: str
    status: str = 'incomplete'
    due_date: Optional[date] = None
    start_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    completed_by: Optional[str] = None
    is_milestone: bool = False
    num_likes: int = 0
    num_subtasks: int = 0
    num_comments: int = 0


class Comment(BaseModel):
    comment_id: str = Field(default_factory=generate_uuid)
    task_id: str
    user_id: str
    comment_type: str = 'comment'
    text: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_pinned: bool = False
    num_likes: int = 0


class CustomFieldDefinition(BaseModel):
    field_id: str = Field(default_factory=generate_uuid)
    organization_id: str
    name: str
    description: Optional[str] = None
    field_type: str
    is_global: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


class CustomFieldEnumOption(BaseModel):
    option_id: str = Field(default_factory=generate_uuid)
    field_id: str
    name: str
    color: Optional[str] = None
    position: int
    enabled: bool = True


class CustomFieldValue(BaseModel):
    value_id: str = Field(default_factory=generate_uuid)
    task_id: str
    field_id: str
    text_value: Optional[str] = None
    number_value: Optional[float] = None
    date_value: Optional[date] = None
    enum_option_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)


class Tag(BaseModel):
    tag_id: str = Field(default_factory=generate_uuid)
    organization_id: str
    name: str
    color: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class TaskTag(BaseModel):
    task_tag_id: str = Field(default_factory=generate_uuid)
    task_id: str
    tag_id: str
    created_at: datetime = Field(default_factory=datetime.now)


class Attachment(BaseModel):
    attachment_id: str = Field(default_factory=generate_uuid)
    task_id: str
    uploaded_by: str
    filename: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    storage_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class Portfolio(BaseModel):
    portfolio_id: str = Field(default_factory=generate_uuid)
    organization_id: str
    name: str
    description: Optional[str] = None
    owner_id: Optional[str] = None
    color: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)