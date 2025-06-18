# 🛒 VALUEGATE POS SYSTEM

A powerful multi-business Point‑of‑Sale system with:

- 🖥️ **Backend**: FastAPI + PostgreSQL with JWT authentication and barcode-enabled PDF receipts
- 📊 **Dashboard**: Streamlit-based analytics and transaction management
- 🖨️ **Desktop App**: Tkinter POS for offline use with auto-sync and thermal printing
- 📱 **Mobile App**: React Native POS app (Expo) for Android
- 🧾 **Receipts**: PDF format with logo, barcode, customer & seller details
- 📦 **Extras**: Excel reporting, auto email summaries, Docker-ready setup

---

## ⚙️ Prerequisites

- Python 3.11+
- PostgreSQL (hosted e.g., on Supabase)
- Node.js and npm
- Expo CLI (for mobile app):   ```bash
  npm install -g expo-cli
USB thermal printer drivers (for desktop receipts)

🧪 Setup Instructions
🔧 1. Backend (FastAPI)
bash
Copy
Edit
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
Set up .env in the backend/ folder:

ini
Copy
Edit
DATABASE_URL=postgresql://postgres:Ngams2715**@db.fgxebhqyspfwmqjqnpgr.supabase.co:5432/postgres
SECRET_KEY=your-secret-key
🖥️ 2. Streamlit Dashboard (Admin Panel)
bash
Copy
Edit
cd dashboard
pip install -r requirements.txt
streamlit run app.py
Make sure .env in the dashboard/ folder contains:

bash
Copy
Edit
DATABASE_URL=postgresql://postgres:Ngams2715**@db.fgxebhqyspfwmqjqnpgr.supabase.co:5432/postgres
🖨️ 3. Desktop App (Tkinter)
bash
Copy
Edit
cd desktop_app
pip install -r requirements.txt
python app.py
Supports offline data entry with auto-sync every 30 seconds (background thread). Set up a local SQLite database for offline use.

📱 4. Mobile App (React Native)
bash
Copy
Edit
cd mobile_app
npm install
expo start
Log in via QR code using Expo Go on Android.

Make sure API URLs match your deployed FastAPI backend.

📤 Deployment
You can deploy the backend on:

Render

Railway

Supabase (for PostgreSQL hosting only)

To connect your Supabase PostgreSQL:

bash
Copy
Edit
DATABASE_URL=postgresql://postgres:password@db.fgxebhqyspfwmqjqnpgr.supabase.co:5432/postgres
📧 Email Reports (Optional)
Enable automatic daily/weekly email of sales reports using:

SMTP with smtplib

Excel generation via pandas.to_excel()

🧾 Sample Receipt Preview
Receipts include:

Business logo (optional)

Barcode receipt ID

Seller & customer details

Item breakdown

PDF + Excel exports

✅ Tech Stack Summary
Layer Stack
Backend FastAPI, SQLAlchemy, JWT
Database PostgreSQL (Supabase)
Frontend Web Streamlit
Desktop App Tkinter
Mobile App React Native (Expo)
PDF/Barcode fpdf, python-barcode
Reports Pandas, Excel, CSV, Email

📎 License
MIT License

👩🏽‍💻 Author
Asogwa Chinenye Joy
Valuegate Consulting
Email: <asogwachinenye10@gmail.com>
Twitter: <https://x.com/AsogwaChin82174>
