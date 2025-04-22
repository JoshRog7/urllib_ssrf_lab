from flask import Flask, request
import urllib.request

app = Flask(__name__)

@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    if not url:
        return "Missing URL parameter", 400

    try:
        with urllib.request.urlopen(url) as response:
            return response.read(), 200
    except Exception as e:
        return f"Request failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
