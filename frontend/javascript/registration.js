const full_name=document.getElementById("full-name");
const username=document.getElementById("username");
const Email=document.getElementById("email");
const highestClass=document.getElementById("highest-class");
const school_college=document.getElementById("school-name");
const city=document.getElementById("city");
const state=document.getElementById("state");
const country=document.getElementById("country");
const job_title=document.getElementById("job-title");
const companyname=document.getElementById("company-name");
const yearofexperiance=document.getElementById("years-of-experience");
const keyskills=document.getElementById("key-skills");
const password=document.getElementById("password");

const regibtn=document.getElementById("registerbtn");

const responsebox=document.querySelector(".responsebox");

async function connect() {
    regibtn.disabled=true;
   
    let input={
  "Full_Name" :full_name.value,
  "Username":username.value,
  "Email": Email.value,
  "Highest_Class":highestClass.value,
  "School_College":school_college.value,
  "CurrentLocation": {
    "city":city.value,
    "state":state.value,
    "country": country.value
  },
  "work_history": {
    "job_title":job_title.value,
    "Company_Name":companyname.value,
    "Year_of_Experience":yearofexperiance.value||0
  },
  "Key_skills":keyskills.value,
  "Password":password.value
  }
  
 const url="http://127.0.0.1:8000/auth/Registration"
  try{
    let response= await fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify(input)
    });

    let data=await response.json();
    const res=data.message||"someting went wrong";

    console.log(data)
    regibtn.disabled=false;

    if(data.detail||data.details){
        responsebox.innerHTML=`${data.detail||data.details}`;
    }
    else {
        responsebox.innerHTML=`<p style="color:green;">${res}</p>`;
    }
    
    if (response.ok()){
        window.location.assign("login.html")
    }
  }
  catch (error) {
        console.error("error:", error);
        responsebox.innerHTML=`<p style="color:red;">Failed to Register</p>`;
    }
 
};

regibtn.addEventListener('click', connect);