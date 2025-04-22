from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Internal API: You shouldn’t be here via SSRF!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
