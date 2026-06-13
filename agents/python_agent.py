import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

# Allowed modules only — prevents arbitrary code execution
SAFE_GLOBALS = {
    "__builtins__": {
        "print": print,
        "range": range,
        "len": len,
        "list": list,
        "dict": dict,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "enumerate": enumerate,
        "zip": zip,
        "sorted": sorted,
        "sum": sum,
        "min": min,
        "max": max,
        "abs": abs,
        "round": round,
        "isinstance": isinstance,
        "hasattr": hasattr,
        "getattr": getattr,
    }
}


def execute_python(code, datasets):
    scope = {
        "pd": pd,
        "plt": plt,
        "sns": sns,
        "output_df": None,
    }
    scope.update(datasets)

    try:
        exec(code, SAFE_GLOBALS.copy(), scope)
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        raise

    return scope.get("output_df")