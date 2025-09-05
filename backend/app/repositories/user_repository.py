"""
User repository for database operations.
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..models.user import User, RefreshToken, AuditLog
from ..schemas.user import UserCreate
from . import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model with specialized database operations."""

    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.get_by_field("username", username)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.get_by_field("email", email)

    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        """Get user by username or email."""
        return self.db.query(User).filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()

    def user_exists(self, username: str, email: str) -> bool:
        """Check if user exists by username or email."""
        return self.db.query(User).filter(
            or_(User.username == username, User.email == email)
        ).first() is not None

    def create_user(self, user_data: UserCreate, hashed_password: str) -> User:
        """Create a new user with hashed password."""
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_active_user_by_id(self, user_id: int) -> Optional[User]:
        """Get active user by ID."""
        return self.db.query(User).filter(
            User.id == user_id, User.is_active == True
        ).first()

    def update_last_login(self, user: User) -> User:
        """Update user's last login timestamp."""
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Repository for RefreshToken model."""

    def __init__(self, db: Session):
        super().__init__(db, RefreshToken)

    def create_refresh_token(self, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        """Create a new refresh token."""
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def get_valid_token(self, token: str) -> Optional[RefreshToken]:
        """Get valid (non-revoked, non-expired) refresh token."""
        return self.db.query(RefreshToken).filter(
            RefreshToken.token == token,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()

    def revoke_token(self, token: str) -> bool:
        """Revoke a refresh token."""
        db_token = self.db.query(RefreshToken).filter(
            RefreshToken.token == token
        ).first()
        
        if db_token:
            db_token.is_revoked = True
            self.db.commit()
            return True
        return False

    def revoke_all_user_tokens(self, user_id: int) -> None:
        """Revoke all refresh tokens for a user."""
        self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).update({"is_revoked": True})
        self.db.commit()


class AuditLogRepository(BaseRepository[AuditLog]):
    """Repository for AuditLog model."""

    def __init__(self, db: Session):
        super().__init__(db, AuditLog)

    def create_audit_log(
        self,
        user_id: Optional[int],
        action: str,
        resource: str,
        resource_id: Optional[str] = None,
        details: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """Create a new audit log entry."""
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        return audit_log

    def get_user_audit_logs(self, user_id: int, limit: int = 100):
        """Get audit logs for a specific user."""
        return self.db.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(AuditLog.created_at.desc()).limit(limit).all()
