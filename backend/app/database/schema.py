from app.database.config import sessionlocal,base
from sqlalchemy import Column,Integer,String,Boolean,VARCHAR,DateTime,TIMESTAMP


#we have to store work history in a userdatatable in json format 
# as a string because sqlalchemy does not support nested models directly. 
# So we will store work history as a JSON string in the userdatatable table. 
# When we retrieve the user data, we can parse the JSON string back into a Python dictionary or object. 


def getdb():
    db=sessionlocal()
    try:    
        yield db
    finally:
        db.close() 

class userdatatable(base):
    __tablename__="userdatatable"
    Id=Column(Integer, autoincrement=True)
    Full_Name=Column(VARCHAR(40),nullable=False)
    Username=Column(VARCHAR(40),primary_key=True)
    Email=Column(VARCHAR(100),unique=True,nullable=False)
    Highest_Class=Column(VARCHAR(20),nullable=False)
    School_College=Column(VARCHAR(100),nullable=False)
    CurrentLocation=Column(VARCHAR(100),nullable=False)
    work_history=Column(VARCHAR(150),nullable=True)
    Key_skills=Column(VARCHAR(100),nullable=True)
    hashed_Password=Column(VARCHAR(255), nullable=False)
    is_active=Column(Boolean,default=True)  

class studysession(base):
    __tablename__="studysession"
    Id=Column(Integer, autoincrement=True,primary_key=True)
    Username=Column(VARCHAR(40) ,nullable=False)
    Subject=Column(VARCHAR(40),nullable=False)
    start_time=Column(DateTime)
    End_time=Column(DateTime,default=None)
    Duration=Column(DateTime,default=None)
    created_at=Column(TIMESTAMP,default=None)
    self_rated_focus=Column(Integer, default=0)
    breaks_taken=Column(Integer,default=0)
    computed_focus_score=Column(Integer,default=0)
    status=Column(VARCHAR(15), nullable=False)

class alarmtable(base):
    __tablename__="alarmtable"
    Id=Column(Integer, autoincrement=True,primary_key=True)
    Username=Column(VARCHAR(40), nullable=False)
    alarm_Time=Column(DateTime,default=None,nullable=False)
    Label=Column(VARCHAR(30),nullable=True,default=None)
    repeat_on=Column(VARCHAR(100),nullable=True,default=None)
    snooze_count=Column(Integer,nullable=True,default=0)
    actual_wakeup_time=Column(DateTime,nullable=True,default=None)
    created_at=Column(TIMESTAMP,default=None)
    status=Column(VARCHAR(15), nullable=False)

