from fastapi import APIRouter, status

router = APIRouter(prefix="/api/v1", tags=["Products"])


@router.post("/", response_model=dict, status_code=status.HTTP_200_OK)
def ping():
    return {"message": "pong"}
