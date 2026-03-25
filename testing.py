import pandas as pd
import joblib

# load trained model
model = joblib.load("model/combined_model.pkl")

# -----------------------------
# CHANGE FILE NAME HERE
# -----------------------------
file_name = "Data/Wednesday-workingHours.pcap_ISCX.csv"

df = pd.read_csv(file_name)

print("Testing on:", file_name)
print("Original shape:", df.shape)

# -----------------------------
# CLEAN DATA
# -----------------------------
df.columns = df.columns.str.strip()

df.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
df.dropna(inplace=True)

# -----------------------------
# CHECK LABEL EXISTS
# -----------------------------
if 'Label' in df.columns:
    y_true = df['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1)
    X = df.drop('Label', axis=1)
else:
    y_true = None
    X = df

print("Cleaned shape:", X.shape)

# -----------------------------
# PREDICT
# -----------------------------
try:
    y_pred = model.predict(X)

    print("\nPrediction done!")

    if y_true is not None:
        from sklearn.metrics import classification_report, confusion_matrix

        print("\nConfusion Matrix:")
        print(confusion_matrix(y_true, y_pred))

        print("\nClassification Report:")
        print(classification_report(y_true, y_pred))

except Exception as e:
    print("\nERROR:")
    print(e)
	

