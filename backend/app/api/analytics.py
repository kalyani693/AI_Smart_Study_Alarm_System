from fastapi import APIRouter, Depends,HTTPException,status
from app.services.auth import authentication
from app.services.analytics import sleep_hours,get_performance,focus_score_per_timeOfday,subject_distribution
from app.services.analytics import get_stats
from app.database.schema import getdb
from sqlalchemy.orm import session
from typing import Annotated


router=APIRouter()
auth=authentication()
dependancy=Annotated[session,Depends(getdb)]


@router.post("/stats")
async def analytics(db:dependancy,userdata=Depends(auth.check_user)):
    return await get_stats(userdata,db)

@router.post("/get_sleep_hours")
async def sleepHours(db:dependancy,userdata=Depends(auth.check_user)):
    return await sleep_hours(userdata,db)

@router.post("/get_performance")
async def performance(db:dependancy,userdata=Depends(auth.check_user)):
    return await get_performance(userdata,db)

@router.post("/focus_score_per_timeOfday")
async def focusScorePerTimeOfDay(db:dependancy,userdata=Depends(auth.check_user)):
    return await focus_score_per_timeOfday(userdata,db)

@router.post("/subject_distribution")
async def subjectDistribution(db:dependancy,userdata=Depends(auth.check_user)):
    return await subject_distribution(userdata,db)
