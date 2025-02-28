from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.database_models import User


def get_current_user(token: str, db: Session = Depends(get_db)):
    """
    Dependency for token authentication.

    Args:
        token (str): The authentication token provided by the user.
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the token is invalid or missing, an HTTP 401 Unauthorized exception is raised.

    Returns:
        User: The authenticated user object.
    """
    """Dependency for token authentication"""
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )
    return user
