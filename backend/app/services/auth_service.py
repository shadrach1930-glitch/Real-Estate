"""
Simple JWT authentication for the sales portal.

For MVP we support a single configured sales user via environment variables.
This can be expanded to a proper users table later.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None


def authenticate_sales_user(email: str, password: str) -> dict | None:
    """
    Validate against the configured sales user in environment.

    Required env:
      SALES_USER_EMAIL
      SALES_USER_PASSWORD   (plain — hashed on the fly for MVP simplicity)
      SALES_USER_NAME
    """
    if not settings.sales_user_email or not settings.sales_user_password:
        return None

    if email.lower() != settings.sales_user_email.lower():
        return None

    # For MVP we compare plain (or pre-hashed) password
    if password != settings.sales_user_password:
        # Also try bcrypt hash if the env value looks hashed
        try:
            if not verify_password(password, settings.sales_user_password):
                return None
        except Exception:
            return None

    return {
        "email": settings.sales_user_email,
        "name": settings.sales_user_name or "Sales User",
    }
