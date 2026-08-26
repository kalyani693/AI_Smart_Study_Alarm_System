const username=document.getElementById("_username");
const password=document.getElementById("pass");
const loginbtn=document.getElementById("loginbtn");
const formdata=new FormData();

const responsebox=document.querySelector(".responsebox");


async function connect() {
   const url="http://127.0.0.1:8000/auth/login"
    loginbtn.disabled=true;

    formdata.append("username",username.value);
    formdata.append("password",password.value);
  try{
    let response= await fetch(url,{
        method: 'POST',
        body:formdata
    });
    let data=await response.json();

    console.log(data)
    //regibtn.innerHTML=Register
    loginbtn.disabled=false;

        
    if (data.detail || data?.detail?.error){
        responsebox.innerHTML=`<p style="color:red;">${data.detail||data.details}</p>`;
    }
    else{
        responsebox.innerHTML=`<p style="color:green;">"LoggedIn Successfully!"</p>`;
    }
    if (response.ok){
         //save token in localstorage
        localStorage.setItem("access_token",data.access_token);
        window.location.assign("homePage.html");
    }
    

       
  }
  catch (error) {
        console.error("error:", error);
        //regibtn.innerHTML=Register
        let error_msg = document.createElement("h4");
        error_msg.classList.add("result-msg");
        error_msg.textContent = "something went wrong.\n\nPlease Enter valid Credentials!";
        error_msg.style.color = "red";
        error_msg.style.margin="10px";
        loginbtn.after(error_msg);
    }
 
};

loginbtn.addEventListener('click', connect);