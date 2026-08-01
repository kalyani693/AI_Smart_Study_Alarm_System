from fastapi import  Depends,HTTPException
from app.database.schema import alarmtable
from sqlalchemy import text,func,select
import pandas as pd
from datetime import datetime,timezone
from app.services.ml_service.load_model import snooze_risk_Features,predict_snooze_risk


#['study_importance', 'sleep_duration_prev_night', 'hour_of_alarm', 
# 'snooze_count_last_7_days', 'day_of_week_Friday', 'day_of_week_Monday', 'day_of_week_Saturday', 'day_of_week_Sunday',
#  'day_of_week_Thursday', 'day_of_week_Tuesday', 'day_of_week_Wednesday']

async def snooze_risk_model(user,db,input):
    try:
        stmt=select(func.sum(alarmtable.snooze_count)).where(alarmtable.Username==user.Username).limit(7)
        snooze_Count=db.scalar(stmt)

        info={
            "sleep_duration_prev_night":input.sleep_duration if input else 0,
            "snooze_count_last_7_days":snooze_Count if snooze_Count else 0,
            "study_importance":input.study_importance if input else 0,
            "hour_of_alarm":input.alarm_hour if input else 0,
            "day_of_week":datetime.now(timezone.utc).day
        }

        if info:
            df=pd.DataFrame(info,index=[0])
            encoded_df=pd.get_dummies(df)
            encoded_df=pd.DataFrame(encoded_df).reindex(columns=snooze_risk_Features,fill_value=0)#imp step
            #prediction result
            Pred,prob=predict_snooze_risk(encoded_df)

            if Pred==1:
                    print(f"High risk of snoozing with probability: {prob:.2f}")
            else:
                   print(f"Low risk of snoozing with probability: {1-prob:.2f}")
            return {"Prediction":Pred,
                    "Probability_of_snoozing":prob,
                    "Probability_of_not_snoozing":1-prob}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error:{str(e)}")      


    
