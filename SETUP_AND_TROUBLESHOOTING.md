# AI Data Pipeline Design Assistant - Setup & Troubleshooting

## 🔧 Setup Instructions

### Using uv Package Manager (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   # Windows
   winget install uv
   
   # macOS
   brew install uv
   
   # Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Setup the environment**:
   ```bash
   cd d:\Python_Projects\pipeline_architect
   python setup_with_uv.py
   ```

3. **Activate virtual environment**:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

## 🚀 Running the Application

### Option 1: Streamlit Web App
```bash
streamlit run streamlit_app.py
```

### Option 2: FastAPI Server
```bash
uvicorn api:app --reload
```

### Option 3: CLI Version
```bash
python main.py
```

## 🔍 API Configuration

### Environment Variables (.env file)

```env
# For proxy configuration (Kat Coder)
ANTHROPIC_BASE_URL=https://vanchin.streamlake.ai/api/gateway/v1/endpoints/ep-ojxxnc-1763307745318216617/claude-code-proxy
ANTHROPIC_AUTH_TOKEN=Vrx_44YXeKtTRscaucoafIcqxfhbXqwzdm9kxQ64jEk
API_TIMEOUT_MS=3000000
ANTHROPIC_MODEL=KAT-Coder
ANTHROPIC_SMALL_FAST_MODEL=KAT-Coder

# Alternative: For direct Anthropic API
# ANTHROPIC_API_KEY=your_api_key_here
```

## 🐛 Troubleshooting

### Error: "Missing Action parameter" (400 Bad Request)

**Symptoms:**
- `anthropic.BadRequestError: Error code: 400 - {'request_id': '...', 'ResponseMeta': {'RequestId': '...', 'ErrorCode': 'InvalidArgument', 'ErrorMessage': 'Missing Action parameter'}}`

**Root Cause:**
This error typically occurs when the proxy server expects specific headers or authentication format that aren't being sent correctly.

**Solutions:**

1. **Verify .env file format**:
   - Remove quotes from environment variables
   - Ensure no trailing spaces
   - Use format: `KEY=VALUE` (not `KEY="VALUE"`)

2. **Check proxy configuration**:
   - Verify `ANTHROPIC_BASE_URL` points to the correct proxy endpoint
   - Ensure `ANTHROPIC_AUTH_TOKEN` is valid and not expired

3. **Test API connection**:
   ```bash
   python test_api_config.py
   ```

4. **Debug mode**:
   The `llm.py` file now includes debug prints. Run the app and check the logs for:
   - Base URL being used
   - Auth token format
   - API call details

### Error: ModuleNotFoundError

**Symptoms:**
```
ModuleNotFoundError: No module named 'dotenv'
```

**Solution:**
```bash
# Activate virtual environment first
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
uv pip install -r requirements.txt
```

### Error: Connection Timeout

**Symptoms:**
- API calls timeout after 30 seconds
- Network errors when calling Anthropic API

**Solutions:**

1. **Increase timeout** in `.env`:
   ```env
   API_TIMEOUT_MS=600000  # 10 minutes
   ```

2. **Check network connectivity**:
   - Verify internet connection
   - Check if proxy URL is accessible
   - Try pinging the proxy endpoint

### Error: Authentication Failed

**Symptoms:**
- 401 Unauthorized errors
- Invalid API key messages

**Solutions:**

1. **Verify credentials**:
   - Check if `ANTHROPIC_AUTH_TOKEN` is correct
   - Ensure token hasn't expired

2. **Test with curl**:
   ```bash
   curl -X POST "https://vanchin.streamlake.ai/api/gateway/v1/endpoints/ep-ojxxnc-1763307745318216617/claude-code-proxy/v1/messages" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"model":"KAT-Coder","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]}'
   ```

## 🔧 Debugging Tools

### Test Script
Run the test script to verify API configuration:
```bash
python test_api_config.py
```

This will:
- Load environment variables
- Create Anthropic client with proxy settings
- Test a simple API call
- Display detailed error information if it fails

### Debug Logs
The application now includes debug prints in `llm.py`:
- Shows Base URL being used
- Shows Auth token (first 10 chars)
- Shows API call details
- Shows success/failure status

