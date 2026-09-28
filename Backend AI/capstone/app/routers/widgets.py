from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Widget
from app.schemas import WidgetCreate, WidgetResponse
from app.tenant import get_current_user


router = APIRouter(
    prefix="/widgets",
    tags=["Widgets"],
)


@router.post(
    "",
    response_model=WidgetResponse,
)
def create_widget(
    widget_data: WidgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    widget = Widget(
        name=widget_data.name,
        tenant_id=current_user.tenant_id,
    )

    db.add(widget)
    db.commit()
    db.refresh(widget)

    return widget


@router.get(
    "",
    response_model=list[WidgetResponse],
)
def list_widgets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return db.query(Widget).filter(
        Widget.tenant_id == current_user.tenant_id
    ).all()


@router.get(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def get_widget(
    widget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    widget = db.query(Widget).filter(
        Widget.id == widget_id,
        Widget.tenant_id == current_user.tenant_id,
    ).first()

    if not widget:
        raise HTTPException(
            status_code=404,
            detail="Widget not found",
        )

    return widget