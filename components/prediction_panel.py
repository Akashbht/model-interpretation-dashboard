import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_prediction_panel():
    """Render the predictions panel"""
    st.header("📊 Model Predictions")
    
    if st.session_state.model is None or st.session_state.data is None:
        st.warning("Please upload both model and data first.")
        return
    
    # Generate predictions if not already done
    if st.session_state.predictions is None:
        with st.spinner("Generating predictions..."):
            try:
                predictions = st.session_state.model.predict(st.session_state.data)
                st.session_state.predictions = predictions
                
                # Try to get prediction probabilities for classification
                if hasattr(st.session_state.model, 'predict_proba'):
                    try:
                        pred_proba = st.session_state.model.predict_proba(st.session_state.data)
                        st.session_state.pred_probabilities = pred_proba
                    except:
                        st.session_state.pred_probabilities = None
                
            except Exception as e:
                st.error(f"Error generating predictions: {str(e)}")
                return
    
    # Display prediction statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Predictions", len(st.session_state.predictions))
    
    with col2:
        if np.issubdtype(st.session_state.predictions.dtype, np.number):
            st.metric("Mean Prediction", f"{np.mean(st.session_state.predictions):.3f}")
        else:
            unique_preds = np.unique(st.session_state.predictions)
            st.metric("Unique Classes", len(unique_preds))
    
    with col3:
        if np.issubdtype(st.session_state.predictions.dtype, np.number):
            st.metric("Std Prediction", f"{np.std(st.session_state.predictions):.3f}")
        else:
            most_common = pd.Series(st.session_state.predictions).value_counts().index[0]
            st.metric("Most Common", str(most_common))
    
    with col4:
        if np.issubdtype(st.session_state.predictions.dtype, np.number):
            st.metric("Prediction Range", f"{np.ptp(st.session_state.predictions):.3f}")
        else:
            least_common = pd.Series(st.session_state.predictions).value_counts().index[-1]
            st.metric("Least Common", str(least_common))
    
    # Visualization section
    st.subheader("Prediction Distribution")
    
    # Create distribution plot based on prediction type
    if np.issubdtype(st.session_state.predictions.dtype, np.number):
        # Numerical predictions - histogram
        fig = px.histogram(
            x=st.session_state.predictions,
            nbins=30,
            title="Distribution of Predictions",
            labels={'x': 'Prediction Value', 'count': 'Frequency'}
        )
    else:
        # Categorical predictions - bar chart
        pred_counts = pd.Series(st.session_state.predictions).value_counts()
        fig = px.bar(
            x=pred_counts.index,
            y=pred_counts.values,
            title="Distribution of Predicted Classes",
            labels={'x': 'Predicted Class', 'y': 'Count'}
        )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table with predictions
    st.subheader("Predictions Table")
    
    # Create display dataframe
    display_df = st.session_state.raw_data.copy()
    display_df['Prediction'] = st.session_state.predictions
    
    # Add probability columns if available
    if hasattr(st.session_state, 'pred_probabilities') and st.session_state.pred_probabilities is not None:
        prob_df = pd.DataFrame(
            st.session_state.pred_probabilities,
            columns=[f'Prob_Class_{i}' for i in range(st.session_state.pred_probabilities.shape[1])]
        )
        display_df = pd.concat([display_df, prob_df], axis=1)
    
    # Add instance selection
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.write("**Select Instance for Analysis:**")
        selected_idx = st.selectbox(
            "Choose instance index",
            range(len(display_df)),
            format_func=lambda x: f"Instance {x}",
            key="prediction_instance_selector"
        )
        
        if st.button("🎯 Analyze This Instance", key="analyze_from_predictions"):
            st.session_state.selected_instance = selected_idx
            st.success(f"Selected instance {selected_idx} for analysis")
    
    with col1:
        # Display the data table with highlighting for selected instance
        if 'selected_instance' in st.session_state and st.session_state.selected_instance is not None:
            # Highlight selected row
            styled_df = display_df.style.apply(
                lambda x: ['background-color: #ffeb3b' if x.name == st.session_state.selected_instance else '' for _ in x],
                axis=1
            )
            st.dataframe(styled_df, height=400, use_container_width=True)
        else:
            st.dataframe(display_df, height=400, use_container_width=True)
    
    # Download predictions
    st.subheader("Export Predictions")
    
    # Create CSV download
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Predictions as CSV",
        data=csv,
        file_name="predictions.csv",
        mime="text/csv"
    )