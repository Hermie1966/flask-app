from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my Flask app!"

@app.route("/hello")
def hello():
    return "Hello from Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
