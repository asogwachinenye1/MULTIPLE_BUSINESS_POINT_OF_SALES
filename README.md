# 📦 POS System – Streamlit + FastAPI

This is a full-featured Point of Sale (POS) system that allows business owners to register, manage products, record sales, and generate professional PDF receipts with barcodes.

✅ Features
🧾 Business registration

🔐 User login (admin/user roles)

📦 Product management

🛒 Sales recording

📄 PDF receipt generation with:

Business + customer header

Items list (S/N, Name, Price, Qty, Subtotal)

Tax, Total

Barcode

Signature placeholder

📊 Sales history exportable as CSV & Excel

🛠️ Admin panel for password reset

☁️ PostgreSQL hosted on Supabase

🎨 Streamlit frontend interface

🏗️ Folder Structure
bash
Copy
Edit
pos_project/
│
├── app.py                    # Main Streamlit frontend
├── auth_utils.py             # Password hashing & verification
├── db_config.py              # Database session setup
├── models.py                 # SQLAlchemy models
├── receipt_utils.py          # PDF + barcode receipt generator
├── requirements.txt          # Python dependencies
├── .env                      # Contains SUPABASE_DB_URL
└── README.md                 # Project documentation
🛠️ Setup Instructions

✅ Clone the repository
bash
Copy
Edit
git clone <https://github.com/your-username/pos-system.git>
cd pos-system

✅ Create .env file
Create a .env file and add:

ini
Copy
Edit
SUPABASE_DB_URL=your_postgres_connection_url
You can get this from Supabase project > Database > Connection Info.

✅ Install dependencies
Use pip to install required libraries:

bash
Copy
Edit
pip install -r requirements.txt

✅ Run the app
bash
Copy
Edit
streamlit run app.py
🧾 Sample Receipt Layout
markdown
Copy
Edit

----------------------------------------------------

               [BUSINESS LOGO / NAME]
          Address | Phone | Account Number

Customer: [Name]        Phone: [Phone]
Address:  [Address]

Date: YYYY-MM-DD        Receipt No: XXXXXXXX
Sales Rep: [Cashier Name]

----------------------------------------------------
S/N  Item         Price   Qty   Subtotal
1    Product A    ₦500    2     ₦1000

                     Tax (7.5%): ₦75
                     Total:      ₦1075
----------------------------------------------------

[Barcode Image]

Customer Signature: _______________
Seller Signature: ________________
📦 PDF & Barcode Tools
This app uses:

reportlab – for structured PDF layout

python-barcode – to generate receipt barcode

Pillow – for image rendering

📊 Export Options
Download PDF receipt for every transaction

Export Sales history as:

CSV

Excel (.xlsx)

🧑‍💼 Admin Features
If logged in as admin:

View all registered users

Reset any user’s password securely

💡 Ideas for Future Upgrades
📱 Mobile view / React Native frontend

📦 Inventory alerts

🧾 Invoice printing with POS printer

📤 Auto-email PDF receipts or reports

📅 Daily/Weekly/Monthly sales summaries

📮 Contact
For help or collaboration:
email: <asogwachinenyejoy@gmail.com>
Twitter: <https://x.com/AsogwaChin82174>
