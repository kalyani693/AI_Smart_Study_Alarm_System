from fastapi import FastAPI
from app.api.auth import router as authrouter
from app.api.user import router as u_pro_frouter
import uvicorn

app=FastAPI(title="AI SMART STUDY ALARM SYSTEM")

app.include_router(authrouter,prefix="/auth",tags=["Authentication"])
app.include_router(u_pro_frouter,prefix="/user",tags=["UserProfile"])

def __init__():
    uvicorn.run(app,host="127.0.0.0", port=8000)