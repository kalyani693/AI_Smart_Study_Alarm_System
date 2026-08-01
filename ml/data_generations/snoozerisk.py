import numpy as np
import pandas as pd

np.random.seed(42)

N = 10000

days = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday",
    "Saturday", "Sunday"
]


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# ----------------------------
# Basic user information
# ----------------------------

data = pd.DataFrame({
    "user_id": np.random.randint(1, 501, N),
    "day_of_week": np.random.choice(
        days,
        N,
        p=[0.16,0.16,0.16,0.16,0.16,0.10,0.10]
    )
})

# ----------------------------
# Weekend
# ----------------------------

data["is_weekend"] = (
    data["day_of_week"]
    .isin(["Saturday","Sunday"])
    .astype(int)
)

# ----------------------------
# Study importance
# Most students fall around 5-8
# ----------------------------

data["study_importance"] = np.clip(
    np.random.normal(6.5,2,N).round(),
    1,
    10
).astype(int)

# ----------------------------
# Sleep duration
# Weekend = more sleep
# ----------------------------

sleep = np.random.normal(6.7,1.2,N)

sleep += data["is_weekend"]*0.7

sleep = np.clip(sleep,3.5,10)

data["sleep_duration_prev_night"] = sleep.round(1)

# ----------------------------
# Alarm time
# Important study -> earlier alarm
# ----------------------------

alarm = []

for imp in data["study_importance"]:

    if imp >= 8:
        alarm.append(
            np.random.choice([5,6,7],p=[0.3,0.45,0.25])
        )

    elif imp >=5:
        alarm.append(
            np.random.choice([6,7,8],p=[0.25,0.45,0.30])
        )

    else:
        alarm.append(
            np.random.choice([7,8,9,10],
                             p=[0.15,0.35,0.30,0.20])
        )

data["hour_of_alarm"] = alarm

# ----------------------------
# Previous snooze history
# Depends on sleep
# ----------------------------

base = np.random.poisson(1.2,N)

extra = (
    (7-data["sleep_duration_prev_night"])
    .clip(lower=0)
    .astype(int)
)

data["snooze_count_last_7_days"] = np.clip(
    base+extra,
    0,
    10
)

# ----------------------------
# User personality
# Some people naturally snooze more
# ----------------------------

user_bias = np.random.normal(0,0.6,500)

data["user_bias"] = (
    data["user_id"]
    .apply(lambda x:user_bias[x-1])
)

# ----------------------------
# Random human behaviour
# ----------------------------

noise = np.random.normal(0,0.5,N)

# ----------------------------
# Behaviour model
# ----------------------------

logit = (

    -0.1

    +0.45*(7-data["sleep_duration_prev_night"])

    +0.40*data["snooze_count_last_7_days"]

    +0.35*(8-data["hour_of_alarm"])

    -0.22*data["study_importance"]

    +0.65*data["is_weekend"]

    +data["user_bias"]

    +noise
)

data["snooze_probability"] = sigmoid(logit)

data["did_snooze"] = np.random.binomial(
    1,
    data["snooze_probability"]
)

# Remove hidden columns
data.drop(columns=["user_bias","is_weekend"], inplace=True)

data.to_csv(
    "synthetic_snoozedata.csv",
    index=False
)

#print(data["did_snooze"].value_counts())