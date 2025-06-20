# ---------------- app.py ----------------
import streamlit as st
from db_config import session
from models import User, Business, Product, Sale
from auth_utils import hash_password, verify_password
from receipt_utils import generate_receipt_pdf_and_barcode

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

import os
import uuid
import datetime
import pandas as pd
import io

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

st.set_page_config(page_title="POS System", layout="centered")
st.title("POS System")

if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'role' not in st.session_state:
    st.session_state.role = "user"

page = st.sidebar.selectbox("Navigate", ["Login", "Register", "Dashboard"])

# ---------------- Register ----------------
if page == "Register":
    st.header("Register Your Business")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    business_name = st.text_input("Business Name")
    address = st.text_input("Business Address")
    account_number = st.text_input("Account Number")
    business_phone = st.text_input("Business Phone Number")
    role = st.selectbox("Select Role", ["user", "admin"])

    if st.button("Register"):
        if session.query(User).filter_by(username=username).first():
            st.error("Username already exists.")
        else:
            new_user = User(username=username, email=email, password_hash=hash_password(password), role=role)
            session.add(new_user)
            session.commit()

            new_business = Business(user_id=new_user.id, name=business_name, address=address, account_number=account_number, phone=business_phone)
            session.add(new_business)
            session.commit()
            st.success("Business registered successfully!")

# ---------------- Login ----------------
elif page == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = session.query(User).filter_by(username=username).first()
        if user and verify_password(password, user.password_hash):
            st.session_state.user_id = user.id
            st.session_state.role = user.role
            st.success("Login successful!")
        else:
            st.error("Invalid credentials.")

# ---------------- Dashboard ----------------
elif page == "Dashboard":
    if st.session_state.user_id is None:
        st.warning("Please login to access your dashboard.")
    else:
        user = session.query(User).get(st.session_state.user_id)
        business = session.query(Business).filter_by(user_id=user.id).first()

        st.header(f"{business.name} Dashboard")
        if st.button("Logout"):
            st.session_state.user_id = None
            st.rerun()

        st.write(f"Logged in as: **{user.username}** (Role: {user.role})")

        # ---------- Products ----------
        st.subheader("📦 Your Products")
        products = session.query(Product).filter_by(business_id=business.id).all()
        for p in products:
            st.write(f"{p.name} - ₦{p.price:.2f}")

        st.subheader("➕ Add New Product")
        product_name = st.text_input("Product Name")
        product_price = st.number_input("Price", min_value=0.0, step=0.01)
        if st.button("Add Product"):
            if product_name and product_price > 0:
                new_product = Product(name=product_name, price=product_price, business_id=business.id)
                session.add(new_product)
                session.commit()
                st.success("Product added successfully!")
                st.rerun()
            else:
                st.error("Enter valid name and price.")

        # ---------- Purchase ----------
        st.subheader("🛒 Buy a Product")
        if products:
            product_options = {f"{p.name} - ₦{p.price:.2f}": p.id for p in products}
            selected_product = st.selectbox("Select Product", list(product_options.keys()))
            product = session.query(Product).get(product_options[selected_product])

            with st.form("buy_form"):
                quantity = st.number_input("Quantity", min_value=1, step=1)
                customer_name = st.text_input("Customer Name")
                customer_address = st.text_input("Customer Address")
                customer_phone = st.text_input("Customer Phone Number")
                sales_rep = st.text_input("Sales Rep/Cashier Name")
                submit = st.form_submit_button("Confirm Purchase")

            if submit:
                total = quantity * product.price
                receipt_no = str(uuid.uuid4())[:8]
                timestamp = datetime.datetime.now()

                sale = Sale(
                    product_id=product.id,
                    quantity=quantity,
                    total=total,
                    customer_name=customer_name,
                    customer_address=customer_address,
                    customer_phone=customer_phone,
                    sales_rep=sales_rep,
                    receipt_number=receipt_no,
                    timestamp=timestamp
                )
                session.add(sale)
                session.commit()

                receipt_data = {
                    "business": {
                        "name": business.name,
                        "address": business.address,
                        "phone": business.phone
                    },
                    "customer": {
                        "name": customer_name,
                        "phone": customer_phone,
                        "address": customer_address
                    },
                    "items": [{
                        "name": product.name,
                        "price": product.price,
                        "quantity": quantity
                    }],
                    "receipt_no": receipt_no,
                    "seller": sales_rep,
                    "payment_mode": "Cash",
                    "tax_rate": 0.075,
                    "date": timestamp.strftime("%Y-%m-%d")
                }

                pdf_path = generate_receipt_pdf_and_barcode(receipt_data)

                st.success("Purchase successful!")
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Download PDF Receipt", data=f, file_name=f"{receipt_no}.pdf", mime="application/pdf")

        # ---------- Sales History ----------
        st.subheader("📈 Sales History")
        all_sales = session.query(Sale).join(Product).filter(Product.business_id == business.id).all()
        if not all_sales:
            st.info("No sales yet.")
        else:
            df_sales = pd.DataFrame([{
                "Product": s.product.name,
                "Quantity": s.quantity,
                "Total": s.total,
                "Customer": s.customer_name,
                "Date": s.timestamp.strftime('%Y-%m-%d'),
                "Sales Rep": s.sales_rep,
                "Receipt": s.receipt_number
            } for s in all_sales])

            st.dataframe(df_sales)
            st.download_button("📤 Export as CSV", data=df_sales.to_csv(index=False), file_name="sales.csv", mime="text/csv")
            excel_buffer = io.BytesIO()
            df_sales.to_excel(excel_buffer, index=False, engine='openpyxl')
            st.download_button("📥 Export as Excel", data=excel_buffer.getvalue(), file_name="sales.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # ---------- Admin Panel ----------
        if st.session_state.role == "admin":
            st.subheader("🛠️ Admin Panel")
            st.write("All Registered Users:")
            for u in session.query(User).all():
                st.write(f"🧑 {u.username} - {u.role}")

            st.markdown("---")
            st.subheader("🔐 Reset a User's Password")
            target_username = st.text_input("Username to Reset")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")

            if st.button("Reset Password"):
                if not target_username or not new_password or not confirm_password:
                    st.error("All fields are required.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    user_to_update = session.query(User).filter_by(username=target_username).first()
                    if not user_to_update:
                        st.error("User not found.")
                    else:
                        user_to_update.password_hash = hash_password(new_password)
                        session.commit()
                        st.success(f"Password for '{target_username}' has been reset successfully.")
