import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,confusion_matrix
import pickle

data=pd.read_csv("synthetic_snoozedata.csv")
model=LogisticRegression()

#our data does not have any misssing values or null values, so we can proceed to split the data into features and target variable.
# all columns of features are already scaled to between(1 to 10) 

#Encode column day_of_week
replace_val={
    True:1,
    False:0
}
encoded_df=pd.get_dummies(data,columns=["day_of_week"]).replace(replace_val)

features=encoded_df.drop(columns=["user_id","did_snooze","snooze_probability"])
target=np.array(data["did_snooze"])


xtrain,xtest,ytrain,ytest=train_test_split(features,target,test_size=0.2,random_state=42)

model.fit(xtrain,ytrain)

y_pred=model.predict(xtest)

"""print("Classification Report:")
print(classification_report(ytest,y_pred))
print("Confusion Matrix:")
print(confusion_matrix(ytest,y_pred))"""

#save model and features
#print(xtrain.columns.tolist())#->['study_importance', 'sleep_duration_prev_night', 'hour_of_alarm', 
# 'snooze_count_last_7_days', 'day_of_week_Friday', 'day_of_week_Monday', 'day_of_week_Saturday', 'day_of_week_Sunday',
#  'day_of_week_Thursday', 'day_of_week_Tuesday', 'day_of_week_Wednesday']

with open("snooze_risk_pred_model.pkl","wb") as f:
   pickle.dump(model,f)
with open("snooze_model_feature.pkl","wb") as f:
   pickle.dump(xtrain.columns.tolist(),f)





