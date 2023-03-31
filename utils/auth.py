"""
auth.py
Authentication utility functions
"""

# Import dependencies
from random import randint
from utils.servers import UserManager
from passlib.context import CryptContext


# Define helper variables
user_manager = UserManager()
context = CryptContext(schemes=["bcrypt"])

# Validate user registration
def validate_user_registration(username: str, email: str):
    # Check if username and email are valid
    _username = user_manager.get_user_data(username)
    if _username is None:
        _email = user_manager.get_user_data(username, email)
        if _email is None:
            return 1

        elif _email is not None:
            return 71

    elif _username is not None:
        return 42

# Authenticate user with username and password
def authenticate_user(username: str, password: str):
    _username = user_manager.get_user_data(username)
    if _username is not None:
        password_verification = verify_password_hash(username, password)
        if password_verification == 1:
            return 1

        elif password_verification == 0:
            return 30

    elif _username is None:
        return 10

# Create password hash
def create_password_hash(plain_password: str):
    return context.hash(plain_password)

# Verify password hash
def verify_password_hash(username: str, plain_password: str):
    hashed_password = user_manager.get_user_data(username, "Password")
    return context.verify(plain_password, hashed_password)

# Generate otp
def generate_otp():
    otp = ""
    for digits in range(4):
        otp += str(randint(1, 9))

    return otp
