from db_config import db
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    businesses = db.relationship('Business', backref='owner', cascade="all, delete-orphan")


class Business(db.Model):
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    account_number = db.Column(db.String(50))
    phone = db.Column(db.String(20))  # ✅ Ensure this is added



class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    sales = db.relationship("Sale", back_populates="product", cascade="all, delete-orphan")


class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String, default=lambda: str(uuid.uuid4())[:8], unique=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    customer_name = db.Column(db.String(100))
    customer_address = db.Column(db.String(200))
    customer_phone = db.Column(db.String(20))
    sales_rep = db.Column(db.String(100))

    product = db.relationship("Product", back_populates="sales")
