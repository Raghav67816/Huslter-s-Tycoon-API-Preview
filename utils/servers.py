"""
servers.py
Server utitlity functions for querying data from database.
"""

# Import dependencies
from typing import Optional
from trycourier import Courier
from config.settings import DatabseConfig


# Define helper variables
database_config = DatabseConfig()
email_client_auth_key = "pk_prod_KHEBV5DZPS48BAMA2AX3267SVB2Y"
client = Courier(auth_token=email_client_auth_key)


# Define collections
users_collections = database_config.users_collections

"""
User Manager
Handles requests for user related information
"""

class UserManager:

    # Get user custom data
    @staticmethod
    def get_user_data(username: str, key: str = "Username"):
        raw_data = users_collections.find_one({"Username": username})
        if raw_data is None:
            return None

        elif raw_data is not None:
            return raw_data[key]

    # Update user data
    @staticmethod
    def update_user_data(username: str, data: Optional[dict] = {}, key: Optional[str] = "", value: str = "", update_type: int = 26):
        if update_type == 26: # Single update
            users_collections.update_one({"Username": username}, {"$set": {key: value}})

        elif update_type == 28: # Dictionary update
            users_collections.update_many({"Username": username}, {"$set": data})

class EmailHandler:

    # Send email for email verification
    @staticmethod
    def send_email_for_email_verification(username: str, email: str, otp: str):
        response = client.send_message(
            message={
                "to": {"email": email},
                "template": "BDM7EENE7S41FPPDCSBTTH4F628E",
                "data": {
                    "username": username,
                    "otp": otp
                }
            }
        )

    # Send email to reset password
    def send_email_to_reset_password(username: str, email: str):
        response = client.send_message(
            message={
                "to": {"email": email},
                "template": "BDM7EENE7S41FPPDCSBTTH4F628E",
                "data": {
                    "username": username,
                }
            }
        )
