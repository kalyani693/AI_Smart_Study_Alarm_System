const username=document.getElementById("_username");
const password=document.getElementById("pass");
const loginbtn=document.getElementById("loginbtn");
const formdata=new FormData();


async function connect() {
   const url="http://127.0.0.1:8000/auth/login"
    /* Create loader
    let loader = document.createElement("div");
    loader.classList.add("loader");
    loader.textContent = "";
    loginbtn.innerHTML=loader;*/

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

    


    let result = document.createElement("h3");
        result.classList.add("result-msg");
        
    if (data.detail || data?.detail?.error){
        result.textContent = data?.detail?.error;
        result.style.color = "red";
    }
    else{
        result.textContent="LoggedIn Successfully!";
    }
    
    loginbtn.after(result);

    if (response.ok){
        //save token in localstorage
        localStorage.setItem("access_token",data.access_token);

        setTimeout(() => {
                window.location.href("index.html")
            }, 10000);
    }    
  }
  catch (error) {
        console.error("error:", error);
        //regibtn.innerHTML=Register
        let error_msg = document.createElement("h4");
        error_msg.classList.add("result-msg");
        error_msg.textContent = "something went wrong.\nPlease Enter valid Credentials!";
        error_msg.style.color = "red";
        loginbtn.after(error_msg);
    }
 
};

loginbtn.addEventListener('click', connect);