import pandas as pd
import joblib

# load model
model = joblib.load("model/ids_model.pkl")

# load CICIDS dataset
df = pd.read_csv("Data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")

print("Original shape:", df.shape)

# -----------------------------
# CLEAN DATA
# -----------------------------

# remove infinite values
df.replace([float('inf'), float('-inf')], pd.NA, inplace=True)

# drop null values
df.dropna(inplace=True)

# -----------------------------
# REMOVE LABEL COLUMN
# -----------------------------
if 'Label' in df.columns:
    df.drop('Label', axis=1, inplace=True)

# -----------------------------
# KEEP ONLY NUMERIC DATA
# -----------------------------
df = df.select_dtypes(include=['number'])

print("After cleaning shape:", df.shape)

# -----------------------------
# TAKE SAMPLE
# -----------------------------
sample = df.iloc[0].values.reshape(1, -1)

print("Sample shape:", sample.shape)

# -----------------------------
# TRY PREDICTION
# -----------------------------
try:
    prediction = model.predict(sample)
    print("Prediction:", prediction)
except Exception as e:
    print("ERROR OCCURRED:")
    print(e)
