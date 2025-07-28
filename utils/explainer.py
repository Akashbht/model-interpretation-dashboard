import streamlit as st
import shap
import lime
import lime.lime_tabular
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ExplainerManager:
    """Manager class for SHAP and LIME explainers"""
    
    def __init__(self, model, data):
        """
        Initialize explainers
        
        Args:
            model: Trained ML model
            data: pandas DataFrame with training/background data
        """
        self.model = model
        self.data = data
        self.shap_explainer = None
        self.lime_explainer = None
        self.background_data = None
        
        # Initialize explainers
        self._initialize_shap()
        self._initialize_lime()
    
    def _initialize_shap(self):
        """Initialize SHAP explainer"""
        try:
            # Use a sample of data as background for SHAP
            if len(self.data) > 100:
                self.background_data = shap.sample(self.data, 100)
            else:
                self.background_data = self.data
            
            # Try different SHAP explainers based on model type
            try:
                # Try TreeExplainer first (for tree-based models)
                self.shap_explainer = shap.TreeExplainer(self.model)
            except:
                try:
                    # Try LinearExplainer for linear models
                    self.shap_explainer = shap.LinearExplainer(self.model, self.background_data)
                except:
                    # Fall back to KernelExplainer (slower but works for any model)
                    self.shap_explainer = shap.KernelExplainer(self.model.predict, self.background_data)
            
            st.success("SHAP explainer initialized successfully!")
            
        except Exception as e:
            st.error(f"Error initializing SHAP explainer: {str(e)}")
            self.shap_explainer = None
    
    def _initialize_lime(self):
        """Initialize LIME explainer"""
        try:
            # Determine mode based on prediction output
            try:
                sample_pred = self.model.predict(self.data.iloc[:1])
                if hasattr(self.model, 'predict_proba'):
                    mode = 'classification'
                else:
                    mode = 'regression'
            except:
                mode = 'regression'  # Default to regression
            
            # Create LIME explainer
            self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                self.data.values,
                feature_names=self.data.columns,
                mode=mode,
                discretize_continuous=True
            )
            
            st.success("LIME explainer initialized successfully!")
            
        except Exception as e:
            st.error(f"Error initializing LIME explainer: {str(e)}")
            self.lime_explainer = None
    
    def get_shap_global_importance(self):
        """Get global feature importance using SHAP"""
        if self.shap_explainer is None:
            return None
        
        try:
            # Calculate SHAP values for the dataset
            shap_values = self.shap_explainer.shap_values(self.data)
            
            # Handle different output formats
            if isinstance(shap_values, list):
                # Multi-class classification - use first class
                shap_values = shap_values[0]
            
            # Calculate mean absolute SHAP values for each feature
            importance = np.abs(shap_values).mean(axis=0)
            
            return pd.DataFrame({
                'feature': self.data.columns,
                'importance': importance
            }).sort_values('importance', ascending=False)
            
        except Exception as e:
            st.error(f"Error calculating SHAP global importance: {str(e)}")
            return None
    
    def get_shap_local_explanation(self, instance_idx):
        """Get local explanation for a specific instance using SHAP"""
        if self.shap_explainer is None:
            return None
        
        try:
            # Get single instance
            instance = self.data.iloc[instance_idx:instance_idx+1]
            
            # Calculate SHAP values
            shap_values = self.shap_explainer.shap_values(instance)
            
            # Handle different output formats
            if isinstance(shap_values, list):
                shap_values = shap_values[0]
            
            return {
                'shap_values': shap_values[0],
                'feature_names': self.data.columns,
                'instance_values': instance.values[0]
            }
            
        except Exception as e:
            st.error(f"Error calculating SHAP local explanation: {str(e)}")
            return None
    
    def get_lime_local_explanation(self, instance_idx, num_features=10):
        """Get local explanation for a specific instance using LIME"""
        if self.lime_explainer is None:
            return None
        
        try:
            # Get single instance
            instance = self.data.iloc[instance_idx].values
            
            # Generate LIME explanation
            explanation = self.lime_explainer.explain_instance(
                instance,
                self.model.predict,
                num_features=num_features
            )
            
            # Extract feature importance
            importance_dict = dict(explanation.as_list())
            
            return {
                'feature_importance': importance_dict,
                'explanation_object': explanation
            }
            
        except Exception as e:
            st.error(f"Error calculating LIME local explanation: {str(e)}")
            return None
    
    def create_global_importance_plot(self):
        """Create plotly figure for global feature importance"""
        importance_df = self.get_shap_global_importance()
        
        if importance_df is None:
            return None
        
        # Create bar plot
        fig = px.bar(
            importance_df.head(15),  # Show top 15 features
            x='importance',
            y='feature',
            orientation='h',
            title='Global Feature Importance (SHAP)',
            labels={'importance': 'Mean |SHAP Value|', 'feature': 'Features'}
        )
        
        fig.update_layout(
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def create_local_explanation_plot(self, explanation_data, method='SHAP'):
        """Create plotly figure for local explanation"""
        if explanation_data is None:
            return None
        
        try:
            if method == 'SHAP':
                shap_values = explanation_data['shap_values']
                feature_names = explanation_data['feature_names']
                
                # Create DataFrame for plotting
                plot_df = pd.DataFrame({
                    'feature': feature_names,
                    'shap_value': shap_values
                }).sort_values('shap_value', key=abs, ascending=False).head(15)
                
                # Create bar plot
                fig = px.bar(
                    plot_df,
                    x='shap_value',
                    y='feature',
                    orientation='h',
                    title='Local Feature Explanation (SHAP)',
                    labels={'shap_value': 'SHAP Value', 'feature': 'Features'},
                    color='shap_value',
                    color_continuous_scale='RdBu_r'
                )
                
            else:  # LIME
                importance_dict = explanation_data['feature_importance']
                
                # Create DataFrame for plotting
                plot_df = pd.DataFrame([
                    {'feature': feature, 'importance': importance}
                    for feature, importance in importance_dict.items()
                ]).sort_values('importance', key=abs, ascending=False)
                
                # Create bar plot
                fig = px.bar(
                    plot_df,
                    x='importance',
                    y='feature',
                    orientation='h',
                    title='Local Feature Explanation (LIME)',
                    labels={'importance': 'LIME Importance', 'feature': 'Features'},
                    color='importance',
                    color_continuous_scale='RdBu_r'
                )
            
            fig.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating explanation plot: {str(e)}")
            return None