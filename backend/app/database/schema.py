from app.database.config import sessionlocal,base
from sqlalchemy import Column,Integer,String,Boolean,VARCHAR


#we have to store work history in a userdatatable in json format 
# as a string because sqlalchemy does not support nested models directly. 
# So we will store work history as a JSON string in the userdatatable table. 
# When we retrieve the user data, we can parse the JSON string back into a Python dictionary or object. 

class userdatatable(base):
    __tablename__="userdatatable"
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


def getdb():
    db=sessionlocal()
    try:    
        yield db
    finally:
        db.close()    