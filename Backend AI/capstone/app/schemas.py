from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    password: str
    tenant_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TenantResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WidgetCreate(BaseModel):
    name: str


class WidgetResponse(BaseModel):
    id: int
    name: str
    tenant_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SubmissionCreate(BaseModel):
    data: str


class SubmissionResponse(BaseModel):
    id: int
    widget_id: int
    tenant_id: int
    data: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)