# data_handler.py - A module for handling fitness data operations

import pandas as pd 
from statistics import mean
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserMetrics

# Function to save user data
def save_user_data(user_id, user_metrics, db : Session):
    user_metrics_entry = UserMetrics(user_id=user_id, **user_metrics)
    db.add(user_metrics_entry)
    db.commit()

# Function to get user data
def get_user_data(user_id, db: Session):
    user_metrics = db.query(UserMetrics).filter(UserMetrics.user_id == user_id).all()
    if not user_metrics:
        return None
    return pd.DataFrame([metric.to_dict() for metric in user_metrics])


# Function to analyze user data and generate feedback
def analyze_user_data(user_metrics_df):
    avg_left_back = mean(user_metrics_df['left_back'])
    avg_right_back = mean(user_metrics_df['right_back'])
    avg_left_leg = mean(user_metrics_df['left_leg'])
    avg_right_leg = mean(user_metrics_df['right_leg'])

    avg_back = mean([avg_left_back, avg_right_back])
    avg_leg = mean([avg_left_leg, avg_right_leg])

    avg_total_left = avg_left_back + avg_left_leg
    avg_total_right = avg_right_back + avg_right_leg
    
    feedback = {
        "back_pressure": f"You are averaging {avg_back} units of pressure on your back.",
        "leg_pressure": f"You are averaging {avg_leg} units of pressure on your legs.",
        "left_vs_right": f"You are averaging {avg_total_left} units of pressure on your left side vs {avg_total_right} units of pressure on your rightside"
    }
    
    return feedback

