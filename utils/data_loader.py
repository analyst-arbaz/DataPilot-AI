import pandas as pd
import logging

logger = logging.getLogger(__name__)


def load_file(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            return pd.read_excel(file)
        else:
            logger.warning(f"Unsupported file type: {file.name}")
            return None
    except Exception as e:
        logger.error(f"Failed to load {file.name}: {e}")
        return None