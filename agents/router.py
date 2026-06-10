def detect_agent(prompt):
    text = str(prompt).lower()

    if any(w in text for w in [
        "clean", "missing", "null", "duplicate", "fix missing", "fix data",
        "fill null", "fill missing", "drop null", "drop duplicate",
        "impute", "nulls", "blanks", "empty values", "data cleaning",
        "data quality", "handle missing", "fix null", "remove null",
        "fix quality", "quality issues",
    ]):
        return "cleaning"

    if any(w in text for w in [
        "summary", "describe", "columns", "dataset", "information",
        "data types", "dtypes", "missing values", "dataset info",
        "profile", "overview", "column names", "what columns",
        "schema", "fields", "attributes", "show info", "about this data",
        "what is this dataset", "explain columns",
    ]):
        return "profiling"

    if any(w in text for w in [
        "sql", "query", "select", "where", "join", "group by", "from",
        "top 10", "top 5", "count", "sum", "average", "aggregate",
        "filter rows", "fetch", "retrieve", "total revenue", "by category",
        "by country", "by region", "by city", "by product", "by customer",
        "revenue by", "sales by", "records", "all rows",
    ]):
        return "sql"

    if any(w in text for w in [
        "plot", "chart", "graph", "histogram", "heatmap", "scatter",
        "bar chart", "line chart", "pie chart", "visualize", "visualization",
        "correlation", "distribution", "boxplot", "pairplot",
        "new column", "add column", "create column", "calculated column",
        "matplotlib", "seaborn", "plotly", "draw", "figure", "trend",
    ]):
        return "python"

    if any(w in text for w in [
        "business", "insights", "strategy", "growth", "opportunities",
        "risks", "profit", "revenue", "recommendations", "executive summary",
        "analysis report", "kpi", "performance", "findings", "summarize",
        "tell me about", "explain data", "what is happening", "outcomes",
    ]):
        return "business"

    return "general"