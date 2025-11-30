from state import PipelineState
from llm import call_claude

SYSTEM_PROMPT = """
You are a senior Snowflake data engineer and architect.
Generate a comprehensive Snowflake-native ETL pipeline design based on the provided pipeline context.

Requirements:
- Design for the bronze-silver-gold architecture using Snowflake features
- Include proper database, schema, and table organization
- Consider PII masking and data security requirements
- Account for performance optimization (clustering keys, materialized views)
- Use Snowflake best practices for data loading and transformation

Output Structure:
1. Snowflake Architecture Overview
2. Database and Schema Design (bronze, silver, gold layers)
3. Stages for Data Ingestion (external/internal)
4. Pipes for Continuous Data Loading with Auto-Ingest
5. Streams for Change Data Capture
6. Tasks for Orchestration and Scheduling
7. Stored Procedures for Complex Transformations
8. Security and Access Control (RBAC, data masking)
9. Performance Optimization Strategies
10. Cost Management and Monitoring

Include specific Snowflake components:
- CREATE DATABASE and CREATE SCHEMA statements
- CREATE STAGE for data sources (S3, Azure, GCS)
- CREATE PIPE for auto-ingestion with Snowpipe
- CREATE STREAM to track changes on tables
- CREATE TASK for scheduling transformations
- CREATE PROCEDURE for complex business logic
- Virtual Warehouse sizing and auto-scaling configurations
- Time Travel and Fail-safe configurations
- Data masking policies and row access policies

Use proper Snowflake SQL syntax and conventions.
"""


def snowflake_designer_node(state: PipelineState) -> PipelineState:
    """Generate Snowflake pipeline design."""
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
        "Design a Snowflake-native ETL pipeline based on this architecture:\n\n"
        f"{context}\n\n"
        "Focus on Snowflake-specific implementations and best practices."
    )

    snowflake_design = call_claude(SYSTEM_PROMPT, user_content, max_tokens=2500)
    state["snowflake_design"] = snowflake_design
    return state