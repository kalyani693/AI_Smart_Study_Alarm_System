from fastapi import APIRouter,HTTPException,Depends
from app.database.schema import alarmtable,getdb
from app.api.auth import authentication
from app.models.study_alarm import createalarm,editalarm
from sqlalchemy.orm import session
from typing import Annotated
from sqlalchemy import text
from datetime import datetime,timezone
from sqlalchemy import select,func

router=APIRouter()
dependancy=Annotated[session,Depends(getdb)]
auth=authentication()

@router.post("/alarm")
def createalram(input:createalarm,db:dependancy,user=Depends(auth.check_user)):
    try:
     alarmdata=alarmtable(Username=user.Username,alarm_Time=input.Time,
                         Label=input.label,repeat_on=input.repeat_on,created_at=datetime.now(timezone.utc),status="active")

     db.add(alarmdata)
     db.commit()
     alarm=db.query(alarmtable).filter(alarmtable.Label==input.label).first()
     return{"message":"Alarm Created Successfully!!",
            "Time":input.Time,
            "Label":input.label,
            "Alarm_Id":alarm.Id if alarm else None}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error in creating alarm:{str(e)}") 
    

@router.get("/alarm/{alarm_id}")
def getalarm(alarm_id:int,db:dependancy,user=Depends(auth.check_user)):
    try:
        alarm=db.query(alarmtable).filter(alarmtable.Id==alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=400,detail=f"Alarm with Id:{alarm_id} is not Found")
        return{"message":"Success!!",
               "Time":alarm.alarm_Time,
               "Label":alarm.Label}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error in getting alarm:{str(e)}")   

@router.patch("/Snooze/{alarm_id}")
def snoozealarm(alarm_id:int,db:dependancy,user=Depends(auth.check_user)):
    try:
        alarm=db.query(alarmtable).filter(alarmtable.Id==alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=400,detail=f"Alarm with Id:{alarm_id} is not Found")
        
        elif alarm.status=="dismissed":
            raise HTTPException(status_code=200,detail=f"The alarm is already dismissed.")
        
        alarm.snooze_count+=1
        db.commit()

        return{"message":f"Alarm Id:{alarm_id} will again ring in 5 min"}

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error in snoozing alarm:{str(e)}") 


@router.patch("/dismis/{alarm_id}")
def dismisalarm(alarm_id:int,db:dependancy,user=Depends(auth.check_user)):
    try:
        alarm=db.query(alarmtable).filter(alarmtable.Id==alarm_id).first()

        if not alarm:
          raise HTTPException(status_code=400,detail=f"Alarm with Id:{alarm_id} is not Found")        
        elif alarm.status=="dismissed":
            raise HTTPException(status_code=200,detail=f"The alarm is already dismissed.")
        
        alarm.actual_wakeup_time=datetime.now(timezone.utc)
        alarm.status="dismissed"
        #query=text(f"""update alarmtable set "actual_wakeup_time"={datetime.now(timezone.utc)},"status"="dismissed" where "Id"=={alarm_id};""")
        #response=db.execute(query)
        db.commit()
        return{"message":f"Alarm Id:{alarm_id}, Time:{alarm.alarm_Time} is dismissed."}
       
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error in dismissing alarm:{str(e)}") 

@router.put("/Edit/{alarm_id}",description="You can edit only alram_Time, Label,repeat_on")
def editalarm(input:editalarm,db:dependancy,user=Depends(auth.check_user)):
    try:
        alarm=db.query(alarmtable).filter(alarmtable.Id==input.alarm_id).first()
        
        if not alarm:
            raise HTTPException(status_code=400,detail=f"Alarm with Id:{input.alarm_id} is not Found")        
        elif alarm.status=="dismissed":
            raise HTTPException(status_code=200,detail=f"The alarm is already dismissed. Please create New alarm")

        query=text(f"""update alarmtable set "{(input.what_to_edit).title()}"='{input.new_val}' where "Id"={input.alarm_id};""")
        response=db.execute(query)
        db.commit()
        if response._soft_closed==True:
            return{"message":"Alarm Updated Succesfully!!"}
        else:
            return{"message":"Something went wrong"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error in updating alarm:{str(e)}") 
    

@router.delete("/delete/{alarm_id}")
def delalarm(alarm_id:int,db:dependancy,user=Depends(auth.check_user)):
    try:
        alarm=db.query(alarmtable).filter(alarmtable.Id==alarm_id).first()
                
        if not alarm:
            raise HTTPException(status_code=400,detail=f"Alarm with Id:{alarm_id} is not Found")

        alarm.status="deleted"
        db.commit()
        return{"message":"Alarm deleted Succesfully!!"}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error in deleting alarm:{str(e)}")

@router.get("/existing_alarm")
def getexistingalarm(db:dependancy,user=Depends(auth.check_user)):
    try:
        stm=select(alarmtable).where(alarmtable.Username==user.Username, alarmtable.status!="deleted")
        alarm=db.execute(stm).scalars().all()
        if not alarm:
            return{"detail":"No existing data Found"}
        return{"alarms":alarm}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error in getting alarm:{str(e)}")     
