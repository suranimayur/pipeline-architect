"""
Pipeline state definitions and data models.

This module defines the state schema used throughout the pipeline workflow,
including all the data structures that flow between nodes and are used
to maintain context and results throughout the pipeline execution.
"""

from typing import TypedDict, Optional, Dict, Any, List, Literal, Union

# Type aliases for better readability
CloudProvider = Literal["azure", "aws", "gcp", "hybrid", "unknown"]
WorkloadType = Literal["batch", "streaming", "mixed", "unknown"]
DataSensitivity = Literal["none", "pii", "financial", "health", "restricted", "unknown"]


class PipelineState(TypedDict, total=False):
    """
    Complete state structure for the pipeline workflow.
    
    This TypedDict represents the complete state that flows through
    all nodes in the pipeline workflow, containing both input data
    and generated outputs.
    """
    
    # Original user input
    user_query: str
    """Original natural language description of pipeline requirements"""
    
    # Parsed/extracted fields from input
    cloud: Optional[CloudProvider]
    """Cloud provider preference (azure/aws/gcp/hybrid/unknown)"""
    
    workload_type: Optional[WorkloadType]
    """Type of workload (batch/streaming/mixed/unknown)"""
    
    source_systems: Optional[str]
    """Description of data source systems"""
    
    target_systems: Optional[str]
    """Description of target systems and destinations"""
    
    data_volume: Optional[str]
    """Data volume and frequency (e.g., '200GB/day')"""
    
    latency_requirements: Optional[str]
    """Latency and performance requirements"""
    
    data_sensitivity: Optional[DataSensitivity]
    """Data sensitivity level (none/pii/financial/etc.)"""
    
    # Generated outputs from various nodes
    architecture: Optional[str]
    """Generated cloud architecture design and explanation"""
    
    pyspark_code: Optional[str]
    """Generated PySpark/Databricks code template"""
    
    iam_design: Optional[str]
    """IAM and security design recommendations"""
    
    cost_tips: Optional[str]
    """Cost optimization recommendations"""
    
    performance_tips: Optional[str]
    """Performance optimization recommendations"""
    
    final_answer: Optional[str]
    """Combined final answer with all components"""
    
    # ETL tool specific outputs
    etl_tool: Optional[str]
    """Selected ETL tool (talend/informatica/abinitio/dbt/snowflake)"""
    
    etl_tool_design: Optional[str]
    """ETL tool-specific design and configuration"""
    
    dbt_design: Optional[str]
    """DBT pipeline design and configuration"""
    
    snowflake_design: Optional[str]
    """Snowflake-native pipeline design"""
    
    python_design_code: Optional[str]
    """Python orchestration code for pipeline execution"""
    
    # Orchestration and deployment outputs
    orchestration_plan: Optional[str]
    """Orchestration and scheduling plan"""
    
    airflow_dag_code: Optional[str]
    """Generated Airflow DAG code"""
    
    # Interview and documentation outputs
    interview_qa: Optional[str]
    """Interview-style Q&A based on the design"""
    
    bbg_explanation: Optional[str]
    """ByteByteGo-style explanation"""
    
    bbg_mermaid: Optional[str]
    """Mermaid diagram for visualization"""
    
    bbg_image_ideas: Optional[str]
    """Image/DIagram ideas for documentation"""
    
    # Metadata and tracking
    pipeline_id: Optional[str]
    """Unique identifier for this pipeline design"""
    
    timestamp: Optional[str]
    """Timestamp of pipeline execution"""
    
    version: Optional[str]
    """Version of the pipeline design"""
    
    metadata: Optional[Dict[str, Any]]
    """Additional metadata and configuration"""
    
    # Error handling
    errors: Optional[List[str]]
    """List of errors encountered during execution"""
    
    warnings: Optional[List[str]]
    """List of warnings generated during execution"""


# Additional specialized state types for specific workflows
class ArchitectureState(TypedDict, total=False):
    """State specific to architecture design workflow"""
    cloud_choice: CloudProvider
    architecture_diagram: str
    component_list: List[str]
    integration_notes: str


class CodeGenerationState(TypedDict, total=False):
    """State specific to code generation workflow"""
    code_template: str
    configuration: Dict[str, Any]
    dependencies: List[str]
    deployment_notes: str


class SecurityState(TypedDict, total=False):
    """State specific to security design workflow"""
    access_controls: Dict[str, str]
    encryption_settings: Dict[str, str]
    compliance_requirements: List[str]
    audit_configuration: Dict[str, Any]


__all__ = [
    "PipelineState",
    "ArchitectureState", 
    "CodeGenerationState",
    "SecurityState",
    "CloudProvider",
    "WorkloadType", 
    "DataSensitivity"
]