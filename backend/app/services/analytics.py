from fastapi import Depends,HTTPException
from typing import Annotated
from sqlalchemy import select,func
from app.database.schema import userdatatable,alarmtable,studysession
from datetime import datetime,timedelta
import numpy as np


async def get_stats(user,db):
  try:
    seven_days_ago=datetime.utcnow()-timedelta(days=7)
    #total study hours, average focus score, current streak, number of session
    query=select(func.sum(func.extract('epoch',studysession.Duration))).where(studysession.Username==user.Username,studysession.created_at>=seven_days_ago)

    total_study_seconds=db.scalar(query)

    query2=select(func.avg(studysession.computed_focus_score)).where(studysession.Username==user.Username,studysession.created_at>=seven_days_ago)
    average_focus_score=db.scalar(query2)

    query3=query2=select(func.count(studysession.Id)).where(studysession.Username==user.Username,studysession.created_at>=seven_days_ago)
    no_of_sessions=db.scalar(query3)

    return{"total_study_hours":np.ceil(total_study_seconds/3600) if total_study_seconds else 0,
           "total_study_min":np.ceil(total_study_seconds/60) if total_study_seconds else 0,
           "average_focus_score":average_focus_score if average_focus_score else 0,
           "number_of_sessions":no_of_sessions if no_of_sessions else 0}
  
  except Exception as e:
    raise HTTPException(status_code=500,detail=f"Error:{str(e)}")   


async def sleep_hours(user,db):
  try:
     stm=select(alarmtable.created_at, alarmtable.actual_wakeup_time).where(alarmtable.Username==user.Username,alarmtable.status!="active").order_by(alarmtable.created_at.desc())
     data=db.execute(stm).all()
     sleep_hours=[]
     for data in data:
         wake=data.actual_wakeup_time
         start=data.created_at
         if wake and start:
             sleep_hours.append(wake-start)
         else:
             sleep_hours.append(None)
     valid_hours=[t.total_seconds()/3600 for t in sleep_hours if t is not None] 
     if valid_hours:
         return{"sleep_hours":valid_hours}
     else:
      return {"sleep_hours":0}    
                 
  
  except Exception as e:
      raise HTTPException(status_code=500,detail=f"Error:{str(e)}") 


async def get_performance(user,db):
   try:
      stm=select(studysession.created_at, func.avg(studysession.computed_focus_score)).where(studysession.Username==user.Username).group_by(studysession.created_at).order_by(studysession.created_at.desc())
      data=db.execute(stm).all()
      if not data:
          return {"message":"No data found for the user."}
      return {({"date":data.created_at if data.created_at else None ,
              "average_focus_score":data[1] if data else 0} for data in data)
              }

   except Exception as e:
         raise HTTPException(status_code=500,detail=f"Error:{str(e)}") 

async def subject_distribution(user,db):
   try:
       smt=select(studysession.Subject,func.count(studysession.Id),func.avg(studysession.computed_focus_score)).filter(studysession.Username==user.Username).group_by(studysession.Subject)
       data=db.execute(smt).all()
       if not data:
           return {"message":"No study session data found for the user."}
       else:
           return{({"subject":row[0] if row[0] else None,
                    "sessions":row[1] if row[1] else 0,
                    "avg_focus_score":row[2] if row[2] else 0} for row in data)}
   except Exception as e:
            raise HTTPException(status_code=500,detail=f"Error:{str(e)}")    
      
async def focus_score_per_timeOfday(user,db):
   try:
       smt=select(studysession.Time_of_day,func.avg(studysession.computed_focus_score)).filter(studysession.Username==user.Username).group_by(studysession.Time_of_day)
       data=db.execute(smt).all()
       if not data:
           return {"message":"No data found for the user."}
       else:
           return{({"Time_of_day":row[0] if row[0] else None,
                    "avg_focus_score":row[1] if row[1] else 0} for row in data)}
   except Exception as e:
            raise HTTPException(status_code=500,detail=f"Error:{str(e)}") 
       