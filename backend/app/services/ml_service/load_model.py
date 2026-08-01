import joblib
from fastapi import HTTPException

model_version='1.0'
try:
 #load model
 focus_score_model=joblib.load("app/services/ml_service/ml_models/focus_score_pred_model.pkl")
 focus_score_Features=joblib.load("app/services/ml_service/ml_models/focusscore_model_feature.pkl")

 snooze_risk_model=joblib.load("app/services/ml_service/ml_models/snooze_risk_pred_model.pkl")
 snooze_risk_Features=joblib.load("app/services/ml_service/ml_models/snooze_model_feature.pkl")

 print("model loaded successfully✔")
except Exception as e:
  raise HTTPException(status_code=500,detail=f"Error:{str(e)}")

def predict_focus(encoded_df):
  prediction = focus_score_model.predict(encoded_df)[0]
  return prediction           

def predict_snooze_risk(encoded_df):
    prediction = int(snooze_risk_model.predict(encoded_df)[0])
    probability=float(snooze_risk_model.predict_proba(encoded_df)[0][1])
           
    return prediction ,probability         
     