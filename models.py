from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String(200), nullable=False)
    role = Column(String(20), default="user")

    business = relationship("Business", back_populates="owner", uselist=False)

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100), nullable=False)
    address = Column(String(200))
    phone = Column(String(20))
    account_number = Column(String(50))

    owner = relationship("User", back_populates="business")
    products = relationship("Product", back_populates="business")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    business_id = Column(Integer, ForeignKey("businesses.id"))

    business = relationship("Business", back_populates="products")
    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    customer_name = Column(String(100))
    customer_address = Column(String(200))
    customer_phone = Column(String(20))
    sales_rep = Column(String(100))
    receipt_number = Column(String(50), unique=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="sales")
