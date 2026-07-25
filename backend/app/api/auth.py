from fastapi import APIRouter, Depends,HTTPException,status
from app.services.auth import authentication
from app.models.auth import userData
from app.database.schema import getdb
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router=APIRouter()


authService=authentication()
dependancy=Annotated[Session,Depends(getdb)]


@router.post("/Registration")
async def register_user(userinfo:userData,db:dependancy):
    return await authService.registration_service(userinfo,db)

@router.post("/login")
async def userlogin(user:Annotated[OAuth2PasswordRequestForm,Depends()],db:dependancy):
    return await authService.login_service(user,db)