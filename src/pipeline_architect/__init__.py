"""
Pipeline Architect - AI-powered data pipeline design assistant.

This package provides comprehensive tools for designing, generating, and managing
data pipeline architectures with AI assistance.

Core Components:
- Graph workflows for pipeline orchestration
- LLM integration for AI-powered design
- State management for pipeline execution
- Node-based architecture for extensibility

Usage:
    from pipeline_architect import PipelineState, build_graph
    from pipeline_architect.llm import get_llm_client

    # Initialize state
    state = PipelineState(user_query="Your pipeline requirements")
    
    # Build and execute pipeline
    graph = build_graph()
    result = graph.invoke(state)
"""

__version__ = "1.0.0"
__author__ = "Pipeline Architect Team"
__email__ = "team@pipelinearchitect.com"

# Import main components for easy access
from .core.graph import build_graph
from .core.state import PipelineState
from .models.pipeline import PipelineDesign, ArchitectureDesign, CodeGenerationResult
from .services.llm_service import LLMService
from .services.security_service import SecurityService
from .services.optimization_service import OptimizationService

# Version information
VERSION = __version__

# Package metadata
__all__ = [
    "build_graph",
    "PipelineState", 
    "PipelineDesign",
    "ArchitectureDesign",
    "CodeGenerationResult",
    "LLMService",
    "SecurityService",
    "OptimizationService",
    "VERSION"
]