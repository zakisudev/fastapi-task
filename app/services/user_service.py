from sqlalchemy.orm import Session
from app.models.database_models import User, Post
from fastapi import HTTPException
from cachetools import TTLCache
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# Cache for 5 minutes (300 seconds)
cache = TTLCache(maxsize=100, ttl=300)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your-secret-key-here"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserService:
    """Business logic for user operations"""

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to verify against.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        Create a JWT token.

        Args:
            data (dict): The data to encode in the token.

        Returns:
            str: The encoded JWT token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def signup(db: Session, email: str, password: str):
        """
        Handle user signup.

        Args:
            db (Session): The database session.
            email (str): The email address of the user.
            password (str): The plain password of the user.

        Returns:
            dict: A dictionary containing the JWT token for the newly created user.

        Raises:
            HTTPException: If the email is already registered.
        """
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = UserService.get_password_hash(password)
        user = User(email=email, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)

        token = UserService.create_access_token({"sub": user.email})
        user.token = token
        db.commit()

        return {"token": token}

    @staticmethod
    def login(db: Session, email: str, password: str):
        """
        Handle user login.

        Args:
            db (Session): The database session.
            email (str): The email address of the user.
            password (str): The plain password of the user.

        Returns:
            dict: A dictionary containing the JWT token for the authenticated user.

        Raises:
            HTTPException: If the credentials are invalid.
        """
        user = db.query(User).filter(User.email == email).first()
        if not user or not UserService.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = UserService.create_access_token({"sub": user.email})
        user.token = token
        db.commit()

        return {"token": token}

    @staticmethod
    def add_post(db: Session, text: str, user: User):
        """
        Create a new post.

        Args:
            db (Session): The database session.
            text (str): The content of the post.
            user (User): The user creating the post.

        Returns:
            dict: A dictionary containing the ID of the newly created post.

        Raises:
            HTTPException: If the post text exceeds 1MB limit.
        """
        if len(text.encode("utf-8")) > 1048576:  # Check if text is larger than 1MB
            raise HTTPException(status_code=400, detail="Post text exceeds 1MB limit")

        post = Post(text=text, user_id=user.id)
        db.add(post)
        db.commit()
        db.refresh(post)
        cache.pop(user.id, None)
        return {"post_id": post.id}

    @staticmethod
    def get_posts(db: Session, user: User):
        """
        Get all posts for a user with caching.

        Args:
            db (Session): The database session.
            user (User): The user whose posts are to be retrieved.

        Returns:
            list: A list of dictionaries containing the user's posts.
        """
        if user.id in cache:
            return cache[user.id]

        posts = db.query(Post).filter(Post.user_id == user.id).all()
        posts_data = [
            {"id": p.id, "text": p.text, "created_at": p.created_at} for p in posts
        ]
        cache[user.id] = posts_data
        return posts_data

    @staticmethod
    def delete_post(db: Session, post_id: int, user: User):
        """
        Delete a user's post.

        Args:
            db (Session): The database session.
            post_id (int): The ID of the post to delete.
            user (User): The user who owns the post.

        Returns:
            dict: A dictionary containing a message indicating the post was deleted.

        Raises:
            HTTPException: If the post is not found.
        """
        post = (
            db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
        )
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        db.delete(post)
        db.commit()
        cache.pop(user.id, None)
        return {"message": "Post deleted"}
