import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Load the trained model and encoders
model = joblib.load("hotel_booking_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

app = Flask(__name__)

@app.route("/")
def home():
    return "Hotel Booking Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.json

        # Convert data to DataFrame
        df = pd.DataFrame([data])

        # Encode categorical features
        categorical_cols = ['type_of_meal_plan', 'room_type_reserved', 'market_segment_type']
        for col in categorical_cols:
            if col in df:
                df[col] = label_encoders[col].transform(df[col])

        # Make a prediction
        prediction = model.predict(df)[0]
        
        return jsonify({"prediction": "Canceled" if prediction == 1 else "Not Canceled"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
