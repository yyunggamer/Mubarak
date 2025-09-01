from flask import Flask, jsonify

# Create Flask app instance
app = Flask(__name__)

# Root endpoint
@app.route("/")
def home():
    return jsonify(message="Hello from Flask running in an Alpine-based Docker container!")

# Another example endpoint
@app.route("/health")
def health():
    return jsonify(status="OK", container="alpine_python")

if __name__ == "__main__":
    # Run the app on host 0.0.0.0 (so Docker can expose it), port 8000
    app.run(host="0.0.0.0", port=8000)
