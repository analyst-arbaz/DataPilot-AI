import duckdb
import re
import logging

logger = logging.getLogger(__name__)


def _to_table_name(filename):
    name = filename.replace(".csv", "").replace(".xlsx", "")
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if name[0].isdigit():
        name = "t_" + name
    return name.lower()


def run_sql(query, datasets):
    conn = duckdb.connect()

    for fname, df in datasets.items():
        tname = _to_table_name(fname)
        conn.register(tname, df)
        logger.debug(f"Registered: {tname}")

    return conn.execute(query).fetchdf()


def get_table_names(datasets):
    return {fname: _to_table_name(fname) for fname in datasets}