
from fastapi import Depends,HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.database.schema import getdb
from sqlalchemy.orm import Session
from app.database.schema import userdatatable
from pwdlib import PasswordHash
import os
from jose import jwt
from dotenv import load_dotenv


dependancy=Annotated[Session,Depends(getdb)]
password_hash=PasswordHash.recommended()
oAuth2schema=OAuth2PasswordBearer(tokenUrl="/auth/login")
load_dotenv()

class authentication():
    def __init__(self):
        self.secret_key=os.getenv('SECRET_KEY')
        self.algorithm=os.getenv('ALGORITHM')
        self.expiration_time=os.getenv('EXPIRATION_TIME')


    async def registration_service(self,userInfo,db):
        
        user=db.query(userdatatable).filter(userdatatable.Username==userInfo.Username).first()
        email=db.query(userdatatable).filter(userdatatable.Email==userInfo.Email).first()
        if user:
            raise HTTPException(status_code=400, detail="Username already exists")
        if email:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        hashpassword=password_hash.hash(userInfo.Password)
        try:    
            data=userdatatable(
                Full_Name=userInfo.Full_Name,
                Username=userInfo.Username,
                Email=userInfo.Email,
                Highest_Class=userInfo.Highest_Class,
                School_College=userInfo.School_College,
                CurrentLocation=f"{userInfo.CurrentLocation.city}, {userInfo.CurrentLocation.state}, {userInfo.CurrentLocation.country}",
                work_history=f"{{\"job_title\": \"{userInfo.work_history.job_title}\", \"Company_Name\": \"{userInfo.work_history.Company_Name}\", \"Year_of_Experience\": {userInfo.work_history.Year_of_Experience}}}" if userInfo.work_history else None,
                           
                Key_skills=userInfo.Key_skills,
                hashed_Password=hashpassword,
                is_active=True
            )

            db.add(data)
            db.commit()
            return{"message":"User Registered Successfully!!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error occurred while fetching user: {e}")

    async def login_service(self,credential,db):
        try:  
            user=db.query(userdatatable).filter(userdatatable.Username==credential.username).first()
            
            if user:
                if user.is_active==False:
                    raise HTTPException( status_code=406,detail=f"Account with this Username has been deleted. status:Not active")
                if password_hash.verify(credential.password,user.hashed_Password):
                    token=jwt.encode(claims={'_username':credential.username,'password':credential.password,"expiration_time":self.expiration_time},
                                    key=self.secret_key,algorithm=self.algorithm)
                    return{'access_token':token,"token_type":"bearer"}  # important formating
                else:
                    raise HTTPException(status_code=422,detail="password is wrong")
            else:
                raise HTTPException(status_code=400,detail="Account with this Username is not Available")
        except Exception as e:
            raise HTTPException(status_code=500, detail={"error":str(e)})

    async def check_user(self,db:dependancy, token:str=Depends(oAuth2schema)):
        try:
            secret_key=os.getenv('SECRET_KEY')
            algo=os.getenv('ALGORITHM')
            payload=jwt.decode(token,key=secret_key,algorithms=algo)
            username=payload.get('_username')
            password=payload.get('password')
            expiring_time=payload.get('expiration_time')
            user=db.query(userdatatable).filter(userdatatable.Username==username).first()
            if user and password_hash.verify(password,user.hashed_Password):
                return user
            else:
                raise HTTPException(status_code=401,detail="Invalid Token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401,detail="Token Expired")
        #except jwt.InvalidTokenError:
            raise HTTPException(status_code=401,detail="Invalid Token")       
        
