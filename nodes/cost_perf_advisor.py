from state import PipelineState
from llm import call_claude

SYSTEM_PROMPT = """    You are a cost optimization and performance tuning expert for Spark on cloud.

Given:
- cloud, workload type
- data volume, latency needs
- high-level architecture

Provide:
1. Cost considerations (compute, storage, data transfer).
2. Suggestions for keeping costs under control:
   - autoscaling, spot/preemptible instances, scheduling, right-sizing
   - compression, file size tuning, partitioning
3. Performance tuning tips:
   - partitioning strategy
   - caching, broadcast joins, bucketing (if applicable)
   - optimizing small files, compaction / OPTIMIZE / VACUUM concepts

Make it practical and concrete, but **do not use real pricing numbers or APIs**.
You can give qualitative ranges (e.g. "low / medium / high") and clearly state
that any numbers are rough estimates only.
"""


def cost_perf_advisor_node(state: PipelineState) -> PipelineState:
    user_query = state.get("user_query", "")
    cloud = state.get("cloud")
    workload_type = state.get("workload_type")
    vol = state.get("data_volume")
    latency = state.get("latency_requirements")
    arch = state.get("architecture")

    user_content = f"""User description:
    {user_query}

    Parsed info:
    - cloud: {cloud}
    - workload_type: {workload_type}
    - data_volume: {vol}
    - latency_requirements: {latency}

    Architecture:
    {arch}
    """

    tips = call_claude(SYSTEM_PROMPT, user_content, max_tokens=1200)
    # You could try to separate cost vs performance, but for now keep in one field
    state["cost_tips"] = tips
    state["performance_tips"] = tips  # same content reused
    return state
