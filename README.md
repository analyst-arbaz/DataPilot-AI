# ⚡ DataPilot AI
### Intelligent Multi-Agent Data Analysis Platform — From Raw Data to Real Decisions

> 🏆 Submitted for **Microsoft Agents League Hackathon 2026** — Creative Apps Track  
> 🤖 Built with **GitHub Copilot** | Powered by **Azure AI Foundry (gpt-4.1-mini)**  
> 💡 Integrates **Microsoft Foundry IQ** intelligence layer

---

## 🎬 Demo Video

[![DataPilot AI Demo](https://img.shields.io/badge/YouTube-Watch%20Demo-red?style=for-the-badge&logo=youtube)](https://youtu.be/Dn5Wr3BHDqU)

---

## 🎯 What is DataPilot AI?

DataPilot AI is a fully automated, multi-agent data analysis platform. Upload any CSV or Excel file and the system instantly:

- 🧹 **Cleans** your data — removes duplicates, fixes nulls
- 📋 **Profiles** every column — types, missing %, unique values
- 🗄️ **Runs SQL** — natural language to DuckDB queries
- 📊 **Visualizes** — AI-generated charts and correlation heatmaps
- 💼 **Business Insights** — strategy, risks, opportunities via LLM
- 📄 **PDF Report** — downloadable full analysis report with code log

No coding needed. Just upload and get insights in seconds.

---

## 🏗️ Architecture Diagram

![DataPilot AI Architecture](architecture_diagram.png)

> Built with **GitHub Copilot** · Powered by **Azure AI Foundry (Foundry IQ)** · Orchestrated via **LangChain**

---

## 💡 Microsoft IQ Integration — Foundry IQ

DataPilot AI integrates **Microsoft Foundry IQ** as its core intelligence layer:

| Component | Microsoft Technology |
|---|---|
| LLM Inference | Azure AI Foundry — gpt-4.1-mini |
| Endpoint | Azure AI Foundry services endpoint |
| Orchestration | LangChain + Azure AI Foundry API |
| AI Development | GitHub Copilot (VS Code) |

All LLM calls — chart generation, business analysis, SQL generation — are routed through **Azure AI Foundry**, making DataPilot AI a Foundry IQ powered platform.

---

## 🤖 How GitHub Copilot Was Used

| Area | How Copilot Helped |
|---|---|
| Multi-agent routing logic | Copilot suggested intent detection patterns in `router.py` |
| SQL query generation | Copilot autocompleted DuckDB query patterns in `sql_agent.py` |
| Data cleaning logic | Copilot recommended dtype-aware null filling strategies |
| ReportLab PDF formatting | Copilot generated boilerplate for styles and layout |
| Streamlit UI components | Copilot accelerated dashboard and layout code |
| LangChain integration | Copilot suggested chain patterns for LLM calls |
| Azure AI Foundry setup | Copilot helped configure Foundry IQ endpoint integration |

> GitHub Copilot acted as a **pair programmer** throughout — speeding up development, catching bugs, and suggesting best practices at every step.

---

## 🧠 Multi-Agent Architecture

```
User uploads CSV / Excel
         ↓
    Router Agent
   (detects intent from prompt)
         ↓
┌─────────────────────────────────────────┐
│  Cleaning Agent  →  Remove nulls/dups   │
│  Profiling Agent →  Dataset overview    │
│  SQL Agent       →  DuckDB queries      │
│  Python Agent    →  Visualizations      │
│  Business Agent  →  LLM insights        │
│  Report Agent    →  PDF generation      │
└─────────────────────────────────────────┘
         ↓
    Azure AI Foundry (Foundry IQ)
   (gpt-4.1-mini via Azure AI endpoint)
         ↓
  Results shown on screen
  PDF report downloadable
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 Auto Analysis | 5-step analysis runs automatically on upload |
| 🧹 Smart Cleaning | Handles nulls, duplicates, whitespace, all dtypes |
| 🗄️ Natural Language SQL | Type in plain English, get SQL results instantly |
| 📊 AI Visualizations | LLM generates the right chart for your data |
| 💼 Business Insights | Senior consultant-level analysis via Azure AI Foundry |
| 📄 PDF Export | Download full business report |
| 📋 Analysis Code Log | Download all code and queries as PDF or TXT |
| 💬 Chat Interface | Ask anything about your data |
| 🔄 Multi-file Support | Upload and switch between multiple datasets |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Development | GitHub Copilot (VS Code) |
| Microsoft IQ Layer | Azure AI Foundry — Foundry IQ |
| LLM Model | gpt-4.1-mini via Azure AI Foundry |
| LLM Framework | LangChain |
| SQL Engine | DuckDB |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| PDF Generation | ReportLab |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
DataPilot-AI/
│
├── main.py                       # Main Streamlit app
├── requirements.txt              # Dependencies
├── .env.example                  # Environment variables template
├── architecture_diagram.png      # Architecture diagram
│
├── agents/
│   ├── router.py                 # Intent detection — routes to correct agent
│   ├── cleaning_agent.py         # Data cleaning
│   ├── profiling_agent.py        # Dataset profiling
│   ├── sql_agent.py              # DuckDB SQL execution
│   ├── python_agent.py           # Python/visualization code execution
│   ├── business_agent.py         # LLM business analysis
│   ├── report_agent.py           # Business PDF generation
│   └── analysis_report_agent.py  # Analysis code log PDF generation
│
├── utils/
│   ├── data_loader.py            # CSV/Excel file loader
│   ├── helper.py                 # Code extraction utility
│   └── llm.py                    # Azure AI Foundry LLM setup
│
└── dashboards/
    └── dashboard.py              # Interactive Streamlit dashboard
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/DataPilot-AI.git
cd DataPilot-AI
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
```bash
cp .env.example .env
```

### 5. Run the app
```bash
streamlit run main.py
```

---

## 🔑 Environment Variables

Add the following to your `.env` file:

```env
# Azure AI Foundry — Primary LLM (Foundry IQ)
LLM_PROVIDER=foundry
AZURE_ENDPOINT=https://your-resource.services.ai.azure.com/openai/v1
AZURE_API_KEY=your_azure_api_key_here
AZURE_DEPLOYMENT=gpt-4.1-mini

# GitHub Models — Backup LLM (optional)
# LLM_PROVIDER=github
# GITHUB_TOKEN=your_github_token_here
```

Get your Azure AI Foundry credentials:
1. Go to ai.azure.com and create a project
2. Deploy gpt-4.1-mini model
3. Copy endpoint and API key from deployment page

---

## 💬 Supported Prompts

**Cleaning:** `clean my data` · `fix missing values` · `remove duplicates`

**Profiling:** `show dataset info` · `describe columns` · `data overview`

**SQL:** `top 10 records` · `group by country` · `total revenue by category`

**Visualization:** `create histogram` · `show correlation` · `plot sales trend`

**Business:** `give business insights` · `executive summary` · `growth strategy`

---

## 🏆 Hackathon Submission — Microsoft Agents League 2026

**Track:** Creative Apps  
**Challenge:** Build innovative applications with AI-assisted development using GitHub Copilot  
**Microsoft IQ:** Foundry IQ — Azure AI Foundry (gpt-4.1-mini)

### Why DataPilot AI fits the Creative Apps track:
- ✅ Built entirely with **GitHub Copilot** as AI-assisted development tool
- ✅ Integrates **Microsoft Foundry IQ** — Azure AI Foundry as LLM backbone
- ✅ Multi-agent architecture — 6 specialized agents working in pipeline
- ✅ Solves a real business problem — data analysis for non-technical users
- ✅ Analysis Code Log — users can download all code and SQL queries as PDF
- ✅ Fully demo-able — upload any CSV and get insights in seconds

---

## 👨‍💻 Developer

**Arbaz Khan**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Arbaz%20Khan-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/arbaz-data-analyst)
[![YouTube](https://img.shields.io/badge/YouTube-data__with__arbaz-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@data_with_arbaz)
[![Demo](https://img.shields.io/badge/Demo%20Video-Watch%20Now-red?style=for-the-badge&logo=youtube)](https://youtu.be/Dn5Wr3BHDqU)

---

*Built with ❤️ for Microsoft Agents League Hackathon 2026*
