from fastapi import APIRouter, Depends,HTTPException,status
from app.services.auth import authentication
from app.models.userprofile import userprofileresponse
from app.database.schema import getdb
from sqlalchemy.orm import session
from typing import Annotated


router=APIRouter()
auth=authentication()
dependancy=Annotated[session,Depends(getdb)]

@router.get("/userProfile",response_model=dict[str,userprofileresponse])
def user(userdata=Depends(auth.check_user)):
    return{"message":userdata}

