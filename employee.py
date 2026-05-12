from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="John")
    last_name: str = Field(..., min_length=1, max_length=50, example="Doe")
    email: EmailStr = Field(..., example="john.doe@company.com")
    phone: Optional[str] = Field(None, max_length=20, example="+1-555-0100")
    department: str = Field(..., min_length=1, max_length=100, example="Engineering")
    job_title: str = Field(..., min_length=1, max_length=100, example="Software Engineer")
    salary: float = Field(..., gt=0, example=75000.00)
    is_active: bool = Field(default=True)
    hire_date: Optional[str] = Field(None, example="2024-01-15")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    job_title: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None
    hire_date: Optional[str] = None


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EmployeeListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    employees: list[EmployeeResponse]
