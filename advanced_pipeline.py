import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# -----------------------------
# FILE LIST
# -----------------------------
files = [
    "Data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
    "Data/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
    "Data/Wednesday-workingHours.pcap_ISCX.csv"
]

dfs = []

# -----------------------------
# LOAD + CLEAN FUNCTION
# -----------------------------
def load_and_clean(file):
    df = pd.read_csv(file)
   
    # fix column names
    df.columns = df.columns.str.strip()
   
    # clean
    df.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
    df.dropna(inplace=True)
   
    return df

# -----------------------------
# LOAD ALL DATASETS
# -----------------------------
for file in files:
    print(f"Loading: {file}")
    dfs.append(load_and_clean(file))

# -----------------------------
# COMBINE
# -----------------------------
df = pd.concat(dfs, ignore_index=True)

print("\nCombined shape:", df.shape)

# -----------------------------
# LABEL PROCESSING
# -----------------------------
df['Label'] = df['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1)

print("\nLabel distribution:")
print(df['Label'].value_counts())

# -----------------------------
# SPLIT
# -----------------------------
X = df.drop('Label', axis=1)
y = df['Label']

# -----------------------------
# SCALING (IMPORTANT)
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print("\nTraining shape:", X_train.shape)
print("Testing shape:", X_test.shape)

# -----------------------------
# MODEL (STRONGER CONFIG)
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# EVALUATION
# -----------------------------
y_pred = model.predict(X_test)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# SAVE EVERYTHING
# -----------------------------
joblib.dump(model, "model/advanced_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("\nModel + Scaler saved!")
