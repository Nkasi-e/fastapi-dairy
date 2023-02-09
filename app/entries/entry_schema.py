from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class EntryBase(BaseModel):
    title: constr(min_length=3)
    content: constr(min_length=3)


class CreateEntry(EntryBase):
    pass


class UserDetails(BaseModel):
    firstname: str
    email: EmailStr

    class Config:
        orm_mode = True


class EntryOut(EntryBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserDetails

    class Config:
        orm_mode = True
