"""
auth.py
Handles authentication endpoints and processes authentication
"""

# Import dependencies
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# Import models
from models.auth_models import (
    Login, NewUser
)

# JWT imports
from fastapi_jwt_auth import AuthJWT
from config.settings import JWTSettings, JWTSettings

# Import utitility functions
from utils.servers import UserManager, users_collections, EmailHandler
from utils.auth import (
    validate_user_registration, create_password_hash, authenticate_user, generate_otp
)

# Define helper variables
auth_router = APIRouter(prefix="/auth", tags=["Authenticator"])
user_manager = UserManager()
jwt_settings = JWTSettings()


# User registration
@auth_router.post("/register")
async def register_user(user_details: NewUser):
    user_validation = validate_user_registration(user_details.username, user_details.email)
    if user_validation == 42:
        return JSONResponse(content={"Results": "Registration failed.", "Error": "Username not available."})

    elif user_validation == 71:
        return JSONResponse(content={"Results": "Registration failed.", "Error": "Email already exists."})

    elif user_validation == 1:
        user_data = {
            "Username": user_details.username,
            "Email": user_details.email,
            "Password": create_password_hash(user_details.password),
            "JWT Tokens": {
                "Access Token": "",
                "Refresh Token": "",
            },
            "Profile": {
                "Avatar": "",
                "Description": "",
                "Friends": []
            },
            "Banking Details": {
                "Account Pin": user_details.account_pin,
                "Balance": 1000,
                "Transactions": []
            },
            "Email Verified": False,
            "Verification Code": "",
        }

        users_collections.insert_one(user_data)
        return JSONResponse(content={"Results": "Registration successful.", "Info": "Please verify your email address."})

# Login user
@auth_router.post("/login")
async def login_user(login_details: Login, Authorize: AuthJWT = Depends()):
    user_authentication = authenticate_user(login_details.username, login_details.password)
    if user_authentication == 1:
        payload = {
            "username": login_details.username,
            "password": user_manager.get_user_data(login_details.username, "Password"),
            "email verified": user_manager.get_user_data(login_details.username, "Email Verified")
        }
        access_token = Authorize.create_access_token(subject=login_details.username, user_claims=payload,
        expires_time=jwt_settings.access_token_exp_time, fresh=True)
        refresh_token = Authorize.create_refresh_token(subject=login_details.username, expires_time=jwt_settings.refresh_token_exp_time,
        algorithm="HS256"
        )
        user_manager.update_user_data(login_details.username, key="JWT Tokens.Access Token", value=access_token, update_type=26)
        user_manager.update_user_data(login_details.username, key="JWT Tokens.Refresh Token", value=refresh_token, update_type=26)
        return JSONResponse(content={"Results": "Login successful.", "Access token": access_token,
        "Refresh token": refresh_token
        })

    elif user_authentication == 30 or 10:
        return JSONResponse(content={"Results": "Login failed.", "Error": "Invalid username or password."})

# Generate new access token
@auth_router.post("/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    username = Authorize.get_jwt_subject()
    password = user_manager.get_user_data(username, "Password")
    payload = {
        "username": username,
        "password": password
    }
    new_access_token = Authorize.create_access_token(username, user_claims=payload, fresh=True)
    user_manager.update_user_data(username, key="JWT Tokens.Access Token", value=new_access_token, update_type=26)
    return JSONResponse(content={"Results": "Success"})

# Logout user
@auth_router.post("/logout")
def logout(Authorize: AuthJWT = Depends()):
    Authorize.fresh_jwt_required()
    username = Authorize.get_jwt_subject()
    user_manager.update_user_data(username, key="JWT Tokens.Access Token", value="", update_type=26)
    return JSONResponse(content={"Results": "Success"})
