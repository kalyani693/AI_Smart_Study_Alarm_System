import numpy as np
import pandas as pd

np.random.seed(42)

n_samples = 10000

time_of_day = [
    "Morning",
    "Afternoon",
    "Evening",
    "Night"
]

subject_type = [
    "Python",
    "DSA",
    "DBMS",
    "Operating Systems",
    "Machine Learning",
    "Aptitude",
    "Ai",
    "Java"
]

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

data = pd.DataFrame({
    "time_of_day": np.random.choice(time_of_day, n_samples),

    "subject_type": np.random.choice(subject_type, n_samples),

    "session_duration_inmin":  np.round(
        np.random.uniform(10, 120, n_samples),
        1
    ),
    "breaks_taken_count": np.random.randint(1, 11, n_samples),

    "day_of_week": np.random.choice(days, n_samples)
})

Normalized_focus_Score = []

for _, row in data.iterrows():

    score = 50


    # Morning generally performs better
    if row["time_of_day"] == "Morning":
        score += 10
    elif row["time_of_day"] == "Evening":
        score += 5
    elif row["time_of_day"] == "Night":
        score -= 5

    # Weekend adjustment
    if row["day_of_week"] in ["Saturday", "Sunday"]:
        score -= 3

    # Subject-specific effect
    if row["subject_type"] == "Machine Learning":
        score -= 2

    if row["subject_type"] == "Python":
        score += 2

    if row["subject_type"] == "DSA":
        score -= 1

    # Random human variation
    score += np.random.normal(0, 5)

    score = np.clip(score, 1, 100)

    Normalized_focus_Score.append(round(score, 2))

data["Normalized_focus_Score"] = Normalized_focus_Score

data.to_csv(
    "synthetic_performance_data.csv",
    index=False
)

print(data.head())
