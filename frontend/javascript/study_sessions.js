const sessionHistory=document.querySelector("#history");
const popup=document.querySelector(".popup");
const table=document.querySelector(".historytable");

async function get_session_history(){
  const token=localStorage.getItem("access_token");  
  try{
   const url="http://127.0.0.1:8000/study/history";

    let response=await fetch(url,{
      method:"GET",
      headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"}
   } );

   let data= await response.json();
   const historydata=data.sessionData||[];

   //table design
   let historytable=`<table border="1" style="width:100%; text-align:center;">
                    <tr>
                        <th>Subject</th>
                        <th>Start-Time</th>
                        <th>End-Time</th>
                        <th>Created-at</th>
                        <th>Self Rated Focus</th>
                        <th>Breaks taken</th>
                        <th>Status</th>
                        <th>Time of Day</th>
                    </tr>`;

  // add historydata data
  historydata.forEach((item) => {
    historytable+=`
              <tr>
                <td>${item.Subject ||'-'}</td>
                <td>${item.start_time ||'-'}</td>
                <td>${item.End_time ||'-'}</td>
                <td>${item.created_at ||'-'}</td>
                <td>${item.self_rated_focus ||'-'}</td>
                <td>${item.breaks_taken ||'-'}</td>
                <td>${item.status ||'-'}</td>
                <td>${item.Time_of_day ||'-'}</td>
              </tr>
  ` ; 
  });

  // close table tag
  historytable+=`</table>`;

  table.innerHTML=historytable;
                   
}
catch (error)
{
    console.log("error fetching histor:",error);
    table.innerHTML="<p> Failed to Load session history</p>";
    
}};



sessionHistory.addEventListener("click",async ()=>{
        
        popup.classList.add("show");
        //popup.style.display="block";
        table.innerHTML="<p> Loading history..</p>";

        //function call
        await get_session_history();
});

/*sessionHistory.addEventListener("click",  async function(event){
    event.preventDefault();

    if(popup.style.display==='none'|| popup.style.display===''){
        popup.style.display="block";
         table.innerHTML="<p> Loading history..</p>";
          //function call
        await get_session_history();
    }
    else{
        popup.style.display= 'none';
    }
});*/