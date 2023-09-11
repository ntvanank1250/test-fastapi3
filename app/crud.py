from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas

# Customer


def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(
        email=customer.email, password=customer.password)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer_id: int, customer_new: schemas.Customer):
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id).first()
    if customer:
        customer.email = customer_new.email
        customer.is_active = customer_new.is_active
        customer.items = customer_new.items
        db.commit()
        db.refresh(customer)
    return customer


def change_pass_customer(db: Session, customer_id: int, use_new: schemas.ChangePassword):
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id).first()
    old_password = use_new.old_password
    if customer.password != old_password:
        raise HTTPException(
            status_code=400, detail="Old password is incorrect")
    if customer.email != use_new.email:
        raise HTTPException(status_code=400, detail="Email is incorrect")
    if customer:
        fake_password = use_new.password
        customer.password = fake_password
        db.commit()
        use_new.message = "Change password complete"

    return use_new

# Item


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def update_item(db: Session, item_id: int, item_new: schemas.ItemBase):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item:
        item.title = item_new.title
        item.description = item_new.description
        db.commit()
        db.refresh(item)
    return item
