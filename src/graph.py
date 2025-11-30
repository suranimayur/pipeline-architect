from __future__ import annotations

from langgraph.graph import StateGraph, END

from state import PipelineState
from nodes.input_parser import input_parser_node
from nodes.architecture_planner import architecture_planner_node
from nodes.code_generator import code_generator_node
from nodes.iam_designer import iam_designer_node
from nodes.cost_perf_advisor import cost_perf_advisor_node
from nodes.answer_composer import answer_composer_node

import os


def build_graph():
    """
    Build and compile the LangGraph workflow for the AI-based data pipeline
    design assistant.

    Nodes:
    - input_parser         : parse user query, extract cloud, workload, etc.
    - architecture_planner : design high-level architecture
    - code_generator       : generate PySpark / Databricks code
    - iam_designer         : IAM / security design
    - cost_perf_advisor    : cost & performance tips
    - answer_composer      : combine everything into final_answer
    """
    workflow = StateGraph(PipelineState)

    # Register nodes
    workflow.add_node("input_parser", input_parser_node)
    workflow.add_node("architecture_planner", architecture_planner_node)
    workflow.add_node("code_generator", code_generator_node)
    workflow.add_node("iam_designer", iam_designer_node)
    workflow.add_node("cost_perf_advisor", cost_perf_advisor_node)
    workflow.add_node("answer_composer", answer_composer_node)

    # Define edges / flow
    workflow.set_entry_point("input_parser")
    workflow.add_edge("input_parser", "architecture_planner")
    workflow.add_edge("architecture_planner", "code_generator")
    workflow.add_edge("code_generator", "iam_designer")
    workflow.add_edge("iam_designer", "cost_perf_advisor")
    workflow.add_edge("cost_perf_advisor", "answer_composer")
    workflow.add_edge("answer_composer", END)

    app = workflow.compile()
    return app
