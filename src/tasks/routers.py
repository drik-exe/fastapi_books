from fastapi import APIRouter, BackgroundTasks, Depends

from tasks.tasks import send_email_report
from users.auth import get_current_user



router = APIRouter(prefix="/report")


@router.get("/report")
def get_report(user=Depends(get_current_user)):
    send_email_report.delay(user.username)
    return {"status": 200}
