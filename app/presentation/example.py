from fastapi import APIRouter, status

router = APIRouter(prefix="", tags=["Example"])


@router.post("/ping", response_model=dict, status_code=status.HTTP_200_OK)
def ping():
    return {"message": "pong"}
