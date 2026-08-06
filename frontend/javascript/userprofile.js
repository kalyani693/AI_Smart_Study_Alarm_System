const popup = document.getElementById("pop");
const menubtn = document.getElementById("menu");
const back = document.getElementById("back");

// Open and close navigation overlay
menubtn.addEventListener('click', () => {
    popup.classList.add('show');
});

back.addEventListener('click', () => {
    popup.classList.remove('show');
});

// Logout handler (clears dynamic URL params and redirects)
const logoutItem = document.querySelector(".menucard p:nth-child(4)");
if (logoutItem) {
    logoutItem.style.cursor = "pointer";
    logoutItem.addEventListener("click", () => {
        
        localStorage.removeItem("access_token");
        window.location.href = "index.html";
    });
}

// Function to load and display user profile details dynamically
const url = "http://127.0.0.1:8000/user/userProfile";
 async function loadUserProfile() {
    const token=localStorage.getItem("access_token")
    
    try{
         let response = await fetch(url, {
            method:'GET',
            headers:{"Authorization":`Bearer ${token}`,
                     "Content-Type":"application/json"}
        });
        let data = await response.json();
        console.log(data)

    let userinfo=data.message;
    const user = {
        username: userinfo.Username|| "priti_dev",
        fullname: userinfo.Full_Name|| "priti Sonawane",
        email:userinfo.Email|| "priti@example.com",
        highestclass:userinfo.Highest_Class|| "B.Tech (Computer Science & Engineering)",
        school_college:userinfo.School_College||"Government college delhi.",
        location:userinfo.CurrentLocation||"Delhi,Uttar Pradesh, India",
        work_history:userinfo.work_history||"{job Type:Developer, Comapany Name: Microsoft, Year of Experience:2}",
        key_skills:userinfo.Key_skills||"python,java etc"
    };

    // Update greeting heading
    const greetingText = document.querySelector(".greetings h2");
    if (greetingText) {
        greetingText.textContent = `Welcome ${user.fullname}!`;
    }

    // Populate user profile info block dynamically
    const infoContainer = document.querySelector(".info");
    if (infoContainer) {
        infoContainer.innerHTML = `
            <p><strong>Username:</strong> ${user.username}</p>
            <p><strong>Full Name:</strong> ${user.fullname}</p>
            <p><strong>Email:</strong> ${user.email}</p>
            <p><strong>Highest Class:</strong> ${user.highestclass}</p>
            <p><strong>School/College Name:</strong> ${user.school_college}</p>
            <p><strong>Location/Address:</strong> ${user.location}</p>
            <p><strong>Work History:</strong>Job Title: ${user.work_history.job_title||"-"},
                                             Company Name: ${user.work_history.Company_Name||"-"}
                                             Year of Experience: ${user.work_history.Year_of_Experience||0}</p>
            <p><strong>Key Skills:</strong> ${user.key_skills}</p>
        `;
    }
    }
    catch{
       alert("Something went wrong while fetching user information. Please make sure backend is running.");
    }
    
}

// Execute profile load
document.addEventListener("DOMContentLoaded", loadUserProfile);