from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.db.models import Customer as Customer
from sqlalchemy.exc import IntegrityError
from typing import Any, List

# from app.schemas.customer import Customer
from app.db.session import SessionLocal


def list_customer(db: Session) -> List[CustomerResponse]:
    return db.query(Customer).all()


def create_customer(customer: CustomerCreate, db: Session) -> Customer:
    """Create a new customer"""
    try:
        db = SessionLocal()
        db_customer = Customer(
            name=customer.name,
            mobile=customer.mobile,
            age=customer.age,
            active=customer.active,
            status=customer.status.value,
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Duplicate mobile number")
