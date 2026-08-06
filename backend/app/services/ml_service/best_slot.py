from app.database.schema import studysession
from fastapi import HTTPException
from sqlalchemy import text

async def getbest_Slot(db,user):
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
                        return{"message":"Morning (6am - 11am)"}
                    else:
                        return{"message":"Night (8pm-11pm)"}
                else:
                    if evening_avg_score>night_avg_score:
                        return{"message":"Evening (6pm - 8pm)"}  
                    else:
                        return{"message":"Night (8pm - 11pm)"} 
            else:
                if afternoon_avg_score>evening_avg_score:
                    if afternoon_avg_score>night_avg_score:
                       return{"message":"Afternoon (12pm -5pm)"}
                    else:
                        return{"message":"Night (8pm - 11pm)"}
                else:
                    if evening_avg_score>night_avg_score:
                        return{"message":"Evening (6pm - 8pm)"}   
                    else:
                        return{"message":"Night (8pm - 11pm)"} 
     except Exception as e:
           raise HTTPException(status_code=500,detail=f"Error in Finding Best Slot. Error:{str(e)}") 