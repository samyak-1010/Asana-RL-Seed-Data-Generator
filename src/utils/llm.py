"""
LLM utilities for content generation using Anthropic API.
"""
import logging
import time
from typing import List, Optional
from anthropic import Anthropic
import config

logger = logging.getLogger(__name__)


class LLMGenerator:
    """Wrapper for Anthropic API for generating realistic content."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """Initialize LLM generator."""
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        if not self.api_key:
            logger.warning("No API key provided. LLM generation will be disabled.")
            self.client = None
        else:
            self.client = Anthropic(api_key=self.api_key)
        self.model = model or config.LLM_MODEL
        self.call_count = 0
        self.total_tokens = 0
        
    def generate(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = None,
        system: str = None
    ) -> str:
        """
        Generate text using Claude API.
        
        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)
            system: System prompt
            
        Returns:
            Generated text
        """
        if not self.client:
            logger.warning("LLM client not initialized. Returning placeholder.")
            return "[LLM-GENERATED-CONTENT]"
            
        try:
            max_tokens = max_tokens or config.LLM_MAX_TOKENS
            temperature = temperature if temperature is not None else config.LLM_TEMPERATURE
            
            message_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            if system:
                message_params["system"] = system
                
            response = self.client.messages.create(**message_params)
            
            self.call_count += 1
            self.total_tokens += response.usage.input_tokens + response.usage.output_tokens
            
            # Extract text from response
            text = response.content[0].text
            
            logger.debug(f"LLM call #{self.call_count}: {len(text)} chars generated")
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return "[LLM-ERROR]"
            
    def generate_batch(
        self,
        prompts: List[str],
        max_tokens: int = None,
        temperature: float = None,
        system: str = None,
        delay: float = 0.5
    ) -> List[str]:
        """
        Generate multiple texts with rate limiting.
        
        Args:
            prompts: List of prompts
            max_tokens: Maximum tokens per generation
            temperature: Sampling temperature
            system: System prompt
            delay: Delay between calls (seconds)
            
        Returns:
            List of generated texts
        """
        results = []
        for i, prompt in enumerate(prompts):
            result = self.generate(prompt, max_tokens, temperature, system)
            results.append(result)
            
            # Rate limiting
            if i < len(prompts) - 1:
                time.sleep(delay)
                
        return results
        
    def get_stats(self) -> dict:
        """Get usage statistics."""
        return {
            'call_count': self.call_count,
            'total_tokens': self.total_tokens
        }


def load_prompt_template(template_name: str) -> str:
    """
    Load prompt template from file.
    
    Args:
        template_name: Name of template file (without .txt extension)
        
    Returns:
        Template content
    """
    try:
        with open(f'prompts/{template_name}.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Prompt template not found: {template_name}")
        return ""


def format_prompt(template: str, **kwargs) -> str:
    """
    Format prompt template with variables.
    
    Args:
        template: Prompt template with {variable} placeholders
        **kwargs: Variable values
        
    Returns:
        Formatted prompt
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.error(f"Missing template variable: {e}")
        return template