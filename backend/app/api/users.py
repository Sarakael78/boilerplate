"""
API router for user-related endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.user import User, UserCreate, Token
from ..core.security import get_password_hash, verify_password, create_access_token
from ..models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check if user already exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
