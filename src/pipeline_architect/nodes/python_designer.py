from state import PipelineState
from llm import call_claude

SYSTEM_PROMPT = """
You are a senior data engineer.

Given the pipeline design details (architecture, code, IAM, cost/perf), generate
Python code that represents the pipeline orchestration / design.

It can be:
- Either a simple, clear Python script with functions for each stage, OR
- An Airflow DAG-like structure.

Requirements:
- Use clear function names for stages: ingest, bronze, silver, gold, publish.
- Include comments that reference the cloud services (Azure Blob, Databricks, Synapse, etc.).
- Do NOT actually run Spark; just show the high-level structure.
- Code should be valid Python and well-formatted.
"""

def python_designer_node(state: PipelineState) -> PipelineState:
    arch = state.get("architecture", "") or ""
    code = state.get("pyspark_code", "") or ""
    iam = state.get("iam_design", "") or ""
    tips = state.get("cost_tips", "") or ""
    final = state.get("final_answer", "") or ""

    context = final or "\n\n".join([
        "ARCHITECTURE:\n" + arch,
        "PYSPARK CODE (snippet):\n" + code,
        "IAM:\n" + iam,
        "COST/PERF:\n" + tips,
    ])

    user_content = f"Here is the pipeline design. Generate Python orchestration code based on this:\n\n{context}"

    python_code = call_claude(SYSTEM_PROMPT, user_content, max_tokens=1500)
    state["python_design_code"] = python_code
    return state
