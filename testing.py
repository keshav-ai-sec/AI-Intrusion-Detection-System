import pandas as pd
import joblib

# -----------------------------
# LOAD MODEL + SCALER
# -----------------------------
model = joblib.load("model/universal_model.pkl")
scaler = joblib.load("model/universal_scaler.pkl")

# -----------------------------
# LOAD UNSW DATASET WITH HEADERS
# -----------------------------
file_name = "Data/UNSW-NB15_1.csv"

columns = [
    "srcip","sport","dstip","dsport","proto","state","dur",
    "sbytes","dbytes","sttl","dttl","sloss","dloss","service",
    "Sload","Dload","Spkts","Dpkts","swin","dwin","stcpb","dtcpb",
    "smeansz","dmeansz","trans_depth","res_bdy_len","Sjit","Djit",
    "Stime","Ltime","Sintpkt","Dintpkt","tcprtt","synack","ackdat",
    "is_sm_ips_ports","ct_state_ttl","ct_flw_http_mthd","is_ftp_login",
    "ct_ftp_cmd","ct_srv_src","ct_srv_dst","ct_dst_ltm","ct_src_ltm",
    "ct_src_dport_ltm","ct_dst_sport_ltm","ct_dst_src_ltm","label"
]

df = pd.read_csv(file_name, names=columns, low_memory=False)

print("Testing on:", file_name)
print("Original shape:", df.shape)

# -----------------------------
# CLEAN DATA
# -----------------------------
df.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
df.dropna(inplace=True)

print("After cleaning:", df.shape)

# -----------------------------
# FEATURE MAPPING (UNSW → COMMON)
# -----------------------------
mapped = pd.DataFrame({
    "duration": df["dur"],
    "packet_count": df["Spkts"] + df["Dpkts"],
    "byte_count": df["sbytes"] + df["dbytes"],
    "packet_rate": df["Sload"],
    "byte_rate": df["sbytes"],
    "packet_size_mean": df["smeansz"],
    "packet_size_max": df["dmeansz"]
})

# -----------------------------
# FINAL CLEAN
# -----------------------------
mapped.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
mapped.dropna(inplace=True)

print("Mapped shape:", mapped.shape)

# -----------------------------
# SCALE
# -----------------------------
X_scaled = scaler.transform(mapped)

# -----------------------------
# PREDICT
# -----------------------------
predictions = model.predict(X_scaled)

print("\nSample predictions:", predictions[:20])

# -----------------------------
# (OPTIONAL) CHECK DISTRIBUTION
# -----------------------------
import numpy as np

unique, counts = np.unique(predictions, return_counts=True)

print("\nPrediction Distribution:")
for u, c in zip(unique, counts):
    print(f"{'Normal' if u == 0 else 'Attack'}: {c}")
