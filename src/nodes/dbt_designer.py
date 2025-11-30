from state import PipelineState
from llm import call_claude

SYSTEM_PROMPT = """
You are a senior DBT (Data Build Tool) specialist.
Generate a comprehensive DBT pipeline design based on the provided pipeline context.

Requirements:
- Design for the bronze-silver-gold architecture if applicable
- Include proper model layering and dependencies
- Consider PII masking and data quality requirements
- Account for performance optimization and incremental loads
- Use DBT best practices

Output Structure:
1. DBT Project Architecture Overview
2. Models Directory Structure with file hierarchy
3. YAML Schema Files with descriptions and tests
4. Sample DBT Models with Jinja templating
5. Custom Macros for reusable logic
6. Materialization and Performance Strategies
7. CI/CD and Deployment Notes

Include specific DBT components:
- staging/*.sql - Raw data cleaning and standardization
- staging/*.yml - Schema tests and descriptions  
- marts/*.sql - Business logic and transformations
- marts/*.yml - Business rule tests
- macros/ - Custom Jinja macros for reusability
- dbt_project.yml configuration

Use proper DBT syntax and conventions.
"""


def dbt_designer_node(state: PipelineState) -> PipelineState:
    """Generate DBT pipeline design."""
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
        "Design a DBT pipeline based on this architecture:\n\n"
        f"{context}\n\n"
        "Focus on DBT-specific implementations and best practices."
    )

    dbt_design = call_claude(SYSTEM_PROMPT, user_content, max_tokens=2500)
    state["dbt_design"] = dbt_design
    return state