from state import PipelineState
from llm import call_claude

SYSTEM_PROMPT = """    You are a cloud security engineer.

Based on the pipeline architecture and cloud choice, propose an IAM / access
control design.

Output structure:
1. Short summary of security approach.
2. List of identities (service principals / roles / users).
3. Permissions needed per identity (high-level).
4. One or two example policy snippets:
   - For Azure: outline role assignments / RBAC and storage permissions.
   - For AWS: outline IAM role and inline policy JSON with placeholders
     like <bucket-name>, <role-name>, etc.

Focus on:
- Least privilege
- Separation of duties (ingest vs transform vs consume)
- Protecting sensitive data (e.g. PII)
"""


def iam_designer_node(state: PipelineState) -> PipelineState:
    cloud = state.get("cloud")
    arch = state.get("architecture")
    user_query = state.get("user_query", "")

    user_content = f"""Cloud: {cloud}
    Architecture:
    {arch}

    Original description:
    {user_query}
    """

    iam = call_claude(SYSTEM_PROMPT, user_content, max_tokens=1200)
    state["iam_design"] = iam
    return state
