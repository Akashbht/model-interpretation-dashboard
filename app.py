import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import pickle
import os
from io import BytesIO
import base64

# Import utility modules
from utils.model_loader import ModelLoader
from utils.data_processor import DataProcessor
from utils.explainer import ExplainerManager
from components.upload_section import render_upload_section
from components.prediction_panel import render_prediction_panel
from components.explanation_panel import render_explanation_panel
from components.whatif_analysis import render_whatif_analysis

# Configure Streamlit page
st.set_page_config(
    page_title="Model Interpretation Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    st.title("🔍 Model Interpretation Dashboard")
    st.markdown("**Visualize and interpret black-box ML model predictions using SHAP and LIME**")
    
    # Initialize session state
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'explainer_manager' not in st.session_state:
        st.session_state.explainer_manager = None
    if 'predictions' not in st.session_state:
        st.session_state.predictions = None
    if 'selected_instance' not in st.session_state:
        st.session_state.selected_instance = None
    
    # Sidebar for uploads and configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Model and data upload section
        model_uploaded, data_uploaded = render_upload_section()
        
        if model_uploaded and data_uploaded:
            st.success("✅ Model and data loaded successfully!")
            
            # Initialize explainer if not already done
            if st.session_state.explainer_manager is None:
                with st.spinner("Initializing explainers..."):
                    st.session_state.explainer_manager = ExplainerManager(
                        st.session_state.model, 
                        st.session_state.data
                    )
                st.success("Explainers initialized!")
    
    # Main content area
    if st.session_state.model is not None and st.session_state.data is not None:
        
        # Create tabs for different functionalities
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Predictions", 
            "🔍 Global Explanations", 
            "🎯 Local Explanations", 
            "🔄 What-If Analysis"
        ])
        
        with tab1:
            render_prediction_panel()
        
        with tab2:
            if st.session_state.explainer_manager:
                render_explanation_panel("global")
        
        with tab3:
            if st.session_state.explainer_manager:
                render_explanation_panel("local")
        
        with tab4:
            if st.session_state.explainer_manager:
                render_whatif_analysis()
    
    else:
        # Welcome screen when no model/data is loaded
        st.markdown("""
        ## Welcome to the Model Interpretation Dashboard!
        
        To get started:
        1. **Upload a trained ML model** (sklearn, XGBoost) in the sidebar
        2. **Upload a dataset** (.csv) for analysis
        3. **Explore predictions** and explanations across different tabs
        
        ### Features:
        - 📊 **Predictions**: View model predictions on your dataset
        - 🔍 **Global Explanations**: Understand overall feature importance
        - 🎯 **Local Explanations**: Analyze individual prediction explanations
        - 🔄 **What-If Analysis**: Modify features and see prediction changes
        
        ### Supported:
        - **Models**: scikit-learn, XGBoost (pickled/joblib format)
        - **Data**: CSV files with numerical and categorical features
        - **Explanations**: SHAP and LIME
        """)

if __name__ == "__main__":
    main()