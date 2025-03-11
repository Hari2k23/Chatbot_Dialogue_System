from flask import Flask, render_template, request, jsonify
import joblib  # For loading the chatbot model
import pandas as pd  # If needed for processing
import random  # For simple responses (replace with ML model if available)

app = Flask(__name__)

# Load your trained chatbot model (modify as needed)
try:
    model = joblib.load("chatbot_model.pkl")  # Update with your actual model file
except:
    model = None  # Handle case where the model is not found

# Example response function (Replace with your model's response logic)
def get_chatbot_response(user_input):
    responses = ["Hello! How can I help you?", "I'm here to assist you.", "Tell me more about your query."]
    return random.choice(responses)

# Serve the HTML page
@app.route("/")
def home():
    return render_template("index.html")

# Handle chatbot requests
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    
    if model:
        # If using an ML model, process input and generate response
        response = model.predict([user_message])[0]
    else:
        response = get_chatbot_response(user_message)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
