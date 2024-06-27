from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services import customer_service
from typing import List
from app.utils.dependencies import get_db

router = APIRouter()


@router.post("/create/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    return customer_service.create_customer(customer=customer, db=db)


@router.get("/list/", response_model=List[CustomerResponse])
def list_customer(db: Session = Depends(get_db)):
    """List all customer"""
    customers = customer_service.list_customer(db)
    # import pdb

    # pdb.set_trace()
    return customers
