from state import PipelineState
from llm import call_claude
import json
import re

SYSTEM_PROMPT = """
You are a senior system design educator who explains complex architectures
in a visual, ByteByteGo-style format.

Your job:
- Take the AI-generated pipeline design (architecture, code, IAM, cost tips).
- Produce a concise but clear system design explainer.
- Design a flow diagram for the architecture.
- Suggest fun GIF / animation ideas for slides.

Output format (VERY IMPORTANT):
Return a single JSON object with keys:
- explanation_markdown: string, Markdown formatted explanation.
  Use sections like:
    ## Problem
    ## Requirements
    ## High-level Architecture
    ## Data Flow
    ## Trade-offs & Scaling

- mermaid_code: string, a Mermaid flowchart definition ONLY, e.g.

    ```mermaid
    flowchart LR
      A[User] --> B[API]
    ```

  Use LR or TB layout and keep nodes/components readable.

- image_ideas: list of 2-4 short strings suggesting fun, colorful GIF/image ideas
  that would match this explanation (for example, what animation could show
  the data flowing through the system).

Do NOT include any text outside the JSON. Do NOT wrap the JSON in backticks.
"""


def bytebytego_explainer_node(state: PipelineState) -> PipelineState:
    """Use the full pipeline design as input and generate a ByteByteGo-style
    explanation + diagram spec.
    """

    final_answer = state.get("final_answer") or ""
    arch = state.get("architecture") or ""

    if not final_answer and not arch:
        # Nothing to explain
        return state

    user_content = f"""Here is the AI-generated pipeline design that you should
turn into a ByteByteGo-style system design explainer:

================== PIPELINE DESIGN ==================
{final_answer}

================== ARCHITECTURE ONLY ==================
{arch}
"""

    raw = call_claude(SYSTEM_PROMPT, user_content, max_tokens=2000)

    data = {
        "explanation_markdown": final_answer,
        "mermaid_code": "",
        "image_ideas": [],
    }

    try:
        # Try to recover JSON even if there is some extra text
        match = re.search(r"\\{[\\s\\S]*\\}\\s*$", raw)
        if match:
            data = json.loads(match.group(0))
        else:
            data = json.loads(raw)
    except Exception:
        # Fallback: keep original answer as explanation
        data["explanation_markdown"] = final_answer or arch

    state["bbg_explanation"] = data.get("explanation_markdown") or final_answer
    state["bbg_mermaid"] = data.get("mermaid_code")
    image_ideas = data.get("image_ideas") or []

    if isinstance(image_ideas, list):
        state["bbg_image_ideas"] = "\n".join(f"- {idea}" for idea in image_ideas)
    else:
        state["bbg_image_ideas"] = str(image_ideas) if image_ideas else None

    return state
