"""
user_routes.py
Handles requests on endpoints related to user profile
"""

# Import dependencies
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# Utility imports
from utils.servers import UserManager

# Security imports
from fastapi_jwt_auth import AuthJWT

# Import models
from models.user_models import (
    UpdateProfile
)


# Define helper variables
user_manager = UserManager()
user_router = APIRouter(prefix="/user", tags=["User Manager"])

# Update user profile
@user_router.post("/update")
async def update_user_profile(profile_details: UpdateProfile, Authorize: AuthJWT = Depends()):
    Authorize.fresh_jwt_required()
    try:
        username = Authorize.get_jwt_subject()
        user_email = user_manager.get_user_data(username, "Email")
        data_to_update = {
            "Username": profile_details.username,
            "Email": profile_details.email,
            "Profile.Description": profile_details.description,
            "Profile.Avatar": profile_details.avatar,
            "Banking Details.Account Pin": profile_details.account_pin,
        }
        user_manager.update_user_data(username, data_to_update, "", update_type=28)

        if user_email != profile_details.email:
            user_manager.update_user_data(username, {}, "Email Verified", False, 26)

        return JSONResponse(content={"Results": "Profile successfully updated"})

    except Exception as profile_update_error:
        return JSONResponse(content={"Results": "Cannot update your profile", "Error": str(profile_update_error)})
