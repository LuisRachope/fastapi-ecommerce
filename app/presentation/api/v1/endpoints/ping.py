from fastapi import APIRouter

router = APIRouter(prefix="", tags=["System"])


@router.get("/ping", response_model=str, status_code=200)
def ping():
   return "pong"
