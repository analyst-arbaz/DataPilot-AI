import pandas as pd
import logging

logger = logging.getLogger(__name__)


def clean_dataset(df):
    df = df.copy()

    rows_before = len(df)
    nulls_before = df.isnull().sum().sum()

    df.drop_duplicates(inplace=True)
    duplicates_removed = rows_before - len(df)

    for col in df.columns:
        if df[col].isnull().all():
            continue

        try:
            is_text = (
                df[col].dtype == "object"
                or df[col].dtype.name in ("string", "StringDtype")
                or str(df[col].dtype) == "category"
            )

            if is_text:
                freq = df[col].mode()
                if len(freq) > 0:
                    df[col] = df[col].fillna(freq[0])

            elif pd.api.types.is_numeric_dtype(df[col]):
                mid = df[col].median()
                if pd.notna(mid):
                    df[col] = df[col].fillna(mid)

            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].ffill()

            else:
                fallback = df[col].mode()
                if len(fallback) > 0:
                    df[col] = df[col].fillna(fallback[0])

        except Exception as e:
            logger.warning(f"Skipping null fill for '{col}': {e}")

    for col in df.select_dtypes(include=["object", "string"]).columns:
        try:
            df[col] = df[col].str.strip()
        except Exception as e:
            logger.warning(f"Skipping whitespace strip for '{col}': {e}")

    nulls_after = df.isnull().sum().sum()

    summary = {
        "original_rows":      rows_before,
        "cleaned_rows":       len(df),
        "duplicates_removed": duplicates_removed,
        "nulls_before":       int(nulls_before),
        "nulls_after":        int(nulls_after),
        "nulls_fixed":        int(nulls_before) - int(nulls_after),
    }

    return df, summary