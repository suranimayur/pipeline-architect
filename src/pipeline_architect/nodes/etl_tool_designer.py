from state import PipelineState
from llm import call_claude

SYSTEM_PROMPT = """
You are a senior data engineer.

Given the pipeline design details (architecture, code, IAM, cost/perf), generate
Python code that represents the pipeline orchestration / design.

It can be:
- Either a simple, clear Python script with functions for each stage, OR
- An Airflow DAG-like structure (but keep it simple).

Requirements:
- Use clear function names for stages: ingest, bronze, silver, gold, publish.
- Include comments that reference the cloud services (e.g., Azure Blob, Databricks, Synapse).
- Do NOT actually run Spark; just show the high-level structure.
- Code should be valid Python and well-formatted.
"""


def etl_tool_designer_node(state: PipelineState) -> PipelineState:
    """Generate high-level Python orchestration code for the pipeline."""
    architecture = state.get("architecture", "") or ""
    pyspark_code = state.get("pyspark_code", "") or ""
    iam = state.get("iam_design", "") or ""
    cost = state.get("cost_tips", "") or ""
    final = state.get("final_answer", "") or ""

    context = final or "\n\n".join(
        [
            "ARCHITECTURE:\n" + architecture,
            "PYSPARK CODE (snippet):\n" + pyspark_code,
            "IAM DESIGN:\n" + iam,
            "COST/PERF TIPS:\n" + cost,
        ]
    )

    user_content = (
        "Here is the pipeline design. Generate Python orchestration code based on this:\n\n"
        f"{context}"
    )

    python_code = call_claude(SYSTEM_PROMPT, user_content, max_tokens=1500)
    state["python_design_code"] = python_code
    return state
