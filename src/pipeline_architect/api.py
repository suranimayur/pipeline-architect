"""
FastAPI web server for Pipeline Architect.

This module provides a REST API for the pipeline design assistant,
allowing programmatic access to the pipeline generation functionality.
"""

import os
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .core.graph import build_graph
from .core.state import PipelineState
from .utils.config import get_settings
from .utils.logger import setup_logging, get_logger


class PipelineRequest(BaseModel):
    """Request model for pipeline design."""
    description: str
    etl_tool: str = None


class PipelineResponse(BaseModel):
    """Response model for pipeline design."""
    success: bool
    message: str = ""
    data: Dict[str, Any] = {}


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    details: Dict[str, Any] = {}


# Initialize settings and logging
settings = get_settings()
setup_logging(level=settings.logging.level)

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
if settings.security.allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    
    # Validate configuration
    if not settings.llm.anthropic_api_key and not (settings.llm.anthropic_base_url and settings.llm.anthropic_auth_token):
        logger.warning("LLM API keys not configured properly")
    
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on application shutdown."""
    logger.info("Shutting down application")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "success": True,
        "message": f"{settings.app_name} v{settings.app_version}",
        "environment": settings.environment,
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "design": "/api/v1/design"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "success": True,
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment
    }


@app.post("/api/v1/design", response_model=PipelineResponse)
async def design_pipeline(request: PipelineRequest):
    """
    Generate a data pipeline design based on the provided description.
    
    Args:
        request: Pipeline design request with description
        
    Returns:
        Pipeline design response with all generated components
    """
    try:
        logger.info(f"Received pipeline design request")
        logger.debug(f"Request description: {request.description[:100]}...")
        
        # Build and run pipeline graph
        graph_app = build_graph()
        state: PipelineState = {"user_query": request.description}
        
        # Add ETL tool selection if provided
        if request.etl_tool:
            state["etl_tool"] = request.etl_tool
        
        # Execute pipeline
        out_state = graph_app.invoke(state)
        
        # Extract relevant data
        response_data = {
            "final_answer": out_state.get("final_answer", ""),
            "architecture": out_state.get("architecture"),
            "pyspark_code": out_state.get("pyspark_code"),
            "iam_design": out_state.get("iam_design"),
            "cost_tips": out_state.get("cost_tips"),
            "performance_tips": out_state.get("performance_tips"),
            "etl_tool_design": out_state.get("etl_tool_design"),
            "dbt_design": out_state.get("dbt_design"),
            "snowflake_design": out_state.get("snowflake_design"),
            "python_design_code": out_state.get("python_design_code"),
            "orchestration_plan": out_state.get("orchestration_plan"),
            "airflow_dag_code": out_state.get("airflow_dag_code"),
            "interview_qa": out_state.get("interview_qa"),
            "pipeline_id": out_state.get("pipeline_id"),
            "timestamp": out_state.get("timestamp")
        }
        
        logger.info("Pipeline design completed successfully")
        
        return PipelineResponse(
            success=True,
            message="Pipeline design generated successfully",
            data=response_data
        )
        
    except Exception as e:
        logger.error(f"Pipeline design failed: {e}", exc_info=True)
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Pipeline design generation failed",
                "message": str(e)
            }
        )


@app.post("/api/v1/validate", response_model=PipelineResponse)
async def validate_pipeline(request: PipelineRequest):
    """
    Validate a pipeline description without generating the full design.
    
    Args:
        request: Pipeline description to validate
        
    Returns:
        Validation result
    """
    try:
        logger.info("Received pipeline validation request")
        
        # Basic validation of input
        if not request.description or len(request.description.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid input",
                    "message": "Description must be at least 10 characters long"
                }
            )
        
        # Run input parser to validate
        from .nodes.input_parser import input_parser_node
        
        state: PipelineState = {"user_query": request.description}
        parsed_state = input_parser_node(state)
        
        # Check if parsing was successful
        if not parsed_state.get("cloud") and not parsed_state.get("workload_type"):
            return PipelineResponse(
                success=False,
                message="Input validation passed but could not extract key information",
                data={
                    "parsed_fields": {
                        "cloud": parsed_state.get("cloud"),
                        "workload_type": parsed_state.get("workload_type"),
                        "source_systems": parsed_state.get("source_systems"),
                        "target_systems": parsed_state.get("target_systems"),
                        "data_volume": parsed_state.get("data_volume"),
                        "latency_requirements": parsed_state.get("latency_requirements"),
                        "data_sensitivity": parsed_state.get("data_sensitivity")
                    }
                }
            )
        
        logger.info("Pipeline validation completed successfully")
        
        return PipelineResponse(
            success=True,
            message="Pipeline description is valid and can be processed",
            data={
                "parsed_fields": {
                    "cloud": parsed_state.get("cloud"),
                    "workload_type": parsed_state.get("workload_type"),
                    "source_systems": parsed_state.get("source_systems"),
                    "target_systems": parsed_state.get("target_systems"),
                    "data_volume": parsed_state.get("data_volume"),
                    "latency_requirements": parsed_state.get("latency_requirements"),
                    "data_sensitivity": parsed_state.get("data_sensitivity")
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pipeline validation failed: {e}", exc_info=True)
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Pipeline validation failed",
                "message": str(e)
            }
        )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle uncaught exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run with uvicorn
    uvicorn.run(
        "src.pipeline_architect.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.logging.level.lower()
    )