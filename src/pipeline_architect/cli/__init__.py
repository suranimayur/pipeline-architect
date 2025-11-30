"""
Command Line Interface for Pipeline Architect.

This module provides the CLI interface for running the pipeline design assistant
from the command line with various options and configurations.
"""

from .main import main
from .commands import design, validate, version

__all__ = [
    "main",
    "design",
    "validate", 
    "version"
]