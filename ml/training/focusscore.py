import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error,mean_absolute_error,root_mean_squared_error
import pickle



#load data
data=pd.read_csv("synthetic_focusscore_data.csv")
#print(data.head())

#No missing values or null values due synthetic data generation

#Encode column time_of_day, subject_type, day_of_week
replace_val={
    True:1,
    False:0
}
encoded_df=pd.get_dummies(data,columns=["time_of_day","subject_type","day_of_week"]).replace(replace_val)
#print(encoded_df.head())

#split into features and target column
features=encoded_df.drop(columns=["Normalized_focus_Score"])

target=encoded_df["Normalized_focus_Score"]

#spliting
xtrain,xtest,ytarin,ytest=train_test_split(features,target,test_size=0.2,random_state=42)

#print(xtrain)



model=LinearRegression()
model.fit(xtrain,ytarin)


y_pred=model.predict(xtest)

print("MAPE:",mean_absolute_percentage_error(ytest,y_pred))#0.079 which is far good, value closser to 0.0 means mini error in prediction

#save model
with open("focus_score_pred_model.pkl","wb") as f:
   pickle.dump(model,f)
with open("focusscore_model_feature.pkl","wb") as f:
   pickle.dump(xtrain.columns.tolist(),f)







