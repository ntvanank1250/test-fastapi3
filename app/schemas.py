from pydantic import BaseModel
from typing import Optional
# pydantic khai báo thuộc tính sử dụng (name: str):, còn SQLAlchemy  khai báo thuộc tính sử dụng =  (name = Column(String))

# ITEM


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


# CUSTOMER
class CustomerBase(BaseModel):
    email: str


class CustomerCreate(CustomerBase):
    password: str


class ChangePassword(CustomerCreate):
    old_password: str

    class Config:
        extra = "allow"


class CustomerImage(CustomerBase):
    list_image: list
    image: str


class Customer(CustomerBase):
    id: int
    is_active: bool
    items: list

    class Config:
        from_attributes = True

# USER


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    create_at: str

# DOMAIN


class DomainCreate(BaseModel):
    name: str
    status: str
    domain_id: str
    user_id: int
    create_at: str

# ORIGIN


class OriginCreate(BaseModel):
    name: str
    upstr_host: str
    upstr_address: str
    protocol: str
    domain_id: int
    create_at: str
