# 🛡️ ShieldAI — AI-Powered Intrusion Detection System

> **Real-time Network Anomaly Detection powered by Machine Learning**

A production-ready, enterprise-grade Threat Intelligence Platform that uses a trained **Random Forest** classifier to detect malicious network traffic in real time. Features a sleek glassmorphic web dashboard, a fully async REST API, and an ML inference pipeline trained on the **CICIDS** benchmark dataset.

---

## 📸 Preview

The dashboard streams live packet classifications in real time — each row is a network flow analyzed by the ML model in milliseconds.

```
ShieldAI | Threat Intelligence Platform
         | Real-time Network Anomaly Detection
──────────────────────────────────────────────────────────────
 Total Analyzed   │  Threats Blocked  │  Active Models  │  Status
   473,650        │      794 🔴        │       1         │  Secure ✅
──────────────────────────────────────────────────────────────
 Time     │ Source IP      │ Dest IP      │ Protocol │ Conf.  │ Label
 15:24:47 │ 192.168.1.30   │ 10.0.2.9     │ UDP/9267  │ 71.5%  │ BENIGN
 15:24:46 │ 192.168.1.240  │ 10.0.1.57    │ UDP/59230 │ 86.5%  │ BENIGN
 15:24:45 │ 192.168.1.27   │ 10.0.5.83    │ TCP/80    │ 84.0%  │ ATTACK 🔴
```

---

## 📁 Project Structure

```
AI-IDS/
├── app/                          # FastAPI web application
│   ├── main.py                   # API routes & app entry point
│   ├── inference.py              # ML model loading & prediction logic
│   ├── templates/
│   │   └── index.html            # Glassmorphic dashboard UI
│   └── static/
│       ├── css/style.css         # Dark-mode glassmorphism styles
│       └── js/main.js            # Live streaming & dashboard logic
│
├── model/                        # Trained ML artifacts
│   ├── advanced_model.pkl        # Primary RandomForest model (CICIDS)
│   ├── scaler.pkl                # StandardScaler for feature normalization
│   ├── cicids_model.pkl          # Alternate CICIDS-only model
│   ├── combined_model.pkl        # Multi-dataset combined model
│   ├── ids_model.pkl             # Basic IDS model
│   ├── universal_model.pkl       # Universal multi-class model
│   └── universal_scaler.pkl      # Scaler for universal model
│
├── Data/                         # CICIDS dataset CSVs (not included in repo)
├── advanced_pipeline.py          # Model training script (primary)
├── train_cicids.py               # Alternate training pipeline
├── testing.py                    # Model testing & evaluation script
├── test_cicids.py                # CICIDS-specific test script
├── universal.py                  # Universal model training
├── load_data.py                  # Dataset loading utilities
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | FastAPI (async) + Uvicorn |
| **ML Inference** | Scikit-learn (RandomForestClassifier) |
| **Data Processing** | Pandas, NumPy |
| **Frontend** | Vanilla HTML/CSS/JS (Glassmorphism design) |
| **Templating** | Jinja2 |
| **Model Persistence** | Joblib |
| **Dataset** | CICIDS 2017 (Canadian Institute for Cybersecurity) |

---

## 🚀 Getting Started

### 1. Prerequisites

- Python **3.9+**
- pip

### 2. Install Dependencies

```bash
pip install fastapi uvicorn scikit-learn pandas numpy joblib jinja2 python-multipart
```

### 3. Run the Server

```bash
cd app
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Open the Dashboard

```
http://localhost:8000
```

The dashboard will immediately begin streaming live simulated traffic through the ML model.

---

## 🌐 API Reference

Base URL: `http://localhost:8000`

### Interactive Docs

Full Swagger UI available at:
```
http://localhost:8000/docs
```

---

### `GET /`
**Serve Dashboard**

Returns the glassmorphic ShieldAI web dashboard.

---

### `GET /api/stream`
**Stream Simulated Traffic**

Generates a randomized mock network flow, classifies it with the ML model, and returns the result. Designed to be polled by the frontend every second to simulate live traffic.

**Response:**
```json
{
  "packet": {
    "source_ip": "192.168.1.147",
    "dest_ip": "10.0.3.92",
    "protocol": "TCP",
    "port": 443,
    "Flow Duration": 512.4,
    "..."
  },
  "analysis": {
    "prediction": 0,
    "label": "BENIGN",
    "confidence": 0.865
  }
}
```

---

### `POST /api/predict`
**Analyze Custom Traffic**

Submit your own network flow feature vector for classification.

**Request Body:**
```json
{
  "data": {
    "Destination Port": 80,
    "Flow Duration": 1234,
    "Total Fwd Packets": 5,
    "Total Backward Packets": 3,
    "..."
  }
}
```

**Response:**
```json
{
  "prediction": 1,
  "label": "ATTACK",
  "confidence": 0.91
}
```

