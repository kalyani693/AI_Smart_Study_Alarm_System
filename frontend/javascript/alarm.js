const createAlarm=document.querySelector("#new_alarm");
let timeip=document.getElementById("timeinput");
let labelip=document.getElementById("labelinput");

const create_popup=document.querySelector(".createalarm_popup")
const responseBox=document.querySelector(".responsebox");

const token=localStorage.getItem("access_token");


//create alarm function
async function create_alarm() {

  try{
    const url="http://127.0.0.1:8000/alarm/alarm";
    
    //checkbox inputs

    const checkboxes=document.querySelectorAll('input[name="day"]:checked');
    const selected_days=Array.from(checkboxes).map(cb =>cb.value);
    
    let input={
    "Time":timeip.value,
    "label":labelip.value,
    "repeat_on":selected_days
    };

    let response= await fetch(url,{
        method:"POST",
        headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"},
        body:JSON.stringify(input)           
    });

    let data= await response.json();
    if (data.detail||data.details){
         responseBox.innerHTML=`${data.detail||data.details}`;
    }else{
        responseBox.innerHTML=`<p>Response= ${data.message}<br>
           <h4> Time: ${data.Time}</h4>
           <h4> Label: ${data.Label}</h4>
        </p>`;
    }
    }
    catch (error){
        console.error(error);
        responseBox.innerHTML="Failed to create alarm";
    }
};

createAlarm.addEventListener("click", async ()=>{
      
      create_popup.classList.add("show");
      const create=document.querySelector("#createbtn");
      // call function
      create.addEventListener("click", await create_alarm)
});



//delete alarm
const messagebox=document.querySelector(".message");

async function deleteAlarm(alarm_id){
   try{
    const url=`http://127.0.0.1:8000/alarm/delete/${alarm_id}`;
    
    let response= await fetch(url,{
        method:"DELETE",
        headers:{"Authorization":`Bearer ${token}`}          
    });

    let data= await response.json();
    
    if (data.detail||data.details){
         messagebox.innerHTML=`${data.detail||data.details}`;
    }else{
      
        messagebox.innerHTML=`<p>${data.message||"Failed to delete alarm"}
        </p>`;
        //refresh page
        get_alarms();
    }
    }
    catch (error){
        console.error(error);
        messagebox.innerHTML=`<p style="color:red";>Failed to delete alarm</p>`;
    }
};



//Get existing alarms
const existingalarm=document.querySelector(".existing_Alarms");

async function get_alarms() {

  try{
    const url="http://127.0.0.1:8000/alarm/existing_alarm";

    let response= await fetch(url,{
        method:"GET",
        headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"}         
    });

    let data= await response.json();
    const alarms=data.alarms;

    let alarm_structure=``;

    if (data.detail||data.details){
      existingalarm.innerHTML=`${data.detail||data.details}`;
    }else{
         alarm_structure+=`<div class="alarm-item"><span><h4> alarm_Time </h4></span> 
            <span><h4>Label</h4></span>
            <span><h4>Repeat_on</h4></span>
            <span><h4>Snooze_count</h4></span>
            <span><h4>Status</h4></span>
            <span><h4>Delete</span></h4></div><br>
            
          `;
       alarms.forEach(item => {
          alarm_structure+=`<div class="alarm-item"><span>${item.alarm_Time}</span> 
            <span>${item.Label||"-"}</span>
            <span>${item.repeat_on||"-"}</span>
            <span>${item.snooze_count||0}</span>
            <span>${item.status||"-"}</span>
            <button class="delete-btn" onclick="deleteAlarm('${item.Id}')">Delete</button></div><br>
            <br>
          `;
       }); 
       existingalarm.innerHTML=alarm_structure;
    }
    }
    catch (error){
        console.error(error);
        existingalarm.innerHTML="Failed to load existing alarms";
    }
};

//execute on refresh page
document.addEventListener("DOMContentLoaded", get_alarms);





