# app.py
from flask import Flask, request, jsonify
import joblib
import numpy as np
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

MODEL_PATH = os.environ.get('MODEL_PATH', 'model.joblib')
model_bundle = joblib.load(MODEL_PATH)
model = model_bundle['model']
columns = model_bundle['columns']

app = Flask(__name__)

PRED_COUNTER = Counter('app_predictions_total', 'Number of predictions', ['result'])

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/predict", methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error":"JSON body required"}), 400
    if isinstance(data, dict):
        if 'features' in data:
            X = np.array(data['features']).reshape(1, -1)
        else:
            X = np.array([data.get(c, 0) for c in columns]).reshape(1, -1)
    else:
        return jsonify({"error":"Invalid JSON format"}), 400

    pred = model.predict(X)[0]
    PRED_COUNTER.labels(result=str(int(pred))).inc()
    return jsonify({'prediction': int(pred)})

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
