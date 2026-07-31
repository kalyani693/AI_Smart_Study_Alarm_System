from fastapi import HTTPException
from app.database.schema import studysession
from sqlalchemy import func,select
from datetime import datetime
import pandas as pd
from app.services.ml_service.load_model import predict_focus,focus_score_Features


def timeofday():
    start_time_hr=datetime.now().strftime("%H")
    if start_time_hr in ["5","6","7","8","9","10","11","12"]:
        return "Morning"
    elif start_time_hr in ["13","14","15","16","17"]:
        return "Afternoon"
    elif start_time_hr in ["18","19","20"]:
        return "Evening"
    else:
        return "Night"

#->['session_duration_inmin', 'breaks_taken_count', 
#'time_of_day_Afternoon', 'time_of_day_Evening', 'time_of_day_Morning', 'time_of_day_Night', 
#'subject_type_Ai', 'subject_type_Aptitude', 'subject_type_DBMS', 'subject_type_DSA', 'subject_type_Java', 
#'subject_type_Machine Learning', 'subject_type_Operating Systems', 'subject_type_Python', 'day_of_week_Friday', 
#'day_of_week_Monday', 'day_of_week_Saturday', 'day_of_week_Sunday', 'day_of_week_Thursday', 'day_of_week_Tuesday', 'day_of_week_Wednesday']

async def focus_Score_model(input,user,db):
    try:
        stmt=select(func.sum(studysession.breaks_taken)).where(studysession.Username==user.Username) 
        breaks_Count=db.scalar(stmt)
        user_ip={
            "breaks_taken_count":breaks_Count if breaks_Count else 0,
            "time_of_day":timeofday(),
            "session_duration_inmin":input.session_duration_inmin if input else 0,
        "subject_type":input.subject_type if input else 0,
            "day_of_week":datetime.day
        }    
        if user_ip: 
            df=pd.DataFrame(user_ip,index=[0])
            encoded_df=pd.get_dummies(df)
            encoded_df=pd.DataFrame(encoded_df).reindex(columns=focus_score_Features,fill_value=0)#imp step
            #prediction result
            Pred=predict_focus(encoded_df)
            return {"message":round(Pred,2)}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error:{str(e)}")    





