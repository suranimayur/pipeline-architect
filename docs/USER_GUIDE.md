# User Guide

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Using the Streamlit Interface](#using-the-streamlit-interface)
4. [Using the CLI](#using-the-cli)
5. [Using the FastAPI Server](#using-the-fastapi-server)
6. [Input Guidelines](#input-guidelines)
7. [Output Interpretation](#output-interpretation)
8. [ETL Tool Support](#etl-tool-support)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

## Overview

The AI Data Pipeline Design Assistant helps you design comprehensive data pipelines by analyzing your requirements and generating:
- Cloud architecture diagrams and descriptions
- PySpark/Databricks code templates
- IAM and security configurations
- Cost and performance optimization recommendations
- ETL tool-specific designs
- Orchestration plans and Airflow DAGs
- Interview-style Q&A

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Anthropic API access (Claude)
- Optional: OpenAI API for image generation

### Installation
```bash
# Clone the repository
git clone https://github.com/your-org/pipeline-architect.git
cd pipeline-architect

# Set up virtual environment
uv venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

## Using the Streamlit Interface

The Streamlit interface provides a user-friendly web application for pipeline design.

### Launching the Interface
```bash
uv run streamlit run src/streamlit_app.py
```

### Interface Overview

#### 1. Input Section
- **Pipeline Description**: Describe your data pipeline requirements in natural language
- **ETL Tool Selection**: Choose from Talend, Informatica, Ab Initio, DBT, or Snowflake
- **Generate Button**: Click to start the pipeline design process

#### 2. Output Tabs
- **🏗 Architecture**: Cloud architecture design and recommendations
- **🐍 PySpark Code**: Generated PySpark/Databricks code
- **🔐 IAM**: Security and access control design
- **💰 Cost & Performance**: Optimization recommendations
- **⚙️ Python Design**: Python orchestration code
- **🛠 ETL Design**: ETL tool-specific designs
- **🏗️ DBT Design**: DBT project structure and models
- **❄️ Snowflake Design**: Snowflake-native ETL design
- **📅 Orchestration / DAG**: Airflow DAG and scheduling plans
- **🧠 Interview Q&A**: Technical questions and answers

### Input Examples

#### Example 1: Azure Delta Lake Pipeline
```
I have CSV files landing in Azure Blob (~200GB/day) and want to build a 
bronze-silver-gold Delta Lake in Azure Databricks and expose curated tables 
to Power BI. Daily batch is fine, there is customer PII like email and phone.
```

#### Example 2: AWS Streaming Pipeline
```
I need a real-time streaming pipeline for IoT sensor data (50K events/sec) 
using AWS Kinesis, processing with Spark Structured Streaming, storing in 
Delta Lake on EMR, and serving to AWS QuickSight. Data contains sensitive 
sensor readings that need encryption.
```

#### Example 3: Snowflake Native Pipeline
```
Design a Snowflake-native ETL pipeline for e-commerce data. Sources include 
Shopify orders, customer data from Salesforce, and product catalog from MySQL. 
Need to handle 1M transactions/day with real-time inventory updates.
```

## Using the CLI

The command-line interface provides a text-based way to generate pipeline designs.

### Running the CLI
```bash
uv run python src/main.py
```

### CLI Workflow
1. The application will prompt you to enter a pipeline description
2. Enter your requirements in natural language
3. The system will process your input and generate the pipeline design
4. Results will be displayed in the terminal

### CLI Output
The CLI displays a formatted summary of all generated components:
- Architecture overview
- Code snippets
- Security considerations
- Performance recommendations

## Using the FastAPI Server

The FastAPI server provides a REST API for programmatic access to the pipeline design functionality.

### Starting the Server
```bash
uv run uvicorn src.api:app --reload
```

### API Endpoints

#### Root Endpoint
- **GET /**: Health check and usage information

#### Design Endpoint
- **POST /design**: Generate pipeline design

**Request Body:**
```json
{
  "description": "Your pipeline description here"
}
```

**Response:**
```json
{
  "final_answer": "Complete pipeline design summary",
  "architecture": "Architecture details",
  "pyspark_code": "Generated PySpark code",
  "iam_design": "IAM and security design",
  "cost_tips": "Cost optimization recommendations",
  "performance_tips": "Performance optimization recommendations"
}
```

### API Usage Examples

#### Using curl
```bash
curl -X POST "http://localhost:8000/design" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "I have CSV files landing in Azure Blob (~200GB/day)..."
  }'
```

#### Using Python
```python
import requests

url = "http://localhost:8000/design"
data = {
    "description": "I have CSV files landing in Azure Blob (~200GB/day)..."
}

response = requests.post(url, json=data)
result = response.json()
print(result["final_answer"])
```

## Input Guidelines

### What to Include in Your Description

1. **Data Sources**
   - File formats (CSV, JSON, Parquet, etc.)
   - Data volume and frequency
   - Source systems (databases, APIs, files)

2. **Processing Requirements**
   - Batch vs. streaming
   - Transformation complexity
   - Data quality requirements

3. **Target Systems**
   - Destination platforms (Power BI, Snowflake, etc.)
   - Reporting needs
   - Data access patterns

4. **Cloud Platform**
   - Azure, AWS, GCP, or hybrid
   - Specific services (Databricks, Redshift, etc.)

5. **Security Requirements**
   - Data sensitivity (PII, financial, etc.)
   - Compliance requirements
   - Access control needs

6. **Performance Requirements**
   - Latency expectations
   - Throughput requirements
   - Scalability needs

### Input Quality Tips

**Good Examples:**
- "I have 500GB/day of JSON logs from web servers that need real-time processing for fraud detection"
- "Customer transaction data from MySQL (~100GB) needs ETL to Snowflake with daily updates"
- "Sensor data (10K events/sec) requires streaming processing with anomaly detection"

**Needs Improvement:**
- "I need a data pipeline" (too vague)
- "Data stuff" (insufficient detail)
- "Make it work" (no requirements specified)

## Output Interpretation

### Architecture Design

The architecture section provides:
- **Cloud service recommendations** (Azure Blob, S3, etc.)
- **Data flow diagrams** (text-based)
- **Service integration patterns**
- **Scalability considerations**

### PySpark Code

Generated code includes:
- **Data ingestion** from specified sources
- **Bronze layer** raw data storage
- **Silver layer** cleaned and standardized data
- **Gold layer** business-ready data
- **Partitioning strategies** for performance
- **Error handling** and logging

### IAM Design

Security recommendations cover:
- **Role-based access control** (RBAC)
- **Data masking policies** for PII
- **Encryption requirements** (at rest and in transit)
- **Audit logging** configurations
- **Zero-trust architecture** principles

### Cost & Performance Tips

Optimization recommendations include:
- **Autoscaling configurations**
- **Data partitioning strategies**
- **Caching mechanisms**
- **Resource sizing guidelines**
- **Cost monitoring setup**

## ETL Tool Support

### Talend
- **Component-based job designs**
- **tMap transformations** for data mapping
- **tFileInputDelimited** for file processing
- **Connection management** for databases
- **Error handling** and logging patterns

### Informatica
- **Source Qualifier** configurations
- **Expression transformations** for calculations
- **Lookup transformations** for data enrichment
- **Aggregator transformations** for summarization
- **Target load strategies** for performance

### Ab Initio
- **Graph-based workflows**
- **Reformat transformations** for data structure changes
- **Join components** for data merging
- **Rollup operations** for aggregation
- **Partitioning strategies** for parallel processing

### DBT (Data Build Tool)
- **Project structure** with staging, marts, and models
- **YAML schema files** with column descriptions and tests
- **Jinja templating** for dynamic SQL generation
- **Materialization strategies** (table, view, incremental)
- **CI/CD integration** for deployment

### Snowflake
- **Native ETL design** using Snowflake features
- **Stage configurations** for data loading
- **Pipe setups** for continuous ingestion
- **Stream implementations** for CDC
- **Task scheduling** for automation
- **Stored procedures** for complex logic

## Troubleshooting

### Common Issues

#### API Key Errors
**Problem:** "Invalid API key" or authentication failures
**Solution:**
1. Verify your API key in `.env` file
2. Check for typos or extra spaces
3. Ensure the key has the required permissions
4. Test with the API provider's console

#### Timeout Errors
**Problem:** API calls timing out
**Solution:**
1. Increase `API_TIMEOUT_MS` in `.env`
2. Check your internet connection
3. Verify API service status
4. Try a simpler pipeline description

#### Dependency Issues
**Problem:** Import errors or missing packages
**Solution:**
1. Reinstall dependencies: `uv pip install -r requirements.txt`
2. Check Python version compatibility
3. Verify virtual environment activation
4. Check for conflicting package versions

#### Streamlit Issues
**Problem:** Streamlit not starting or displaying errors
**Solution:**
1. Ensure Streamlit is installed: `uv pip install streamlit`
2. Check for port conflicts (default: 8501)
3. Verify all dependencies are installed
4. Check Streamlit logs for specific errors

### Getting Help

1. **Check the logs** for detailed error messages
2. **Review the troubleshooting guide** in docs/
3. **Search existing issues** on GitHub
4. **Create a new issue** with detailed information:
   - Python version
   - Package versions
   - Error messages
   - Steps to reproduce

### Debug Mode

Enable debug logging by setting:
```bash
LOG_LEVEL=DEBUG
```

This provides detailed information about:
- API calls and responses
- Internal processing steps
- Error details and stack traces

## Best Practices

### For Input Descriptions

1. **Be Specific**: Include data volumes, frequencies, and formats
2. **Define Requirements**: Clearly state performance and security needs
3. **Provide Context**: Explain the business use case
4. **Include Constraints**: Mention budget, timeline, or technical limitations

### For Production Use

1. **API Key Management**:
   - Use environment variables
   - Implement key rotation
   - Monitor usage and set alerts

2. **Error Handling**:
   - Implement retry logic
   - Handle rate limiting
   - Log errors for analysis

3. **Performance Optimization**:
   - Cache results when appropriate
   - Use asynchronous processing
   - Monitor response times

4. **Security**:
   - Validate all inputs
   - Use HTTPS for API calls
   - Implement proper access controls

### For Team Collaboration

1. **Document Assumptions**: Record decisions and rationale
2. **Version Control**: Track changes to pipeline designs
3. **Code Reviews**: Review generated code for quality
4. **Testing**: Validate designs in development environments

### For Scaling

1. **Modular Design**: Break complex pipelines into smaller components
2. **Reusable Components**: Create templates for common patterns
3. **Monitoring**: Implement metrics and alerting
4. **Documentation**: Maintain up-to-date architecture documentation

## Next Steps

After generating your pipeline design:

1. **Review the Architecture**: Ensure it meets your requirements
2. **Validate the Code**: Test the generated PySpark code
3. **Implement Security**: Apply IAM and access control recommendations
4. **Optimize Performance**: Apply cost and performance tips
5. **Choose ETL Tools**: Select the most appropriate tools for your needs
6. **Plan Orchestration**: Set up scheduling and monitoring
7. **Prepare for Interviews**: Review the Q&A section for technical discussions

For additional help or questions, please refer to our [FAQ](faq.md) or [create an issue](https://github.com/your-org/pipeline-architect/issues).