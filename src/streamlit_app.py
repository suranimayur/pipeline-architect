import os
from typing import Any, Dict

import streamlit as st
from dotenv import load_dotenv

from graph import build_graph
from state import PipelineState
from llm import call_claude
from doc_utils import load_reference_text  # <-- make sure doc_utils.py exists

# ---------- ENV + SETUP ----------
if os.path.exists(".env"):
    load_dotenv()

# Load reference architecture docs (optional)
REFERENCE_TEXT = load_reference_text()  # reads from ./reference_docs

st.set_page_config(
    page_title="AI Data Pipeline Design Assistant",
    page_icon="🧠",
    layout="wide",
)

# ---------- GLOBAL STYLES & HEADER ----------
st.markdown(
    """
    <style>
        /* Page background */
        .main {
            background: radial-gradient(circle at top left, #2b2b40, #121212 60%);
        }
        /* Fancy title */
        .title-text {
            text-align: center;
            font-size: 42px;
            font-weight: 900;
            background: linear-gradient(90deg, #ff6f61, #ffcc00, #7bff00, #00c8ff, #ff00f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 3s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from {
                text-shadow: 0 0 8px rgba(255, 0, 0, 0.4), 0 0 12px rgba(255,255,255,0.2);
            }
            to {
                text-shadow: 0 0 18px rgba(0, 255, 179, 0.6), 0 0 22px rgba(255,255,255,0.4);
            }
        }
        .sub-title {
            text-align: center;
            font-size: 20px;
            color: #d0d0d0;
            margin-top: -10px;
            margin-bottom: 10px;
        }
        .feature-card {
            padding: 12px;
            margin-top: 10px;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
            border: 1px solid rgba(255,255,255,0.15);
        }
        .section-header {
            font-size: 22px;
            font-weight: 700;
            color: #ffcc00;
            padding-top: 5px;
            text-decoration: underline;
        }
        /* Tabs styling */
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            margin-right: 8px;
            padding: 8px 14px;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffb300;
            color: #000000 !important;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 class="title-text">🚀 AI Data Pipeline Design Assistant 🌈</h1>
    <p class="sub-title">
        Generate <b>cloud architecture</b>, <b>PySpark</b>, <b>ETL</b>, <b>orchestration</b>, 
        <b>Airflow DAGs</b> & <b>interview Q&A</b> in one click.
    </p>
    """,
    unsafe_allow_html=True,
)



