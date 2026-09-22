from fastapi import APIRouter, Depends, HTTPException
from app.auth.models import User
from app.auth.security import get_current_user
router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])
@router.get("/{job_id}")
def get_job(job_id: str, user: User = Depends(get_current_user)):
    if not job_id.startswith("job-"):
        raise HTTPException(404, "Job not found")
    return {"id": job_id, "status": "completed", "tenant_id": user.tenant_id}
