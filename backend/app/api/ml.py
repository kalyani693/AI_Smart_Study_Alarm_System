from fastapi import APIRouter, Depends
from app.services.auth import authentication
from app.services.ml_service.best_slot import getbest_Slot
from app.services.ml_service.focus_score import focus_Score_model
from app.services.ml_service.snooze_risk import snooze_risk_model
from app.models.ai_ml_models import focus_score_input,snooze_risk_input
from app.database.schema import getdb
from sqlalchemy.orm import Session
from typing import Annotated


router=APIRouter()
dependacy=Annotated[Session,Depends(getdb)]
auth=authentication()

@router.post("/best-slot")
async def BestSlot(db:dependacy,user=Depends(auth.check_user)):
  return await getbest_Slot(db,user)  
     
@router.post("/Focus-score",description="""input->{session_duration_inmin:int     
                                                   subject_type:str["Python","DSA", "DBMS", "Operating Systems", "Machine Learning", "Aptitude", "Ai","Java"]}""")
async def focusscore(db:dependacy,input:focus_score_input,user=Depends(auth.check_user)):
  return await focus_Score_model(input,user,db)
  
@router.post("/Snooze-risk",description=" ")
async def snoozerisk(db:dependacy,input:snooze_risk_input,user=Depends(auth.check_user)):
   return await snooze_risk_model(user,db,input)
        

    