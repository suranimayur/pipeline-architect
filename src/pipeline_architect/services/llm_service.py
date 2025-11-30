"""
LLM Service for Pipeline Architect.

This module provides a centralized service for interacting with Large Language Models,
handling API keys, configuration, and common LLM operations used throughout the application.
"""

import os
import time
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

from anthropic import Anthropic
from openai import OpenAI

from ..utils.config import get_settings
from ..utils.logger import get_logger


class LLMService:
    """
    Service for managing LLM interactions and configurations.
    
    This service handles:
    - API key management and configuration
    - LLM client initialization and connection
    - Common LLM operations and utilities
    - Error handling and retry logic
    """
    
    def __init__(self):
        """Initialize the LLM service with configuration."""
        self.settings = get_settings()
        self.logger = get_logger(__name__)
        
        # Initialize clients
        self._anthropic_client = None
        self._openai_client = None
        
        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 1.0  # seconds
        
    @property
    def anthropic_client(self) -> Anthropic:
        """Get or create Anthropic client."""
        if self._anthropic_client is None:
            self._anthropic_client = self._create_anthropic_client()
        return self._anthropic_client
    
    @property 
    def openai_client(self) -> OpenAI:
        """Get or create OpenAI client."""
        if self._openai_client is None:
            self._openai_client = self._create_openai_client()
        return self._openai_client
    
    def _create_anthropic_client(self) -> Anthropic:
        """Create and configure Anthropic client."""
        try:
            # Try standard Anthropic API key first
            api_key = self.settings.anthropic_api_key
            
            if not api_key:
                # Check for proxy configuration
                base_url = self.settings.anthropic_base_url
                auth_token = self.settings.anthropic_auth_token
                
                if base_url and auth_token:
                    self.logger.info("Using proxy configuration for Anthropic API")
                    self.logger.debug(f"Base URL: {base_url}")
                    
                    return Anthropic(
                        base_url=base_url.strip(),
                        api_key=auth_token.strip(),
                        default_headers={
                            "Authorization": f"Bearer {auth_token.strip()}",
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        }
                    )
                else:
                    raise RuntimeError(
                        "No valid Anthropic configuration found. "
                        "Set either ANTHROPIC_API_KEY or both ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN."
                    )
            
            self.logger.info("Using standard Anthropic API configuration")
            return Anthropic(api_key=api_key)
            
        except Exception as e:
            self.logger.error(f"Failed to create Anthropic client: {e}")
            raise
    
    def _create_openai_client(self) -> OpenAI:
        """Create and configure OpenAI client."""
        try:
            api_key = self.settings.openai_api_key
            
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY not configured")
            
            self.logger.info("Using OpenAI API configuration")
            return OpenAI(api_key=api_key)
            
        except Exception as e:
            self.logger.error(f"Failed to create OpenAI client: {e}")
            raise
    
    def call_llm(
        self,
        system_prompt: str,
        user_content: str,
        max_tokens: int = 2000,
        model: Optional[str] = None,
        temperature: float = 0.2
    ) -> str:
        """
        Call LLM with rate limiting and error handling.
        
        Args:
            system_prompt: System prompt for the LLM
            user_content: User input content
            max_tokens: Maximum tokens for response
            model: LLM model to use (defaults to configured model)
            temperature: Temperature for response generation
            
        Returns:
            LLM response text
            
        Raises:
            RuntimeError: If LLM call fails
        """
        # Rate limiting
        self._enforce_rate_limit()
        
        if model is None:
            model = self.settings.anthropic_model
            
        try:
            self.logger.debug(f"Calling LLM with model: {model}")
            self.logger.debug(f"System prompt length: {len(system_prompt)} chars")
            self.logger.debug(f"User content length: {len(user_content)} chars")
            
            # Make API call
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_content}
                ],
                timeout=self.settings.api_timeout_ms / 1000
            )
            
            self.logger.debug("LLM call successful")
            
            # Extract response text
            response_text = self._extract_response_text(response)
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"LLM call failed: {e}")
            # Try fallback model if configured
            if model != self.settings.anthropic_fallback_model:
                self.logger.info(f"Trying fallback model: {self.settings.anthropic_fallback_model}")
                return self.call_llm(
                    system_prompt=system_prompt,
                    user_content=user_content,
                    max_tokens=max_tokens,
                    model=self.settings.anthropic_fallback_model,
                    temperature=temperature
                )
            raise RuntimeError(f"LLM call failed after retries: {e}")
    
    def _extract_response_text(self, response) -> str:
        """Extract text content from LLM response."""
        try:
            # Handle different response formats
            parts = []
            for block in response.content:
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
            
        except Exception as e:
            self.logger.error(f"Failed to extract response text: {e}")
            return ""
    
    def _enforce_rate_limit(self):
        """Enforce minimum time between API calls."""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        
        if time_since_last < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self._last_request_time = time.time()
    
    def get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.utcnow().isoformat()
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate that API keys are configured and working."""
        results = {
            "anthropic": False,
            "openai": False
        }
        
        try:
            # Test Anthropic connection
            self.anthropic_client.beta
            results["anthropic"] = True
            self.logger.info("Anthropic API key validation successful")
        except Exception as e:
            self.logger.warning(f"Anthropic API key validation failed: {e}")
        
        try:
            # Test OpenAI connection
            self.openai_client.api_key
            results["openai"] = True
            self.logger.info("OpenAI API key validation successful")
        except Exception as e:
            self.logger.warning(f"OpenAI API key validation failed: {e}")
        
        return results


# Global LLM service instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get global LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


__all__ = ["LLMService", "get_llm_service"]