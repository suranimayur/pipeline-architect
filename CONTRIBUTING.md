# Contributing to AI Data Pipeline Design Assistant

Thank you for considering contributing to the AI Data Pipeline Design Assistant! We welcome contributions from everyone.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Development Setup](#development-setup)
4. [Coding Guidelines](#coding-guidelines)
5. [Testing](#testing)
6. [Submitting Changes](#submitting-changes)
7. [Issue Reporting](#issue-reporting)
8. [Feature Requests](#feature-requests)
9. [Documentation](#documentation)
10. [Community](#community)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful in all interactions and avoid any discriminatory, offensive, or harassing behavior.

## How to Contribute

There are many ways to contribute:

- 🐛 **Report bugs** - Create issues for bugs you find
- 💡 **Request features** - Suggest new features or improvements
- 📝 **Improve documentation** - Help make our docs better
- 🔧 **Write code** - Submit pull requests for new features or bug fixes
- 🧪 **Testing** - Help improve test coverage
- 📖 **Help others** - Answer questions in issues or discussions

## Development Setup

### Prerequisites

- Python 3.11 or higher
- uv package manager
- Git

### Setup Process

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pipeline-architect.git
   cd pipeline-architect
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   uv venv
   
   # Activate virtual environment
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   
   # Install development dependencies
   uv pip install -r requirements-dev.txt
   
   # Install pre-commit hooks
   pre-commit install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys for testing
   ```

4. **Verify setup**
   ```bash
   # Run tests
   uv run pytest
   
   # Run linting
   uv run ruff check src/
   
   # Run formatting
   uv run black src/
   ```

## Coding Guidelines

### Code Style

We follow these style guides:

- **Formatting**: [Black](https://black.readthedocs.io/) (line length: 88)
- **Linting**: [Ruff](https://docs.astral.sh/ruff/)
- **Type Hints**: [MyPy](https://mypy.readthedocs.io/) compatible
- **Documentation**: Google style docstrings

### Pre-commit Hooks

Our pre-commit hooks automatically format and check your code:

```bash
# Run pre-commit manually
uv run pre-commit run --all-files
```

### Naming Conventions

- **Functions/Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

### Type Hints

Always use type hints:

```python
from typing import List, Dict, Optional, Union

def process_pipeline(
    user_query: str,
    cloud_platform: Optional[str] = None,
    workload_type: Optional[str] = None
) -> Dict[str, str]:
    """Process pipeline description and generate design.
    
    Args:
        user_query: Natural language pipeline description
        cloud_platform: Target cloud platform
        workload_type: Type of workload (batch/streaming)
    
    Returns:
        Dictionary containing pipeline design components
    """
    # Implementation
    pass
```

### Docstrings

Use Google style docstrings:

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """Example function with Google style docstring.
    
    Args:
        param1: The first parameter.
        param2: The second parameter. Defaults to 0.
    
    Returns:
        bool: The return value.
    
    Raises:
        ValueError: If param1 is empty.
    
    Examples:
        >>> example_function("test")
        True
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    return True
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_main.py         # Main functionality
├── test_api.py          # API tests
├── test_streamlit.py    # Streamlit tests
├── test_graph.py        # Graph workflow tests
└── test_nodes/          # Node-specific tests
    ├── __init__.py
    ├── test_input_parser.py
    └── test_*.py
```

### Writing Tests

```python
import pytest
from unittest.mock import patch, MagicMock
from state import PipelineState
from llm import call_claude
from nodes.input_parser import input_parser_node

class TestInputParser:
    """Test cases for input parser node."""
    
    def test_basic_input_parsing(self):
        """Test parsing of basic input."""
        state = {
            "user_query": "I need a data pipeline for CSV files"
        }
        
        result = input_parser_node(state)
        
        assert "user_query" in result
        assert isinstance(result, dict)
    
    @patch('nodes.input_parser.call_claude')
    def test_llm_integration(self, mock_call_claude):
        """Test integration with LLM."""
        mock_call_claude.return_value = '{"cloud": "azure", "workload_type": "batch"}'
        
        state = {"user_query": "Azure pipeline"}
        result = input_parser_node(state)
        
        mock_call_claude.assert_called_once()
        assert result["cloud"] == "azure"
    
    def test_empty_input(self):
        """Test handling of empty input."""
        state = {"user_query": ""}
        result = input_parser_node(state)
        
        # Should return state unchanged
        assert result["user_query"] == ""
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_api.py

# Run tests with pattern
uv run pytest -k "test_input_parser"

# Run integration tests
uv run pytest -m integration

# Run specific test
uv run pytest tests/test_api.py::test_design_endpoint
```

### Test Fixtures

```python
# tests/conftest.py
import pytest
from state import PipelineState

@pytest.fixture
def sample_state() -> PipelineState:
    return {
        "user_query": "Test pipeline description",
        "cloud": "azure",
        "workload_type": "batch"
    }

@pytest.fixture
def sample_architecture() -> str:
    return """
    ## Architecture Overview
    - Azure Blob Storage
    - Azure Databricks
    - Delta Lake
    """

@pytest.fixture
def mock_llm_response():
    def _mock_response(content: str):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=content)]
        return mock_response
    return _mock_response
```

## Submitting Changes

### Creating Pull Requests

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding guidelines
   - Write tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run tests
   uv run pytest
   
   # Run linting
   uv run ruff check src/
   
   # Run formatting
   uv run black src/
   
   # Run type checking
   uv run mypy src/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add your feature description
   
   - Describe what this commit does
   - List any significant changes
   - Reference related issues (#123)"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create pull request**
   - Go to GitHub and create a pull request
   - Fill out the PR template
   - Request review from maintainers

### Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add DBT support for ETL tool designs

fix: Resolve API timeout issues

docs: Update user guide with new examples

test: Add comprehensive test coverage for input parser
```

### Pull Request Template

```markdown
## Summary
Brief description of changes.

## Test plan
- [ ] Tests pass locally
- [ ] New functionality tested
- [ ] Documentation updated
- [ ] Breaking changes documented

## Breaking changes
List any breaking changes and migration steps.

## Self-certification
- [ ] I have tested my changes
- [ ] I have updated documentation
- [ ] My code follows the project style
- [ ] No sensitive information exposed
```

## Issue Reporting

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check the documentation** for solutions
3. **Try troubleshooting steps** from our guide

### How to Report Bugs

Use the bug report template:

```markdown
**Describe the bug**
Clear and concise description.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
Clear and concise description.

**Screenshots**
If applicable, add screenshots.

**Environment info**
- OS: [e.g. macOS 12.0]
- Python version: [e.g. 3.11.0]
- Package versions: [e.g. langgraph==1.0.0]

**Additional context**
Any other context about the problem.
```

### How to Request Features

Use the feature request template:

```markdown
**Is your feature request related to a problem?**
Clear and concise description.

**Describe the solution you'd like**
Clear and concise description.

**Describe alternatives you've considered**
Clear and concise description.

**Additional context**
Add any context or screenshots.
```

## Feature Requests

### Submitting Feature Requests

1. **Create an issue** with the `feature-request` label
2. **Describe the feature** and its benefits
3. **Provide use cases** and examples
4. **Consider implementation** approach
5. **Be open to discussion** and alternatives

### Feature Request Guidelines

- **Clear description**: What is the feature?
- **Use cases**: Why is this feature needed?
- **Examples**: How would it work?
- **Benefits**: What value does it add?
- **Alternatives**: Are there existing solutions?

## Documentation

### Documentation Structure

```
docs/
├── README.md              # Main documentation
├── USER_GUIDE.md          # User documentation
├── DEVELOPER_GUIDE.md     # Developer documentation
├── API_REFERENCE.md       # API reference
├── ARCHITECTURE.md        # Architecture documentation
├── TROUBLESHOOTING.md     # Troubleshooting guide
└── FAQ.md                 # Frequently asked questions
```

### Writing Documentation

1. **Keep it clear and concise**
2. **Use examples** to illustrate concepts
3. **Include code snippets** where helpful
4. **Update existing docs** when making changes
5. **Use proper formatting** and structure

### Documentation Standards

- **Markdown format**
- **Clear headings** and structure
- **Code examples** with syntax highlighting
- **Links to related documentation**
- **Version-specific information**

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community discussions
- **Email**: [dev@your-org.com](mailto:dev@your-org.com)

### Getting Help

1. **Documentation**: Check our docs first
2. **Issues**: Search existing issues
3. **Discussions**: Ask questions in GitHub Discussions
4. **Email**: Contact the team directly

### Contributing to Discussions

- **Be respectful** and helpful
- **Search before asking** to avoid duplicates
- **Provide context** for your questions
- **Share solutions** that worked for you

## Recognition

We appreciate all contributions! Contributors will be recognized in:

- **Release notes** for significant contributions
- **README.md** contributor section
- **Special mentions** for outstanding contributions

## Questions?

If you have questions about contributing, please:

1. Read this guide thoroughly
2. Check our [FAQ](FAQ.md)
3. Create a [discussion](https://github.com/your-org/pipeline-architect/discussions)
4. Email us at [dev@your-org.com](mailto:dev@your-org.com)

## Additional Resources

- [Python Developer Guide](https://devguide.python.org/)
- [Git Best Practices](https://github.com/0nn0/git-best-practices/)
- [Open Source Guides](https://opensource.guide/)

Thank you for contributing to the AI Data Pipeline Design Assistant! 🎉