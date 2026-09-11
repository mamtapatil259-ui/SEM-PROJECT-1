import os
import pandas as pd
import numpy as np

def _read_json(path):
    try:
        return pd.read_json(path)
    except ValueError:
        return pd.read_json(path, lines=True)

def load_dataset(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext in (".tsv", ".txt"):
        df = pd.read_csv(path, sep="\t")
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    elif ext in (".json", ".jsonl"):
        df = _read_json(path)
    else:
        raise ValueError("Unsupported file format.")

    if df.empty:
        raise ValueError("The dataset is empty.")

    for c in df.columns:
        if df[c].dtype == "object":
            numeric = pd.to_numeric(df[c], errors="coerce")
            if numeric.notna().mean() >= 0.90:
                df[c] = numeric

    return df

def dataset_summary(df):
    numeric = df.select_dtypes(include=np.number)
    categorical = df.select_dtypes(exclude=np.number)

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_values": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "numeric_columns": int(len(numeric.columns)),
        "categorical_columns": int(len(categorical.columns))
    }
