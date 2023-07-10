from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import random, time

app = Flask(__name__)

REQ  = Counter("service_requests_total", "Requests handled", ["status"])
LAT  = Histogram("request_latency_seconds", "Request latency", ["endpoint"])

@app.route("/api/v1/items", methods=["POST"])
@LAT.labels("/api/v1/items").time()
def create_item():
    if random.random() < 0.93:
        REQ.labels("success").inc()
        return jsonify(msg="stored"), 201
    REQ.labels("failed").inc()
    return jsonify(error="db busy"), 503

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
