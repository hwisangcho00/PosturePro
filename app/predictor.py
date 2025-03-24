import pandas as pd
import joblib

model = joblib.load('ml_model/posture_classifier.pkl')

def predict_posture(input_data):
    """
    Predicts the posture classification based on input data.
    :param input_data: DataFrame containing the input features.
    :return: Predicted class label.
    """
    # turn input_data (initially json) into a dataframe
    prediction = model.predict(input_data)
    return prediction
