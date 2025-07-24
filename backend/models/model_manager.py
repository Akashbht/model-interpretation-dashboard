from typing import Dict, Any, List, Optional
import json
import os
from .gpt_connector import GPTConnector
from .claude_connector import ClaudeConnector
from .base_connector import BaseModelConnector

class ModelManager:
    """Manages all available models and their configurations"""
    
    def __init__(self):
        self.models = {}
        self.config_file = "models_config.json"
        self._load_default_models()
        self._load_config()
    
    def _load_default_models(self):
        """Load default model configurations"""
        # OpenAI models
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            gpt_models = [
                'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k'
            ]
            for model in gpt_models:
                self.models[f"openai_{model}"] = {
                    'connector_class': GPTConnector,
                    'api_key': openai_api_key,
                    'model_name': model,
                    'enabled': True
                }
        
        # Anthropic models
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_api_key:
            claude_models = [
                'claude-3-opus-20240229', 'claude-3-sonnet-20240229', 
                'claude-3-haiku-20240307', 'claude-2.1'
            ]
            for model in claude_models:
                self.models[f"anthropic_{model}"] = {
                    'connector_class': ClaudeConnector,
                    'api_key': anthropic_api_key,
                    'model_name': model,
                    'enabled': True
                }
    
    def _load_config(self):
        """Load model configurations from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Update existing models with saved config
                    for model_id, model_config in config.items():
                        if model_id in self.models:
                            self.models[model_id].update(model_config)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def _save_config(self):
        """Save current model configurations to file"""
        try:
            # Only save serializable parts (exclude connector_class)
            config = {}
            for model_id, model_data in self.models.items():
                config[model_id] = {
                    'model_name': model_data['model_name'],
                    'enabled': model_data['enabled'],
                    'api_key': model_data.get('api_key', ''),
                    'custom_endpoint': model_data.get('custom_endpoint', '')
                }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of all available models"""
        models_list = []
        
        for model_id, model_data in self.models.items():
            if model_data.get('enabled', True):
                try:
                    connector = self._create_connector(model_id)
                    if connector:
                        model_info = connector.get_model_info()
                        model_info['id'] = model_id
                        model_info['connected'] = connector.validate_connection()
                        models_list.append(model_info)
                except Exception as e:
                    print(f"Error getting info for model {model_id}: {e}")
        
        return models_list
    
    def add_model(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new custom model"""
        try:
            model_id = f"custom_{model_config['name']}"
            
            # TODO: Add support for custom endpoints
            # For now, assume it's either OpenAI or Anthropic compatible
            
            self.models[model_id] = {
                'connector_class': GPTConnector,  # Default to GPT for custom models
                'api_key': model_config.get('api_key', ''),
                'model_name': model_config['name'],
                'enabled': True,
                'custom_endpoint': model_config.get('endpoint', '')
            }
            
            self._save_config()
            
            return {'success': True, 'model_id': model_id}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_model_connector(self, model_id: str) -> Optional[BaseModelConnector]:
        """Get connector instance for a specific model"""
        return self._create_connector(model_id)
    
    def _create_connector(self, model_id: str) -> Optional[BaseModelConnector]:
        """Create connector instance for a model"""
        if model_id not in self.models:
            return None
        
        model_data = self.models[model_id]
        
        try:
            connector_class = model_data['connector_class']
            api_key = model_data.get('api_key', '')
            model_name = model_data['model_name']
            
            if not api_key:
                return None
            
            return connector_class(api_key=api_key, model_name=model_name)
            
        except Exception as e:
            print(f"Error creating connector for {model_id}: {e}")
            return None