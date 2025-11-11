"""
Model Configuration Utility for Google ADK Course
Based on Kaggle 5-Day Agents Course - Copyright 2025 Google LLC
Licensed under Apache 2.0

Provides intelligent model selection based on agent type and use case.
Respects environment variables for custom model configuration.
"""

import os
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv(Path(__file__).parent.parent / '.env')

AgentType = Literal["text", "multimodal", "pro"]


class ModelConfig:
    """
    Centralized model configuration based on environment variables.
    
    All models MUST be configured via environment variables in .env file:
    - GEMINI_TEXT_MODEL: For text agents
    - GEMINI_MULTIMODAL_MODEL: For multimodal agents  
    - GEMINI_PRO_MODEL: For complex reasoning
    
    Loads from .env automatically - no manual configuration needed!
    """
    
    @staticmethod
    def get_model(agent_type: AgentType = "text") -> str:
        """
        Get the appropriate model based on agent type.
        
        Args:
            agent_type: Type of agent ("text", "multimodal", "pro")
        
        Returns:
            Model identifier string from environment variable
        
        Environment Variables (REQUIRED in .env):
            GEMINI_TEXT_MODEL: Text model name
            GEMINI_MULTIMODAL_MODEL: Multimodal model name
            GEMINI_PRO_MODEL: Pro model name
        """
        if agent_type == "text":
            model = os.getenv("GEMINI_TEXT_MODEL")
            if not model:
                raise ValueError("GEMINI_TEXT_MODEL not found in .env file")
            return model
        elif agent_type == "multimodal":
            model = os.getenv("GEMINI_MULTIMODAL_MODEL")
            if not model:
                raise ValueError("GEMINI_MULTIMODAL_MODEL not found in .env file")
            return model
        elif agent_type == "pro":
            model = os.getenv("GEMINI_PRO_MODEL")
            if not model:
                raise ValueError("GEMINI_PRO_MODEL not found in .env file")
            return model
        else:
            # Fallback to text model
            model = os.getenv("GEMINI_TEXT_MODEL")
            if not model:
                raise ValueError("GEMINI_TEXT_MODEL not found in .env file")
            return model
    
    @staticmethod
    def get_text_model() -> str:
        """Get model for text-only agents (most agents)."""
        return ModelConfig.get_model("text")
    
    @staticmethod
    def get_multimodal_model() -> str:
        """Get model for multimodal agents (image generation, etc.)."""
        return ModelConfig.get_model("multimodal")
    
    @staticmethod
    def get_pro_model() -> str:
        """Get model for complex reasoning."""
        return ModelConfig.get_model("pro")


# Convenience functions for backward compatibility
def get_text_model() -> str:
    """Get model for text-only agents."""
    return ModelConfig.get_text_model()


def get_multimodal_model() -> str:
    """Get model for multimodal agents."""
    return ModelConfig.get_multimodal_model()


def get_pro_model() -> str:
    """Get model for complex reasoning."""
    return ModelConfig.get_pro_model()
