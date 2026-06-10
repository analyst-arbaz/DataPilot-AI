import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.use("Agg")

from utils.data_loader import load_file
from utils.llm import llm
from utils.helper import extract_python_code

from agents.router import detect_agent
from agents.cleaning_agent import clean_dataset
from agents.profiling_agent import profile_dataset
from agents.sql_agent import run_sql, get_table_names
from agents.python_agent import execute_python
from agents.business_agent import business_analysis
from agents.report_agent import create_pdf
from dashboards.dashboard import show_dashboard


st.set_page_config(
    page_title="DataPilot AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stHeader"] { background: transparent !important; }
</style>

<div style="width:100%;height:5px;background:linear-gradient(to right,#F25022 25%,#7FBA00 25% 50%,#00A4EF 50% 75%,#FFB900 75%);border-radius:3px;margin-bottom:1.2rem;"></div>

<div style="padding: 1.5rem 0 1rem 0;">
  <h1 style="font-size:2.5rem;font-weight:700;margin:0;padding:0;">
    ⚡ DataPilot AI
  </h1>
  <p style="font-size:1.05rem;color:#888;margin:0.3rem 0 0 0;">
    Your Intelligent Data Co-Pilot — From Raw Data to Real Decisions
  </p>
</div>

<div style="
  background: linear-gradient(135deg, #0f3460 0%, #16213e 50%, #1a1a2e 100%);
  border-radius: 14px;
  padding: 1.5rem 2rem;
  margin-bottom: 1.5rem;
  border-left: 5px solid #00A4EF;
">
  <h3 style="color:#ffffff;margin:0 0 0.5rem 0;font-size:1.1rem;">🎯 What is DataPilot AI?</h3>
  <p style="color:#c0cfe0;margin:0;font-size:0.95rem;line-height:1.7;">
    DataPilot AI is an end-to-end intelligent data analysis platform powered by <strong style="color:#00A4EF;">GitHub Models (GPT-4o mini)</strong>.
    Simply upload any CSV or Excel file and the system automatically cleans your data, profiles it,
    runs SQL analysis, generates visualizations, and delivers business insights — all in seconds.
    Built for <strong style="color:#FFB900;">Microsoft Agents League Hackathon 2026</strong>.
  </p>
</div>

<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:1.8rem;">
  <div style="background:#1a1a2e;border:1px solid #F25022;border-radius:12px;padding:1rem;text-align:center;">
    <div style="font-size:1.8rem;">🧹</div>
    <div style="color:#F25022;font-weight:600;font-size:0.85rem;margin-top:0.4rem;">Auto Clean</div>
    <div style="color:#888;font-size:0.75rem;margin-top:0.2rem;">Remove nulls & duplicates</div>
  </div>
  <div style="background:#1a1a2e;border:1px solid #7FBA00;border-radius:12px;padding:1rem;text-align:center;">
    <div style="font-size:1.8rem;">📊</div>
    <div style="color:#7FBA00;font-weight:600;font-size:0.85rem;margin-top:0.4rem;">Smart Visuals</div>
    <div style="color:#888;font-size:0.75rem;margin-top:0.2rem;">AI-generated charts</div>
  </div>
  <div style="background:#1a1a2e;border:1px solid #00A4EF;border-radius:12px;padding:1rem;text-align:center;">
    <div style="font-size:1.8rem;">🗄️</div>
    <div style="color:#00A4EF;font-weight:600;font-size:0.85rem;margin-top:0.4rem;">SQL Analysis</div>
    <div style="color:#888;font-size:0.75rem;margin-top:0.2rem;">Natural language to SQL</div>
  </div>
  <div style="background:#1a1a2e;border:1px solid #FFB900;border-radius:12px;padding:1rem;text-align:center;">
    <div style="font-size:1.8rem;">💼</div>
    <div style="color:#FFB900;font-weight:600;font-size:0.85rem;margin-top:0.4rem;">Business Insights</div>
    <div style="color:#888;font-size:0.75rem;margin-top:0.2rem;">Strategy & recommendations</div>
  </div>
  <div style="background:#1a1a2e;border:1px solid #c0c0c0;border-radius:12px;padding:1rem;text-align:center;">
    <div style="font-size:1.8rem;">📄</div>
    <div style="color:#c0c0c0;font-weight:600;font-size:0.85rem;margin-top:0.4rem;">PDF Report</div>
    <div style="color:#888;font-size:0.75rem;margin-top:0.2rem;">Download full report</div>
  </div>
</div>
""", unsafe_allow_html=True)


# Session state init
defaults = {
    "datasets":        {},
    "business_report": None,
    "analyzed_files":  set(),
    "chat_history":    [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def build_tables_info(datasets):
    info = ""
    names = get_table_names(datasets)
    for fname, df in datasets.items():
        info += f"\nTable: {names[fname]}  (file: {fname})\n"
        info += f"Columns: {list(df.columns)}\n"
        info += f"Shape: {df.shape[0]} rows x {df.shape[1]} cols\n"
    return info


def run_auto_analysis(df, file_name, tables_info):
    st.markdown(f"## 🚀 Auto Analysis: `{file_name}`")

    bar = st.progress(0, text="Starting...")
    bar.progress(5, text="Step 1/5 — Cleaning...")
    st.markdown("---")

    # Step 1 — Clean
    with st.expander("🧹 Step 1 — Data Cleaning", expanded=True):
        with st.spinner("Cleaning..."):
            cleaned_df, summary = clean_dataset(df)
        st.session_state.datasets[file_name] = cleaned_df

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Original Rows",     summary["original_rows"])
        c2.metric("Cleaned Rows",       summary["cleaned_rows"])
        c3.metric("Duplicates Removed", summary["duplicates_removed"])
        c4.metric("Nulls Fixed",        summary["nulls_fixed"])

        st.success("Dataset cleaned.")
        st.dataframe(cleaned_df.head(), width="stretch")

    bar.progress(20, text="Step 2/5 — Profiling...")
    df = cleaned_df

    # Step 2 — Profile
    with st.expander("📋 Step 2 — Dataset Profile", expanded=True):
        with st.spinner("Profiling..."):
            profile = profile_dataset(df)
        st.dataframe(profile, width="stretch")

    bar.progress(40, text="Step 3/5 — SQL...")

    # Step 3 — SQL
    with st.expander("🗄️ Step 3 — SQL Analysis", expanded=True):
        tnames   = get_table_names(st.session_state.datasets)
        tname    = tnames[file_name]
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()

        queries = {
            "Top 10 Records": f"SELECT * FROM {tname} LIMIT 10",
            "Row Count":      f"SELECT COUNT(*) AS total_rows FROM {tname}",
        }

        if num_cols:
            avg_expr = ", ".join(
                [f'AVG("{c}") AS avg_{c.replace(" ","_").lower()}' for c in num_cols[:5]]
            )
            queries["Column Averages"] = f"SELECT {avg_expr} FROM {tname}"

        if cat_cols and num_cols:
            gc, nc = cat_cols[0], num_cols[0]
            queries[f"Total {nc} by {gc}"] = (
                f'SELECT "{gc}", SUM("{nc}") AS total '
                f'FROM {tname} GROUP BY "{gc}" ORDER BY 2 DESC LIMIT 10'
            )

        for label, q in queries.items():
            st.markdown(f"**{label}**")
            st.code(q, language="sql")
            try:
                st.dataframe(run_sql(q, st.session_state.datasets), width="stretch")
            except Exception as e:
                st.error(f"SQL error: {e}")
            st.markdown("")

    bar.progress(60, text="Step 4/5 — Visualizations...")

    # Step 4 — Charts
    with st.expander("📊 Step 4 — Auto Visualizations", expanded=True):
        num_cols  = df.select_dtypes(include="number").columns.tolist()
        cat_cols  = df.select_dtypes(include=["object", "string"]).columns.tolist()

        if num_cols:
            viz_prompt = f"""You are a Python data visualization expert.

Dataset columns: {list(df.columns)}
Numeric columns: {num_cols}
Category columns: {cat_cols}
Shape: {df.shape}
Sample:
{df.head(3).to_string()}

Write Python code using matplotlib and seaborn to create:
1. A histogram of the most relevant numeric column
2. A correlation heatmap if there are 2+ numeric columns
3. A bar chart of the top values in the most relevant category column
4. A line or trend chart of numeric data

Rules:
- 'df' is already available as a variable
- Use plt.figure() for each chart
- Display with st.pyplot(plt)
- Import matplotlib.pyplot as plt, seaborn as sns, streamlit as st
- No plt.show()
- Call dropna() before plotting
- Add descriptive titles
- Use tight_layout()
- SEABORN RULES (strict):
  * Never use palette= without also setting hue=
  * For barplot: use hue=x_col, legend=False
  * For countplot: use hue=x_col, legend=False
  * If you don't need color grouping, skip palette entirely
"""
            with st.spinner("Generating charts..."):
                try:
                    resp = llm.invoke(viz_prompt)
                    code = extract_python_code(resp.content)
                    st.code(code, language="python")

                    scope = {"df": df, "pd": pd, "plt": plt, "sns": sns, "st": st}
                    exec(code, {}, scope)
                    plt.close("all")

                except Exception as e:
                    st.error(f"Chart error: {e}")
                    plt.close("all")
                    st.bar_chart(df[num_cols[0]])

    bar.progress(80, text="Step 5/5 — Business analysis...")

    # Step 5 — Business insights
    with st.expander("💼 Step 5 — Business Analysis", expanded=True):
        with st.spinner("Running analysis..."):
            try:
                result = business_analysis(
                    "Give complete business insights, key findings, risks, opportunities, growth strategy and executive summary.",
                    tables_info,
                    df=df,
                )
                st.session_state.business_report = result
                st.markdown(result)
                st.markdown("---")

                try:
                    pdf_path = create_pdf(result, "business_report.pdf")
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "📄 Download Business Report PDF",
                            data=f.read(),
                            file_name="business_report.pdf",
                            mime="application/pdf",
                            width="stretch",
                        )
                except Exception as e:
                    st.error(f"PDF error: {e}")

            except Exception as e:
                st.error(f"Analysis error: {e}")

    bar.progress(100, text="All done!")
    st.success(f"✅ Analysis complete for **{file_name}**!")


# File uploader
uploaded_files = st.file_uploader(
    "📂 Upload CSV or Excel Files",
    accept_multiple_files=True,
    type=["csv", "xlsx"],
)

if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.datasets:
            df = load_file(file)
            if df is not None:
                st.session_state.datasets[file.name] = df

# Sidebar
current_df       = None
selected_dataset = None
tables_info      = build_tables_info(st.session_state.datasets)

if st.session_state.datasets:
    st.sidebar.success(f"✅ {len(st.session_state.datasets)} dataset(s) loaded")

    selected_dataset = st.sidebar.selectbox(
        "Active Dataset",
        list(st.session_state.datasets.keys()),
    )
    current_df = st.session_state.datasets[selected_dataset]

    st.sidebar.markdown("---")
    st.sidebar.subheader("Dataset Info")
    st.sidebar.write("Rows:",    current_df.shape[0])
    st.sidebar.write("Columns:", current_df.shape[1])
    st.sidebar.write("Nulls:",   int(current_df.isnull().sum().sum()))

    st.sidebar.markdown("---")
    if st.sidebar.button("🧹 Re-Clean Dataset"):
        cleaned_df, summary = clean_dataset(current_df)
        st.session_state.datasets[selected_dataset] = cleaned_df
        current_df = cleaned_df
        st.sidebar.success(
            f"Done — removed {summary['duplicates_removed']} duplicates, "
            f"fixed {summary['nulls_fixed']} nulls."
        )

    if st.sidebar.button("🔄 Re-Run Analysis"):
        st.session_state.analyzed_files.discard(selected_dataset)
        st.rerun()

    if st.session_state.business_report:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Business Report")
        try:
            pdf_path = create_pdf(st.session_state.business_report, "business_report.pdf")
            with open(pdf_path, "rb") as f:
                st.sidebar.download_button(
                    "📄 Download PDF",
                    data=f.read(),
                    file_name="business_report.pdf",
                    mime="application/pdf",
                )
        except Exception:
            pass


# Auto-analysis trigger
if st.session_state.datasets:
    for fname, df in st.session_state.datasets.items():
        if fname not in st.session_state.analyzed_files:
            run_auto_analysis(df, fname, tables_info)
            st.session_state.analyzed_files.add(fname)

    if current_df is not None:
        st.markdown("---")
        show_dashboard(current_df)


# Chat
if st.session_state.datasets:
    st.markdown("---")
    st.subheader("💬 Ask About Your Data")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask anything about your data...")

    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            agent = detect_agent(prompt)
            st.caption(f"Agent: {agent}")

            if agent == "cleaning":
                cleaned_df, summary = clean_dataset(current_df)
                st.session_state.datasets[selected_dataset] = cleaned_df
                reply = (
                    f"✅ Done!\n\n"
                    f"- Duplicates removed: **{summary['duplicates_removed']}**\n"
                    f"- Nulls fixed: **{summary['nulls_fixed']}**\n"
                    f"- Rows remaining: **{summary['cleaned_rows']}**"
                )
                st.markdown(reply)
                st.dataframe(cleaned_df.head(), width="stretch")
                st.session_state.chat_history.append({"role": "assistant", "content": reply})

            elif agent == "profiling":
                profile = profile_dataset(current_df)
                st.dataframe(profile, width="stretch")
                st.session_state.chat_history.append({"role": "assistant", "content": "Profile shown above."})

            elif agent == "sql":
                sql_prompt = f"""You are a DuckDB SQL expert.

Tables available: {list(get_table_names(st.session_state.datasets).values())}
Schema:
{tables_info}

Request: {prompt}

Return only the SQL query — no explanation, no markdown.
"""
                resp      = llm.invoke(sql_prompt)
                sql_query = resp.content.replace("```sql", "").replace("```", "").strip()
                st.code(sql_query, language="sql")
                try:
                    result = run_sql(sql_query, st.session_state.datasets)
                    st.dataframe(result, width="stretch")
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"```sql\n{sql_query}\n```",
                    })
                except Exception as e:
                    err = f"❌ SQL Error: {e}"
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err})

            elif agent == "python":
                py_prompt = f"""Write Python code using pandas, matplotlib, seaborn, and streamlit.

Columns: {list(current_df.columns)}
Shape: {current_df.shape}

Task: {prompt}

Rules:
- 'df' is already available
- Import plt, sns, st at the top
- Use st.pyplot(plt) to show charts
- No plt.show(), no print()
- Store any result dataframe in output_df
- Call dropna() before plotting
- Add chart titles
- For seaborn barplot/countplot: always set hue= and legend=False, never use palette= without hue=
"""
                resp = llm.invoke(py_prompt)
                code = extract_python_code(resp.content)
                st.code(code, language="python")

                try:
                    scope = {
                        "df": current_df, "pd": pd,
                        "plt": plt, "sns": sns, "st": st, "output_df": None,
                    }
                    scope.update(st.session_state.datasets)
                    exec(code, {}, scope)
                    plt.close("all")

                    if scope.get("output_df") is not None:
                        st.dataframe(scope["output_df"], width="stretch")

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"```python\n{code}\n```",
                    })

                except Exception as e:
                    plt.close("all")
                    err = f"❌ Error: {e}"
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err})

            elif agent == "business":
                with st.spinner("Analyzing..."):
                    result = business_analysis(prompt, tables_info, df=current_df)

                st.session_state.business_report = result
                st.markdown(result)
                st.markdown("---")

                try:
                    pdf_path = create_pdf(result, "business_report.pdf")
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "📄 Download PDF Report",
                            data=f.read(),
                            file_name="business_report.pdf",
                            mime="application/pdf",
                            width="stretch",
                        )
                except Exception as e:
                    st.error(f"PDF error: {e}")

                st.session_state.chat_history.append({"role": "assistant", "content": result})

            else:
                general_prompt = f"""You are a data analyst.

Dataset:
{tables_info}

Sample:
{current_df.head(3).to_string()}

Question: {prompt}

Give a clear, specific answer based on the data.
"""
                resp = llm.invoke(general_prompt)
                st.markdown(resp.content)
                st.session_state.chat_history.append({"role": "assistant", "content": resp.content})

else:
    st.info("👆 Upload a CSV or Excel file to get started.")


st.markdown("""
<div style="
  margin-top: 3rem;
  padding: 1.2rem 2rem;
  background: linear-gradient(135deg, #1a1a2e, #0f3460);
  border-radius: 12px;
  border-top: 3px solid;
  border-image: linear-gradient(to right, #F25022, #7FBA00, #00A4EF, #FFB900) 1;
  text-align: center;
">
  <p style="color:#888;font-size:0.8rem;margin:0;">
    ⚡ <strong style="color:#00A4EF;">DataPilot AI</strong> &nbsp;|&nbsp;
    Built for <strong style="color:#FFB900;">Microsoft Agents League Hackathon 2026</strong> &nbsp;|&nbsp;
    Powered by <strong style="color:#7FBA00;">GitHub Models</strong>
  </p>
</div>
""", unsafe_allow_html=True)