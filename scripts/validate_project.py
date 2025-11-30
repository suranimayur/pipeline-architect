#!/usr/bin/env python3
"""
Project Validation Script for Pipeline Architect

This script validates the project structure, imports, and basic functionality
to ensure everything is working correctly after the reorganization.
"""

import sys
import os
import importlib.util
from pathlib import Path
from typing import List, Tuple

def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 11):
        print(f"❌ Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def check_project_structure():
    """Check if project structure is correct."""
    print("\n📁 Checking project structure...")
    
    required_files = [
        "src/pipeline_architect/__init__.py",
        "src/pipeline_architect/core/graph.py",
        "src/pipeline_architect/core/state.py",
        "src/pipeline_architect/api.py",
        "src/pipeline_architect/cli/main.py",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "README.md",
        "Dockerfile",
        "docker-compose.yml",
        ".github/workflows/ci.yml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ Project structure is correct")
    return True

def check_imports():
    """Check if all imports work correctly."""
    print("\n📦 Checking imports...")
    
    import_tests = [
        ("pipeline_architect", "from pipeline_architect import __version__"),
        ("core.graph", "from pipeline_architect.core.graph import build_graph"),
        ("core.state", "from pipeline_architect.core.state import PipelineState"),
        ("api", "from pipeline_architect import api"),
        ("cli.main", "from pipeline_architect.cli.main import main"),
    ]
    
    failed_imports = []
    for module_name, import_statement in import_tests:
        try:
            exec(import_statement)
            print(f"✅ {module_name}")
        except Exception as e:
            print(f"❌ {module_name}: {e}")
            failed_imports.append((module_name, str(e)))
    
    if failed_imports:
        print("\n❌ Import failures:")
        for module_name, error in failed_imports:
            print(f"   - {module_name}: {error}")
        return False
    
    print("✅ All imports successful")
    return True

def check_configuration():
    """Check configuration loading."""
    print("\n⚙️ Checking configuration...")
    
    try:
        # Add src to path temporarily
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        from pipeline_architect.utils.config import get_settings
        
        # Test configuration loading
        settings = get_settings()
        print(f"✅ Configuration loaded successfully")
        print(f"   - App Name: {settings.app_name}")
        print(f"   - Version: {settings.app_version}")
        print(f"   - Environment: {settings.environment}")
        
        # Check LLM configuration
        if settings.llm.anthropic_api_key or (settings.llm.anthropic_base_url and settings.llm.anthropic_auth_token):
            print("✅ LLM configuration is valid")
        else:
            print("⚠️  LLM API keys not configured (expected for testing)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def check_cli():
    """Check CLI functionality."""
    print("\n💻 Checking CLI...")
    
    try:
        from pipeline_architect.cli.main import parse_arguments
        
        # Test argument parsing
        args = parse_arguments()
        print("✅ CLI argument parser works")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI error: {e}")
        return False

def check_api_structure():
    """Check API structure."""
    print("\n🌐 Checking API structure...")
    
    try:
        from pipeline_architect.api import app
        print("✅ FastAPI app structure is valid")
        
        # Check endpoints
        endpoints = [route.path for route in app.routes]
        expected_endpoints = ["/", "/health", "/api/v1/design", "/api/v1/validate"]
        
        for endpoint in expected_endpoints:
            if endpoint in endpoints:
                print(f"✅ Endpoint {endpoint} exists")
            else:
                print(f"⚠️  Endpoint {endpoint} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ API error: {e}")
        return False

def check_test_structure():
    """Check test structure."""
    print("\n🧪 Checking test structure...")
    
    test_files = [
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/unit/",
        "tests/integration/",
        "tests/e2e/"
    ]
    
    missing = []
    for test_file in test_files:
        if not Path(test_file).exists():
            missing.append(test_file)
    
    if missing:
        print("⚠️  Missing test files/directories:")
        for file_path in missing:
            print(f"   - {file_path}")
        return False
    
    print("✅ Test structure is correct")
    return True

def check_dependencies():
    """Check if required packages are available."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        "fastapi", "uvicorn", "pydantic", "langgraph", 
        "anthropic", "openai", "pytest", "black", "ruff"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements-dev.txt")
        return False
    
    print("✅ All dependencies available")
    return True

def run_basic_functionality_test():
    """Run a basic functionality test."""
    print("\n🚀 Running basic functionality test...")
    
    try:
        # Test state creation
        from pipeline_architect.core.state import PipelineState
        test_state: PipelineState = {
            "user_query": "Test pipeline description",
            "cloud": "azure",
            "workload_type": "batch"
        }
        print("✅ State creation works")
        
        # Test graph building (without execution)
        from pipeline_architect.core.graph import build_graph
        graph = build_graph()
        print("✅ Graph building works")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Run all validation checks."""
    print("🧪 Pipeline Architect - Project Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Project Structure", check_project_structure),
        ("Dependencies", check_dependencies),
        ("Imports", check_imports),
        ("Configuration", check_configuration),
        ("CLI", check_cli),
        ("API Structure", check_api_structure),
        ("Test Structure", check_test_structure),
        ("Basic Functionality", run_basic_functionality_test),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} failed with exception: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 VALIDATION SUMMARY")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {check_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("=" * 70)
    print(f"Total Checks: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL CHECKS PASSED! Project is ready for testing.")
        print("\nNext steps:")
        print("1. Configure your API keys in .env file")
        print("2. Run: python -m pipeline_architect.cli.main --help")
        print("3. Run: uvicorn src.pipeline_architect.api:app --reload")
        print("4. Run tests: pytest tests/")
        return True
    else:
        print(f"\n⚠️  {failed} check(s) failed. Please review and fix issues.")
        print("\nCommon fixes:")
        print("- Install dependencies: pip install -r requirements-dev.txt")
        print("- Set up virtual environment: python -m venv .venv")
        print("- Activate environment: source .venv/bin/activate (Linux/Mac) or .venv\\Scripts\\activate (Windows)")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)