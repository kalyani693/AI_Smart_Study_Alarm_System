from fastapi import FastAPI
from app.api.auth import router as authrouter
from app.api.user import router as u_pro_frouter
from app.api.study import router as studyrouter
from app.api.alarm import router as alarmrouter
from app.api.ml import router as mlrouter
from app.api.ai import router as airouter
from app.api.analytics import router as analyticsrouter
import uvicorn

app=FastAPI(title="AI SMART STUDY ALARM SYSTEM")

app.include_router(authrouter,prefix="/auth",tags=["Authentication"])
app.include_router(u_pro_frouter,prefix="/user",tags=["UserProfile"])
app.include_router(studyrouter,prefix="/study",tags=["Sessions"])
app.include_router(alarmrouter,prefix="/alarm",tags=["Alarm"])
app.include_router(mlrouter,prefix="/ml",tags=["ML Endpoints"])
app.include_router(airouter,prefix="/ai",tags=["AI Endpoints"])
app.include_router(analyticsrouter,prefix="/analytics",tags=["Analytics"])


def __init__():
    uvicorn.run(app,host="127.0.0.0", port=8000)