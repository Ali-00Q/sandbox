import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["auth"])

SECRET_KEY = os.getenv("JWT_SECRET", os.getenv("SECRET_KEY", "default-jwt-secret-key-change-in-production"))
ALGORITHM = "HS256"

DEMO_USER = os.getenv("AUTH_USERNAME", "admin").lower()
DEMO_PASS = os.getenv("AUTH_PASSWORD", "admin123")

_mock_users_passwords = {
    DEMO_USER: bcrypt.hashpw(DEMO_PASS.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
    "user@example.com": bcrypt.hashpw("user123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
    "user": bcrypt.hashpw("user123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
}

class LoginRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict | None = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest) -> TokenResponse:
    identifier = (credentials.username or credentials.email or "").strip().lower()
    if not identifier or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username/email and password are required"
        )

    hashed_password = _mock_users_passwords.get(identifier)
    if not hashed_password or not verify_password(credentials.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    expires_delta = timedelta(hours=24)
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": identifier,
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user={"username": identifier}
    )
