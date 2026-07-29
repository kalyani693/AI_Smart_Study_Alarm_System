from app.database.schema import studysession
from fastapi import HTTPException
from sqlalchemy import text

def getbest_Slot(db,user):
     try: 
        userinfo=db.query(studysession).filter(studysession.Username==user.Username).all()
        if not userinfo:
            return{"message":"Morning, Evening"}
        else:
            morging_avg_score=db.execute(text(f"""select avg("self_rated_focus") from studysession where "Time_of_day"='Morning' """)).scalar() or 0
            afternoon_avg_score=db.execute(text(f"""select avg("self_rated_focus") from studysession where "Time_of_day"='Afternoon' """)).scalar() or 0
            evening_avg_score=db.execute(text(f"""select avg("self_rated_focus") from studysession where "Time_of_day"='Evening' """)).scalar() or 0
            night_avg_score=db.execute(text(f"""select avg("self_rated_focus") from studysession where "Time_of_day"='Night' """)).scalar() or 0
    
            if morging_avg_score>afternoon_avg_score:
                if morging_avg_score>evening_avg_score:
                    if morging_avg_score>night_avg_score:
                        return{"message":"Morning"}
                    else:
                        return{"message":"Night"}
                else:
                    if evening_avg_score>night_avg_score:
                        return{"message":"Evening"}  
                    else:
                        return{"message":"Night"} 
            else:
                if afternoon_avg_score>evening_avg_score:
                    if afternoon_avg_score>night_avg_score:
                       return{"message":"Afternoon"}
                    else:
                        return{"message":"Night"}
                else:
                    if evening_avg_score>night_avg_score:
                        return{"message":"Evening"}   
                    else:
                        return{"message":"Night"} 
     except Exception as e:
           raise HTTPException(status_code=500,detail=f"Error in Finding Best Slot. Error:{str(e)}") 