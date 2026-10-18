import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

router = APIRouter(tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

DEMO_USERNAME = os.getenv("DEMO_USERNAME", "admin")
DEMO_EMAIL = os.getenv("DEMO_EMAIL", "admin@example.com")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "password123")

_demo_salt = bcrypt.gensalt()
DEMO_PASSWORD_HASH = bcrypt.hashpw(DEMO_PASSWORD.encode("utf-8"), _demo_salt).decode("utf-8")

USERS_DB = {
    DEMO_USERNAME: {
        "id": "1",
        "username": DEMO_USERNAME,
        "email": DEMO_EMAIL,
        "password_hash": DEMO_PASSWORD_HASH,
    }
}

security = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str = Field(min_length=1)


class UserResponse(BaseModel):
    id: str
    username: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/api/login", response_model=TokenResponse)
@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest) -> TokenResponse:
    identifier = credentials.username or credentials.email
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required",
        )

    user = None
    for u in USERS_DB.values():
        if u["username"] == identifier or u["email"] == identifier:
            user = u
            break

    if not user and (identifier == DEMO_USERNAME or identifier == DEMO_EMAIL):
        if verify_password(credentials.password, DEMO_PASSWORD_HASH):
            user = USERS_DB[DEMO_USERNAME]

    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        data={"sub": user["id"], "username": user["username"], "email": user["email"]}
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user["id"],
            username=user["username"],
            email=user["email"],
        ),
    )


@router.get("/api/me", response_model=UserResponse)
@router.get("/me", response_model=UserResponse)
def get_me(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> UserResponse:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return UserResponse(
            id=str(user_id),
            username=payload.get("username", "user"),
            email=payload.get("email", "user@example.com"),
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
