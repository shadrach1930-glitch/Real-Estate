"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import LoginRequest, TokenResponse, UserOut
from app.services.auth_service import (
    authenticate_sales_user,
    create_access_token,
    decode_token,
)

router = APIRouter()
security = HTTPBearer(auto_error=False)


@router.post("/auth/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    user = authenticate_sales_user(body.email, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token({"sub": user["email"], "name": user["name"]})
    return TokenResponse(
        access_token=token,
        email=user["email"],
        name=user["name"],
    )


@router.get("/auth/me", response_model=UserOut)
async def me(credentials: HTTPAuthorizationCredentials | None = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return UserOut(email=payload.get("sub", ""), name=payload.get("name", ""))


def require_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    """Dependency for protecting routes."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload
