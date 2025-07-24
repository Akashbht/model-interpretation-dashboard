import openai
import time
from typing import Dict, Any, List
from .base_connector import BaseModelConnector

class GPTConnector(BaseModelConnector):
    """Connector for OpenAI GPT models"""
    
    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        super().__init__(model_name)
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name
        
    def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response from GPT model"""
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            end_time = time.time()
            latency = end_time - start_time
            
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
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
            'provider': 'OpenAI',
            'max_context_length': self._get_context_length(),
            'cost_per_1k_tokens': self._get_cost_per_1k_tokens(),
            'modalities': ['text']
        }
    
    def _get_context_length(self) -> int:
        """Get context length for the model"""
        context_lengths = {
            'gpt-4': 8192,
            'gpt-4-32k': 32768,
            'gpt-4-turbo': 128000,
            'gpt-3.5-turbo': 4096,
            'gpt-3.5-turbo-16k': 16384
        }
        return context_lengths.get(self.model_name, 4096)
    
    def _get_cost_per_1k_tokens(self) -> float:
        """Get cost per 1K tokens (approximate values)"""
        costs = {
            'gpt-4': 0.03,
            'gpt-4-32k': 0.06,
            'gpt-4-turbo': 0.01,
            'gpt-3.5-turbo': 0.002,
            'gpt-3.5-turbo-16k': 0.004
        }
        return costs.get(self.model_name, 0.002)