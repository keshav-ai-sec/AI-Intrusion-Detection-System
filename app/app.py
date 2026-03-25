from flask import Flask, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# load model
model = joblib.load("../model/ids_model.pkl")

# load dataset (same preprocessing)
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

df = pd.read_csv("../Data/KDDTrain+.txt", names=columns)

# preprocess same as training
df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)
df.drop('difficulty', axis=1, inplace=True)

df = pd.get_dummies(df, columns=['protocol_type', 'service', 'flag'])

X = df.drop('label', axis=1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict():
    # take first row as sample
    sample = X.iloc[0].values.reshape(1, -1)

    prediction = model.predict(sample)[0]

    if prediction == 0:
        result = "Normal Traffic ✅"
    else:
        result = "Attack Detected 🚨"

    return render_template('index.html', prediction_text=result)

if __name__ == "__main__":
    app.run(debug=True)