st.markdown(
    """
    <div class="feature-card">
        <span class="section-header">🎯 What this assistant can do</span>
        <br><br>
        🏗️ <b>Cloud Architecture</b> (Azure / AWS / medallion / streaming & batch)<br>
        ⚡ <b>PySpark / Databricks Code</b> for bronze–silver–gold pipelines<br>
        🔐 <b>IAM & Security Design</b> (PII masking, RLS, zero-trust)<br>
        💰 <b>Cost & Performance Tips</b> (autoscaling, partitioning, caching)<br>
        🛠️ <b>ETL Job Design</b> for Talend, Informatica, Ab Initio, DBT, Snowflake<br>
        🌐 <b>Orchestration Plan</b> + <b>Airflow DAG (.py)</b><br>
        🧠 <b>Interview-style Q&A</b> based on the generated pipeline<br>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- SESSION STATE ----------
if "out_state" not in st.session_state:
    st.session_state.out_state = None

if "python_design_code" not in st.session_state:
    st.session_state.python_design_code = None

if "etl_tool_design" not in st.session_state:
    st.session_state.etl_tool_design = None

if "dbt_design" not in st.session_state:
    st.session_state.dbt_design = None

if "snowflake_design" not in st.session_state:
    st.session_state.snowflake_design = None

if "orchestration_plan" not in st.session_state:
    st.session_state.orchestration_plan = None

if "airflow_dag_code" not in st.session_state:
    st.session_state.airflow_dag_code = None

if "interview_qa" not in st.session_state:
    st.session_state.interview_qa = None

if "interview_error" not in st.session_state:
    st.session_state.interview_error = None

# ---------- USER INPUT ----------
default_example = (
    "I have CSV files landing in Azure Blob (~200GB/day) and want to build a "
    "bronze-silver-gold Delta Lake in Azure Databricks and expose curated tables "
    "to Power BI. Daily batch is fine, there is customer PII like email and phone."
)

st.markdown("### ✏️ Describe your pipeline scenario")

description = st.text_area(
    "",
    value=default_example,
    height=200,
    help="Mention cloud (Azure/AWS), sources, targets, volume, latency, PII, etc.",
)

etl_tool_option = st.selectbox(
    "🛠️ Optional: choose a target ETL tool design",
    ["None", "Talend", "Informatica", "Ab Initio", "DBT", "Snowflake"],
    index=0,
)

# ---------- HELPER FUNCTIONS ----------
def _build_context_for_state(out_state: Dict[str, Any]) -> str:
    """Helper to build text context from pipeline state."""
    architecture = out_state.get("architecture", "") or ""
    pyspark_code = out_state.get("pyspark_code", "") or ""
    iam = out_state.get("iam_design", "") or ""
    cost = out_state.get("cost_tips", "") or ""
    final = out_state.get("final_answer", "") or ""

    base = final or "\n\n".join(
        [
            "ARCHITECTURE:\n" + architecture,
            "PYSPARK CODE:\n" + pyspark_code,
            "IAM DESIGN:\n" + iam,
            "COST & PERFORMANCE:\n" + cost,
        ]
    )

    if REFERENCE_TEXT:
        ref_part = "\n\nREFERENCE_ARCHITECTURE_NOTES:\n" + REFERENCE_TEXT[:4000]
        return base + ref_part

    return base


def generate_python_design_code(out_state: Dict[str, Any]) -> str:
    """Generate high-level Python orchestration code."""
    context = _build_context_for_state(out_state)

    system_prompt = (
        "You are a senior data engineer.\n"
        "Generate Python orchestration code for this pipeline:\n"
        "- Use functions for each stage: ingest(), bronze(), silver(), gold(), publish()\n"
        "- Include comments referencing the main services (e.g., Azure Blob, Databricks, Synapse, Power BI)\n"
        "- Do not execute Spark; just show control / orchestration flow\n"
        "- Code must be valid Python and easy to read.\n"
    )

    user_content = "Pipeline design:\n" + context
    return call_claude(system_prompt, user_content, max_tokens=1500)


def generate_etl_design(out_state: Dict[str, Any], etl_tool: str) -> str:
    """Generate ETL-tool pipeline design."""
    etl_tool = etl_tool.strip()
    if etl_tool == "None":
        return "_No ETL tool selected._"

    # If we already have a dedicated design from the graph, use it
    if etl_tool == "DBT" and out_state.get("dbt_design"):
        return out_state["dbt_design"]
    elif etl_tool == "Snowflake" and out_state.get("snowflake_design"):
        return out_state["snowflake_design"]

    context = _build_context_for_state(out_state)

    if etl_tool == "DBT":
        system_prompt = (
            "You are a senior data engineer specializing in DBT (Data Build Tool).\n"
            "Generate a comprehensive DBT pipeline design based on the pipeline context.\n\n"
            "FORMAT:\n"
            "- DBT Project Overview and Architecture\n"
            "- Models Directory Structure (staging, intermediate, marts)\n"
            "- YAML Schema Files with column descriptions and tests\n"
            "- Sample DBT Models using Jinja templating and macros\n"
            "- Transformation Logic (PII masking, deduplication, surrogate keys)\n"
            "- Materialization Strategies (table, view, incremental)\n"
            "- Performance Optimization and Best Practices\n"
            "- CI/CD and Deployment Considerations\n\n"
            "Include specific DBT components:\n"
            "- staging/*.sql - Raw data cleaning and standardization\n"
            "- staging/*.yml - Schema tests and descriptions\n"
            "- marts/*.sql - Business logic and transformations\n"
            "- marts/*.yml - Business rule tests\n"
            "- macros/ - Custom Jinja macros for reusability\n"
            "- dbt_project.yml configuration\n\n"
            "Example transformations:\n"
            "- {{ config(materialized='incremental', unique_key='id') }}\n"
            "- {{ dbt_utils.surrogate_key(['column1', 'column2']) }}\n"
            "- {{ mask_pii(column_name) }} macro for PII masking\n"
            "Return as Markdown with code blocks."
        )
    elif etl_tool == "Snowflake":
        system_prompt = (
            "You are a senior Snowflake data engineer.\n"
            "Generate a comprehensive Snowflake-native ETL pipeline design.\n\n"
            "FORMAT:\n"
            "- Snowflake Architecture Overview\n"
            "- Database and Schema Design (bronze, silver, gold)\n"
            "- Stages for Data Ingestion (external/internal)\n"
            "- Pipes for Continuous Data Loading\n"
            "- Streams for Change Data Capture\n"
            "- Tasks for Orchestration and Scheduling\n"
            "- Stored Procedures for Complex Transformations\n"
            "- Performance Optimization (clustering keys, materialized views)\n"
            "- Security and Access Control\n\n"
            "Include specific Snowflake components:\n"
            "- CREATE STAGE for data sources\n"
            "- CREATE PIPE for auto-ingestion\n"
            "- CREATE STREAM to track changes\n"
            "- CREATE TASK for scheduling transformations\n"
            "- CREATE PROCEDURE for complex logic\n"
            "- Virtual Warehouse sizing and auto-scaling\n"
            "- Time Travel and Fail-safe configurations\n\n"
            "Example components:\n"
            "- CREATE OR REPLACE STAGE my_stage URL='s3://bucket/path'\n"
            "- CREATE OR REPLACE PIPE my_pipe AUTO_INGEST=TRUE AS COPY INTO...\n"
            "- CREATE OR REPLACE STREAM my_stream ON TABLE bronze_table\n"
            "- CREATE OR REPLACE TASK my_task WAREHOUSE=compute_warehouse AFTER...\n"
            "Return as Markdown with SQL code blocks."
        )
    else:
        system_prompt = (
            "You are a senior ETL architect.\n"
            f"Generate an ETL pipeline design for this tool ({etl_tool}).\n\n"
            "FORMAT:\n"
            "- Tool name and short overview\n"
            "- Component Flow with tool-specific components\n"
            "- Sample transformation logic (e.g., PII masking, deduplication)\n"
            "- Optimization and scheduling notes\n\n"
            "Examples of style:\n"
            "- Talend: tFileInputDelimited -> tMap -> tFilterRow -> tAggregateRow -> tAzureStorageOutput\n"
            "- Informatica: [Source Qualifier] -> [Expression] -> [Lookup] -> [Aggregator] -> [Target]\n"
            "- Ab Initio: (Read) -> [Reformat] -> [Join] -> [Rollup] -> (Write)\n"
            "Keep it as design/pseudo-code, not proprietary XML.\n"
        )

    user_prompt = f"ETL Tool: {etl_tool}\nPipeline Context:\n{context}"
    return call_claude(system_prompt, user_prompt, max_tokens=2000)


def generate_orchestration_plan(out_state: Dict[str, Any]) -> str:
    """Generate orchestration / scheduling plan in Markdown."""
    context = _build_context_for_state(out_state)

    system_prompt = (
        "You are an expert in orchestration tools (Airflow / ADF / Databricks Jobs).\n"
        "Given the pipeline design, produce an orchestration and scheduling plan.\n\n"
        "Include:\n"
        "- High-level approach (e.g., Airflow DAG or ADF pipeline)\n"
        "- List of tasks/activities: ingest_raw, bronze_load, silver_transform, gold_aggregate, publish_to_bi\n"
        "- Dependencies between tasks\n"
        "- Suggested schedule (e.g., daily batch, streaming + batch hybrid)\n"
        "- Notes on retries, SLAs, alerting.\n\n"
        "Return the answer in Markdown with headings and bullet points.\n"
    )

    user_content = "Pipeline design:\n" + context
    return call_claude(system_prompt, user_content, max_tokens=1800)


def generate_airflow_dag_code(out_state: Dict[str, Any]) -> str:
    """Generate an Airflow DAG .py file content for this pipeline."""
    context = _build_context_for_state(out_state)

    system_prompt = (
        "You are an expert Apache Airflow engineer.\n"
        "Generate ONLY valid Python code for an Airflow DAG defining this data pipeline.\n\n"
        "Requirements:\n"
        "- DAG id: 'pipeline_orchestration_dag'\n"
        "- Use default_args with retries, email_on_failure=False\n"
        "- Define tasks using PythonOperator or DummyOperator for:\n"
        "  ingest_raw, bronze_load, silver_transform, gold_aggregate, publish_to_bi\n"
        "- Set clear task dependencies in the right order.\n"
        "- Do NOT include explanations or comments outside the code.\n"
        "Return ONLY Python code, no markdown.\n"
    )

    user_content = "Pipeline design:\n" + context
    return call_claude(system_prompt, user_content, max_tokens=1500)


def generate_interview_qa(out_state: Dict[str, Any]) -> str:
    """Generate interview Q&A based on design."""
    context = _build_context_for_state(out_state)

    system_prompt = (
        "You are a senior data engineering interviewer.\n"
        "Generate 8–12 interview questions and answers based on this pipeline.\n"
        "Focus on Spark, orchestration, cloud services, data modeling, performance, and security.\n"
        "Format as Markdown with headings like '### Q1. ...' and 'Answer:'.\n"
    )

    return call_claude(system_prompt, "Pipeline:\n" + context, max_tokens=2000)

# ---------- RUN BUTTON ----------
st.markdown("---")

if st.button("✨ Generate Pipeline Design + Code + Orchestration + Q&A", type="primary"):
    if not description.strip():
        st.warning("Please enter a pipeline description.")
    else:
        # 1) Run main LangGraph pipeline
        with st.spinner("🧠 Running base pipeline with LangGraph + Claude..."):
            app = build_graph()
            state: PipelineState = {"user_query": description}
            out_state = app.invoke(state)

        st.session_state.out_state = out_state
        st.session_state.python_design_code = None
        st.session_state.etl_tool_design = None
        st.session_state.orchestration_plan = None
        st.session_state.airflow_dag_code = None
        st.session_state.interview_qa = None
        st.session_state.interview_error = None

        # 2) Generate Python design
        with st.spinner("⚙️ Generating Python orchestration code..."):
            st.session_state.python_design_code = generate_python_design_code(out_state)

        # 3) Generate ETL design (if ETL tool selected)
        if etl_tool_option != "None":
            with st.spinner(f"🛠️ Generating {etl_tool_option} ETL design..."):
                st.session_state.etl_tool_design = generate_etl_design(out_state, etl_tool_option)
                
                # Store in specific session state variables for DBT and Snowflake
                if etl_tool_option == "DBT":
                    st.session_state.dbt_design = st.session_state.etl_tool_design
                elif etl_tool_option == "Snowflake":
                    st.session_state.snowflake_design = st.session_state.etl_tool_design
        else:
            st.session_state.etl_tool_design = "_No ETL tool selected._"

        # 4) Generate orchestration / scheduling plan
        with st.spinner("📅 Generating orchestration / scheduling plan..."):
            st.session_state.orchestration_plan = generate_orchestration_plan(out_state)

        # 5) Generate Airflow DAG code
        with st.spinner("📜 Generating Airflow DAG code (.py)..."):
            st.session_state.airflow_dag_code = generate_airflow_dag_code(out_state)

        # 6) Generate Interview Q&A
        try:
            with st.spinner("🧪 Generating Interview Q&A..."):
                st.session_state.interview_qa = generate_interview_qa(out_state)
            st.success("✅ Design + Code + ETL + Orchestration + DAG + Q&A generated!")
        except Exception as e:
            st.session_state.interview_error = str(e)
            st.error(f"Interview Q&A generation failed: {e}")

# ---------- OUTPUT TABS ----------
if not st.session_state.out_state:
    st.info("Enter details above and click the button to generate your pipeline design.")
else:
    out_state = st.session_state.out_state
    arch = out_state.get("architecture", "_No architecture_")
    code = out_state.get("pyspark_code", "_No code_")
    iam = out_state.get("iam_design", "_No IAM_")
    tips = out_state.get("cost_tips", "_No cost/perf_")

    python_design = st.session_state.python_design_code or "_No Python design code generated._"
    etl_design = st.session_state.etl_tool_design or "_No ETL tool design generated._"
    dbt_design = st.session_state.dbt_design or out_state.get("dbt_design", "_No DBT design generated._")
    snowflake_design = st.session_state.snowflake_design or out_state.get("snowflake_design", "_No Snowflake design generated._")
    orchestration_plan = st.session_state.orchestration_plan or "_No orchestration plan generated._"
    airflow_dag_code = st.session_state.airflow_dag_code or ""
    interview_qa = st.session_state.interview_qa or "No Q&A generated"

    (
        tab_arch,
        tab_code,
        tab_iam,
        tab_cost,
        tab_python,
        tab_etl,
        tab_dbt,
        tab_snowflake,
        tab_orch,
        tab_qa,
    ) = st.tabs(
        [
            "🏗 Architecture",
            "🐍 PySpark Code",
            "🔐 IAM",
            "💰 Cost & Performance",
            "⚙️ Python Design",
            "🛠 ETL Design",
            "🏗️ DBT Design",
            "❄️ Snowflake Design",
            "📅 Orchestration / DAG",
            "🧠 Interview Q&A",
        ]
    )

    with tab_arch:
        st.markdown("### 🏗 Architecture Overview")
        st.markdown(arch)

    with tab_code:
        st.markdown("### 🐍 PySpark / Databricks Starter Code")
        st.code(code, language="python")

    with tab_iam:
        st.markdown("### 🔐 IAM & Access Control Design")
        st.markdown(iam)

    with tab_cost:
        st.markdown("### 💰 Cost & Performance Tips")
        st.markdown(tips)

    with tab_python:
        st.markdown("### ⚙️ Python Orchestration / Design Code")
        st.code(python_design, language="python")

    with tab_etl:
        st.markdown("### 🛠 ETL Tool Pipeline Design")
        st.markdown(etl_design)

    with tab_dbt:
        st.markdown("### 🏗️ DBT Pipeline Design")
        st.markdown(dbt_design)

    with tab_snowflake:
        st.markdown("### ❄️ Snowflake Pipeline Design")
        st.markdown(snowflake_design)

    with tab_orch:
        st.markdown("### 📅 Orchestration / Scheduling Plan")
        st.markdown(orchestration_plan)

        if airflow_dag_code:
            st.markdown("#### 📜 Download Airflow DAG (.py)")
            st.download_button(
                label="Download DAG as pipeline_dag.py",
                data=airflow_dag_code,
                file_name="pipeline_dag.py",
                mime="text/x-python",
            )
            with st.expander("Preview DAG code"):
                st.code(airflow_dag_code, language="python")

    with tab_qa:
        st.markdown("### 🧠 Interview Questions & Answers")
        if st.session_state.interview_qa:
            st.markdown(interview_qa)
        elif st.session_state.interview_error:
            st.error(f"Interview Q&A error: {st.session_state.interview_error}")
        else:
            st.info("Interview Q&A not generated yet.")
