import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
if os.path.exists(".env"):
    load_dotenv()

# Simple helper for calling Claude from different nodes

_client = None

def get_client() -> Anthropic:
    global _client
    if _client is None:
        # Try standard Anthropic API key first
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # If no standard API key, check for Kat Coder configuration
        if not api_key:
            base_url = os.getenv("ANTHROPIC_BASE_URL")
            auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
            
            if base_url and auth_token:
                print("🔧 Using proxy configuration for Anthropic API...")
                print(f"📡 Base URL: {base_url}")
                print(f"🔑 Auth Token: {auth_token[:10]}...")
                
                # Configure for proxy with proper headers
                # Note: For some proxies, you might need to pass the token as api_key parameter
                _client = Anthropic(
                    base_url=base_url.strip(),
                    api_key=auth_token.strip(),
                    default_headers={
                        "Authorization": f"Bearer {auth_token.strip()}",
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }
                )
                return _client
            else:
                raise RuntimeError(
                    "❌ No valid Anthropic configuration found. "
                    "Set either ANTHROPIC_API_KEY or both ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN. "
                    "Current environment variables found:"
                    f"\n  ANTHROPIC_API_KEY: {api_key is not None}"
                    f"\n  ANTHROPIC_BASE_URL: {base_url is not None}"
                    f"\n  ANTHROPIC_AUTH_TOKEN: {auth_token is not None}"
                )
        
        print("🔧 Using standard Anthropic API configuration...")
        _client = Anthropic(api_key=api_key)
    return _client

def call_claude(system_prompt: str, user_content: str, max_tokens: int = 2000) -> str:
    client = get_client()
    
    # Try to get the model from environment variable, default to KAT-Coder
    model = os.getenv("ANTHROPIC_MODEL", "KAT-Coder")
    
    # Get timeout from environment or use default
    timeout_ms = os.getenv("API_TIMEOUT_MS", "300000")
    try:
        timeout_seconds = int(timeout_ms) / 1000
    except ValueError:
        timeout_seconds = 300  # 5 minutes default
    
    try:
        print(f"📡 Calling Claude API with model: {model}, timeout: {timeout_seconds}s")
        print(f"📝 System prompt length: {len(system_prompt)} chars")
        print(f"📝 User content length: {len(user_content)} chars")
        
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=0.2,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_content}
            ],
            timeout=timeout_seconds
        )
        print("✅ API call successful!")
        
        # Anthropic messages API returns a list of content blocks
        # Handle different block types safely
        parts = []
        for block in resp.content:
            block_dict = block.model_dump() if hasattr(block, 'model_dump') else {}
            
            # Try to extract text content from different block types
            if 'text' in block_dict:
                parts.append(block_dict['text'])
            elif 'content' in block_dict and isinstance(block_dict['content'], str):
                parts.append(block_dict['content'])
            elif hasattr(block, '__dict__') and 'text' in block.__dict__:
                parts.append(block.__dict__['text'])
            elif str(block).strip():
                # Fallback: use string representation if it contains meaningful content
                block_str = str(block).strip()
                if block_str and not block_str.startswith('<'):
                    parts.append(block_str)
        
        return "\n".join(parts).strip()
        
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        # Try fallback model if the primary one fails
        fallback_model = os.getenv("ANTHROPIC_SMALL_FAST_MODEL", "claude-3-5-sonnet-latest")
        if model != fallback_model:
            print(f"Trying fallback model: {fallback_model}")
            resp = client.messages.create(
                model=fallback_model,
                max_tokens=max_tokens,
                temperature=0.2,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_content}
                ],
            )
            
            parts = []
            for block in resp.content:
                block_dict = block.model_dump() if hasattr(block, 'model_dump') else {}
                
                if 'text' in block_dict:
                    parts.append(block_dict['text'])
                elif 'content' in block_dict and isinstance(block_dict['content'], str):
                    parts.append(block_dict['content'])
                elif hasattr(block, '__dict__') and 'text' in block.__dict__:
                    parts.append(block.__dict__['text'])
                elif str(block).strip():
                    block_str = str(block).strip()
                    if block_str and not block_str.startswith('<'):
                        parts.append(block_str)
            
            return "\n".join(parts).strip()
        
        # If all else fails, raise the exception
        raise
