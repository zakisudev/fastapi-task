from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserCreate(BaseModel):
    """
    Schema for user signup.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The password for the user, must be at least 8 characters long.
    """

    email: EmailStr
    password: str

    @validator("password")
    def password_strength(cls, v):
        """
        Validate the strength of the password.

        Args:
            v (str): The password to validate.

        Raises:
            ValueError: If the password is less than 8 characters long.

        Returns:
            str: The validated password.
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The password for the user.
    """

    email: EmailStr
    password: str


class PostCreate(BaseModel):
    """
    Schema for creating posts.

    Attributes:
        text (str): The content of the post, must be less than 1MB in size.
    """

    text: str

    @validator("text")
    def validate_size(cls, v):
        """
        Validate the size of the post content.

        Args:
            v (str): The post content to validate.

        Raises:
            ValueError: If the post content exceeds 1MB in size.

        Returns:
            str: The validated post content.
        """
        if len(v.encode("utf-8")) > 1048576:  # 1MB in bytes
            raise ValueError("Post size exceeds 1MB limit")
        return v


class PostDelete(BaseModel):
    """
    Schema for deleting posts.

    Attributes:
        post_id (int): The ID of the post to delete.
    """

    post_id: int
