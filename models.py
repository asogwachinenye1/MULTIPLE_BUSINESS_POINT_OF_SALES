from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)
    business = relationship("Business", back_populates="user", uselist=False)

class Business(Base):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    account_number = Column(String)
    phone = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="business")
    products = relationship("Product", back_populates="business")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    business_id = Column(Integer, ForeignKey('businesses.id'))
    business = relationship("Business", back_populates="products")
    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    total = Column(Float)
    customer_name = Column(String)
    customer_address = Column(String)
    customer_phone = Column(String)
    sales_rep = Column(String)
    receipt_number = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    product = relationship("Product", back_populates="sales")
