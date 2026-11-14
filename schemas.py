from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=10, max_length=128)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=40)
    notes: str | None = None

class ClientOut(ClientCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    description: str | None = None
    status: str = "active"

class ProjectOut(ProjectCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    status: str = "todo"
    priority: str = "normal"
    due_date: datetime | None = None

class TaskOut(TaskCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    created_at: datetime
