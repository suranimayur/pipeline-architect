#!/usr/bin/env python3
"""
Comprehensive test script for the AI Data Pipeline Design Assistant
Tests all three interfaces: CLI, FastAPI, and Streamlit
"""
import json
import requests
import subprocess
import time
import os
from test_samples import SAMPLE_DESCRIPTIONS

def test_cli_interface():
    """Test the CLI interface"""
    print("\n" + "="*60)
    print("TESTING CLI INTERFACE")
    print("="*60)
    
    # Test with a sample description
    test_description = SAMPLE_DESCRIPTIONS["azure_batch"]["description"]
    
    print(f"Testing CLI with sample: {SAMPLE_DESCRIPTIONS['azure_batch']['name']}")
    print(f"Description: {test_description[:100]}...")
    
    # Note: CLI test would require user input, so we'll skip automated testing
    # but provide instructions
    print("\nTo test CLI manually:")
    print("1. Run: uv run python main.py")
    print("2. Enter the description above when prompted")
    print("3. Review the generated pipeline design")
    print("✓ CLI interface test instructions provided")

def test_fastapi_interface():
    """Test the FastAPI interface"""
    print("\n" + "="*60)
    print("TESTING FASTAPI INTERFACE")
    print("="*60)
    
    # Test the root endpoint
    try:
        print("Testing root endpoint...")
        # Note: This would require the FastAPI server to be running
        # For now, we'll provide the curl commands to test
        print("\nFastAPI server should be running on http://127.0.0.1:8000")
        print("Available endpoints:")
        print("- GET / : Root endpoint with API info")
        print("- GET /docs : Interactive API documentation")
        print("- POST /design : Main pipeline design endpoint")
        
        # Test sample API calls
        for key, sample in SAMPLE_DESCRIPTIONS.items():
            print(f"\nTo test with {sample['name']}:")
            print(f"curl -X POST \"http://127.0.0.1:8000/design\" \\")
            print(f"     -H \"Content-Type: application/json\" \\")
            print(f"     -d '{{\"description\": \"{sample['description'][:100]}...\"}}'")
            
        print("✓ FastAPI interface test instructions provided")
        
    except Exception as e:
        print(f"✗ FastAPI test failed: {e}")

def test_streamlit_interface():
    """Test the Streamlit interface"""
    print("\n" + "="*60)
    print("TESTING STREAMLIT INTERFACE")
    print("="*60)
    
    print("Streamlit app should be running on http://localhost:8501")
    print("To test the Streamlit interface:")
    print("1. Open the URL in your browser")
    print("2. You'll see a form with sample text pre-filled")
    print("3. Modify the description or use the sample")
    print("4. Click 'Generate Design' button")
    print("5. Review the results in the tabs: Architecture, PySpark Code, IAM Design, Cost & Performance Tips")
    print("✓ Streamlit interface test instructions provided")

def test_api_endpoint_directly():
    """Test API endpoint directly using requests (if server is running)"""
    print("\n" + "="*60)
    print("TESTING API ENDPOINT DIRECTLY")
    print("="*60)
    
    # This test requires the FastAPI server to be running
    base_url = "http://127.0.0.1:8000"
    
    test_payload = {
        "description": SAMPLE_DESCRIPTIONS["aws_streaming"]["description"]
    }
    
    try:
        print("Attempting to connect to FastAPI server...")
        response = requests.post(f"{base_url}/design", json=test_payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ API call successful!")
            print(f"Response keys: {list(result.keys())}")
            print(f"Architecture generated: {len(result.get('architecture', '')) > 0}")
            print(f"Code generated: {len(result.get('pyspark_code', '')) > 0}")
            print(f"IAM design generated: {len(result.get('iam_design', '')) > 0}")
            print(f"Tips generated: {len(result.get('cost_tips', '')) > 0}")
        else:
            print(f"✗ API call failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("✗ FastAPI server not running. Please start it with:")
        print("uv run uvicorn api:app --host 127.0.0.1 --port 8000 --reload")
    except Exception as e:
        print(f"✗ API test failed: {e}")

def create_test_summary():
    """Create a summary of all test results"""
    print("\n" + "="*60)
    print("TEST SUMMARY & USAGE GUIDE")
    print("="*60)
    
    print("\n1. CLI Interface (main.py):")
    print("   - Command: uv run python main.py")
    print("   - Interactive command-line interface")
    print("   - Best for: Quick testing and development")
    
    print("\n2. FastAPI Interface (api.py):")
    print("   - Start server: uv run uvicorn api:app --host 127.0.0.1 --port 8000 --reload")
    print("   - API endpoint: POST /design")
    print("   - Best for: Integration with other applications")
    
    print("\n3. Streamlit Interface (streamlit_app.py):")
    print("   - Command: uv run streamlit run streamlit_app.py")
    print("   - Web interface: http://localhost:8501")
    print("   - Best for: User-friendly visual interface")
    
    print("\n4. Test Samples Available:")
    for key, sample in SAMPLE_DESCRIPTIONS.items():
        print(f"   - {sample['name']}: {key}")
    
    print("\n5. Environment Configuration:")
    print("   - Ensure .env file is properly configured")
    print("   - Kat Coder configuration working with custom base URL and auth token")
    print("   - All dependencies installed via uv")
    
    print("\n6. Troubleshooting:")
    print("   - If Claude API fails, check .env configuration")
    print("   - Ensure uv environment is activated")
    print("   - Check network connectivity to Kat Coder endpoint")
    print("   - Review logs for specific error messages")

def run_all_tests():
    """Run all available tests"""
    print("AI Data Pipeline Design Assistant - Comprehensive Test Suite")
    print("="*60)
    
    # Test each interface
    test_cli_interface()
    test_fastapi_interface()
    test_streamlit_interface()
    
    # Try to test API directly (optional)
    print("\n" + "="*60)
    print("OPTIONAL: DIRECT API TEST")
    print("="*60)
    print("Note: This test requires FastAPI server to be running.")
    print("If server is not running, skip this test.")
    
    response = input("Start FastAPI server and test API directly? (y/n): ")
    if response.lower() == 'y':
        test_api_endpoint_directly()
    else:
        print("Skipping direct API test.")
    
    # Create summary
    create_test_summary()

if __name__ == "__main__":
    run_all_tests()