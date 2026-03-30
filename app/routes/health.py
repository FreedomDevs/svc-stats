from fastapi import APIRouter
from app.responses import success_response
from app.codes import Codes

router = APIRouter(tags=["heals"])

@router.get("/live")
def get_live():
    return success_response(data={"alive": True}, code=Codes.LIVE_OK, message="svc-stats жив")
