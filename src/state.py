from typing import TypedDict, List, Dict, Optional
from typing import TypedDict, Optional

class PipelineState(TypedDict, total=False):
    # Original user prompt
    user_query: str

    # Parsed / inferred fields
    cloud: Optional[str]                 # "azure" | "aws" | "hybrid" | None
    workload_type: Optional[str]         # "batch" | "streaming" | "mixed" | None
    source_systems: Optional[str]
    target_systems: Optional[str]
    data_volume: Optional[str]
    latency_requirements: Optional[str]
    data_sensitivity: Optional[str]

    # Node outputs
    architecture: Optional[str]
    pyspark_code: Optional[str]
    iam_design: Optional[str]
    cost_tips: Optional[str]
    performance_tips: Optional[str]
    final_answer: Optional[str]

    # ByteByteGo-style explainer outputs
    bbg_explanation: Optional[str]
    bbg_mermaid: Optional[str]
    bbg_image_ideas: Optional[str]
    
    #ETL Tool Selection
    python_design_code: Optional[str]   # Python orchestration / design code
    etl_tool: Optional[str]             # "talend" | "informatica" | "abinitio" | "dbt" | "snowflake" | None
    etl_tool_design: Optional[str]      # Pseudo-code / job design for chosen ETL tool
    
    # DBT and Snowflake designs
    dbt_design: Optional[str]           # DBT pipeline design
    snowflake_design: Optional[str]     # Snowflake pipeline design
