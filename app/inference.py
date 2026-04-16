import joblib
import pandas as pd
import numpy as np

# Load model and scaler
# Make sure to update paths to absolute or relative to where main.py runs
MODEL_PATH = "../model/advanced_model.pkl"
SCALER_PATH = "../model/scaler.pkl"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"Warning: Model or scaler could not be loaded. {e}")
    model = None
    scaler = None

# Expected features based on the CICIDS dataset used in advanced_pipeline.py
# Extracted from Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv and stripped
RAW_COLUMNS = " Destination Port, Flow Duration, Total Fwd Packets, Total Backward Packets,Total Length of Fwd Packets, Total Length of Bwd Packets, Fwd Packet Length Max, Fwd Packet Length Min, Fwd Packet Length Mean, Fwd Packet Length Std,Bwd Packet Length Max, Bwd Packet Length Min, Bwd Packet Length Mean, Bwd Packet Length Std,Flow Bytes/s, Flow Packets/s, Flow IAT Mean, Flow IAT Std, Flow IAT Max, Flow IAT Min,Fwd IAT Total, Fwd IAT Mean, Fwd IAT Std, Fwd IAT Max, Fwd IAT Min,Bwd IAT Total, Bwd IAT Mean, Bwd IAT Std, Bwd IAT Max, Bwd IAT Min,Fwd PSH Flags, Bwd PSH Flags, Fwd URG Flags, Bwd URG Flags, Fwd Header Length, Bwd Header Length,Fwd Packets/s, Bwd Packets/s, Min Packet Length, Max Packet Length, Packet Length Mean, Packet Length Std, Packet Length Variance,FIN Flag Count, SYN Flag Count, RST Flag Count, PSH Flag Count, ACK Flag Count, URG Flag Count, CWE Flag Count, ECE Flag Count, Down/Up Ratio, Average Packet Size, Avg Fwd Segment Size, Avg Bwd Segment Size, Fwd Header Length,Fwd Avg Bytes/Bulk, Fwd Avg Packets/Bulk, Fwd Avg Bulk Rate, Bwd Avg Bytes/Bulk, Bwd Avg Packets/Bulk,Bwd Avg Bulk Rate,Subflow Fwd Packets, Subflow Fwd Bytes, Subflow Bwd Packets, Subflow Bwd Bytes,Init_Win_bytes_forward, Init_Win_bytes_backward, act_data_pkt_fwd, min_seg_size_forward,Active Mean, Active Std, Active Max, Active Min,Idle Mean, Idle Std, Idle Max, Idle Min"
EXPECTED_FEATURES = [c.strip() for c in RAW_COLUMNS.split(',')]

def predict_threat(data_dict: dict) -> dict:
    """
    Takes a dictionary representing a network packet/flow,
    formats it, scales it, and returns the prediction.
    """
    if not model or not scaler:
        return {"error": "Model or scaler not loaded properly."}

    # Ensure all expected features are present (fill missing with 0)
    # and in the exact correct order
    feature_vector = []
    for feature in EXPECTED_FEATURES:
        feature_vector.append(float(data_dict.get(feature, 0.0)))
    
    # Convert to 2D array
    X = np.array(feature_vector).reshape(1, -1)
    
    # Scale
    X_scaled = scaler.transform(X)
    
    # Predict (0 = BENIGN, 1 = Attack)
    prediction = int(model.predict(X_scaled)[0])
    
    # Get probability if available
    try:
        probabilities = model.predict_proba(X_scaled)[0]
        confidence = float(max(probabilities))
    except (AttributeError, IndexError):
        confidence = 1.0
        
    return {
        "prediction": prediction,
        "label": "BENIGN" if prediction == 0 else "ATTACK",
        "confidence": confidence
    }

def generate_mock_traffic() -> dict:
    """
    Generates a single randomized mock traffic payload for the dashboard simulator.
    Mostly generates benign traffic with occasional simulated attacks.
    """
    import random
    is_attack = random.random() < 0.15 # 15% chance of anomalous traffic
    
    mock_data = {}
    for feature in EXPECTED_FEATURES:
        if is_attack and feature in ["Total Length of Fwd Packets", "Flow Duration", "Packet Length Mean"]:
            # Inject extreme values
            mock_data[feature] = random.uniform(10000, 1000000)
        else:
            # Normalish values
            mock_data[feature] = random.uniform(0, 1000)
            
    # Include some raw metadata for the UI to display neatly
    ui_metadata = {
        "source_ip": f"192.168.1.{random.randint(1, 255)}",
        "dest_ip": f"10.0.{random.randint(0, 5)}.{random.randint(1, 255)}",
        "protocol": random.choice(["TCP", "UDP", "HTTP", "HTTPS"]),
        "port": random.randint(1024, 65535) if random.random() > 0.5 else random.choice([80, 443, 22, 21, 53])
    }
    
    mock_data.update(ui_metadata)
    return mock_data
