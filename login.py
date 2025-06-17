from db_config import get_connection
from auth_utils import verify_password

def login(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user is None:
            print("Username not found.")
            return False

        user_id, password_hash = user
        if verify_password(password, password_hash):
            print(f"✅ Login successful! User ID: {user_id}")
            return True
        else:
            print("❌ Incorrect password.")
            return False

    except Exception as e:
        print(f"Login error: {e}")
        return False

    finally:
        if conn:
            cur.close()
            conn.close()

# Only runs when you directly run login.py
if __name__ == "__main__":
    username_input = input("Enter username: ")
    password_input = input("Enter password: ")
    login(username_input, password_input)
