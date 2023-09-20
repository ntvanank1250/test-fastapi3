from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas

# CUSTOMER

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

# ITEM
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

# USER
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
            name = user.name,
            email = user.email,
            password = user.password,
            create_at = user.create_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Domain
def get_domain(db: Session, id_domain: int):
    return db.query(models.Domain).filter(models.Domain.id == id_domain).first()

def get_domain_by_name(db: Session, name: int):
    return db.query(models.Domain).filter(models.Domain.name == name).first()

def get_domains(db: Session,user_id, skip: int = 0, limit: int = 100):
    query = db.query(models.Domain)
    query = query.filter(models.Domain.user_id == user_id)
    query = query.offset(skip).limit(limit)
    return query.all()

def create_domain(db: Session, domain: schemas.DomainCreate):
    db_domain = models.Domain(
            name = domain.name,
            status = domain.status,
            user_id = domain.user_id,
            domain_id = domain.domain_id,
            create_at = domain.create_at)
    db.add(db_domain)
    db.commit()
    db.refresh(db_domain)
    return db_domain

# Origin
def get_origin(db: Session, origin_id: int):
    return db.query(models.Origin).filter(models.Origin.id == origin_id).first()

def get_origins(db: Session,domain_id, skip: int = 0, limit: int = 100):
    query = db.query(models.Origin)
    query = query.filter(models.Origin.domain_id == domain_id)
    query = query.offset(skip).limit(limit)
    return query.all()

def create_origin(db: Session, origin: schemas.OriginCreate):
    db_origin = models.Origin(
            name = origin.name,
            upstr_host = origin.upstr_host,
            upstr_address = origin.upstr_address,
            protocol = origin.protocol,
            domain_id = origin.domain_id,
            create_at = origin.create_at)
    db.add(db_origin)
    db.commit()
    db.refresh(db_origin)
    return db_origin