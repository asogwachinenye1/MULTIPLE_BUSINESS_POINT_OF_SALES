import bcrypt

def hash_password(plain_password):
    # Hash a plain password and return the hashed version
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(plain_password, hashed_password):
    # Verify a plain password against the hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
