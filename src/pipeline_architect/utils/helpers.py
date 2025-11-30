"""
Helper utilities for Pipeline Architect.

This module provides various helper functions used throughout the application
for validation, formatting, and common utility operations.
"""

from typing import Any, Dict, List, Optional
import json
import re
from datetime import datetime


def validate_pipeline_input(user_query: str) -> List[str]:
    """
    Validate user input for pipeline design.
    
    Args:
        user_query: User's pipeline description
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    if not user_query or not user_query.strip():
        errors.append("Pipeline description cannot be empty")
    
    if len(user_query.strip()) < 10:
        errors.append("Pipeline description is too short (minimum 10 characters)")
    
    if len(user_query) > 5000:
        errors.append("Pipeline description is too long (maximum 5000 characters)")
    
    return errors


def generate_pipeline_id(prefix: str = "pipeline") -> str:
    """
    Generate a unique pipeline ID.
    
    Args:
        prefix: Prefix for the pipeline ID
        
    Returns:
        Unique pipeline ID
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    import random
    import string
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}_{timestamp}_{random_suffix}"


def format_pipeline_output(data: Dict[str, Any], format_type: str = "json") -> str:
    """
    Format pipeline output data.
    
    Args:
        data: Pipeline data to format
        format_type: Output format (json, markdown, text)
        
    Returns:
        Formatted output string
    """
    if format_type == "json":
        return json.dumps(data, indent=2, default=str)
    elif format_type == "markdown":
        return _dict_to_markdown(data)
    else:
        return str(data)


def _dict_to_markdown(data: Dict[str, Any], indent: int = 0) -> str:
    """Convert dictionary to markdown format."""
    lines = []
    
    for key, value in data.items():
        indent_str = "#" * (indent + 1)
        lines.append(f"{indent_str} {key}")
        
        if isinstance(value, dict):
            lines.append(_dict_to_markdown(value, indent + 1))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    lines.append(_dict_to_markdown(item, indent + 2))
                else:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{value}")
        
        lines.append("")
    
    return "\n".join(lines)


def sanitize_input(text: str) -> str:
    """
    Sanitize input text by removing potentially harmful content.
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove potential script tags
    text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove potential HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove potential SQL injection patterns
    sql_patterns = [
        r"(\bunion\b|\bselect\b|\binsert\b|\bupdate\b|\bdelete\b|\bdrop\b|\bcreate\b|\balter\b)",
        r"(\bor\b|\band\b)\s+\w+\s*[=<>]",
        r"'(\s*;\s*|\s*--\s*)",
    ]
    
    for pattern in sql_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Limit length
    if len(text) > 10000:
        text = text[:10000]
    
    return text.strip()


def extract_keywords(text: str) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: Input text
        
    Returns:
        List of extracted keywords
    """
    # Simple keyword extraction based on common data pipeline terms
    keywords = []
    
    pipeline_keywords = [
        "azure", "aws", "gcp", "cloud", "databricks", "snowflake", "redshift",
        "bigquery", "kafka", "spark", "streaming", "batch", "etl", "elt",
        "delta", "lake", "warehouse", "bi", "power", "quick", "tableau",
        "pyspark", "python", "scala", "sql", "dbt", "talend", "informatica"
    ]
    
    text_lower = text.lower()
    for keyword in pipeline_keywords:
        if keyword in text_lower:
            keywords.append(keyword)
    
    return list(set(keywords))  # Remove duplicates


def format_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}PB"


def is_valid_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def safe_get(data: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary value using dot notation.
    
    Args:
        data: Dictionary to search
        key_path: Dot notation path (e.g., "user.profile.name")
        default: Default value if path not found
        
    Returns:
        Value at path or default
    """
    keys = key_path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


__all__ = [
    "validate_pipeline_input",
    "generate_pipeline_id", 
    "format_pipeline_output",
    "sanitize_input",
    "extract_keywords",
    "format_size",
    "is_valid_email",
    "safe_get"
]