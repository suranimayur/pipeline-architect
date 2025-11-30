#!/usr/bin/env python3
"""
Test script to verify the Anthropic API configuration works correctly.
This helps debug the "Missing Action parameter" error.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
if os.path.exists(".env"):
    load_dotenv()
    print("✓ Loaded .env file")

# Test the client configuration
try:
    from anthropic import Anthropic
    print("✓ Anthropic library imported successfully")
except ImportError as e:
    print(f"✗ Failed to import Anthropic: {e}")
    sys.exit(1)

# Get configuration values
base_url = os.getenv("ANTHROPIC_BASE_URL")
auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
model = os.getenv("ANTHROPIC_MODEL", "KAT-Coder")
timeout_ms = os.getenv("API_TIMEOUT_MS", "300000")

print(f"Base URL: {base_url}")
print(f"Auth Token: {auth_token[:10] if auth_token else 'None'}...")
print(f"Model: {model}")
print(f"Timeout: {timeout_ms}ms")

# Configure the client with proxy settings
if base_url and auth_token:
    print("\n🔧 Setting up Anthropic client with proxy configuration...")
    
    client = Anthropic(
        base_url=base_url.strip(),
        api_key=auth_token.strip(),
        default_headers={
            "Authorization": f"Bearer {auth_token.strip()}",
            "Content-Type": "application/json"
        }
    )
    print("✓ Client configured successfully")
    
    # Test a simple API call
    try:
        print("\n📡 Testing API connection...")
        response = client.messages.create(
            model=model,
            max_tokens=100,
            temperature=0.1,
            system="Just say 'Hello, this is a test!' in one sentence.",
            messages=[
                {"role": "user", "content": "Hello"}
            ],
            timeout=30
        )
        print("✓ API call successful!")
        print(f"Response: {response.content[0].text[:50]}...")
        
    except Exception as e:
        print(f"✗ API call failed: {e}")
        print(f"Error type: {type(e).__name__}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code if e.response else 'N/A'}")
        sys.exit(1)
else:
    print("✗ Missing required environment variables")
    sys.exit(1)

print("\n🎉 All tests passed! The API configuration is working correctly.")