import numpy as np
import pandas as pd
import streamlit as st


def show_dashboard(df):
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()

    st.subheader("📊 Interactive Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows",           df.shape[0])
    c2.metric("Columns",        df.shape[1])
    c3.metric("Numeric Cols",   len(num_cols))
    c4.metric("Missing Values", int(df.isnull().sum().sum()))

    st.markdown("---")

    if num_cols:
        left, right = st.columns([1, 3])
        with left:
            col   = st.selectbox("Numeric Column", num_cols, key="dash_num")
            ctype = st.radio("Chart Type", ["Bar", "Line", "Histogram"], key="dash_chart")
        with right:
            if ctype == "Bar":
                st.bar_chart(df[col])
            elif ctype == "Line":
                st.line_chart(df[col])
            else:
                counts, edges = np.histogram(df[col].dropna(), bins=20)
                hist = pd.DataFrame({"bin": edges[:-1].round(2), "count": counts}).set_index("bin")
                st.bar_chart(hist)

    if cat_cols:
        st.markdown("---")
        left2, right2 = st.columns([1, 3])
        with left2:
            cat = st.selectbox("Category Column", cat_cols, key="dash_cat")
        with right2:
            vc = df[cat].value_counts().head(15).reset_index()
            vc.columns = [cat, "Count"]
            st.bar_chart(vc.set_index(cat))

    if len(num_cols) >= 2:
        st.markdown("---")
        with st.expander("🔥 Correlation Matrix"):
            corr = df[num_cols].corr().round(2)
            st.dataframe(
                corr.style.background_gradient(cmap="RdYlGn", axis=None),
                width="stretch"
            )