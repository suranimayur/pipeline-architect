# 🧪 Testing Guide for Pipeline Architect

This guide provides comprehensive instructions for testing the Pipeline Architect project at every level.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start Testing (UV Package Manager)](#quick-start-testing-uv-package-manager)
3. [Testing Levels](#testing-levels)
4. [Testing with Docker](#testing-with-docker)
5. [CI/CD Testing (UV Package Manager)](#cicd-testing-uv-package-manager)
6. [Troubleshooting (UV Package Manager)](#troubleshooting-uv-package-manager)

## 🎯 Prerequisites

Before testing, ensure you have:

- **Python 3.11+** installed
- **uv** package manager (recommended) or pip
- **Docker** and **Docker Compose** (for containerized testing)
- **Git** for version control

### Environment Setup (UV Package Manager)
```bash
# Clone the repository
git clone https://github.com/pipeline-architect/pipeline-architect.git
cd pipeline-architect

# Create UV environment
uv venv

# Activate virtual environment (UV)
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# Install dependencies with UV
uv pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (see below)
```

### Required Environment Variables
For basic testing, you need at least one LLM API key:

```bash
# Option 1: Anthropic Claude (recommended)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Option 2: Anthropic with proxy
ANTHROPIC_BASE_URL=https://your-proxy-endpoint.com
ANTHROPIC_AUTH_TOKEN=your_proxy_auth_token

# Option 3: OpenAI (for image generation)
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Quick Start Testing

### 1. **Configuration Validation**
```bash
# Test configuration
python -c "
from pipeline_architect.utils.config import get_settings
settings = get_settings()
print('✅ Configuration valid!')
print(f'Environment: {settings.environment}')
print(f'LLM Provider: {settings.llm.anthropic_api_key is not None and \"Anthropic\" or \"Proxy\"}')
"
```

### 2. **Import Testing**
```bash
# Test all imports work correctly
python -c "
import pipeline_architect
from pipeline_architect.core.graph import build_graph
from pipeline_architect.core.state import PipelineState
from pipeline_architect.cli.main import main
print('✅ All imports successful!')
"
```

### 3. **CLI Interface Test**
```bash
# Test CLI help
python -m pipeline_architect.cli.main --help

# Test version
python -m pipeline_architect.cli.main --version
```

### 4. **API Server Test**
```bash
# Start API server in background
uvicorn src.pipeline_architect.api:app --host 0.0.0.0 --port 8000 &

# Test health endpoint
curl http://localhost:8000/health

# Test API documentation
# Open browser to: http://localhost:8000/docs
```

## 🧪 Testing Levels

### Level 1: Unit Tests
Test individual components in isolation.

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific unit tests
pytest tests/unit/test_config.py -v
pytest tests/unit/test_state.py -v
pytest tests/unit/test_llm_service.py -v

# Run with coverage
pytest tests/unit/ --cov=src --cov-report=html
```

**Expected Output:**
```
tests/unit/test_config.py::test_llm_settings PASSED
tests/unit/test_config.py::test_security_settings PASSED
tests/unit/test_config.py::test_validation_errors PASSED
... [more tests]
```

### Level 2: Integration Tests
Test component interactions.

```bash
# Run integration tests
pytest tests/integration/ -v

# Integration tests with real LLM (requires API key)
pytest tests/integration/test_llm_integration.py -v -k "not mock"

# Mocked integration tests
pytest tests/integration/ -v -k "mock"
```

### Level 3: End-to-End Tests
Test complete workflow scenarios.

```bash
# Run E2E tests
pytest tests/e2e/ -v

# E2E test with full pipeline
pytest tests/e2e/test_full_pipeline.py -v

# E2E test with different ETL tools
pytest tests/e2e/test_etl_tools.py -v
```

### Level 4: Manual Testing
Interactive testing of the application.

#### CLI Testing (UV Package Manager)
```bash
# Test with sample input
uv run python -m pipeline_architect.cli.main --prompt "I have CSV files in Azure Blob and want a Delta Lake on Databricks"

# Test with file input
echo "Design a streaming pipeline for IoT data" > test_input.txt
uv run python -m pipeline_architect.cli.main --input-file test_input.txt --output-file test_output.md

# Test ETL tool selection
uv run python -m pipeline_architect.cli.main --prompt "E-commerce data pipeline" --etl-tool dbt
```

#### API Testing (UV Package Manager)
```bash
# Test pipeline design endpoint
uv run uvicorn src.pipeline_architect.api:app --host 0.0.0.0 --port 8000 &

curl -X POST "http://localhost:8000/api/v1/design" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "I have CSV files landing in Azure Blob (~200GB/day) and want to build a bronze-silver-gold Delta Lake in Azure Databricks"
  }'

# Test validation endpoint
curl -X POST "http://localhost:8000/api/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Test pipeline description"
  }'
```

## 🐳 Testing with Docker

### Quick Docker Test
```bash
# Build and run Docker image
docker build -t pipeline-architect:latest .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_api_key \
  pipeline-architect:latest

# Test Docker health check
curl http://localhost:8000/health
```

### Docker Compose Testing
```bash
# Start full stack
docker-compose up -d

# Check all services
docker-compose ps

# View logs
docker-compose logs pipeline-architect

# Test API
curl http://localhost:8000/health
```

### Docker Health Check
```bash
# Test container health
docker ps  # Should show "healthy" status

# Test application health
curl http://localhost:8000/health
# Expected: {"success":true,"status":"healthy","version":"1.0.0","environment":"production"}
```

## 🔄 CI/CD Testing (UV Package Manager)

### GitHub Actions Simulation
```bash
# Run code quality checks (as in CI)
uv run black --check --diff src tests
uv run ruff check src tests
uv run mypy src

# Run tests (as in CI)
uv run pytest tests/ -v --cov=src --cov-report=xml

# Security scan (as in CI)
uv run bandit -r src/ -f json -o bandit-report.json
```

### Pre-commit Hook Testing (UV Package Manager)
```bash
# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files

# Expected: All hooks should pass
```

## 🧪 Test Scenarios

### Scenario 1: Basic Pipeline Design
**Input:** Simple Azure pipeline description
**Expected:** Complete architecture, code, and recommendations

```bash
python -m pipeline_architect.cli.main --prompt "Azure Blob to Databricks Delta Lake pipeline"
```

### Scenario 2: AWS Streaming Pipeline
**Input:** Real-time streaming requirements
**Expected:** Kinesis, Glue, and streaming architecture

```bash
python -m pipeline_architect.cli.main --prompt "IoT sensor data streaming pipeline with 50K events/sec"
```

### Scenario 3: Snowflake Native Pipeline
**Input:** Snowflake-specific requirements
**Expected:** Snowflake stages, pipes, and native features

```bash
python -m pipeline_architect.cli.main --prompt "Shopify e-commerce data to Snowflake" --etl-tool snowflake
```

### Scenario 4: DBT Pipeline Design
**Input:** DBT-focused pipeline
**Expected:** DBT models, YAML schemas, and Jinja templates

```bash
python -m pipeline_architect.cli.main --prompt "Customer data pipeline with DBT transformations" --etl-tool dbt
```

## 🔍 Test Validation Checklist

### ✅ Configuration Tests
- [ ] Environment variables loaded correctly
- [ ] Configuration validation passes
- [ ] LLM API keys configured
- [ ] Security settings applied

### ✅ Unit Tests
- [ ] All unit tests pass (coverage > 90%)
- [ ] Configuration validation works
- [ ] State management functions correctly
- [ ] LLM service integration works

### ✅ Integration Tests
- [ ] CLI interface works
- [ ] API server starts and responds
- [ ] Database connections (if any) work
- [ ] External API calls work

### ✅ E2E Tests
- [ ] Full pipeline workflow works
- [ ] All ETL tool designs generate correctly
- [ ] Output formatting is correct
- [ ] Error handling works

### ✅ Docker Tests
- [ ] Docker build succeeds
- [ ] Container starts successfully
- [ ] Health checks pass
- [ ] Application responds correctly

### ✅ Performance Tests
- [ ] Response times are acceptable (< 30s)
- [ ] Memory usage is reasonable
- [ ] No memory leaks
- [ ] Concurrent requests handled

### ✅ Security Tests
- [ ] Input validation works
- [ ] Sensitive data is masked in logs
- [ ] API keys are not exposed
- [ ] CORS is configured correctly

## 🐛 Troubleshooting

### Common Issues (UV Package Manager)

#### 1. Import Errors
```bash
# Issue: ModuleNotFoundError
# Solution: Ensure PYTHONPATH is set correctly
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or install in development mode with UV
uv pip install -e .
```

#### 2. API Key Issues
```bash
# Issue: LLM API calls failing
# Solution: Check environment variables
echo $ANTHROPIC_API_KEY  # Should not be empty

# Test LLM connection
uv run python -c "
from pipeline_architect.services.llm_service import get_llm_service
service = get_llm_service()
print('✅ LLM Service working')
"
```

#### 3. Docker Issues
```bash
# Issue: Container won't start
# Solution: Check logs
docker logs <container_id>

# Issue: Port already in use
# Solution: Change port in docker-compose.yml or use different port
```

#### 4. Test Failures
```bash
# Issue: Tests failing
# Solution: Run with verbose output
uv run pytest tests/ -v -s --tb=long

# Check specific test
uv run pytest tests/unit/test_example.py::test_specific_function -v -s
```

#### 5. Performance Issues
```bash
# Issue: Slow response times
# Solution: Check API key limits and network
# Monitor with: docker stats
# Check logs for timeouts or errors
```

#### 6. UV Package Manager Issues
```bash
# Issue: UV not found
# Solution: Install UV
pip install uv

# Issue: Dependencies not installing
# Solution: Clear UV cache and retry
uv cache clean
uv pip install -r requirements-dev.txt

# Issue: Virtual environment not working
# Solution: Recreate UV environment
rm -rf .venv
uv venv
uv run python -c "print('✅ UV environment working')"
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debug
python -m pipeline_architect.cli.main --log-level DEBUG --prompt "test"
```

### Getting Help
- Check [GitHub Issues](https://github.com/pipeline-architect/pipeline-architect/issues)
- Review [Documentation](docs/)
- Ask in [GitHub Discussions](https://github.com/pipeline-architect/pipeline-architect/discussions)

## 📊 Test Results Template

After running tests, document results:

```
Test Date: YYYY-MM-DD
Environment: [development/staging/production]
Python Version: 3.11.x
Dependencies: [list key versions]

Unit Tests: ✅ PASSED (XX/XX)
Integration Tests: ✅ PASSED (XX/XX)
E2E Tests: ✅ PASSED (XX/XX)
Docker Tests: ✅ PASSED (XX/XX)
Performance: ✅ PASSED (Response time: X.Xs)
Security: ✅ PASSED (No vulnerabilities found)

Issues Found: [List any issues]
Resolution: [How issues were resolved]

Overall Status: ✅ READY FOR PRODUCTION
```

---

**Happy Testing! 🧪✨**