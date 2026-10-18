import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(tags=["auth"])

SECRET_KEY = os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY") or "default-jwt-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

DEFAULT_USERNAME = os.getenv("AUTH_USERNAME") or os.getenv("ADMIN_USERNAME") or "admin"
DEFAULT_PASSWORD = os.getenv("AUTH_PASSWORD") or os.getenv("ADMIN_PASSWORD") or "admin123"

DEFAULT_PASSWORD_HASH = bcrypt.hashpw(DEFAULT_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

USERS_DB = {
    DEFAULT_USERNAME: DEFAULT_PASSWORD_HASH
}

class LoginRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

@router.post("/api/login", response_model=TokenResponse)
@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest) -> TokenResponse:
    identifier = credentials.username or credentials.email
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required"
        )

    hashed_password = USERS_DB.get(identifier)

    if not hashed_password and identifier == DEFAULT_USERNAME:
        hashed_password = DEFAULT_PASSWORD_HASH

    if not hashed_password or not verify_password(credentials.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": identifier})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        username=identifier
    )
