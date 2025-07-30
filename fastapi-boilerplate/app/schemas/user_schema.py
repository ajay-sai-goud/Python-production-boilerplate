from pydantic import BaseModel, Field
import datetime

class UserBase(BaseModel):
    """Base model for a user, containing common fields."""
    username: str = Field(..., min_length=3, max_length=50, description="The user's unique username.", example="john_doe")

class UserCreate(UserBase):
    """Model for creating a new user. Inherits from UserBase."""
    pass

class UserDisplay(UserBase):
    """Model for displaying user information in API responses."""
    id: int = Field(..., description="The unique identifier for the user.", example=1)
    created_at: str = Field(..., description="The ISO 8601 timestamp of when the user was created.", example="2023-10-27T10:30:00.123456")

    class Config:
        orm_mode = True
