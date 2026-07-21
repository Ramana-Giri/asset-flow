from pydantic import BaseModel, EmailStr 

class EmployeeCreate(BaseModel):
    name: str
    email_address: EmailStr
    password: str

class EmployeeResponse(BaseModel):
    employee_id: int
    name: str
    email_address: EmailStr

    class Config:
        from_attributes = True