import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_explanation_panel(explanation_type):
    """
    Render explanation panel for global or local explanations
    
    Args:
        explanation_type: 'global' or 'local'
    """
    
    if explanation_type == "global":
        st.header("🔍 Global Feature Importance")
        st.markdown("Understanding which features are most important across all predictions")
        
        # Global SHAP importance
        if st.button("🚀 Calculate Global Importance", key="calc_global"):
            with st.spinner("Calculating global feature importance..."):
                fig = st.session_state.explainer_manager.create_global_importance_plot()
                
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show importance table
                    importance_df = st.session_state.explainer_manager.get_shap_global_importance()
                    if importance_df is not None:
                        st.subheader("Feature Importance Table")
                        st.dataframe(importance_df, use_container_width=True)
                        
                        # Download importance data
                        csv = importance_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Importance Data",
                            data=csv,
                            file_name="global_feature_importance.csv",
                            mime="text/csv"
                        )
                else:
                    st.error("Could not calculate global importance. Please check your model and data.")
    
    else:  # local explanations
        st.header("🎯 Local Feature Explanations")
        st.markdown("Understanding why the model made a specific prediction for individual instances")
        
        # Instance selection
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.subheader("Select Instance")
            
            # Use selected instance from predictions panel if available
            default_idx = st.session_state.selected_instance if st.session_state.selected_instance is not None else 0
            
            instance_idx = st.number_input(
                "Instance Index",
                min_value=0,
                max_value=len(st.session_state.data) - 1,
                value=default_idx,
                step=1,
                key="local_instance_selector"
            )
            
            # Show instance details
            if st.button("📋 Show Instance Details", key="show_instance"):
                st.subheader("Instance Information")
                
                # Show original data
                instance_data = st.session_state.raw_data.iloc[instance_idx]
                prediction = st.session_state.predictions[instance_idx] if st.session_state.predictions is not None else "N/A"
                
                st.write("**Prediction:**", prediction)
                
                # Show probability if available
                if hasattr(st.session_state, 'pred_probabilities') and st.session_state.pred_probabilities is not None:
                    probs = st.session_state.pred_probabilities[instance_idx]
                    prob_df = pd.DataFrame({
                        'Class': [f'Class_{i}' for i in range(len(probs))],
                        'Probability': probs
                    })
                    st.write("**Prediction Probabilities:**")
                    st.dataframe(prob_df, use_container_width=True)
                
                st.write("**Feature Values:**")
                st.dataframe(pd.DataFrame(instance_data).T, use_container_width=True)
        
        with col1:
            # Explanation method selection
            st.subheader("Choose Explanation Method")
            
            explanation_method = st.radio(
                "Select method:",
                ["SHAP", "LIME"],
                horizontal=True,
                help="SHAP is faster and more consistent, LIME provides different perspective"
            )
            
            if st.button(f"🔍 Generate {explanation_method} Explanation", key=f"calc_{explanation_method.lower()}"):
                with st.spinner(f"Calculating {explanation_method} explanation..."):
                    
                    if explanation_method == "SHAP":
                        explanation_data = st.session_state.explainer_manager.get_shap_local_explanation(instance_idx)
                    else:  # LIME
                        explanation_data = st.session_state.explainer_manager.get_lime_local_explanation(instance_idx)
                    
                    if explanation_data is not None:
                        # Create and display plot
                        fig = st.session_state.explainer_manager.create_local_explanation_plot(
                            explanation_data, 
                            method=explanation_method
                        )
                        
                        if fig is not None:
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Show explanation table
                            st.subheader(f"{explanation_method} Explanation Details")
                            
                            if explanation_method == "SHAP":
                                exp_df = pd.DataFrame({
                                    'Feature': explanation_data['feature_names'],
                                    'Feature_Value': explanation_data['instance_values'],
                                    'SHAP_Value': explanation_data['shap_values']
                                }).sort_values('SHAP_Value', key=abs, ascending=False)
                                
                            else:  # LIME
                                exp_df = pd.DataFrame([
                                    {'Feature': feature, 'LIME_Importance': importance}
                                    for feature, importance in explanation_data['feature_importance'].items()
                                ]).sort_values('LIME_Importance', key=abs, ascending=False)
                            
                            st.dataframe(exp_df, use_container_width=True)
                            
                            # Download explanation data
                            csv = exp_df.to_csv(index=False)
                            st.download_button(
                                label=f"📥 Download {explanation_method} Explanation",
                                data=csv,
                                file_name=f"{explanation_method.lower()}_explanation_instance_{instance_idx}.csv",
                                mime="text/csv",
                                key=f"download_{explanation_method.lower()}"
                            )
                        
                        else:
                            st.error(f"Could not create {explanation_method} explanation plot.")
                    
                    else:
                        st.error(f"Could not calculate {explanation_method} explanation. Please check your model and data.")
        
        # Comparison section
        st.subheader("🔄 Compare Explanations")
        st.markdown("Generate both SHAP and LIME explanations to compare different perspectives")
        
        if st.button("⚡ Generate Both SHAP & LIME", key="compare_explanations"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**SHAP Explanation**")
                with st.spinner("Calculating SHAP..."):
                    shap_data = st.session_state.explainer_manager.get_shap_local_explanation(instance_idx)
                    if shap_data:
                        shap_fig = st.session_state.explainer_manager.create_local_explanation_plot(shap_data, "SHAP")
                        if shap_fig:
                            st.plotly_chart(shap_fig, use_container_width=True)
            
            with col2:
                st.markdown("**LIME Explanation**")
                with st.spinner("Calculating LIME..."):
                    lime_data = st.session_state.explainer_manager.get_lime_local_explanation(instance_idx)
                    if lime_data:
                        lime_fig = st.session_state.explainer_manager.create_local_explanation_plot(lime_data, "LIME")
                        if lime_fig:
                            st.plotly_chart(lime_fig, use_container_width=True)