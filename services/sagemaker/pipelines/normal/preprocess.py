import pandas as pd
from sklearn.model_selection import train_test_split
import os

# ========= 入力 =========
INPUT_PATH = "/opt/ml/processing/input/abalone.csv"

# ========= 出力 =========
TRAIN_DIR = "/opt/ml/processing/train"
VAL_DIR   = "/opt/ml/processing/validation"

# 列名（元CSVはヘッダ無し）
COLUMNS = [
    "Sex", "Length", "Diameter", "Height",
    "Whole", "Shucked", "Viscera", "Shell", "Rings"
]

# ---------- Load ----------
df = pd.read_csv(INPUT_PATH, header=None, names=COLUMNS)

# ---------- 前処理 ----------
sex_map = {"I": 0, "F": 1, "M": 2}
df["SexCode"] = df["Sex"].map(sex_map).astype(int)

features = [
    "Length", "Diameter", "Height",
    "Whole", "Shucked", "Viscera", "Shell", "SexCode"
]

# XGBoost形式（ラベル + 特徴量）
dataset = pd.concat([df["Rings"], df[features]], axis=1)

# ---------- split ----------
train_df, val_df = train_test_split(
    dataset,
    test_size=0.2,
    random_state=42
)

# ---------- save ----------
os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VAL_DIR, exist_ok=True)

train_df.to_csv(
    os.path.join(TRAIN_DIR, "train.csv"),
    header=False,
    index=False
)

val_df.to_csv(
    os.path.join(VAL_DIR, "validation.csv"),
    header=False,
    index=False
)

print("Preprocessing completed")
print("Train records:", len(train_df))
print("Validation records:", len(val_df))