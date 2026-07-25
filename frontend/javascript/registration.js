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

const regibtn=document.getElementById("registerbtn")

async function connect() {
   
    /* Create loader
    let loader = document.createElement("div");
    loader.classList.add("loader");
    loader.textContent = "";
    regibtn.innerHTML=loader;*/

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
    "Year_of_Experience":yearofexperiance.value
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
    console.log(data)
    //regibtn.innerHTML=Register
    regibtn.disabled=false;

    let result = document.createElement("h3");
        result.classList.add("result-msg");
        //result.style.color = "green";
        result.textContent = data.message||"Something went worng"||data.detail||"Registration Successful!";
        regibtn.after(result);

    if (response.ok){
        window.location.href="index.html"
    }    
  }
  catch (error) {
        console.error("error:", error);
        //regibtn.innerHTML=Register
        let error_msg = document.createElement("h4");
        error_msg.classList.add("result-msg");
        error_msg.textContent = "something went wrong";
        error_msg.style.color = "red";
        regibtn.after(error_msg);
    }
 
};

regibtn.addEventListener('click', connect);