> **Note:** Missing features default to `0.0`. For accurate results, provide the complete 78-feature CICIDS vector.

---

### `GET /api/stats`
**Get System Statistics**

Returns high-level platform metrics shown in the dashboard header.

**Response:**
```json
{
  "total_analyzed": 342817,
  "threats_blocked": 614,
  "active_models": 1,
  "system_status": "Secure"
}
```

---

## 🧠 ML Pipeline

### Dataset
Trained on the **CICIDS 2017** dataset from the Canadian Institute for Cybersecurity — a widely used intrusion detection benchmark containing:

- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` — DDoS attacks
- `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv` — Web attacks (SQLi, XSS, Brute Force)
- `Wednesday-workingHours.pcap_ISCX.csv` — Mixed benign + attack traffic

### Feature Engineering
- 78 network flow features extracted (packet lengths, inter-arrival times, flags, byte rates, etc.)
- Binary label encoding: `BENIGN → 0`, everything else → `1`
- `StandardScaler` for feature normalization

### Model
```
RandomForestClassifier(
    n_estimators = 200,
    max_depth    = None,   # full trees
    n_jobs       = -1,     # all CPU cores
    random_state = 42
)
```

### Retraining the Model

Place CICIDS CSV files in the `Data/` directory, then run:

```bash
python advanced_pipeline.py
```

Trained artifacts are saved to `model/advanced_model.pkl` and `model/scaler.pkl`.

---

## 🔍 Input Features (CICIDS 78-Feature Vector)

The model expects the following network flow features (column names must match exactly):

<details>
<summary>Click to expand full feature list</summary>

```
Destination Port, Flow Duration, Total Fwd Packets, Total Backward Packets,
Total Length of Fwd Packets, Total Length of Bwd Packets,
Fwd Packet Length Max, Fwd Packet Length Min, Fwd Packet Length Mean, Fwd Packet Length Std,
Bwd Packet Length Max, Bwd Packet Length Min, Bwd Packet Length Mean, Bwd Packet Length Std,
Flow Bytes/s, Flow Packets/s, Flow IAT Mean, Flow IAT Std, Flow IAT Max, Flow IAT Min,
Fwd IAT Total, Fwd IAT Mean, Fwd IAT Std, Fwd IAT Max, Fwd IAT Min,
Bwd IAT Total, Bwd IAT Mean, Bwd IAT Std, Bwd IAT Max, Bwd IAT Min,
Fwd PSH Flags, Bwd PSH Flags, Fwd URG Flags, Bwd URG Flags,
Fwd Header Length, Bwd Header Length, Fwd Packets/s, Bwd Packets/s,
Min Packet Length, Max Packet Length, Packet Length Mean, Packet Length Std, Packet Length Variance,
FIN Flag Count, SYN Flag Count, RST Flag Count, PSH Flag Count, ACK Flag Count,
URG Flag Count, CWE Flag Count, ECE Flag Count, Down/Up Ratio,
Average Packet Size, Avg Fwd Segment Size, Avg Bwd Segment Size, Fwd Header Length,
Fwd Avg Bytes/Bulk, Fwd Avg Packets/Bulk, Fwd Avg Bulk Rate,
Bwd Avg Bytes/Bulk, Bwd Avg Packets/Bulk, Bwd Avg Bulk Rate,
Subflow Fwd Packets, Subflow Fwd Bytes, Subflow Bwd Packets, Subflow Bwd Bytes,
Init_Win_bytes_forward, Init_Win_bytes_backward, act_data_pkt_fwd, min_seg_size_forward,
Active Mean, Active Std, Active Max, Active Min,
Idle Mean, Idle Std, Idle Max, Idle Min
```

</details>

---

## 🧪 Testing

### Test the live stream endpoint
```bash
curl http://localhost:8000/api/stream
```

### Test a custom prediction
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": {"Destination Port": 22, "Flow Duration": 999999, "Total Fwd Packets": 1000}}'
```

### Run the model evaluation script
```bash
python testing.py
```

---

## ⚠️ Known Issues

| Issue | Details |
|---|---|
| `InconsistentVersionWarning` | Model was saved with sklearn 1.8.x; predictions still work on 1.7.x but retrain to eliminate the warning |
| CICIDS data not included | Due to file size (~1GB+), dataset CSVs must be downloaded separately from [UNB CICIDS 2017](https://www.unb.ca/cic/datasets/ids-2017.html) |

---

## 📄 License

This project is for educational and research purposes. Dataset usage is subject to the [CICIDS 2017 Terms of Use](https://www.unb.ca/cic/datasets/ids-2017.html).

---

## 👤 Author

Built as an AI-powered security research project demonstrating real-time network intrusion detection using production-grade ML pipelines and modern web interfaces.
