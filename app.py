import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my Flask app!"

@app.route("/hello")
def hello():
    return "Hello from Render!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # Get JSON data from TradingView
    print("Received Webhook Data:", data)  # Log it for debugging

    if not data:
        return jsonify({"error": "No data received"}), 400

    # Extract specific data (modify based on your TradingView alert setup)
    alert_message = data.get("message", "No message provided")

    # Process the alert (Here, we simply print it)
    print(f"TradingView Alert: {alert_message}")

    # Respond back to TradingView
    return jsonify({"status": "success", "message": "Webhook received!"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port, default to 10000
    app.run(host="0.0.0.0", port=port)
