from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeLogin
from app.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=EmployeeResponse, status_code=201)
def register_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(Employee)
        .filter(Employee.email_address == employee.email_address)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Email address already registered")

    new_employee = Employee(
        name=employee.name,
        email_address=employee.email_address,
        hashed_password=hash_password(employee.password),
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


@router.post("/login")
def login_employee(credentials: EmployeeLogin, db: Session = Depends(get_db)):
    employee = (
        db.query(Employee)
        .filter(Employee.email_address == credentials.email_address)
        .first()
    )

    if not employee or not verify_password(
        credentials.password, employee.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "message": "Login successful",
        "employee id": employee.employee_id,
        "name": employee.name,
    }
