from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas.request_schemas import UserCreate, UserLogin, PostCreate, PostDelete
from app.services.user_service import UserService
from app.dependencies.auth import get_current_user
from app.config.database import get_db
from app.models.database_models import User

router = APIRouter()


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    User signup endpoint.

    Args:
        user (UserCreate): The user data for signup.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the JWT token for the newly created user.
    """
    return UserService.signup(db, user.email, user.password)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint.

    Args:
        user (UserLogin): The user data for login.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the JWT token for the authenticated user.
    """
    return UserService.login(db, user.email, user.password)


@router.post("/posts")
def add_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add post endpoint.

    Args:
        post (PostCreate): The post data.
        current_user (User): The currently authenticated user.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the ID of the newly created post.
    """
    return UserService.add_post(db, post.text, current_user)


@router.get("/posts")
def get_posts(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get posts endpoint.

    Args:
        current_user (User): The currently authenticated user.
        db (Session): The database session.

    Returns:
        list: A list of dictionaries containing the user's posts.
    """
    return UserService.get_posts(db, current_user)


@router.delete("/posts")
def delete_post(
    post: PostDelete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete post endpoint.

    Args:
        post (PostDelete): The post data containing the post ID to delete.
        current_user (User): The currently authenticated user.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a message indicating the post was deleted.
    """
    return UserService.delete_post(db, post.post_id, current_user)
