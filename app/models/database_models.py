from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.config.database import Base


class User(Base):
    """
    Database model for users.

    Attributes:
        id (int): The primary key for the user.
        email (str): The email address of the user, unique and indexed.
        password (str): The hashed password of the user.
        token (str): The JWT token for the user, unique.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(String(255), unique=True)


class Post(Base):
    """
    Database model for posts.

    Attributes:
        id (int): The primary key for the post.
        text (str): The content of the post, stored as a TEXT type.
        user_id (int): The foreign key referencing the user who created the post.
        created_at (datetime): The timestamp when the post was created, defaults to the current time.
    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)  # Use Text type instead of String
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
