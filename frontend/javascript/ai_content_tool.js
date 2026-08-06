const token=localStorage.getItem("access_token");  
//dropdown inputs
let sumarizer_btn=document.getElementById("sumarizer-btn");
let summarizer_box=document.getElementById("summarizer-box");

let quize_btn=document.getElementById("quize-btn")
let quize_box=document.getElementById("quize-box")

sumarizer_btn.addEventListener("click", function(event){
    event.preventDefault();

    if(summarizer_box.style.display==='none'|| summarizer_box.style.display===''){
        summarizer_box.style.display="block";
    }
    else{
        summarizer_box.style.display= 'none';
    }
});

quize_btn.addEventListener("click", function(event){
    event.preventDefault();

    if (quize_box.style.display==='none'|| quize_box.style.display===''){
        quize_box.style.display="block";
    }else{
        quize_box.style.display='none';
    }
});


//summarizer
let summary_popup=document.querySelector(".summary_popup");
let Summarybox=document.querySelector(".Summarybox");

const notes=document.querySelector("#notes-input");
const summarizebtn=document.querySelector("#ok-summarize");
const formdata=new FormData();

//function
async function get_summary() {

  formdata.append("Notes",notes.files[0]);

  try{
   const url="http://127.0.0.1:8000/ai/summarize-notes";

    let response=await fetch(url,{
      method:"POST",
      headers:{"Authorization":`Bearer ${token}`},
      body:formdata              
   } );

   let data= await response.json();
   const summary=data.response||"Failed to summarize";

   if(data.detail||data.details){
     Summarybox.innerHTML=`<h4>${data.detail||data.details}</h4>`;
   }
   else{
      Summarybox.innerHTML=`<p>${summary}</p>`;
   }


  }
  catch (error){
    console.error(error);
    Summarybox.innerHTML="Failed to summarize Notes";
  }
};

summarizebtn.addEventListener("click", async ()=>{
    //call function
    summary_popup.classList.add("show");

    Summarybox.innerHTML="<h4>Generating...</h4>";
    await get_summary();

    
});


//Quizes
let quize_popup=document.querySelector(".quize_popup");
let quizesbox=document.querySelector(".quizesbox");

const topic=document.querySelector("#topic-input");
const getquize_btn=document.querySelector("#ok-quize");
const formdata_=new FormData();

//function
async function get_quizes() {
  formdata_.append("Notes",topic.files[0]);

  try{
   const url="http://127.0.0.1:8000/ai/generate-quiz";

    let response=await fetch(url,{
      method:"POST",
      headers:{"Authorization":`Bearer ${token}`},
      body:formdata_              
   } );

   let data= await response.json();
   const quizes=JSON.parse(data.response)||"Failed to get quizes";

   let quize_structure=``;

   quizes.forEach(qz => {
       quize_structure+=`<div class="quize-item">
            <p>
                <h4 id="question">${qz}. ${qz.question}</h4>
                <br>
                
                <div class="options">
                    <input type="radio" name="option" value="${qz.option_A}", id="op1">
                    <label for="${qz.option_A}">${qz.option_A}</label><br>

                    <input type="radio" name="option" value="${qz.option_B}", id="op2">
                    <label for="${qz.option_B}">${qz.option_B}</label><br>

                    <input type="radio" name="option" value="${qz.option_C}", id="op3">
                    <label for="${qz.option_C}">${qz.option_C}</label><br>

                    <input type="radio" name="option" value="${qz.option_D}", id="op4">
                    <label for="${qz.option_D}">${qz.option_D}</label><br>

                </div>
                <br>
            </p>
        </div>
       `;
   });

   quize_structure+=`<button id="submit_quize" > Submit</button>`;

   if(data.detail||data.details){
     quizesbox.innerHTML=`<h4>${data.detail||data.details}</h4>`;
   }
   else{
      
      quizesbox.innerHTML=quize_structure;
   }


  }
  catch (err){
    console.error(err);
    quizesbox.innerHTML=`<h4>Failed to get quizes</h4>`;
  }
};

getquize_btn.addEventListener("click", async ()=>{
    //call function
    quize_popup.classList.add("show");

    quizesbox.innerHTML=`<h4>Generating...</h4>`;
    await get_quizes();

});



