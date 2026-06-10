import pandas as pd


def profile_dataset(df):
    total = len(df)

    samples = []
    for col in df.columns:
        vals = df[col].dropna()
        samples.append(str(vals.iloc[0]) if len(vals) > 0 else "N/A")

    missing = df.isnull().sum()
    missing_pct = ((missing / total) * 100).round(2).astype(str).add(" %")

    profile = pd.DataFrame({
        "Column":        df.columns.tolist(),
        "Data Type":     df.dtypes.astype(str).tolist(),
        "Missing Count": missing.tolist(),
        "Missing %":     missing_pct.tolist(),
        "Unique Values": df.nunique().tolist(),
        "Sample Value":  samples,
    })

    return profile