from fastapi import APIRouter, Depends,File,UploadFile,Form,HTTPException
from app.services.auth import authentication
from app.database.schema import getdb
from sqlalchemy.orm import Session
from typing import Annotated,Optional
from app.models.ai_ml_models import generate_plan_input,sub_name
from app.services.ai_Service.core_Service import extract_info_from_syllabus,pdf_to_text
from app.services.ai_Service.get_service import gen_plan,summarizer,generate_quiz



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
        user_input=generate_plan_input.model_validate_json(input)
    except Exception as e:
        raise HTTPException(status_code=429,detail=f"Validation  Error:{str(e)}")

    text= await pdf_to_text(sylabus_file)

    if text:
        sylabus_info= await extract_info_from_syllabus(text)
        return await gen_plan(user_input,sylabus_info)
    else:
        return {"message":"Please provide valid pdf, Pdf might be empty."}


@router.post("/summarize-notes")
async def summarize_notes(Notes:UploadFile= File(...),user=Depends(auth.check_user)):#input:str=Form(...,description="""{"Subject":"str"}"""),
    try:
        #subject=sub_name.model_validate_json(input)
        pass
    except Exception as e:
        raise HTTPException(status_code=429,detail=f"Validation  Error:{str(e)}")
    text=await pdf_to_text(Notes)
    return await summarizer(text)


@router.post("/generate-quiz")
async def generatequiz(Notes:UploadFile= File(...),user=Depends(auth.check_user)):
    text=await pdf_to_text(Notes)
    notes_summary=await summarizer(text)
    return await generate_quiz(notes_summary)
    

@router.post("/chatbot")
def chatbot():
    return "personalized chatbot is not ready yet!!, it will available soon."