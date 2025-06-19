# auth_utils.py
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return check_password_hash(hashed, password)
    except ValueError:
        return False  # Handle invalid hash
