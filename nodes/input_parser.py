from state import PipelineState
from llm import call_claude

SYSTEM_PROMPT = """    You are an assistant that parses a user's natural language description of a
cloud data pipeline into structured fields.

Extract and infer when possible:
- cloud: azure / aws / hybrid / unknown
- workload_type: batch / streaming / mixed / unknown
- source_systems: short text
- target_systems: short text
- data_volume: short description (e.g. "200 GB/day")
- latency_requirements: short description
- data_sensitivity: e.g. "PII", "financial", "none mentioned"

If something is not clearly stated, make a best-effort guess and mark that
assumption clearly in parentheses.
Output as a small JSON object with those keys.
"""


def input_parser_node(state: PipelineState) -> PipelineState:
    user_query = state.get("user_query", "")
    if not user_query:
        return state

    user_content = f"""User description:
    {user_query}

    Return JSON with keys:
    cloud, workload_type, source_systems, target_systems, data_volume,
    latency_requirements, data_sensitivity.
    """

    parsed_text = call_claude(SYSTEM_PROMPT, user_content, max_tokens=600)

    # Be defensive: try to locate JSON even if Claude wraps it in text.
    import json
    import re

    json_obj = {}
    try:
        match = re.search(r"\{[\s\S]*\}", parsed_text)
        if match:
            json_obj = json.loads(match.group(0))
    except Exception:
        # If parsing fails, just keep everything as raw text in one field
        json_obj = {
            "cloud": None,
            "workload_type": None,
            "source_systems": None,
            "target_systems": None,
            "data_volume": None,
            "latency_requirements": None,
            "data_sensitivity": None,
        }

    # Merge into state
    state["cloud"] = json_obj.get("cloud")
    state["workload_type"] = json_obj.get("workload_type")
    state["source_systems"] = json_obj.get("source_systems")
    state["target_systems"] = json_obj.get("target_systems")
    state["data_volume"] = json_obj.get("data_volume")
    state["latency_requirements"] = json_obj.get("latency_requirements")
    state["data_sensitivity"] = json_obj.get("data_sensitivity")

    return state
