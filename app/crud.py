from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_new: schemas.User):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.email = user_new.email
        user.is_active = user_new.is_active
        user.items = user_new.items
        db.commit()
        db.refresh(user)
    return user

def change_pass_user(db: Session, user_id: int, use_new: schemas.ChangePassword):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    old_hashed_password = use_new.old_password + "notreallyhashed"
    if user.hashed_password != old_hashed_password:
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    if user.email != use_new.email:
        raise HTTPException(status_code=400, detail="Email is incorrect")
    if user:
        fake_hashed_password = use_new.password + "notreallyhashed"
        user.hashed_password = fake_hashed_password
        db.commit()
        use_new.message = "Change password complete"

    return use_new


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item( db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def update_item(db: Session, item_id: int, item_new: schemas.ItemBase):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item:
        item.title = item_new.title
        item.description = item_new.description
        db.commit()
        db.refresh(item)
    return item


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item