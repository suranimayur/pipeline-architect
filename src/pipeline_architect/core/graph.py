"""
Pipeline workflow graph definition.

This module defines the LangGraph workflow that orchestrates all the nodes
in the data pipeline design process. It provides the main entry point
for executing the complete pipeline design workflow.
"""

from typing import Any
from langgraph.graph import StateGraph, END

from .state import PipelineState
from ..nodes import (
    input_parser_node,
    architecture_planner_node,
    code_generator_node,
    iam_designer_node,
    cost_perf_advisor_node,
    answer_composer_node,
    etl_tool_designer_node
)


def build_graph() -> Any:
    """
    Build and compile the LangGraph workflow for the AI-based data pipeline
    design assistant.

    Returns:
        StateGraph: Compiled workflow graph ready for execution

    Workflow Nodes:
        - input_parser: Parse user query and extract structured information
        - architecture_planner: Design high-level cloud architecture
        - code_generator: Generate PySpark/Databricks code templates
        - iam_designer: Design IAM and security architecture
        - cost_perf_advisor: Provide cost optimization and performance tips
        - etl_tool_designer: Generate ETL tool-specific designs
        - answer_composer: Combine all outputs into final response

    Workflow Flow:
        input_parser 
        → architecture_planner 
        → code_generator 
        → iam_designer 
        → cost_perf_advisor
        → etl_tool_designer
        → answer_composer 
        → END
    """
    workflow = StateGraph(PipelineState)

    # Register all workflow nodes
    workflow.add_node("input_parser", input_parser_node)
    workflow.add_node("architecture_planner", architecture_planner_node)
    workflow.add_node("code_generator", code_generator_node)
    workflow.add_node("iam_designer", iam_designer_node)
    workflow.add_node("cost_perf_advisor", cost_perf_advisor_node)
    workflow.add_node("etl_tool_designer", etl_tool_designer_node)
    workflow.add_node("answer_composer", answer_composer_node)

    # Define workflow edges/flow
    workflow.set_entry_point("input_parser")
    workflow.add_edge("input_parser", "architecture_planner")
    workflow.add_edge("architecture_planner", "code_generator")
    workflow.add_edge("code_generator", "iam_designer")
    workflow.add_edge("iam_designer", "cost_perf_advisor")
    workflow.add_edge("cost_perf_advisor", "etl_tool_designer")
    workflow.add_edge("etl_tool_designer", "answer_composer")
    workflow.add_edge("answer_composer", END)

    # Compile and return the workflow
    compiled_workflow = workflow.compile()
    return compiled_workflow


__all__ = ["build_graph", "PipelineState"]