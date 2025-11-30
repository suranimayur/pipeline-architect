#!/usr/bin/env python3
"""
Setup script using uv package manager.
This script will install all required dependencies using uv.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Setting up AI Data Pipeline Design Assistant...")
    print("=" * 60)
    
    # Check if uv is installed
    if not run_command("uv --version", "Checking uv package manager"):
        print("❌ uv package manager is not installed.")
        print("Please install uv from: https://github.com/astral-sh/uv")
        sys.exit(1)
    
    # Create virtual environment
    if not run_command("uv venv", "Creating virtual environment"):
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Activate virtual environment
    print("🔧 Activating virtual environment...")
    if os.name == 'nt':  # Windows
        activate_cmd = ".venv\\Scripts\\activate"
    else:  # Unix/Linux/Mac
        activate_cmd = "source .venv/bin/activate"
    
    print(f"Please run: {activate_cmd}")
    
    # Install dependencies from pyproject.toml
    if not run_command("uv pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("2. Run: python test_api_config.py (to test the API configuration)")
    print("3. Run: streamlit run streamlit_app.py (to start the web app)")
    print("4. Or run: python main.py (to run the CLI version)")

if __name__ == "__main__":
    main()