from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tenant, User
from app.schemas import TenantResponse
from app.tenant import get_current_user


router = APIRouter(
    prefix="/tenant",
    tags=["Tenant"],
)


@router.get(
    "/me",
    response_model=TenantResponse,
)
def get_my_tenant(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    tenant = db.query(Tenant).filter(
        Tenant.id == current_user.tenant_id
    ).first()

    return tenant