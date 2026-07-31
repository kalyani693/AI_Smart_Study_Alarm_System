import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,root_mean_squared_error,mean_absolute_percentage_error
import pickle

data=pd.read_csv("synthetic_snoozedata.csv")
model=LinearRegression()

#our data does not have any misssing values or null values, so we can proceed to split the data into features and target variable.
# all columns of features are already scaled to between(1 to 10) 
features=data.drop(columns=["user_id","snoozed","snooze_probability"])

def scale_snooze_probability(x):
    return x*10

target=np.array(data["snooze_probability"].apply(scale_snooze_probability))

xtrain,xtest,ytrain,ytest=train_test_split(features,target,test_size=0.2,random_state=42)

model.fit(xtrain,ytrain)

y_pred=model.predict(xtest)

"""print("MAE:",mean_absolute_error(ytest,y_pred))# 0.6792
print("MAPE:",mean_absolute_percentage_error(ytest,y_pred))#0.1432  error is less
print("RMSE:",root_mean_squared_error(ytest,y_pred))#0.8334"""

#save model and features
#print(xtrain.columns.tolist())#->['sleep_duration', 'sleep_quality', 'fatigue_level', 'previous_snooze_count', 'study_importance', 'days_since_last_study', 'alarm_hour']

with open("snooze_risk_pred_model.pkl","wb") as f:
   pickle.dump(model,f)
with open("snooze_model_feature.pkl","wb") as f:
   pickle.dump(xtrain.columns.tolist(),f)





