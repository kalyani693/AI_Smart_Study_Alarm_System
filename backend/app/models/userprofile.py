from typing import Annotated,Optional
from pydantic import BaseModel,Field

class userprofileresponse(BaseModel):
    Full_Name:str
    Username:str
    Email:str
    Highest_Class:str
    School_College:str
    CurrentLocation:str
    work_history:str
    Key_skills:str
