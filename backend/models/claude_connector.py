import anthropic
import time
from typing import Dict, Any, List
from .base_connector import BaseModelConnector

class ClaudeConnector(BaseModelConnector):
    """Connector for Anthropic Claude models"""
    
    def __init__(self, api_key: str, model_name: str = "claude-3-sonnet-20240229"):
        super().__init__(model_name)
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_name = model_name
        
    def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response from Claude model"""
        start_time = time.time()
        
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7),
                messages=[{"role": "user", "content": prompt}]
            )
            
            end_time = time.time()
            latency = end_time - start_time
            
            response_text = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            return {
                'response': response_text,
                'latency': latency,
                'tokens_used': tokens_used,
                'model': self.model_name,
                'success': True
            }
            
        except Exception as e:
            end_time = time.time()
            return {
                'response': None,
                'latency': end_time - start_time,
                'tokens_used': 0,
                'model': self.model_name,
                'success': False,
                'error': str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            'name': self.model_name,
            'provider': 'Anthropic',
            'max_context_length': self._get_context_length(),
            'cost_per_1k_tokens': self._get_cost_per_1k_tokens(),
            'modalities': ['text', 'image'] if 'claude-3' in self.model_name else ['text']
        }
    
    def _get_context_length(self) -> int:
        """Get context length for the model"""
        context_lengths = {
            'claude-3-opus-20240229': 200000,
            'claude-3-sonnet-20240229': 200000,
            'claude-3-haiku-20240307': 200000,
            'claude-2.1': 200000,
            'claude-2.0': 100000,
            'claude-instant-1.2': 100000
        }
        return context_lengths.get(self.model_name, 100000)
    
    def _get_cost_per_1k_tokens(self) -> float:
        """Get cost per 1K tokens (approximate values)"""
        costs = {
            'claude-3-opus-20240229': 0.075,
            'claude-3-sonnet-20240229': 0.015,
            'claude-3-haiku-20240307': 0.0025,
            'claude-2.1': 0.024,
            'claude-2.0': 0.024,
            'claude-instant-1.2': 0.008
        }
        return costs.get(self.model_name, 0.024)