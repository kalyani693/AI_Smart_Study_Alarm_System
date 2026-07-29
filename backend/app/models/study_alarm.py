from pydantic import BaseModel
from typing import List
from datetime import time


class startsessioninput(BaseModel):
    subject:str
    planned_duration:int
    
class endsessioninput(BaseModel):
    Session_Id:int
    self_rated_focus:int
    Breaks_taken:int
    

class createalarm(BaseModel):
    Time:time
    label:str
    repeat_on:List[str]

class editalarm(BaseModel):
    alarm_id:int
    what_to_edit:str
    new_val:str    