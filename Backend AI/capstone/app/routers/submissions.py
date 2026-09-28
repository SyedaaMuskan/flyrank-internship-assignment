from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Submission, User, Widget
from app.schemas import SubmissionCreate, SubmissionResponse
from app.tenant import get_current_user


router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)


@router.post(
    "/{widget_id}",
    response_model=SubmissionResponse,
)
def create_submission(
    widget_id: int,
    submission_data: SubmissionCreate,
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

    submission = Submission(
        widget_id=widget.id,
        tenant_id=current_user.tenant_id,
        data=submission_data.data,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission


@router.get(
    "",
    response_model=list[SubmissionResponse],
)
def list_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return db.query(Submission).filter(
        Submission.tenant_id == current_user.tenant_id
    ).all()