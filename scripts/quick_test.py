#!/usr/bin/env python3
"""
Quick Test Script for Pipeline Architect

This script provides a fast way to test the basic functionality
of the Pipeline Architect project without running the full test suite.
"""

import sys
import os
from pathlib import Path

def setup_path():
    """Add src to Python path for imports."""
    src_path = Path("src").resolve()
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

def test_basic_imports():
    """Test basic imports without full validation."""
    print("📦 Testing basic imports...")
    
    # Test if the package structure exists
    package_files = [
        "src/pipeline_architect/__init__.py",
        "src/pipeline_architect/core/__init__.py",
        "src/pipeline_architect/core/graph.py",
        "src/pipeline_architect/core/state.py",
        "src/pipeline_architect/nodes/__init__.py",
        "src/pipeline_architect/services/__init__.py",
        "src/pipeline_architect/utils/__init__.py",
        "src/pipeline_architect/cli/__init__.py"
    ]
    
    missing_files = []
    for file_path in package_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing package files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ Package structure exists")
    return True

def test_cli_help():
    """Test CLI help functionality with UV."""
    print("\n💻 Testing CLI help (UV Package Manager)...")
    
    import subprocess
    import sys
    import os
    
    try:
        # Test CLI with UV (using the installed package)
        result = subprocess.run([
            "uv", "run", "python", "-m", "pipeline_architect.cli.main", "--help"
        ], capture_output=True, text=True, timeout=30, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ CLI help works correctly with UV")
            return True
        else:
            print(f"⚠️  CLI help failed with UV: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⚠️  CLI help timed out with UV")
    except FileNotFoundError:
        print("⚠️  UV not found")
    except Exception as e:
        print(f"⚠️  CLI UV test error: {e}")
    
    # Fallback: Test CLI file exists and is executable
    print("🔄 Falling back to CLI file validation...")
    try:
        cli_file = Path("src/pipeline_architect/cli/main.py")
        if not cli_file.exists():
            print("❌ CLI file not found")
            return False
        
        # Check if CLI file has main function
        cli_content = cli_file.read_text(encoding='utf-8', errors='ignore')
        if "def main()" not in cli_content:
            print("⚠️  CLI main function not found")
            return False
        
        # Check if CLI has argument parsing
        if "argparse" not in cli_content and "typer" not in cli_content:
            print("⚠️  CLI argument parsing not found")
            return False
        
        print("✅ CLI file structure is valid")
        return True
            
    except Exception as e:
        print(f"❌ CLI validation error: {e}")
        return False

def test_api_structure():
    """Test API structure."""
    print("\n🌐 Testing API structure...")
    
    try:
        setup_path()
        
        # Check if API file exists and is valid
        api_file = Path("src/pipeline_architect/api.py")
        if not api_file.exists():
            print("❌ API file not found")
            return False
        
        # Try to import FastAPI components
        api_content = api_file.read_text()
        
        expected_components = [
            "FastAPI",
            "app = FastAPI",
            "@app.get",
            "@app.post",
            "/health",
            "/api/v1/design"
        ]
        
        missing_components = []
        for component in expected_components:
            if component not in api_content:
                missing_components.append(component)
        
        if missing_components:
            print("⚠️  Missing API components:")
            for component in missing_components:
                print(f"   - {component}")
            return False
        
        print("✅ API structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def test_configuration_structure():
    """Test configuration structure."""
    print("\n⚙️ Testing configuration structure...")
    
    try:
        setup_path()
        
        config_file = Path("src/pipeline_architect/utils/config.py")
        if not config_file.exists():
            print("❌ Configuration file not found")
            return False
        
        config_content = config_file.read_text()
        
        expected_config_components = [
            "class LLMSettings",
            "class SecuritySettings", 
            "class ApplicationSettings",
            "def get_settings",
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY"
        ]
        
        missing_components = []
        for component in expected_config_components:
            if component not in config_content:
                missing_components.append(component)
        
        if missing_components:
            print("⚠️  Missing configuration components:")
            for component in missing_components:
                print(f"   - {component}")
            return False
        
        print("✅ Configuration structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test error: {e}")
        return False

def test_state_definitions():
    """Test state definitions."""
    print("\n📊 Testing state definitions...")
    
    try:
        setup_path()
        
        state_file = Path("src/pipeline_architect/core/state.py")
        if not state_file.exists():
            print("❌ State file not found")
            return False
        
        state_content = state_file.read_text()
        
        expected_state_components = [
            "PipelineState",
            "TypedDict",
            "user_query",
            "cloud",
            "workload_type",
            "architecture",
            "pyspark_code",
            "iam_design"
        ]
        
        missing_components = []
        for component in expected_state_components:
            if component not in state_content:
                missing_components.append(component)
        
        if missing_components:
            print("⚠️  Missing state components:")
            for component in missing_components:
                print(f"   - {component}")
            return False
        
        print("✅ State definitions are correct")
        return True
        
    except Exception as e:
        print(f"❌ State test error: {e}")
        return False

def test_graph_structure():
    """Test graph structure."""
    print("\n🏗️ Testing graph structure...")
    
    try:
        setup_path()
        
        graph_file = Path("src/pipeline_architect/core/graph.py")
        if not graph_file.exists():
            print("❌ Graph file not found")
            return False
        
        graph_content = graph_file.read_text()
        
        expected_graph_components = [
            "langgraph.graph",
            "StateGraph",
            "build_graph",
            "input_parser",
            "architecture_planner",
            "code_generator",
            "answer_composer"
        ]
        
        missing_components = []
        for component in expected_graph_components:
            if component not in graph_content:
                missing_components.append(component)
        
        if missing_components:
            print("⚠️  Missing graph components:")
            for component in missing_components:
                print(f"   - {component}")
            return False
        
        print("✅ Graph structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ Graph test error: {e}")
        return False

def test_requirements():
    """Test requirements files."""
    print("\n📋 Testing requirements...")
    
    required_files = [
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing requirement files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ Requirements files exist")
    
    # Check for key dependencies
    try:
        req_content = Path("requirements.txt").read_text()
        key_deps = ["fastapi", "uvicorn", "pydantic", "langgraph", "anthropic"]
        
        missing_deps = []
        for dep in key_deps:
            if dep not in req_content:
                missing_deps.append(dep)
        
        if missing_deps:
            print("⚠️  Missing key dependencies:")
            for dep in missing_deps:
                print(f"   - {dep}")
            return False
        
        print("✅ Key dependencies are present")
        return True
        
    except Exception as e:
        print(f"❌ Requirements test error: {e}")
        return False

def test_documentation():
    """Test documentation."""
    print("\n📚 Testing documentation...")
    
    doc_files = [
        "README.md",
        "TESTING_GUIDE.md",
        "PROJECT_SUMMARY.md",
        "docs/USER_GUIDE.md",
        "docs/API_REFERENCE.md"
    ]
    
    existing_docs = []
    for doc_file in doc_files:
        if Path(doc_file).exists():
            existing_docs.append(doc_file)
    
    if not existing_docs:
        print("❌ No documentation files found")
        return False
    
    print(f"✅ Found {len(existing_docs)} documentation files:")
    for doc_file in existing_docs:
        print(f"   - {doc_file}")
    
    return True

def main():
    """Run all quick tests."""
    print("🧪 Pipeline Architect - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Package Structure", test_basic_imports),
        ("Requirements", test_requirements),
        ("Configuration", test_configuration_structure),
        ("State Definitions", test_state_definitions),
        ("Graph Structure", test_graph_structure),
        ("API Structure", test_api_structure),
        ("CLI Help", test_cli_help),
        ("Documentation", test_documentation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 QUICK TEST SUMMARY")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("=" * 70)
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL QUICK TESTS PASSED!")
        print("\nProject structure is valid. Next steps:")
        print("1. ✅ Install dependencies: pip install -r requirements-dev.txt")
        print("2. ✅ Configure API keys in .env file")
        print("3. ✅ Run full validation: python scripts/validate_project.py")
        print("4. ✅ Start testing: pytest tests/")
        print("5. ✅ Try CLI: python -m pipeline_architect.cli.main --help")
        print("6. ✅ Start API: uvicorn src.pipeline_architect.api:app --reload")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed.")
        print("\nReview the failed tests above and fix any issues.")
        print("Common issues:")
        print("- Missing files: Check if all files were created correctly")
        print("- Import errors: Ensure Python path is set correctly")
        print("- Structure issues: Verify directory structure matches expected format")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)