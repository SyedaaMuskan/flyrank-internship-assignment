from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models import Tenant, User
from app.schemas import LoginRequest, Token, UserCreate


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=Token,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    tenant = Tenant(
        name=user_data.tenant_name
    )

    db.add(tenant)
    db.flush()

    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        tenant_id=tenant.id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        {
            "sub": str(user.id),
            "tenant_id": user.tenant_id,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post(
    "/login",
    response_model=Token,
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        credentials.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "tenant_id": user.tenant_id,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }