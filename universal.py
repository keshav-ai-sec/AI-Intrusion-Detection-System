import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# -----------------------------
# CICIDS MAPPING
# -----------------------------
def map_cicids(df):
    df.columns = df.columns.str.strip()
   
    df.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
    df.dropna(inplace=True)
   
    mapped = pd.DataFrame({
        "duration": df["Flow Duration"],
        "packet_count": df["Total Fwd Packets"] + df["Total Backward Packets"],
        "byte_count": df["Total Length of Fwd Packets"] + df["Total Length of Bwd Packets"],
        "packet_rate": df["Flow Packets/s"],
        "byte_rate": df["Flow Bytes/s"],
        "packet_size_mean": df["Packet Length Mean"],
        "packet_size_max": df["Max Packet Length"],
        "label": df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)
    })
   
    return mapped


# -----------------------------
# NSL-KDD MAPPING
# -----------------------------
def map_kdd(df):
    columns = [
        "duration","protocol_type","service","flag","src_bytes","dst_bytes",
        "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
        "num_compromised","root_shell","su_attempted","num_root",
        "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
        "is_host_login","is_guest_login","count","srv_count","serror_rate",
        "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
        "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
        "dst_host_same_srv_rate","dst_host_diff_srv_rate",
        "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
        "dst_host_serror_rate","dst_host_srv_serror_rate",
        "dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"
    ]
   
    df.columns = columns
   
    mapped = pd.DataFrame({
        "duration": df["duration"],
        "packet_count": df["count"],
        "byte_count": df["src_bytes"] + df["dst_bytes"],
        "packet_rate": df["srv_count"],
        "byte_rate": df["same_srv_rate"],
        "packet_size_mean": df["dst_host_same_srv_rate"],
        "packet_size_max": df["dst_host_srv_count"],
        "label": df["label"].apply(lambda x: 0 if x == "normal" else 1)
    })
   
    return mapped


# -----------------------------
# UNSW MAPPING (Simplified)
# -----------------------------
def map_unsw(df):
    df.columns = df.columns.str.strip()
   
    mapped = pd.DataFrame({
        "duration": df["dur"],
        "packet_count": df["spkts"] + df["dpkts"],
        "byte_count": df["sbytes"] + df["dbytes"],
        "packet_rate": df["rate"],
        "byte_rate": df["sbytes"],
        "packet_size_mean": df["smean"],
        "packet_size_max": df["dmean"],
        "label": df["label"]
    })
   
    return mapped


# -----------------------------
# LOAD DATASETS (UPDATE PATHS)
# -----------------------------
cicids = map_cicids(pd.read_csv("Data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"))
kdd = map_kdd(pd.read_csv("Data/KDDTrain+.txt"))
# unsw = map_unsw(pd.read_csv("Data/UNSW-NB15_1.csv"))  # optional

# -----------------------------
# COMBINE
# -----------------------------
df = pd.concat([cicids, kdd], ignore_index=True)

print("Combined shape:", df.shape)

# -----------------------------
# SPLIT
# -----------------------------
X = df.drop("label", axis=1)
y = df["label"]

# -----------------------------
# SCALING
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# -----------------------------
# MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=200, n_jobs=-1)
model.fit(X_train, y_train)

# -----------------------------
# EVALUATE
# -----------------------------
y_pred = model.predict(X_test)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# SAVE
# -----------------------------
joblib.dump(model, "model/universal_model.pkl")
joblib.dump(scaler, "model/universal_scaler.pkl")

print("\nUniversal model saved!")
