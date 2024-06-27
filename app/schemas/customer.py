from pydantic import BaseModel


from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class CustomerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class CustomerCreate(BaseModel):
    name: str
    mobile: str = Field(..., pattern=r"^\d{10}$")
    age: Optional[int] = Field(None, ge=0, le=100)
    active: bool = True
    status: CustomerStatus = CustomerStatus.ACTIVE

    class Config:
        from_attributes = True


class CustomerResponse(BaseModel):
    name: str
    mobile: str
    age: Optional[int]
    active: bool
    status: CustomerStatus
