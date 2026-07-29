import numpy as np
import pandas as pd


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


np.random.seed(42)

n = 10_000

data = pd.DataFrame({
    "user_id": np.random.randint(1, 501, n),

    "sleep_duration": np.clip(
        np.random.normal(6.5, 1.5, n),
        3,
        10
    ),

    "sleep_quality": np.random.randint(1, 11, n),

    "fatigue_level": np.random.randint(1, 11, n),

    "previous_snooze_count": np.random.poisson(1.5, n),

    "study_importance": np.random.randint(1, 11, n),

    "days_since_last_study": np.random.randint(0, 8, n),

})


# Alarm time in hours
data["alarm_hour"] = np.random.choice(
    [5, 6, 7, 8, 9, 10],
    n
)


# Create a behavioural score
logit = (
    -2.0

    # Poor sleep increases snooze probability
    + 0.35 * (7 - data["sleep_duration"])

    # Poor sleep quality increases snooze probability
    + 0.25 * (10 - data["sleep_quality"])

    # Fatigue increases snooze probability
    + 0.35 * data["fatigue_level"]

    # Previous snoozing behaviour increases future snoozing
    + 0.45 * data["previous_snooze_count"]

    # Early alarms are harder to wake up for
    + 0.25 * (8 - data["alarm_hour"])

    # Higher study importance reduces snoozing
    - 0.20 * data["study_importance"]


    # Long gap since study increases avoidance
    + 0.15 * data["days_since_last_study"]
)


data["snooze_probability"] = sigmoid(logit)


# Generate actual behaviour
data["snoozed"] = np.random.binomial(
    1,
    data["snooze_probability"]
)


data.to_csv(
    "synthetic_snoozedata.csv",
    index=False
)

print(data.head())