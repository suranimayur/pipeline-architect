"""
Core components for Pipeline Architect.

This module contains the essential building blocks for the pipeline design system,
including the workflow graph, state management, and core orchestration logic.
"""

from .graph import build_graph
from .state import PipelineState

__all__ = ["build_graph", "PipelineState"]