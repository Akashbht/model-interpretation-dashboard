from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseModelConnector(ABC):
    """Base class for all model connectors"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response from the model"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information and capabilities"""
        pass
    
    def validate_connection(self) -> bool:
        """Test if the model connection is working"""
        try:
            test_response = self.generate_response("Hello, can you respond?")
            return test_response.get('success', False)
        except:
            return False