## 📝 Configuration Tips

1. **Model Selection**:
   - Use `KAT-Coder` for the proxy
   - Use `claude-3-5-sonnet-latest` for direct Anthropic API

2. **Timeout Settings**:
   - Default: 300 seconds (5 minutes)
   - Increase for complex queries: 600-900 seconds

3. **Headers**:
   - The proxy expects `Authorization: Bearer {token}`
   - Content-Type should be `application/json`

## 🚨 Common Issues

### Issue: "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC= 1"
This environment variable should not have a space after the equals sign:
```env
# ❌ Wrong
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC= 1

# ✅ Correct
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
```

### Issue: Proxy URL Format
Ensure the proxy URL is correct and doesn't have trailing spaces:
```env
# ❌ Wrong
ANTHROPIC_BASE_URL="https://example.com/proxy "

# ✅ Correct
ANTHROPIC_BASE_URL=https://example.com/proxy
```

## 📞 Getting Help

If you're still experiencing issues:

1. Run `python test_api_config.py` and share the output
2. Check the debug logs in the application
3. Verify your network connection and proxy settings
4. Contact support with:
   - The exact error message
   - Your `.env` file (with sensitive info redacted)
   - Output from the test script
   - Debug logs from `llm.py`

## 🆕 New Features: DBT and Snowflake ETL Designs

### DBT (Data Build Tool) Support

The application now supports generating comprehensive DBT pipeline designs including:

- **DBT Project Architecture**: Complete project structure with staging, intermediate, and marts layers
- **YAML Schema Files**: Column descriptions, data tests, and documentation
- **Jinja Templating**: Reusable macros and dynamic SQL generation
- **Materialization Strategies**: Table, view, and incremental materializations
- **Performance Optimization**: Best practices for DBT models and transformations
- **CI/CD Integration**: Deployment and testing strategies

**Example Output Structure:**
```
models/
├── staging/
│   ├── staging_sales.yml
│   └── staging_sales.sql
├── marts/
│   ├── marts_customer.yml
│   └── marts_customer.sql
├── macros/
│   └── mask_pii.sql
└── dbt_project.yml
```

### Snowflake Native ETL Support

The application now supports generating Snowflake-native ETL pipeline designs including:

- **Database & Schema Design**: Bronze, silver, gold layer architecture
- **Data Ingestion**: Stages and Pipes for continuous loading
- **Change Data Capture**: Streams for tracking data changes
- **Orchestration**: Tasks for scheduling and automation
- **Stored Procedures**: Complex business logic implementation
- **Performance Optimization**: Clustering keys, materialized views, virtual warehouse sizing
- **Security**: RBAC, data masking, and row access policies

**Example Components Generated:**
```sql
-- Stage for data ingestion
CREATE OR REPLACE STAGE my_stage URL='s3://bucket/path';

-- Pipe for auto-ingestion
CREATE OR REPLACE PIPE my_pipe AUTO_INGEST=TRUE
AS COPY INTO bronze_table FROM @my_stage;

-- Stream for CDC
CREATE OR REPLACE STREAM my_stream ON TABLE bronze_table;

-- Task for orchestration
CREATE OR REPLACE TASK my_task
WAREHOUSE=compute_warehouse
SCHEDULE='USING CRON 0 2 * * * UTC'
AS MERGE INTO silver_table USING (SELECT * FROM bronze_table)...
```

### Usage

1. **Select ETL Tool**: In the Streamlit app, choose "DBT" or "Snowflake" from the ETL tool dropdown
2. **Generate Design**: After running the base pipeline, the app will automatically generate the selected ETL design
3. **View Results**: Find the dedicated tabs for "🏗️ DBT Design" and "❄️ Snowflake Design"

### Architecture Integration

The new ETL designs integrate seamlessly with the existing pipeline architecture:
- **Input Parser**: Extracts requirements for DBT/Snowflake specific features
- **Architecture Planner**: Designs compatible cloud architecture
- **Code Generator**: Creates PySpark code that works with DBT/Snowflake layers
- **ETL Designers**: Generate tool-specific implementations
- **Orchestration**: Coordinates between different ETL tools and Airflow