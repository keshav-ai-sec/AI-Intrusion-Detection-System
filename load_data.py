import pandas as pd

# column names
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

# load dataset
df = pd.read_csv("Data/KDDTrain+.txt", names=columns)

print("Shape:", df.shape)

# Convert label to binary
df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)

print("\nLabel value counts:")
print(df['label'].value_counts())

# -----------------------------
# Convert categorical columns
# -----------------------------

categorical_cols = ['protocol_type', 'service', 'flag']

df = pd.get_dummies(df, columns=categorical_cols)

print("\nAfter encoding shape:", df.shape)

print("\nSample data after encoding:")
print(df.head())
