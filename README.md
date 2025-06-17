# 🛒 VALUEGATE POS SYSTEM

A fully integrated multi-business Point‑of‑Sale system with:

- 🖥️ **Backend**: FastAPI + PostgreSQL, JWT auth, barcode-enabled receipts
- 📊 **Dashboard**: Streamlit analytics for sales insights and summaries
- 🖨️ **Desktop App**: Tkinter-based offline POS with auto-sync and thermal printing
- 📱 **Mobile App**: React Native POS for Android (Expo)
- 🧾 **PDF Receipts**: Barcode, logo, customer, seller, and transaction details
- 📦 **Extras**: Excel reporting, email summaries, Docker deployment support

---

## ⚙️ Prerequisites

- Python 3.11+
- Node.js and npm
- PostgreSQL (13+ recommended)
- Expo CLI for mobile app  
  👉 Install with: `npm install -g expo-cli`
- (Optional) USB thermal printer drivers for desktop receipts

---

## 🧪 Setup Instructions

### 🔧 1. Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
