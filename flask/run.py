# Imports
from flask import Flask, jsonify
from flask_cors import CORS

# App

app = Flask(__name__)
CORS(app)

# Routes

@app.route("/")
def init():
    return jsonify('Initializing')

# Setup

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
