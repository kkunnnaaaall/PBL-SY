import joblib
import os
import numpy as np
from .blockchain_fetcher import get_transaction_data

# --- Load the trained Model and Scaler ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'model', 'phishing_classifier.pkl')
SCALER_PATH = os.path.join(BASE_DIR, '..', 'model', 'feature_scaler.pkl')

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("ML model and scaler loaded successfully.")
except FileNotFoundError:
    print(f"WARNING: Model/Scaler not found. Did you run the model_trainer.ipynb?")
    model = None
    scaler = None

def predict_ml(txn_hash: str) -> dict:
    """
    Analyzes a transaction using the trained ML model.
    """
    if not model or not scaler:
        return {"status": "ERROR", "reason": "ML model is not loaded. Run trainer."}

    # 1. Get the real transaction data
    data = get_transaction_data(txn_hash)

    if not data or data.get("error"):
        return {"status": "ERROR", "reason": data.get("error", "Failed to fetch data")}
    
    try:
        # 2. --- Feature Engineering ---
        features_list = [
            data['Value'],
            data['input_data_length'],
            data['is_contract_interaction']
        ]
        
        features_array = np.array(features_list).reshape(1, -1)
        
        # 3. --- Scale the Features ---
        features_scaled = scaler.transform(features_array)

        # 4. --- Make Prediction ---
        prediction = model.predict(features_scaled)
        probability = model.predict_proba(features_scaled)[0]

        print(f"ML Prediction: {prediction[0]}, Confidence: {max(probability)}")

        # 5. --- Return Result ---
        if prediction[0] == 1: # 1 = Phishing
            return {
                "status": "PHISHING",
                "reason": f"Transaction flagged by ML model (Confidence: {max(probability)*100:.0f}%)"
            }
        else: # 0 = Safe
            # --- THIS IS THE PART TO CHECK ---
            # Make sure you have this "reason" line!
            return {
                "status": "SAFE",
                "reason": f"Transaction passed ML model checks (Confidence: {max(probability)*100:.0f}%)"
            }
            # ---------------------------------
            
    except Exception as e:
        print(f"Error during ML prediction: {e}")
        return {"status": "ERROR", "reason": f"ML prediction error: {e}"}