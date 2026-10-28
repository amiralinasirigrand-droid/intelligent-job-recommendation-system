import os
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from pwdlib import PasswordHash
from jose import jwt, JWTError
from fastapi import HTTPException
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id: int) -> str:
    secret_key = os.getenv("SECRET_KEY")

    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token
def decode_access_token(token: str) -> int:
    secret_key = os.getenv("SECRET_KEY")

    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"]
        )

        return payload["user_id"]

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )