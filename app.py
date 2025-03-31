from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Flask app p ning successfully on Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import request, jsonify

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json  # Receive JSON data from TradingView
        print("Received data:", data)  # Print it in the Render logs for debugging

        # 🚀 Do something with the data (e.g., send to cTrader, process signals)
        
        return jsonify({"status": "success", "message": "Webhook received!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
