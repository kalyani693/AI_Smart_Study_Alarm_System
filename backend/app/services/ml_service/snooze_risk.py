from fastapi import  Depends,HTTPException
from app.database.schema import alarmtable
from sqlalchemy import text,func,select
import pandas as pd
from datetime import datetime,timezone
from app.services.ml_service.load_model import snooze_risk_Features,predict_snooze_risk


#['sleep_duration', 'sleep_quality', 'fatigue_level', 'previous_snooze_count', 'study_importance', 'days_since_last_study', 'alarm_hour']

async def snooze_risk_model(user,db,input):
    try:
        stmt=select(func.sum(alarmtable.snooze_count)).where(alarmtable.Username==user.Username) 
        snooze_Count=db.scalar(stmt)

        stmt_=select(alarmtable.created_at).where(alarmtable.Username==user.Username).order_by(alarmtable.created_at).limit(1)
         # check by executing in database
        last_study_date=db.scalar(stmt_)

        info={
            "sleep_duration":input.sleep_duration if input else 0,
            "sleep_quality":input.sleep_quality if input else 0 ,
            "fatigue_level":input.fatigue_level if input else 0,
            "previous_snooze_count":snooze_Count if snooze_Count else 0,
            "study_importance":input.study_importance if input else 0,
            "days_since_last_study":(datetime.now(timezone.utc)-last_study_date).days, 
            "alarm_hour":input.alarm_hour if input else 0
        }

        if info:
            df=pd.DataFrame(info,index=[0])
            df_=pd.DataFrame(df).reindex(columns=snooze_risk_Features,fill_value=0)#imp step
            #prediction result
            Pred=predict_snooze_risk(df_)
            return {"message":round(Pred,2)}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error:{str(e)}")      


    
