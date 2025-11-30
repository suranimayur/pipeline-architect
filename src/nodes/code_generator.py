from state import PipelineState
from llm import call_claude

SYSTEM_PROMPT = """    You are an expert PySpark and Databricks engineer.

Given:
- The user's description
- Parsed pipeline info
- The proposed architecture

Generate **starter PySpark code** for the core ETL pipeline.

Requirements:
- Use `spark.read` / `spark.write` APIs.
- Use placeholders for secrets and connection details.
- Include comments for each major step.
- If Delta Lake is a good fit, use format("delta") and partitioning.
- If streaming is mentioned, use Structured Streaming where appropriate.
- The goal is to give the user a strong starting point, not perfect production code.

Output: Only a single Python code block (no extra explanation).
"""


def code_generator_node(state: PipelineState) -> PipelineState:
    user_query = state.get("user_query", "")
    cloud = state.get("cloud")
    workload_type = state.get("workload_type")
    src = state.get("source_systems")
    tgt = state.get("target_systems")
    vol = state.get("data_volume")
    latency = state.get("latency_requirements")
    sensitivity = state.get("data_sensitivity")
    arch = state.get("architecture")

    user_content = f"""User pipeline description:
    {user_query}

    Parsed info:
    - cloud: {cloud}
    - workload_type: {workload_type}
    - source_systems: {src}
    - target_systems: {tgt}
    - data_volume: {vol}
    - latency_requirements: {latency}
    - data_sensitivity: {sensitivity}

    Proposed architecture:
    {arch}
    """

    code = call_claude(SYSTEM_PROMPT, user_content, max_tokens=1800)
    state["pyspark_code"] = code
    return state
