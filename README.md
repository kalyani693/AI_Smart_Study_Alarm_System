# ⏰ AI Smart Study Alarm System

An AI-powered study companion that helps students build better study habits by analyzing focus patterns, snooze behavior, and study history to recommend the best study time.

Instead of acting like a traditional alarm, this system learns from user behavior and provides personalized study insights and reminders.

---

## ✨ Features

- 🔐 User Authentication (JWT)
- 👤 User Profile Management
- ⏰ Smart Study Alarm
- 😴 Snooze Tracking
- 👩🏻‍🎓 Smart study sessions
- 📊 Study Analytics Dashboard
- 📈 Performance Prediction
- 🧠 Best Study Time Recommendation
- 📅 Study Session History
- 📱 Responsive Frontend
- 📄 REST API Documentation

---

## 🚀 Project Overview

The AI Smart Study Alarm System is designed to improve study consistency using data-driven insights.

The application collects information such as:

- Study time
- Subject
- self rated focus score
- Time of day
- Previous snooze history
- Day of week

Using machine learning and historical study patterns, the system predicts:

- Expected study performance/Normalized_focus_Score
- Probability of snoozing
- Best study slot


---

# 🏗️ Architecture

```
Frontend
    │
    ▼
FastAPI Backend
    │
    ├── Authentication
    ├── Study Session APIs
    ├── AI APIs
    ├── Alarm APIs
    ├── Analytics APIs
    ├── ML Prediction APIs
    │
Postgress Database
    │
    ▼
Machine Learning Models
```

---

# 🛠️ Tech Stack

## Backend

- FastAPI
- Python
- Pydantic
- Uvicorn
- SQLAlchemy
- JWT Authentication
- LLM Integration (GEMINI, GROQ, OpenRouter)

## Frontend

- HTML
- CSS
- JavaScript

## Machine Learning

- Scikit-Learn
- Pandas
- NumPy
- Joblib
- pickel

## Database

- PostgresQL

---

# 📂 Project Structure

```
AI-Smart-Study-Alarm-System/

│
├── backend/app
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── database/
│   ├── core/
│   └── main.py
|
├── backend/main
│ 
├── backend/ requirement.txt
│
├── frontend/
│   ├── css/
│   ├── javascript/
│   └── html/
│
├── ml/
│   ├── data_generations/
│   ├── training/
│   ├── ml_models/
│
│
├── README.md
│
└── .gitignore
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/kalyani693/AI_Smart_Study_Alarm_System.git
```

```bash
cd AI-SMART-STUDY-ALARM-SYSTEM
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## Create .env file
---
```
set 

#For Database connection
DATABASE_URL="your Database Url" 

#for JWT authentication
SECRET_KEY= your secret key
ALGORITHM="HS256"

#for LLM integration
GOOGLE_API_KEY=   google api key
openai_api_key=  openai api key
GROQ_API_KEY= groq api key
openrouter_api= openrouter api key
---
```

## Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## Run Backend

```bash
cd backend
uvicorn main:app --reload
```

---

## Open Frontend

Open

```
frontend/html/index.html
```
---

# 📚 API Documentation

After running the server:

Swagger UI

```
http://127.0.0.1:8000/docs
```
---

# 🤖 Machine Learning Models

The project currently includes:

- Performance Prediction Model
- Snooze Prediction Model
- Best Study Slot Recommendation(Temporary  Rule Based)

---

# 📊 Analytics

The dashboard provides:

- Study Hours last 7 days
- NO of sessions Completed in last 7 Days
- Average Focus Score of last 7 days
- Subject-wise Performance
- Sleep vs Focus Trend
- Focus score vs Time of Day


---

# 📸 Screenshots

```
screenshots/login.PNG

screenshots/analytics_dashboard.PNG

screenshots/home page.PNG

screenshots/registration.PNG
```

### Current Limitations

- Alarm  Management CRUD(create, Read, Update, Delete ) is fully implemented. Browser side scheduled alarm triggering is not done yet.
- Response time of API is bit slow. It will be fast soon.


---

# 🧪 Future Improvements

- Email reminders
- Mobile application
- Smart notifications
- personalized AI chatbot assistant
- Cloud deployment

---

### 🤝 Contributing

Contributions are always welcome!

## Step 1

Fork the repository.

## Step 2

Create a new branch.

```bash
git checkout -b feature/your-feature-name
```

## Step 3

Commit your changes.

```bash
git commit -m "Add new feature"
```

## Step 4

Push to your branch.

```bash
git push origin feature/your-feature-name
```

## Step 5

Open a Pull Request.

### Contribution Guidelines

Please ensure that:

- Code follows PEP-8 style guidelines.
- Write meaningful commit messages.
- Test your changes before submitting.
- Keep pull requests focused on one feature or bug fix.
- Update documentation if necessary.
- Be respectful and constructive during code reviews.

---

# 🐞 Reporting Issues

If you discover a bug or have a feature request:

1. Search existing issues first.
2. Open a new issue.
3. Clearly describe the problem.
4. Include steps to reproduce.
5. Add screenshots if applicable.


# 🙌 Acknowledgements

- FastAPI
- Scikit-Learn
- Pandas
- NumPy
- Python Community

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork the repository

🛠️ Contribute to the project

Share it with others!

---

Made with ❤️ using Python, FastAPI, and Machine Learning.
