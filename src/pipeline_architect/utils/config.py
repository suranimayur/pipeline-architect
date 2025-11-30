"""
Configuration management for Pipeline Architect.

This module provides settings management using environment variables
and basic validation for different deployment environments.
"""

import os
from typing import Optional, List, Dict, Any
from pathlib import Path


class LLMSettings:
    """LLM configuration settings."""
    
    def __init__(self):
        # Anthropic settings
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.anthropic_base_url = os.getenv("ANTHROPIC_BASE_URL")
        self.anthropic_auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
        self.anthropic_fallback_model = os.getenv("ANTHROPIC_SMALL_FAST_MODEL", "claude-3-haiku-20240307")
        
        # OpenAI settings
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "dall-e-3")
        
        # API settings
        self.api_timeout_ms = int(os.getenv("API_TIMEOUT_MS", "300000"))


class SecuritySettings:
    """Security and access control settings."""
    
    def __init__(self):
        # Authentication
        self.enable_auth = os.getenv("ENABLE_AUTH", "false").lower() == "true"
        self.jwt_secret = os.getenv("JWT_SECRET")
        self.allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
        
        # Rate limiting
        self.rate_limit_enabled = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
        self.rate_limit_requests = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        self.rate_limit_window = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
        
        # Data protection
        self.pii_masking_enabled = os.getenv("PII_MASKING_ENABLED", "true").lower() == "true"
        self.encryption_enabled = os.getenv("ENCRYPTION_ENABLED", "true").lower() == "true"


class PerformanceSettings:
    """Performance and optimization settings."""
    
    def __init__(self):
        # Caching
        self.cache_enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.cache_ttl = int(os.getenv("CACHE_TTL", "3600"))
        self.cache_max_size = int(os.getenv("CACHE_MAX_SIZE", "1000"))
        
        # Resource management
        self.max_concurrent_requests = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
        self.worker_timeout = int(os.getenv("WORKER_TIMEOUT", "300"))
        
        # Monitoring
        self.metrics_enabled = os.getenv("METRICS_ENABLED", "true").lower() == "true"
        self.profiling_enabled = os.getenv("PROFILING_ENABLED", "false").lower() == "true"


class DatabaseSettings:
    """Database configuration settings."""
    
    def __init__(self):
        # PostgreSQL
        self.postgres_url = os.getenv("POSTGRES_URL")
        
        # Redis
        self.redis_url = os.getenv("REDIS_URL")
        
        # MongoDB (optional)
        self.mongodb_url = os.getenv("MONGODB_URL")
        
        # Document storage
        self.document_storage_path = Path(os.getenv("DOCUMENT_STORAGE_PATH", "./documents"))


class LoggingSettings:
    """Logging configuration settings."""
    
    def __init__(self):
        self.level = os.getenv("LOG_LEVEL", "INFO")
        self.format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.file_path = os.getenv("LOG_FILE_PATH")
        self.max_file_size = int(os.getenv("LOG_MAX_FILE_SIZE", "10485760"))  # 10MB
        self.backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))


class ApplicationSettings:
    """Main application settings."""
    
    def __init__(self):
        # Application metadata
        self.app_name = os.getenv("APP_NAME", "Pipeline Architect")
        self.app_version = os.getenv("APP_VERSION", "1.0.0")
        self.app_description = os.getenv("APP_DESCRIPTION", "AI-powered data pipeline design assistant")
        
        # Environment
        self.environment = os.getenv("ENVIRONMENT", "development")
        
        # Server settings
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8000"))
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        # LLM settings
        self.llm = LLMSettings()
        
        # Security settings
        self.security = SecuritySettings()
        
        # Performance settings
        self.performance = PerformanceSettings()
        
        # Database settings
        self.database = DatabaseSettings()
        
        # Logging settings
        self.logging = LoggingSettings()
        
        # Feature flags
        self.features = self._load_features()
    
    def _load_features(self) -> Dict[str, Any]:
        """Load feature flags from environment."""
        features = {}
        
        # Load individual feature flags
        features["enable_etl_designer"] = os.getenv("FEATURE_ENABLE_ETL_DESIGNER", "true").lower() == "true"
        features["enable_bbg_explainer"] = os.getenv("FEATURE_ENABLE_BBG_EXPLAINER", "true").lower() == "true"
        features["enable_cost_advisor"] = os.getenv("FEATURE_ENABLE_COST_ADVISOR", "true").lower() == "true"
        
        return features
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Validate environment
        valid_environments = ["development", "staging", "production"]
        if self.environment not in valid_environments:
            errors.append(f"Invalid environment: {self.environment}. Must be one of: {valid_environments}")
        
        # Validate API timeout
        if self.llm.api_timeout_ms < 1000 or self.llm.api_timeout_ms > 1800000:
            errors.append("API timeout must be between 1000ms and 30 minutes")
        
        # Check for required keys
        if not self.llm.anthropic_api_key and not (self.llm.anthropic_base_url and self.llm.anthropic_auth_token):
            errors.append("Either ANTHROPIC_API_KEY or both ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN must be set")
        
        return errors


# Global settings instance
_settings = None


def get_settings() -> ApplicationSettings:
    """Get global application settings instance."""
    global _settings
    if _settings is None:
        _settings = ApplicationSettings()
        
        # Validate settings
        errors = _settings.validate()
        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
    
    return _settings


def reload_settings() -> ApplicationSettings:
    """Reload settings from environment."""
    global _settings
    _settings = ApplicationSettings()
    
    # Validate settings
    errors = _settings.validate()
    if errors:
        raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
    
    return _settings


class Settings:
    """Legacy Settings class for backward compatibility."""
    def __init__(self):
        app_settings = get_settings()
        for key, value in app_settings.__dict__.items():
            setattr(self, key, value)


__all__ = [
    "ApplicationSettings",
    "LLMSettings",
    "SecuritySettings",
    "PerformanceSettings",
    "DatabaseSettings",
    "LoggingSettings",
    "Settings",
    "get_settings",
    "reload_settings"
]