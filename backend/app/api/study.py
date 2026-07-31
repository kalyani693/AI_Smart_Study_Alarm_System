from fastapi import APIRouter, Depends,HTTPException,status
from app.services.auth import authentication
from app.database.schema import getdb,studysession
from app.models.study_alarm import endsessioninput,startsessioninput
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime

router=APIRouter()
auth=authentication()
dependancy=Annotated[Session,Depends(getdb)]

@router.post("/startsession",description="""Subject:["Python","DSA", "DBMS", "Operating Systems", "Machine Learning", "Aptitude", "Ai","Java"]
""")
async def start(db:dependancy,input:startsessioninput,user=Depends(auth.check_user)):
    try:
        prevsession=db.query(studysession).filter(studysession.Subject==input.subject and studysession.status=="active").first()
        if prevsession:
            raise HTTPException(status_code=409,detail=f"previos session of {input.subject} is not completed yet. New session Can't  start for this subject.")

        def timeofday():
            start_time_hr=datetime.now().strftime("%H")
            if start_time_hr in ["5","6","7","8","9","10","11","12"]:
                return "Morning"
            elif start_time_hr in ["13","14","15","16","17"]:
                return "Afternoon"
            elif start_time_hr in ["17,""18","19","20"]:
                return "Evening"
            else:
                return "Night"


        info=studysession(
            Username=user.Username,
            Subject=input.subject,
            start_time=datetime.now().strftime("%H:%M:%S"),
            created_at=datetime.now(),
            status="active",
            planned_duration=input.planned_duration,
            Time_of_day=timeofday()
        )

        db.add(info)
        db.commit()
        sessiondata=db.query(studysession).filter(studysession.Subject==input.subject and studysession.status=="active").first()
        return{"message":"Session Started!!",
               "Session_Id":sessiondata.Id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in Starting the Session:{str(e)}") 


@router.post("/Endsession",description="self_rated_focus should be in the range (1 to 5)")
async def end(db:dependancy,input:endsessioninput,user=Depends(auth.check_user)):
    try:
        sessiondata=db.query(studysession).filter(studysession.Id==input.Session_Id ).first()
        if not sessiondata:
            raise HTTPException(status_code=400, detail=f"Session with Id:{input.Session_Id} is not found")
        else:
            data=db.query(studysession).filter(studysession.Id==input.Session_Id and studysession.status=="completed").first()
            if data.status=="completed":
                raise HTTPException(status_code=200,detail=f" The session with Id:{input.Session_Id} is already completed")

        start_dt=datetime.combine(datetime.today(),sessiondata.start_time)   
        endtime=datetime.now().strftime("%H:%M:%S")
        duration=(datetime.now())-start_dt
        duration_min=round(duration.total_seconds()/60, 3)
        computed_focus_score=(sessiondata.planned_duration)/round(duration_min,2) if duration_min > 0 else 1
        query=text(f"""update studysession 
                       set "End_time"='{endtime}',
                       "Duration"='{duration}',
                       "self_rated_focus"='{input.self_rated_focus}',
                       "computed_focus_score"={computed_focus_score},
                       "breaks_taken"='{input.Breaks_taken}',
                       "status"='completed'
                       where "Username"='{user.Username}' and "Id"='{input.Session_Id}'; 
                       """)
        
        response=db.execute(query)
        db.commit()
        if response._soft_closed==True:
            return{"message":"Session Ended!!",
                   "subject":data.Subject,
                   "Id":input.Session_Id}
        else:
            return{"message":"Something went wrong"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in Ending the Session:{str(e)}")  



@router.get("/history")
async def history(db:dependancy,user=Depends(auth.check_user)):
    try:
        sessiondata=db.query(studysession).filter(studysession.Username==user.Username).all()
        if not sessiondata:
            return {"message":"No previos History of session is found."}
        else:
          return {"message":sessiondata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in Ending the Session:{str(e)}")




