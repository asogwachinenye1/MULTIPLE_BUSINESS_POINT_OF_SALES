from db_config import session
from models import User
from werkzeug.security import check_password_hash
from auth_utils import hash_password

def reset_invalid_passwords(default_password="default123"):
    users = session.query(User).all()
    reset_count = 0

    for user in users:
        try:
            # Try validating hash to detect invalid format
            check_password_hash(user.password_hash, "test")
        except Exception:
            print(f"🔁 Resetting invalid password for: {user.username}")
            user.password_hash = hash_password(default_password)
            reset_count += 1

    session.commit()
    print(f"✅ Done. {reset_count} user(s) password reset to default.")

if __name__ == "__main__":
    reset_invalid_passwords()
