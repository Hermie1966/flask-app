import requests
import os
import json  # Reintroduced json for manual serialization
from flask import Flask, request, jsonify

app = Flask(__name__)

# cTrader API credentials (Replace with actual values)
CTRADER_API_URL = "https://demo.ctraderapi.com"  # Change if using demo account
CLIENT_ID = "13918_qwV1AwAgoM9vfyfvQIREM0aIC4okHaEInWfMoR7SKrswBjoiCM"  # From cTrader API portal
CLIENT_SECRET = "Eskh10o1mQbLON1qfZMgCA6k12vGo8SDPDIH8aafkHM4OxtSv8"  # From cTrader API portal
ACCESS_TOKEN = "bxV0JrVz5gY9yWZxsZaqAAdRwHuFI9O_o4Cxvt87p1w"  # Required for authentication
ACCOUNT_ID = "4193313"  # Specifies which trading account to use

def get_account_balance():
    """Fetch account balance from cTrader API."""
    balance_url = f"{CTRADER_API_URL}/accounts/{ACCOUNT_ID}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(balance_url, headers=headers)

    if response.status_code == 200:
        account_info = response.json()
        return account_info.get("balance", 0)  # Return balance, default to 0
    else:
        print(f"Error fetching balance: {response.text}")
        return 0  # Fallback if API call fails

@app.route("/webhook", methods=["POST"])
def webhook():
    """Receives TradingView alerts and places cTrader trades."""
    data = request.json
    print("Received Webhook Data:", data)

    if not data:
        return jsonify({"error": "No data received"}), 400

    # Extract trade details
    ticker = data.get("ticker", "EURUSD")  # Default: EUR/USD
    order_type = data.get("order_type", "market")  # 'market' or 'limit'
    direction = data.get("direction", "buy")  # 'buy' or 'sell'
    price = data.get("price", None)  # Only needed for limit orders

    # Get account balance and trade 100% of it
    account_balance = get_account_balance()
    volume = int(account_balance)  # Trade with full balance

    # Construct order data
    order_data = {
        "accountId": ACCOUNT_ID,
        "ticker": ticker,
        "orderType": order_type.upper(),  # MARKET or LIMIT
        "volume": volume,
        "direction": direction.upper(),  # BUY or SELL
        "price": price if order_type.lower() == "limit" else None  # Only for limit orders
    }

    # Send request to cTrader API
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",  # f-string used here
        "Content-Type": "application/json"
    }

    order_url = f"{CTRADER_API_URL}/orders"
    response = requests.post(order_url, json=order_data, headers=headers)

    if response.status_code == 201:
        return jsonify({"status": "success", "message": "Trade executed successfully!"}), 200
    else:
        return jsonify({"status": "error", "message": response.text}), response.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
