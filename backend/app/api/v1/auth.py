from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..models.user import User
from ..schemas.user import Token
from ..schemas.user import User as UserSchema
from ..schemas.user import UserCreate
from ..services.auth import auth_service, get_current_active_user

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


@router.post(
    "/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED
)
async def register(
    user: UserCreate, db: Session = Depends(get_db), request: Request = None
):
    """
    Register a new user.
    """
    try:
        db_user = auth_service.create_user(db, user)

        # Log audit event
        auth_service.log_audit_event(
            db=db,
            user_id=db_user.id,
            action="user_registered",
            resource="user",
            resource_id=str(db_user.id),
            details=f"User {db_user.username} registered",
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
        )

        return db_user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration",
        ) from None


@router.post("/login", response_model=Token)
async def login(
    username: str, password: str, db: Session = Depends(get_db), request: Request = None
):
    """
    Login user and return access token.
    """
    try:
        token_data = auth_service.login_user(db, username, password)

        # Log audit event
        user = auth_service.authenticate_user(db, username, password)
        if user:
            auth_service.log_audit_event(
                db=db,
                user_id=user.id,
                action="user_login",
                resource="user",
                resource_id=str(user.id),
                details=f"User {user.username} logged in",
                ip_address=request.client.host if request else None,
                user_agent=request.headers.get("user-agent") if request else None,
            )

        return token_data
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login",
        ) from None


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.
    """
    try:
        return auth_service.refresh_access_token(db, refresh_token)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during token refresh",
        ) from None


@router.post("/logout")
async def logout(
    refresh_token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    request: Request = None,
):
    """
    Logout user and revoke refresh token.
    """
    try:
        success = auth_service.logout_user(db, refresh_token)

        # Log audit event
        auth_service.log_audit_event(
            db=db,
            user_id=current_user.id,
            action="user_logout",
            resource="user",
            resource_id=str(current_user.id),
            details=f"User {current_user.username} logged out",
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
        )

        if success:
            return {"message": "Successfully logged out"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during logout",
        ) from None


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information.
    """
    return current_user


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    request: Request = None,
):
    """
    Change user password.
    """
    try:
        # Verify current password
        if not auth_service.verify_password(
            current_password, current_user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        # Update password
        current_user.hashed_password = auth_service.get_password_hash(new_password)
        db.commit()

        # Log audit event
        auth_service.log_audit_event(
            db=db,
            user_id=current_user.id,
            action="password_changed",
            resource="user",
            resource_id=str(current_user.id),
            details=f"User {current_user.username} changed password",
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
        )

        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while changing password",
        ) from None
