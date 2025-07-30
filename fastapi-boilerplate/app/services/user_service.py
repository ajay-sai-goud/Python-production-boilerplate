import datetime
from loguru import logger
from opentelemetry import trace
from fastapi import HTTPException, status

from app import schemas
from app import functions
from app import utils

tracer = trace.get_tracer(__name__)

# In a real application, this would be your database model.
# For this example, we'll just use a simple dictionary and a counter.
fake_user_db = {}
user_id_counter = 1

class UserService:
    """
    Service layer for handling user-related business logic.
    """

    async def create_user(self, user_data: schemas.UserCreate) -> schemas.UserDisplay:
        """
        Creates a new user after validating the username.
        """
        with tracer.start_as_current_span("user_service_create") as span:
            span.set_attribute("user.username", user_data.username)

            # 1. Delegate validation to a dedicated function
            if not functions.is_valid_username(user_data.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid username. Must be at least 3 characters long."
                )

            if user_data.username in fake_user_db:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists."
                )

            # 2. Simulate database interaction
            logger.info(f"Creating user '{user_data.username}' in the database.")
            global user_id_counter
            
            new_user = {
                "id": user_id_counter,
                "username": user_data.username,
                "created_at": datetime.datetime.now()
            }
            fake_user_db[user_data.username] = new_user
            user_id_counter += 1
            
            # 3. Use a utility to format the response data
            formatted_timestamp = utils.format_timestamp_to_iso(new_user["created_at"])

            span.set_attribute("user.id", new_user["id"])
            logger.info(f"User '{new_user['username']}' created successfully with ID {new_user['id']}.")

            return schemas.UserDisplay(
                id=new_user["id"],
                username=new_user["username"],
                created_at=formatted_timestamp
            )
