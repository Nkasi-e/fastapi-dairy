import re
from pydantic import BaseModel, EmailStr, validator, constr
from fastapi import HTTPException
from datetime import datetime


class UserBase(BaseModel):
    firstname: constr(min_length=1, strip_whitespace=True)
    lastname: constr(min_length=1, strip_whitespace=True)
    email: EmailStr
    password: str
    cpassword: str

    @validator("password", pre=True)
    def check_password(cls, password):
        if not re.match(
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$", password
        ):
            raise HTTPException(
                status_code=400,
                detail="Password must have a minimum of 8 characters, 1 Uppercase, 1 lowercase and 1 number",
            )
        return password

    # @validator("firstname")
    # def check_firstname(cls, firstname):
    #     if firstname is None:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="The firstname field is required"
    #         )
    #     return firstname

    # @validator("lastname")
    # def check_lastname(cls, lastname):
    #     if lastname is None:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="The lastname field is required"
    #         )
    #     return lastname

    # @validator("email")
    # def check_email(cls, email):
    #     if email is None:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="The email field is required"
    #         )
    #     return email


class CreateUser(UserBase):
    pass


class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    email: str
    access_token: str
    token_type: str
