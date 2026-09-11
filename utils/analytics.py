import numpy as np

def generate_kpis(df):
    k = [
        {"label": "Total Records", "value": int(len(df))},
        {"label": "Total Columns", "value": int(len(df.columns))},
        {"label": "Missing Values", "value": int(df.isna().sum().sum())},
        {"label": "Duplicate Rows", "value": int(df.duplicated().sum())},
    ]

    nums = df.select_dtypes(include=np.number)
    for c in list(nums.columns)[:2]:
        k.append({
            "label": f"Average {c}",
            "value": round(float(nums[c].mean()), 2)
        })

    return k
