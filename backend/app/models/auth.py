from fastapi import HTTPException
from pydantic import BaseModel,Field, field_validator
from typing import Annotated,Optional



class workhistory(BaseModel):
    job_title:str
    Company_Name:str
    Year_of_Experience:float

class location(BaseModel):
    city:str
    state:str
    country:str    
    
class userData(BaseModel):
    Full_Name:Annotated[str,Field(max_length=40)]
    Username:Annotated[str,Field(max_length=40)]
    Email:Annotated[str,Field(max_length=50)]
    Highest_Class:str
    School_College:str
    CurrentLocation:location
    work_history:Annotated[Optional[workhistory],Field(default=None)]
    Key_skills:str
    Password:str

    @field_validator("Email",mode="after",check_fields=True)
    @classmethod
    def validate_email(cls,Email:str):
        if Email:
           try: 
            email_split=Email.split('@')
            if email_split[1] not in ['gmail.com','yahoo.com','outlook.com','hotmail.com']:
               raise HTTPException(status_code=429,detail="Please Enter a valid email. example:['gmail.com','yahoo.com','outlook.com','hotmail.com']")
            else:
               return Email 
           except Exception as e:
              raise HTTPException(status_code=429,detail=f"Email should be valid/seperated with '@'. error={str(e)}") 




