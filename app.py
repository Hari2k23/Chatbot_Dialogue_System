from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
import random

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("Hotel Reservations.csv")

# Convert all column names to lowercase to avoid case mismatch errors
df.columns = df.columns.str.lower()

# Print column names to verify (optional debug step)
print("Column names in dataset:", df.columns)

# Sample general responses
general_responses = [
    "I'm here to help with hotel bookings! Ask me anything.",
    "Can I help you find a hotel?",
    "Tell me your travel details, and I'll find the best hotel for you!"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Extract JSON data
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message key missing"}), 400

    user_message = data["message"].strip().lower()

    # 1️⃣ Handle Booking Start
    if "book hotel" in user_message:
        return jsonify({"bot_response": "How many adults and kids are staying? Example: '2 adults, 1 kid'."})

    # 2️⃣ Extract adults and children count from user input
    match = re.search(r"(\d+)\s*adults?.*?(\d+)?\s*kid", user_message)
    if match:
        try:
            adults = int(match.group(1))
            kids = int(match.group(2)) if match.group(2) else 0  # Handle missing kids count

            # Ensure correct column names
            adult_col = "no_of_adults"
            kid_col = "no_of_children"
            status_col = "booking_status"  # 'Confirmed' means available in dataset

            # Check room availability
            available_rooms = df[
                (df[adult_col] >= adults) & 
                (df[kid_col] >= kids) & 
                (df[status_col] == "Confirmed")
            ]

            if not available_rooms.empty:
                return jsonify({"bot_response": f"Rooms are available for {adults} adults and {kids} kids!"})
            else:
                return jsonify({"bot_response": "Sorry, no rooms available for the given criteria."})
        except Exception as e:
            return jsonify({"bot_response": f"Error processing request: {str(e)}"})

    # 3️⃣ General chat response (like ChatGPT)
    return jsonify({"bot_response": random.choice(general_responses)})

if __name__ == "__main__":
    app.run(debug=True)
