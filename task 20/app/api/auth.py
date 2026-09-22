from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me")
def current_user():
    return {"message": "Use a bearer token to access protected endpoints"}
