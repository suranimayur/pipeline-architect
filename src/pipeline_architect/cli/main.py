"""
Main CLI entry point for Pipeline Architect.

This module provides the command-line interface for the pipeline design assistant,
allowing users to run the application from the command line with various options.
"""

import sys
import argparse
from pathlib import Path

from ..core.graph import build_graph
from ..core.state import PipelineState
from ..utils.config import get_settings
from ..utils.logger import setup_logging, get_logger


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Data Pipeline Design Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run interactive CLI
  python -m pipeline_architect.cli.main
  
  # Run with specific input file
  python -m pipeline_architect.cli.main --input-file pipeline_description.txt
  
  # Run with prompt
  python -m pipeline_architect.cli.main --prompt "I have CSV files in Azure Blob..."
  
  # Validate configuration
  python -m pipeline_architect.cli.main --validate
  
  # Show version
  python -m pipeline_architect.cli.main --version
        """
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        help="Pipeline description prompt (instead of interactive input)"
    )
    
    parser.add_argument(
        "--input-file",
        type=Path,
        help="File containing pipeline description"
    )
    
    parser.add_argument(
        "--output-file",
        type=Path,
        help="File to write the output to"
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate configuration and exit"
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--etl-tool",
        choices=["talend", "informatica", "abinitio", "dbt", "snowflake"],
        help="Generate ETL tool-specific design"
    )
    
    return parser.parse_args()


def get_user_input_from_file(file_path: Path) -> str:
    """Read pipeline description from file."""
    try:
        content = file_path.read_text(encoding="utf-8").strip()
        if not content:
            raise ValueError("Input file is empty")
        return content
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)


def get_user_input_interactive() -> str:
    """Get pipeline description from interactive input."""
    print("🧠 AI Data Pipeline Design Assistant (CLI)")
    print("=" * 60)
    print("Describe your data pipeline scenario in one or more sentences.")
    print("\nExample:")
    print("  I have CSV files in Azure Blob (~200GB/day) and want a Delta Lake")
    print("  on Databricks with bronze/silver/gold layers and Power BI on top.")
    print("=" * 60)
    
    try:
        user_input = input("Describe your data pipeline scenario:\n> ").strip()
        if not user_input:
            print("No input provided. Exiting.")
            sys.exit(0)
        return user_input
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)


def run_pipeline_design(prompt: str, etl_tool: str = None) -> PipelineState:
    """Run the pipeline design workflow."""
    logger = get_logger(__name__)
    
    try:
        logger.info("Building pipeline graph...")
        app = build_graph()
        
        logger.info("Initializing pipeline state...")
        state: PipelineState = {"user_query": prompt}
        
        if etl_tool:
            state["etl_tool"] = etl_tool
        
        logger.info("Executing pipeline design...")
        final_state = app.invoke(state)
        
        logger.info("Pipeline design completed successfully")
        return final_state
        
    except Exception as e:
        logger.error(f"Pipeline design failed: {e}", exc_info=True)
        raise


def format_output(state: PipelineState) -> str:
    """Format the pipeline design output."""
    output_lines = []
    
    # Add header
    output_lines.append("# 🧠 AI-Generated Data Pipeline Design")
    output_lines.append("")
    
    # Add metadata
    output_lines.append("## 📋 Metadata")
    output_lines.append(f"- **Timestamp:** {state.get('timestamp', 'N/A')}")
    output_lines.append(f"- **Pipeline ID:** {state.get('pipeline_id', 'N/A')}")
    output_lines.append(f"- **ETL Tool:** {state.get('etl_tool', 'N/A')}")
    output_lines.append("")
    
    # Add architecture
    if state.get("architecture"):
        output_lines.append("## 🏗️ Architecture Overview")
        output_lines.append(state["architecture"])
        output_lines.append("")
    
    # Add PySpark code
    if state.get("pyspark_code"):
        output_lines.append("## 🐍 PySpark / Databricks Starter Code")
        output_lines.append("```python")
        output_lines.append(state["pyspark_code"])
        output_lines.append("```")
        output_lines.append("")
    
    # Add IAM design
    if state.get("iam_design"):
        output_lines.append("## 🔐 IAM & Access Control Design")
        output_lines.append(state["iam_design"])
        output_lines.append("")
    
    # Add cost/performance tips
    if state.get("cost_tips"):
        output_lines.append("## 💰 Cost & Performance Tips")
        output_lines.append(state["cost_tips"])
        output_lines.append("")
    
    # Add ETL design if available
    if state.get("etl_tool_design"):
        output_lines.append("## 🛠️ ETL Tool Design")
        output_lines.append(state["etl_tool_design"])
        output_lines.append("")
    
    # Add orchestration plan
    if state.get("orchestration_plan"):
        output_lines.append("## 📅 Orchestration & Scheduling Plan")
        output_lines.append(state["orchestration_plan"])
        output_lines.append("")
    
    # Add errors/warnings
    errors = state.get("errors", [])
    warnings = state.get("warnings", [])
    
    if errors or warnings:
        output_lines.append("## ⚠️ Notes")
        
        if warnings:
            output_lines.append("### Warnings:")
            for warning in warnings:
                output_lines.append(f"- {warning}")
            output_lines.append("")
        
        if errors:
            output_lines.append("### Errors:")
            for error in errors:
                output_lines.append(f"- {error}")
            output_lines.append("")
    
    return "\n".join(output_lines)


def validate_configuration() -> bool:
    """Validate application configuration."""
    logger = get_logger(__name__)
    
    try:
        logger.info("Validating configuration...")
        settings = get_settings()
        
        # Validate LLM configuration
        if settings.llm.anthropic_api_key or (settings.llm.anthropic_base_url and settings.llm.anthropic_auth_token):
            logger.info("✅ LLM configuration valid")
        else:
            logger.error("❌ LLM configuration invalid - missing API keys")
            return False
        
        # Validate other settings
        logger.info(f"✅ Environment: {settings.environment}")
        logger.info(f"✅ App version: {settings.app_version}")
        
        return True
        
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        return False


def main():
    """Main CLI entry point."""
    args = parse_arguments()
    
    # Set up logging
    setup_logging(level=args.log_level)
    logger = get_logger(__name__)
    
    # Handle version
    if args.version:
        from .. import __version__
        print(f"Pipeline Architect v{__version__}")
        return
    
    # Handle validation
    if args.validate:
        success = validate_configuration()
        sys.exit(0 if success else 1)
    
    # Get pipeline description
    if args.input_file:
        prompt = get_user_input_from_file(args.input_file)
    elif args.prompt:
        prompt = args.prompt
    else:
        prompt = get_user_input_interactive()
    
    try:
        # Run pipeline design
        logger.info("Starting pipeline design...")
        final_state = run_pipeline_design(prompt, args.etl_tool)
        
        # Format output
        output = format_output(final_state)
        
        # Handle output
        if args.output_file:
            args.output_file.write_text(output, encoding="utf-8")
            print(f"✅ Design saved to: {args.output_file}")
        else:
            print("\n" + "=" * 60)
            print("🎯 PIPELINE DESIGN RESULT")
            print("=" * 60)
            print(output)
        
    except Exception as e:
        logger.error(f"Pipeline design failed: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()