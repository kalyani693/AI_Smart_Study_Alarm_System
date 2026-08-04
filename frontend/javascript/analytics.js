const chartscontainer=document.querySelector(".charts");
const linechart=document.querySelector("#sleep_performance_btn");
const barchart=document.querySelector("#score_timeofday_btn");
const piechart=document.querySelector("#subject_distribution_btn");
const token=localStorage.getItem("access_token")

 async function connect_backend() {
    const url = "http://127.0.0.1:8000/analytics/stats";
    
    try{
         let response = await fetch(url, {
            method:'POST',
            headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"}
        });
        let data = await response.json();
        console.log(data)

    let total_study_hr=data.total_study_hours;
    let avg_focus_score=data.average_focus_score;
    let number_of_sessions=data.number_of_sessions;

    // Populate analytics info block dynamically
    document.querySelector("#i1 h3").textContent=`${total_study_hr} hr`||0;
    document.querySelector("#i2 h3").textContent=avg_focus_score||0;
    document.querySelector("#i3 h3").textContent=0;
    document.querySelector("#i4 h3").textContent=number_of_sessions||0;
    }
    catch{
       alert("Something went wrong while fetching user information. Please make sure backend is running.");
    }  
}

document.addEventListener("DOMContentLoaded", connect_backend);

//charts
 async function  get_sleepHour_Performance_score(){
   //sleep_hours
   try{
   const url1="http://127.0.0.1:8000/analytics/get_sleep_hours";

   let response1=await fetch(url1,{
      method:"POST",
      headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"}
   } );

   let data1= await response1.json();
   sleep_hours=data1.sleep_hours;

   //study_performance

   const url2="http://127.0.0.1:8000/analytics/get_performance";

   let response2=await fetch(url2 ,{
      method:'POST',
      headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"}
   });
   let data2= await response2.json();
   const performance_score=[];

   for (let row of data2){
      performance_score.push(row.average_focus_score||0)
   };

   return {"sleep_hours":sleep_hours,
      "performance_score": performance_score}  
}
catch(err)
{  console.error(err);  
   //alert("Something went wrong while fetching charts information. Please make sure backend is running.");
}
  };

 async function get_subject_score(){
   try{
   const url="http://127.0.0.1:8000/analytics/subject_distribution";

   let response=await fetch(url,{
      method:"POST",
      headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"}
   } );

   let data= await response.json();
   let subject=[];
   let score=[];
   let sessions=[];
   if (data){
      data.forEach(item => {
         subject.push(item.subject||'-');
         score.push(item.avg_focus_score||0);
         sessions.push(item.sessions||0);
      });  

      return{
         "subject":subject,
         "score":score,
         "sessions":sessions
      }
   }
   else if (data.detail||data.details){
      chartscontainer.innerHTML=`<h4> Failed to Load data:${data.detail||data.details} </h4>`;
   }
   
 }
 catch{
   chartscontainer.innerHTML=`<h4> Failed to Load data</h4>`;
 }
};

async function get_timeofday_score(){
   try{
   const url="http://127.0.0.1:8000/analytics/focus_score_per_timeOfday";

   let response=await fetch(url,{
      method:"POST",
      headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"}
   } );

   let data= await response.json();
   let time_of_day=[];
   let score=[];

   if (data){
      data.forEach(item => {
         time_of_day.push(item.Time_of_day||'-');
         score.push(item.avg_focus_score||0);
      });  

      return{
         "time_of_day":time_of_day,
         "score":score
      }
   }
   else if (data.detail||data.details){
      chartscontainer.innerHTML=`<h4> Failed to Load data:${data.detail||data.details} </h4>`;
   }
   
 }
 catch{
   chartscontainer.innerHTML=`<h4> Failed to Load data</h4>`;
 }
};

 let currentchart=null;
 function charts(x_data, y_data,x_label,y_label, type){
     chartscontainer.innerHTML=`
            <canvas id="myChart"></canvas>`;

            const ctx=document.getElementById('myChart').getContext('2d');

            if(currentchart){
               currentchart.destroy();
            }

            currentchart=new Chart(ctx, {
                type:type,
                data: {
                labels:x_data,
                datasets: [{
                    label: y_label,
                    data:y_data,
                    borderWidth: 1
                }]
                },
                options: {
                scales: {
                    y: {
                    beginAtZero: true
                    }
                }
                }
            });
         };

 linechart.addEventListener("click", async ()=>{
   try{
      const {sleepHours,PerformanceScore}= await get_sleepHour_Performance_score();
      charts(sleepHours,PerformanceScore,'sleep Hours',"performance",'line');
   }
   catch(err){
      console.error(err);
   }    
 });

 barchart.addEventListener("click", async ()=>{
   try{
      const {time_of_day,sessions}=await get_timeofday_score();
      charts(time_of_day,sessions,'Time of Day', "NO of Sessions" ,'bar');
   }
   catch(err){
      console.error(err);
   }    
 });
 

 piechart.addEventListener("click", async ()=>{
   try{
      const {subject,score,sessions}=await get_subject_score();
      charts(subject,sessions, 'Subject','Session','pie');
   }
   catch(err){
      console.error(err);
   }    
 });
 


 


