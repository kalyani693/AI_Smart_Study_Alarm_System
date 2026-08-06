from datetime import datetime
from fastapi import HTTPException
from app.services.ai_Service.core_Service import ask_llm
import json

async def gen_plan(user_input,syllabus):
    prompt=f"""todays_date={datetime.now().strftime("%d/%m/%Y")},
    role:act as a Mentor. a experienced Plan/time-Table generator.
    action: generate a day-wise study plan for provided syllabus till exam date from Tomarrow.
    plan should contain learning,practice as well as revision plan.
    if subjects or topics are more and remaining days are less then prioraties important suject/topics first.
    Response Format: it should be strictly List[JSON]
    like-->[
    {{  "Date":"",
        "Subject":"",
        "Study_duration":"int",
        "Mode":"",
        "Importance_score":"int"
        }},

    {{  "Date":"",
        "Subject":"",
        "Study_duration":"int",
        "Mode":"",
        "Importance_score":"int"

    }}]
          Subject should be string, study duration should int,mode is  
    in[Learning,Practice,Revision], importance score should be in the range(1 t0 10).
    date:DD/MM/YY

    Exam_date,Daily_available_hours={user_input}, 
    syllabus_text={syllabus}.

    dont ask any follow up question.
"""

    try:
      raw_response=ask_llm(prompt)
      if raw_response.startswith("```json") or raw_response.endswith("```"):
            clean_res=raw_response.replace("```json","").replace("```","").strip()
            response=json.load(clean_res)
            print("Study plan is generated successfully!!")
            return {"response":response}
      else: return {"response":raw_response}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error in generating response:{e}") 

async def summarizer(notes_text):
   prompt=f"""role: act as a briliant notes summarizer.
   action: summarize notes text, highlight important topics/points.
   1 page -> max 1-2 paragraph. (do not miss important topics)

   Response format: str
   do not ask any follow up questions

   note text={notes_text}

     """    

   try:
        response=ask_llm(prompt)
        print("Notes summary is created!!")
        return {"response":response}
   except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error in generating response:{e}") 

async def generate_quiz(notes_summary):
    prompt=f"""role: act as a quiz generator.
    action: generate 10 MCQ based quiz on provided notes, to self practice before exams.
    do not ask any follow up questions
    response format->list[json]
    [
        {{
               "question":"..",
                "option_A":"",
                "option_B":"",
                "option_C":"",
                "option_D":"",
                "Answer":""
            
        }},
        {{
               "question":"..",
                "option_A":"",
                "option_B":"",
                "option_C":"",
                "option_D":"",
                "Answer":""
            
        }},
        etc.. ]

    notes_summary={notes_summary}
    
 """  

    try:
        raw_response=ask_llm(prompt)
        if raw_response.startswith("```json") or raw_response.endswith("```"):
            clean_res=raw_response.replace("```json","").replace("```","").strip()
            response=json.load(clean_res)
            print("quizes are generated successfully!!")
            return {"response":response}
        else: return {"response":raw_response}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error in generating response:{e}")  