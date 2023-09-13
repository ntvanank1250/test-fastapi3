from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app import database
Base = database.Base

# CUSTOMER


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("customers.id"))
    owner = relationship("Customer", back_populates="items")


# ADMIN


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    create_at = Column(String)

    domains = relationship("Domain", back_populates="user")


class Domain(Base):
    __tablename__ = "domain"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    status = Column(String)
    domain_id = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    create_at = Column(String)
    user = relationship("User", back_populates="domains")
    origins = relationship("Origin", back_populates="domain")


class Origin(Base):
    __tablename__ = "origin"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    upstr_host = Column(String)
    upstr_address = Column(String)
    protocol = Column(String)
    domain_id = Column(Integer, ForeignKey("domain.id"))
    create_at = Column(String)

    domain = relationship("Domain", back_populates="origins")
