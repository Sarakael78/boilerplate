from datetime import datetime, timedelta
from typing import Optional
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..core.config import settings
from ..db.database import get_db
from ..models.user import User
from ..schemas.user import TokenData, UserCreate
from ..repositories.user_repository import (
    UserRepository, 
    RefreshTokenRepository, 
    AuditLogRepository
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.refresh_token_repo = RefreshTokenRepository(db)
        self.audit_repo = AuditLogRepository(db)
        
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

    def create_refresh_token(self, user_id: int) -> str:
        # Generate a random refresh token
        refresh_token = secrets.token_urlsafe(32)

        # Store refresh token in database
        expires_at = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        self.refresh_token_repo.create_refresh_token(user_id, refresh_token, expires_at)

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

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_username(username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def get_current_user(self, token: str) -> Optional[User]:
        token_data = self.verify_token(token)
        if token_data is None:
            return None

        user = self.user_repo.get_by_id(token_data.user_id)
        if user is None:
            return None
        return user

    def create_user(self, user: UserCreate) -> User:
        # Check if user already exists
        if self.user_repo.user_exists(user.username, user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists",
            )

        # Create new user
        hashed_password = self.get_password_hash(user.password)
        db_user = self.user_repo.create_user(user, hashed_password)

        # Log user creation
        self.audit_repo.create_audit_log(
            user_id=db_user.id,
            action="USER_CREATED",
            resource="user",
            resource_id=str(db_user.id),
            details=f"User {db_user.username} created",
        )

        return db_user

    def login_user(
        self, 
        username: str, 
        password: str, 
        ip_address: Optional[str] = None, 
        user_agent: Optional[str] = None
    ) -> dict:
        user = self.authenticate_user(username, password)
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
        refresh_token = self.create_refresh_token(user.id)

        # Update last login
        self.user_repo.update_last_login(user)

        # Log login
        self.audit_repo.create_audit_log(
            user_id=user.id,
            action="USER_LOGIN",
            resource="auth",
            resource_id=str(user.id),
            details="User login successful",
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60,
        }

    def refresh_access_token(self, refresh_token: str) -> dict:
        # Verify refresh token exists and is not expired
        db_refresh_token = self.refresh_token_repo.get_valid_token(refresh_token)

        if not db_refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # Get user
        user = self.user_repo.get_active_user_by_id(db_refresh_token.user_id)
        if not user:
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

    def logout_user(
        self, 
        refresh_token: str, 
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> bool:
        # Revoke refresh token
        success = self.refresh_token_repo.revoke_token(refresh_token)

        if success and user_id:
            # Log logout
            self.audit_repo.create_audit_log(
                user_id=user_id,
                action="USER_LOGOUT",
                resource="auth",
                resource_id=str(user_id),
                details="User logout",
                ip_address=ip_address,
                user_agent=user_agent,
            )
        
        return success

    def log_audit_event(
        self,
        user_id: Optional[int],
        action: str,
        resource: str,
        resource_id: Optional[str] = None,
        details: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        """Convenience method to log audit events."""
        return self.audit_repo.create_audit_log(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
        )


# Dependency functions
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency to get AuthService instance."""
    return AuthService(db)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    user = auth_service.get_current_user(credentials.credentials)
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
