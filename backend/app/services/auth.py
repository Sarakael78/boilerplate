from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..core.config import settings
from ..db.database import get_db
from ..models.user import AuditLog, RefreshToken, User
from ..schemas.user import TokenData, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, user_id: int, db: Session) -> str:
        # Generate a random refresh token
        import secrets

        refresh_token = secrets.token_urlsafe(32)

        # Store refresh token in database
        expires_at = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        db_refresh_token = RefreshToken(
            user_id=user_id, token=refresh_token, expires_at=expires_at
        )
        db.add(db_refresh_token)
        db.commit()

        return refresh_token

    def verify_token(self, token: str) -> Optional[TokenData]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            if username is None or user_id is None:
                return None
            return TokenData(username=username, user_id=user_id)
        except JWTError:
            return None

    def authenticate_user(
        self, db: Session, username: str, password: str
    ) -> Optional[User]:
        user = db.query(User).filter(User.username == username).first()
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def get_current_user(self, db: Session, token: str) -> Optional[User]:
        token_data = self.verify_token(token)
        if token_data is None:
            return None

        user = db.query(User).filter(User.id == token_data.user_id).first()
        if user is None:
            return None
        return user

    def create_user(self, db: Session, user: UserCreate) -> User:
        # Check if user already exists
        existing_user = (
            db.query(User)
            .filter((User.email == user.email) | (User.username == user.username))
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists",
            )

        # Create new user
        hashed_password = self.get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    def login_user(self, db: Session, username: str, password: str) -> dict:
        user = self.authenticate_user(db, username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )

        # Create tokens
        access_token = self.create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )
        refresh_token = self.create_refresh_token(user.id, db)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60,
        }

    def refresh_access_token(self, db: Session, refresh_token: str) -> dict:
        # Verify refresh token exists and is not expired
        db_refresh_token = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token == refresh_token,
                not RefreshToken.is_revoked,
                RefreshToken.expires_at > datetime.utcnow(),
            )
            .first()
        )

        if not db_refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # Get user
        user = db.query(User).filter(User.id == db_refresh_token.user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        # Create new access token
        access_token = self.create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60,
        }

    def logout_user(self, db: Session, refresh_token: str) -> bool:
        # Revoke refresh token
        db_refresh_token = (
            db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        )

        if db_refresh_token:
            db_refresh_token.is_revoked = True
            db.commit()
            return True
        return False

    def log_audit_event(
        self,
        db: Session,
        user_id: Optional[int],
        action: str,
        resource: str,
        resource_id: Optional[str] = None,
        details: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.add(audit_log)
        db.commit()


# Create service instance
auth_service = AuthService()


# Dependency functions
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    user = auth_service.get_current_user(db, credentials.credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user
