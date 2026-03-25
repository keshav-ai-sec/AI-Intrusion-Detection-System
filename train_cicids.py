import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

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
# LOAD + CLEAN
# -----------------------------
for file in files:
    print(f"\nLoading: {file}")
   
    df = pd.read_csv(file)
   
    # fix column names
    df.columns = df.columns.str.strip()
   
    # clean data
    df.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
    df.dropna(inplace=True)
   
    dfs.append(df)

# -----------------------------
# COMBINE DATA
# -----------------------------
combined_df = pd.concat(dfs, ignore_index=True)

print("\nCombined shape:", combined_df.shape)

# -----------------------------
# LABEL PROCESSING
# -----------------------------
combined_df['Label'] = combined_df['Label'].apply(
    lambda x: 0 if x == 'BENIGN' else 1
)

print("\nLabel distribution:")
print(combined_df['Label'].value_counts())

# -----------------------------
# SPLIT FEATURES
# -----------------------------
X = combined_df.drop('Label', axis=1)
y = combined_df['Label']

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining shape:", X_train.shape)
print("Testing shape:", X_test.shape)

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=100, n_jobs=-1)
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
# SAVE MODEL
# -----------------------------
joblib.dump(model, "model/combined_model.pkl")

print("\nModel saved as combined_model.pkl")
