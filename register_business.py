from db_config import get_connection
from auth_utils import hash_password

def register_business(username, password, email, business_name, address, phone, account_number):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # ✅ Hash the password
        hashed = hash_password(password)

        # ✅ Insert into users table
        cur.execute("""
            INSERT INTO users (username, password_hash, email)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (username, hashed, email))
        user_id = cur.fetchone()[0]

        # ✅ Insert into businesses table
        cur.execute("""
            INSERT INTO businesses (user_id, name, address, phone, account_number)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, business_name, address, phone, account_number))

        conn.commit()
        print("✅ Business and user registered successfully.")

    except Exception as e:
        print(f"❌ Registration failed: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    register_business(
        username="demo_user",
        password="demo12345",
        email="demo@example.com",
        business_name="Demo Business",
        address="123 Market Street",
        phone="08012345678",
        account_number="ACCT-DEMO-001"
    )
