from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
from analysis_engine.rules import check_rules
from analysis_engine.predictor import predict_ml
import sys

app = Flask(__name__)
CORS(app) 

@app.route("/")
def home():
    return "Hello! This is the DApp Phishing Analysis API."

@app.route("/analyze", methods=["POST"])
def analyze_transaction():
    try:
        data = request.json
        transaction_hash = data.get("transaction_hash")

        if not transaction_hash:
            return jsonify({"error": "No transaction_hash provided"}), 400
        
        print(f"--- Received request to analyze: {transaction_hash} ---", file=sys.stderr)

        rule_result = check_rules(transaction_hash)
        
        if rule_result:
            print(f"Result (Rule-Based): PHISHING", file=sys.stderr)
            return jsonify(rule_result)

        ml_result = predict_ml(transaction_hash)
        
        print(f"Result (ML-Model): {ml_result.get('status')}", file=sys.stderr)
        return jsonify(ml_result)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Runs on http://127.0.0.1:5000
    app.run(debug=True, port=5000)