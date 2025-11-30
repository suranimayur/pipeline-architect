# 🚀 UV Package Manager Testing Guide

This guide provides UV package manager specific instructions for testing the Pipeline Architect project.

## 📋 Table of Contents
1. [UV Installation](#uv-installation)
2. [UV Environment Setup](#uv-environment-setup)
3. [UV Testing Commands](#uv-testing-commands)
4. [UV Troubleshooting](#uv-troubleshooting)

## 🧪 UV Installation

### Install UV Package Manager
```bash
# Option 1: Using pip (recommended)
pip install uv

# Option 2: Using curl (Linux/Mac)
curl --proto '=https' --tlsv1.2 -sSf https://install.python.org/uv | sh

# Option 3: Using winget (Windows)
winget install -e --id Astral.sh.UV

# Verify installation
uv --version
```

## 🏗️ UV Environment Setup

### Create UV Virtual Environment
```bash
# Create UV virtual environment
uv venv

# Activate environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Windows CMD:
.venv\Scripts\activate.bat

# Linux/Mac:
source .venv/bin/activate

# Verify activation
uv --python --version
```

### Install Dependencies with UV
```bash
# Install production dependencies
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -r requirements-dev.txt

# Install in development mode (editable)
uv pip install -e .

# Install specific package
uv pip install black ruff mypy pytest
```

## 🧪 UV Testing Commands

### Quick Validation with UV
```bash
# Run quick test script with UV
uv run python scripts/quick_test.py

# Validate project structure
uv run python scripts/validate_project.py
```

### Development Testing with UV
```bash
# Test imports
uv run python -c "
import pipeline_architect
print('✅ Pipeline Architect imports work with UV')
"

# Test CLI
uv run python -m pipeline_architect.cli.main --help

# Test API server
uv run uvicorn src.pipeline_architect.api:app --reload --port 8001

# Test with sample input
uv run python -m pipeline_architect.cli.main --prompt "Test pipeline description"
```

### Code Quality with UV
```bash
# Check code formatting
uv run black --check --diff src tests

# Check linting
uv run ruff check src tests

# Check type hints
uv run mypy src

# Run pre-commit hooks
uv run pre-commit run --all-files

# Install and run pre-commit
uv pip install pre-commit
uv run pre-commit install
uv run pre-commit run --all-files
```

### Testing with UV
```bash
# Run unit tests
uv run pytest tests/unit/ -v

# Run integration tests
uv run pytest tests/integration/ -v

# Run E2E tests
uv run pytest tests/e2e/ -v

# Run all tests with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Run specific test
uv run pytest tests/unit/test_config.py -v

# Run tests with verbose output
uv run pytest tests/ -v -s --tb=short

# Run tests in parallel
uv run pytest tests/ -n auto
```

### Performance Testing with UV
```bash
# Benchmark import times
uv run python -m timeit "import pipeline_architect"

# Memory usage testing
uv run python -m memory_profiler tests/benchmark.py

# Load testing API
uv run python -m locust -f tests/load_test.py --headless -u 10 -r 2 -t 60s
```

### Docker Testing with UV
```bash
# Build with UV in Docker
docker build --build-arg UV_INSTALLER_URL=https://install.python.org/uv -t pipeline-architect-uv .

# Run with UV
docker run -e UV_INSTALLER_URL=https://install.python.org/uv pipeline-architect-uv uv run python -m pipeline_architect.cli.main --help
```

## 🐛 UV Troubleshooting

### Common UV Issues

#### 1. UV Not Found
```bash
# Reinstall UV
pip uninstall uv
pip install uv

# Or use pipx (recommended for global installation)
pip install pipx
pipx install uv

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"  # Linux/Mac
```

#### 2. Virtual Environment Issues
```bash
# Clear UV cache
uv cache clean

# Recreate virtual environment
rm -rf .venv
uv venv

# Recreate with specific Python version
uv venv --python 3.11

# Activate environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

#### 3. Dependency Installation Issues
```bash
# Clear cache and retry
uv cache clean
uv pip install -r requirements-dev.txt

# Install with verbose output
uv pip install -r requirements-dev.txt -v

# Install specific version
uv pip install pytest==7.4.0

# Install from wheel
uv pip install --only-binary :all: pytest
```

#### 4. Testing Issues
```bash
# Check UV Python version
uv run python --version

# Check if packages installed
uv run pip list

# Reinstall pytest
uv pip install --force-reinstall pytest

# Run test with debug output
uv run pytest tests/ -v -s --tb=long
```

#### 5. Performance Issues
```bash
# Check UV cache location
uv cache dir

# Clear cache for better performance
uv cache clean

# Use isolated builds
uv pip install --no-build-isolation package_name
```

### UV Environment Variables

```bash
# Set UV cache directory
export UV_CACHE_DIR=~/.cache/uv

# Set Python version
export UV_PYTHON=3.11

# Set index URL
export UV_INDEX_URL=https://pypi.org/simple

# Set extra index URL
export UV_EXTRA_INDEX_URL=https://your-private-index.com/simple
```

### UV Configuration

Create `uv.toml` for project-specific UV settings:

```toml
[uv]
python = "3.11"
index-url = "https://pypi.org/simple"
extra-index-urls = ["https://your-private-index.com/simple"]
cache-dir = ".uv-cache"
```

### UV vs pip Comparison

| Task | pip Command | UV Command |
|------|-------------|------------|
| Install deps | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| Create venv | `python -m venv .venv` | `uv venv` |
| Install editable | `pip install -e .` | `uv pip install -e .` |
| Check deps | `pip check` | `uv pip check` |
| List deps | `pip list` | `uv pip list` |
| Uninstall | `pip uninstall package` | `uv pip uninstall package` |

### UV Best Practices

1. **Always use UV for this project**
   ```bash
   # ✅ Correct
   uv run python script.py
   
   # ❌ Avoid
   python script.py
   ```

2. **Use UV virtual environments**
   ```bash
   # ✅ Correct
   uv venv
   source .venv/bin/activate
   
   # ❌ Avoid
   python -m venv .venv
   ```

3. **Install dependencies with UV**
   ```bash
   # ✅ Correct
   uv pip install -r requirements-dev.txt
   
   # ❌ Avoid
   pip install -r requirements-dev.txt
   ```

4. **Run tests with UV**
   ```bash
   # ✅ Correct
   uv run pytest tests/
   
   # ❌ Avoid
   pytest tests/
   ```

## 📊 UV Performance Benchmarks

### Installation Speed
```bash
# Benchmark pip vs UV
time pip install -r requirements.txt
time uv pip install -r requirements.txt
```

### Test Execution Speed
```bash
# Benchmark test execution
time uv run pytest tests/
time python -m pytest tests/  # For comparison
```

### Memory Usage
```bash
# Check memory usage
uv run python -m memory_profiler script.py
```

---

**🎉 With UV package manager, you get faster dependency resolution, better caching, and improved performance for all Python operations!**

**Key Benefits of UV:**
- ⚡ **Faster**: 10-100x faster than pip
- 🔒 **Secure**: Built-in security features
- 📦 **Compatible**: Drop-in replacement for pip
- 🚀 **Modern**: Rust-based performance
- 💾 **Efficient**: Smart caching system