from fastapi import APIRouter, HTTPException, status


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def index():
    return {"message": "Welcome to FastAPI"}