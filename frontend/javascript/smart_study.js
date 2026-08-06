//input drop down
let get_plan=document.getElementById("getplan-btn");
let get_plan_box=document.getElementById("getplan-box");


let focus_Score_btn=document.getElementById("focus_score_btn")
let focus_score_box=document.getElementById("focus_score_box")

get_plan.addEventListener("click", function(event){
    event.preventDefault();

    if(get_plan_box.style.display=== 'none'|| get_plan_box.style.display===''){
        get_plan_box.style.display="block";
    }
    else{
        get_plan_box.style.display= 'none';
    }
});

focus_Score_btn.addEventListener("click", function(event){
    let responseconainer=document.querySelector(".res1");
    responseconainer.innerHTML=``;
    event.preventDefault();

    if (focus_score_box.style.display==='none'|| focus_score_box.style.display===''){
        focus_score_box.style.display="block";
    }else{
        focus_score_box.style.display='none';
    }
});


// pass input data to backend
let get_score=document.querySelector("#ok-score");
let get_studyplan=document.querySelector("#ok-studyplan");
let getBest_slot=document.querySelector("#best_slot_btn");
const responsetable=document.querySelector(".responsetable");
const studyplanpopup=document.querySelector(".study_plan_popup");



//Study Plan
//inputs
const sylabusFile=document.querySelector("#file-input");
const examdate=document.querySelector("#exam-input");
const studyhours=document.querySelector("#studyhours-input");
 
async function study_plan_from_backend(){

  const token=localStorage.getItem("access_token");  
  const formdata=new FormData();



  let input={
      "Exam_date":examdate.value,
      "Daily_available_hours":studyhours.value
  };

  formdata.append("input",JSON.stringify(input));
  formdata.append("sylabus_file",sylabusFile.files[0]);

  try{
   const url="http://127.0.0.1:8000/ai/generate-plan";

    let response=await fetch(url,{
      method:"POST",
      headers:{"Authorization":`Bearer ${token}`},
      body:formdata              
   } );

   let data= await response.json();
   const studyPlan=JSON.parse(data.response)||[];

   if(data.detail||data.details){
     console.log(data.detail||data.details);
      responsetable.innerHTML=`<p>Error in feching study plan:${data.detail||data.details}</p>`;
   }else{

   //table design
   let plantable=`<table border="1" style="width:100%; text-align:center; padding:10px;">
                    <tr>
                        <th> Date </th>
                        <th >Subject </th>
                        <th>  Study Duration </th>
                        <th> Mode </th>
                        <th> Importance Score </th>
                    </tr>`;

  // add data
  studyPlan.forEach((item) => {
    plantable+=`
              <tr>
                <td>${item.Date ||'-'}</td>
                <td>${item.Subject ||'-'}</td>
                <td>${item.Study_duration ||'-'}</td>
                <td>${item.Mode ||'-'}</td>
                <td>${item.Importance_score ||'-'}</td>
              </tr>
  ` ; 
  });

  // close table tag
   plantable+=`</table>`;

  responsetable.innerHTML=plantable;
  }
 } 
catch (error)
{
    console.log("error fetching Response:",error);
    responsetable.innerHTML="<p> Failed to Load Response</p>";
    
}                
 



};

get_studyplan.addEventListener("click", async ()=>{

    studyplanpopup.classList.add("show");
    responsetable.innerHTML="Loading Response...";
    //call function
    await study_plan_from_backend();
    
});

//Focus score prediction
//inputs
const session_duration=document.querySelector("#session_duration-input");
const subject=document.querySelector("#subject-type");

let responseconainer=document.querySelector(".res1");

async function PredictFocusScore() {

  responseconainer.innerHTML=``;

  const token=localStorage.getItem("access_token");  

   let input={
    "session_duration_inmin":session_duration.value   ,  
    "subject_type":subject.value
    };

  try{
   const url="http://127.0.0.1:8000/ml/Focus-score";

    let response=await fetch(url,{
      method:"POST",
      headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"},
      body:JSON.stringify(input)            
   } );

   let data= await response.json();
   const result=data.message;
  
   if(data.detail|| data.details){
      responseconainer.textContent=data.detail||data.details;
   }
   else{
     responseconainer.innerHTML=`<h4>Predicted Focus Score: ${result}</h4>`;
   }

  }
  catch (err){
    console.error(err);
    responseconainer.innerHTML=`<h4>failed to Predict Focus Score</h4>`;
  } 
};

get_score.addEventListener("click", async ()=>{
      responseconainer.innerHTML=`Loading...`;
      await PredictFocusScore();
      
});


//Best study slot
let responsebox=document.querySelector(".res2")

async function BestSlot() {
    
  responsebox.innerHTML=null;

  const token=localStorage.getItem("access_token");  

  try{
   const url="http://127.0.0.1:8000/ml/best-slot";

    let response=await fetch(url,{
      method:"POST",
      headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"}        
   } );

   let data= await response.json();
   const result=data.message;
  
   if(data.detail|| data.details){
      responsebox.textContent=data.detail||data.details;
   }
   else{
     responsebox.innerHTML=`<h4>Recommended Best Time slot To study: ${result}</h4>`;
   }

  }
  catch (err){
    console.error(err);
    responsebox.innerHTML=`<h4>failed to get Best Slot</h4>`;
  } 

};

getBest_slot.addEventListener("click", async ()=>{
      responsebox.innerHTML=`Loading...`;
      await BestSlot();
      
});