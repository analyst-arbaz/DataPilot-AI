import pandas as pd
import logging

logger = logging.getLogger(__name__)


def execute_python(code, datasets):
    scope = {"pd": pd, "output_df": None}
    scope.update(datasets)

    try:
        exec(code, {}, scope)
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        raise

    return scope.get("output_df")