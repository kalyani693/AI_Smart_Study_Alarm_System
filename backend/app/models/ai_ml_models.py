from pydantic import BaseModel
from datetime import time,date


class generate_plan_input(BaseModel):
    Exam_date:date
    Daily_available_hours:int

class sub_name(BaseModel):
    Subject:str   

class focus_score_input(BaseModel):
    session_duration_inmin:int     
    subject_type:str

class snooze_risk_input(BaseModel):
    sleep_duration:float
    study_importance:int
    alarm_hour:int
      
