from state import PipelineState

def answer_composer_node(state: PipelineState) -> PipelineState:
    """Combine all node outputs into a single markdown answer."""

    arch = state.get("architecture", "")
    code = state.get("pyspark_code", "")
    iam = state.get("iam_design", "")
    cost = state.get("cost_tips", "")
    perf = state.get("performance_tips", "")

    final = []
    final.append("# AI-Generated Data Pipeline Design\n")

    final.append("## 1. Architecture Overview\n")
    final.append(arch or "_No architecture generated._")
    final.append("\n")

    final.append("## 2. PySpark / Databricks Starter Code\n")
    final.append(code or "_No code generated._")
    final.append("\n")

    final.append("## 3. IAM & Access Control Design\n")
    final.append(iam or "_No IAM design generated._")
    final.append("\n")

    final.append("## 4. Cost & Performance Tips\n")
    if cost or perf:
        # They currently hold the same text
        final.append(cost or perf)
    else:
        final.append("_No cost or performance tips generated._")

    state["final_answer"] = "\n".join(final)
    return state
