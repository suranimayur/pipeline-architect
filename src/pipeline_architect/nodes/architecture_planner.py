from state import PipelineState
from llm import call_claude

SYSTEM_PROMPT = """    You are a senior cloud data architect specializing in **Spark-based** data
platforms on Azure and AWS.

Given:
- cloud preference
- workload type (batch/streaming/mixed)
- source & target systems
- data volume
- latency requirements
- data sensitivity

Design a modern data pipeline using appropriate services.

Guidelines:
- If cloud is azure → prefer ADF, Event Hub, ADLS Gen2, Azure Databricks,
  Azure SQL DB / Synapse, Power BI.
- If cloud is aws → prefer S3, Kinesis, Glue/EMR, Redshift, Athena, QuickSight.
- If cloud unknown → make a reasonable assumption and clearly state it.

Output:
1. Short summary paragraph of the architecture.
2. An ASCII diagram.
3. Bullet list of main components and their roles.
"""


def architecture_planner_node(state: PipelineState) -> PipelineState:
    user_query = state.get("user_query", "")
    cloud = state.get("cloud")
    workload_type = state.get("workload_type")
    src = state.get("source_systems")
    tgt = state.get("target_systems")
    vol = state.get("data_volume")
    latency = state.get("latency_requirements")
    sensitivity = state.get("data_sensitivity")

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
    """

    arch = call_claude(SYSTEM_PROMPT, user_content, max_tokens=1200)
    state["architecture"] = arch
    return state
