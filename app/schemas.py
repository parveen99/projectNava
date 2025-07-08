
#using pydantic validation
from pydantic import BaseModel, EmailStr
from datetime import datetime


class OrganizationCreate(BaseModel):
    email: EmailStr
    password: str
    organization_name: str


class OrganizationResponse(BaseModel):
    id: int
    name: str
    database_name: str
    created_at: datetime
    is_active: bool 
    
    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
