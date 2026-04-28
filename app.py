from flask import Flask, render_template, request, jsonify
import os
import requests  # since you're using it

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Example API route (optional - keep if you use requests)
@app.route("/api", methods=["GET"])
def api_call():
    try:
        response = requests.get("https://api.github.com")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)})


# IMPORTANT: Render compatibility
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )