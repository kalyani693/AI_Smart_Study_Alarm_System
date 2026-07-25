from fastapi import APIRouter, Depends,HTTPException,status
from app.services.auth import authentication
from app.models.userprofile import userprofileresponse


router=APIRouter()
auth=authentication()

@router.get("/userProfile",response_model=dict[str,userprofileresponse])
def user(userdata=Depends(auth.check_user)):
    return{"message":userdata}

