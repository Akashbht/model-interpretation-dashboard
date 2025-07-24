import streamlit as st
import pandas as pd
from utils.model_loader import ModelLoader
from utils.data_processor import DataProcessor

def render_upload_section():
    """
    Render the upload section for model and data files
    
    Returns:
        Tuple of (model_uploaded, data_uploaded) booleans
    """
    st.subheader("📁 Upload Files")
    
    model_uploaded = False
    data_uploaded = False
    
    # Model upload
    st.markdown("**1. Upload ML Model**")
    model_file = st.file_uploader(
        "Choose a model file",
        type=['pkl', 'pickle', 'joblib', 'jl'],
        help="Upload a trained scikit-learn or XGBoost model in pickle/joblib format"
    )
    
    if model_file is not None:
        if st.session_state.model is None:
            with st.spinner("Loading model..."):
                model = ModelLoader.load_model(model_file)
                if model is not None:
                    st.session_state.model = model
                    
                    # Display model info
                    model_info = ModelLoader.get_model_info(model)
                    st.success(f"✅ Model loaded: {model_info['type']}")
                    
                    with st.expander("Model Details"):
                        st.json(model_info)
        else:
            st.success("✅ Model already loaded")
        
        model_uploaded = True
    
    # Data upload
    st.markdown("**2. Upload Dataset**")
    data_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file with your dataset for analysis"
    )
    
    if data_file is not None:
        if st.session_state.data is None:
            with st.spinner("Loading data..."):
                df = DataProcessor.load_data(data_file)
                if df is not None:
                    # Process the data
                    processor = DataProcessor()
                    
                    # Let user select target column (optional)
                    target_options = ['None (No target)'] + list(df.columns)
                    target_selection = st.selectbox(
                        "Select target column (optional)",
                        target_options,
                        help="Select the target column if you want to exclude it from features"
                    )
                    
                    target_col = None if target_selection == 'None (No target)' else target_selection
                    
                    X, y, feature_names = processor.prepare_features(df, target_col)
                    
                    if X is not None:
                        st.session_state.data = X
                        st.session_state.raw_data = df
                        st.session_state.data_processor = processor
                        st.session_state.target = y
                        st.session_state.feature_names = feature_names
                        
                        # Display data info
                        data_info = processor.get_data_info(df)
                        st.success(f"✅ Data loaded: {data_info['shape']} shape")
                        
                        with st.expander("Dataset Details"):
                            st.write("**Shape:**", data_info['shape'])
                            st.write("**Columns:**", len(data_info['columns']))
                            st.write("**Categorical features:**", len(data_info['categorical_columns']))
                            st.write("**Numerical features:**", len(data_info['numerical_columns']))
                            
                            if data_info['missing_values']:
                                missing = {k: v for k, v in data_info['missing_values'].items() if v > 0}
                                if missing:
                                    st.write("**Missing values:**", missing)
        else:
            st.success("✅ Data already loaded")
        
        data_uploaded = True
    
    # Reset button
    if st.button("🔄 Reset All", help="Clear all loaded data and models"):
        st.session_state.model = None
        st.session_state.data = None
        st.session_state.raw_data = None
        st.session_state.data_processor = None
        st.session_state.target = None
        st.session_state.feature_names = None
        st.session_state.explainer_manager = None
        st.session_state.predictions = None
        st.session_state.selected_instance = None
        st.experimental_rerun()
    
    return model_uploaded, data_uploaded