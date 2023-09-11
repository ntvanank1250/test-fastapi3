from pydantic import BaseModel
from typing import Optional
# pydantic khai báo thuộc tính sử dụng (name: str):, còn SQLAlchemy  khai báo thuộc tính sử dụng =  (name = Column(String))
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    email: str


class CustomerCreate(CustomerBase):
    password: str

class ChangePassword(CustomerCreate):
    old_password: str
    class Config:
        extra = "allow"

class Customer(CustomerBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True
#################################
# khai bao cho cac admin

class AdminBase(BaseModel):
    email: str
    password : str
class AdminCreate(CustomerBase):
    name : str
    create_at: str