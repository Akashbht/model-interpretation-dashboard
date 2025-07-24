import joblib
import pickle
import streamlit as st
from sklearn.base import BaseEstimator
import pandas as pd

class ModelLoader:
    """Utility class for loading ML models"""
    
    @staticmethod
    def load_model(uploaded_file):
        """
        Load a model from uploaded file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Loaded model object or None if failed
        """
        try:
            # Get file extension
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension in ['pkl', 'pickle']:
                # Load pickle file
                model = pickle.load(uploaded_file)
            elif file_extension in ['joblib', 'jl']:
                # Load joblib file
                model = joblib.load(uploaded_file)
            else:
                st.error(f"Unsupported file format: {file_extension}. Please use .pkl, .pickle, .joblib, or .jl files.")
                return None
            
            # Validate that it's a sklearn-like model
            if not hasattr(model, 'predict'):
                st.error("Uploaded file does not contain a valid ML model with predict method.")
                return None
            
            return model
            
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return None
    
    @staticmethod
    def get_model_info(model):
        """
        Get information about the loaded model
        
        Args:
            model: Loaded ML model
            
        Returns:
            Dictionary with model information
        """
        info = {
            'type': type(model).__name__,
            'module': type(model).__module__,
            'has_predict_proba': hasattr(model, 'predict_proba'),
            'has_feature_importances': hasattr(model, 'feature_importances_'),
        }
        
        # Try to get number of features if available
        if hasattr(model, 'n_features_in_'):
            info['n_features'] = model.n_features_in_
        elif hasattr(model, 'feature_importances_'):
            info['n_features'] = len(model.feature_importances_)
        
        return info