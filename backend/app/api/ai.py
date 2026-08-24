from fastapi import APIRouter, Depends,File,UploadFile,Form,HTTPException
from app.services.auth import authentication
from app.database.schema import getdb
from sqlalchemy.orm import Session
from typing import Annotated,Optional
from app.models.ai_ml_models import generate_plan_input,sub_name
from app.services.ai_Service.core_Service import extract_info_from_syllabus,extract_text
from app.services.ai_Service.get_service import gen_plan,summarizer,generate_quiz
from datetime import datetime


router=APIRouter()
dependacy=Annotated[Session,Depends(getdb)]
auth=authentication()

description="""input should be in json format->
{"Exam_date":"2026-07-30",
    "Daily_available_hours":int}
"""

@router.post("/generate-plan")
async def generateplan(sylabus_file: UploadFile= File(...),user=Depends(auth.check_user),input:str=Form(...,description=description)):
    try:
        st_time=datetime.now()
        user_input=generate_plan_input.model_validate_json(input)

        
        text=await extract_text(sylabus_file)
        if text:
            sylabus_info=await extract_info_from_syllabus(text)
            print("duration:",datetime.now()-st_time)
            return await gen_plan(user_input,sylabus_info)
        else:
            raise HTTPException(status_code=500,detail="Please enter valid pdf")
        
     
    except Exception as e:
        raise HTTPException(status_code=429,detail=f"Validation  Error:{str(e)}")

    


@router.post("/summarize-notes")
async def summarize_notes(Notes:UploadFile= File(...),user=Depends(auth.check_user)):#input:str=Form(...,description="""{"Subject":"str"}"""),
    try:
        st_time=datetime.now()
        #subject=sub_name.model_validate_json(input)
        #text=await pdf_to_text(Notes)
        text= await extract_text(Notes)
        if text:
         print("duration:",datetime.now()-st_time)
         #return {"len of extracted text":text}
         return await summarizer(text)
        else:
            raise HTTPException(status_code=500,detail="Please upload valid pdf. or check internet connection.")
       
        
    except Exception as e:
        raise HTTPException(status_code=429,detail=f"Validation  Error:{str(e)}")
    


@router.post("/generate-quiz")
async def generatequiz(Notes:UploadFile= File(...),user=Depends(auth.check_user), quizeType:str=Form(...,description="Enter Quize type(MCQ, Fill the Blanks, True/False)")):
    st_time=datetime.now()
    text=await extract_text(Notes)
    notes_summary=await summarizer(text)
    print("duration:",datetime.now()-st_time)
    return await generate_quiz(notes_summary,quizeType)
    

@router.post("/chatbot")
def chatbot():
    return "personalized chatbot is not ready yet!!, it will available soon."