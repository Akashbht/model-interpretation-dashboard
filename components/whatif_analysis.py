import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_whatif_analysis():
    """Render the what-if analysis panel for feature manipulation"""
    st.header("🔄 What-If Analysis")
    st.markdown("Modify feature values to see how they affect model predictions")
    
    if st.session_state.model is None or st.session_state.data is None:
        st.warning("Please upload both model and data first.")
        return
    
    # Initialize what-if session state
    if 'whatif_instance' not in st.session_state:
        st.session_state.whatif_instance = None
    if 'whatif_modified' not in st.session_state:
        st.session_state.whatif_modified = None
    if 'whatif_history' not in st.session_state:
        st.session_state.whatif_history = []
    
    # Instance selection section
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("📋 Select Base Instance")
        
        # Use selected instance from other panels if available
        default_idx = st.session_state.selected_instance if st.session_state.selected_instance is not None else 0
        
        base_instance_idx = st.number_input(
            "Base Instance Index",
            min_value=0,
            max_value=len(st.session_state.data) - 1,
            value=default_idx,
            step=1,
            key="whatif_base_selector"
        )
        
        if st.button("🎯 Load Instance", key="load_whatif_instance"):
            # Load the selected instance
            st.session_state.whatif_instance = st.session_state.data.iloc[base_instance_idx].copy()
            st.session_state.whatif_modified = st.session_state.whatif_instance.copy()
            st.success(f"Loaded instance {base_instance_idx}")
        
        # Reset button
        if st.button("🔄 Reset to Original", key="reset_whatif"):
            if st.session_state.whatif_instance is not None:
                st.session_state.whatif_modified = st.session_state.whatif_instance.copy()
                st.success("Reset to original values")
    
    with col1:
        if st.session_state.whatif_instance is not None:
            st.subheader("📊 Current Prediction")
            
            # Get current prediction
            current_instance = st.session_state.whatif_modified.values.reshape(1, -1)
            current_pred = st.session_state.model.predict(current_instance)[0]
            
            # Display prediction
            col_pred1, col_pred2 = st.columns(2)
            
            with col_pred1:
                st.metric("Current Prediction", f"{current_pred}")
            
            # Show probabilities if available
            if hasattr(st.session_state.model, 'predict_proba'):
                try:
                    current_proba = st.session_state.model.predict_proba(current_instance)[0]
                    max_prob = np.max(current_proba)
                    with col_pred2:
                        st.metric("Confidence", f"{max_prob:.3f}")
                    
                    # Show probability distribution
                    prob_df = pd.DataFrame({
                        'Class': [f'Class_{i}' for i in range(len(current_proba))],
                        'Probability': current_proba
                    })
                    
                    fig_prob = px.bar(
                        prob_df,
                        x='Class',
                        y='Probability',
                        title="Prediction Probabilities"
                    )
                    fig_prob.update_layout(height=300)
                    st.plotly_chart(fig_prob, use_container_width=True)
                    
                except:
                    pass
    
    # Feature modification section
    if st.session_state.whatif_instance is not None:
        st.subheader("🎛️ Modify Features")
        
        # Create tabs for different modification approaches
        tab1, tab2, tab3 = st.tabs(["Manual Edit", "Slider Controls", "Batch Modifications"])
        
        with tab1:
            st.markdown("**Edit individual feature values manually:**")
            
            # Display original and current values in editable form
            original_values = st.session_state.whatif_instance
            modified_values = st.session_state.whatif_modified.copy()
            
            # Create form for editing
            with st.form("manual_edit_form"):
                edited_values = {}
                
                # Create columns for better layout
                num_cols = 3
                cols = st.columns(num_cols)
                
                for i, (feature, value) in enumerate(modified_values.items()):
                    col_idx = i % num_cols
                    
                    with cols[col_idx]:
                        # Determine input type based on data type
                        if np.issubdtype(type(value), np.integer):
                            edited_values[feature] = st.number_input(
                                f"{feature}",
                                value=int(value),
                                step=1,
                                key=f"manual_{feature}"
                            )
                        elif np.issubdtype(type(value), np.floating):
                            edited_values[feature] = st.number_input(
                                f"{feature}",
                                value=float(value),
                                step=0.01,
                                format="%.3f",
                                key=f"manual_{feature}"
                            )
                        else:
                            edited_values[feature] = st.number_input(
                                f"{feature}",
                                value=float(value),
                                step=0.01,
                                format="%.3f",
                                key=f"manual_{feature}"
                            )
                
                if st.form_submit_button("✅ Apply Changes"):
                    st.session_state.whatif_modified = pd.Series(edited_values)
                    st.success("Features updated!")
                    st.rerun()
        
        with tab2:
            st.markdown("**Use sliders to modify features:**")
            
            # Select features to modify with sliders
            selected_features = st.multiselect(
                "Select features to modify:",
                options=list(st.session_state.whatif_modified.index),
                default=list(st.session_state.whatif_modified.index)[:5],  # Default to first 5
                key="slider_features"
            )
            
            if selected_features:
                slider_values = {}
                
                for feature in selected_features:
                    current_value = st.session_state.whatif_modified[feature]
                    
                    # Calculate reasonable range based on data distribution
                    feature_data = st.session_state.data[feature]
                    min_val = float(feature_data.min())
                    max_val = float(feature_data.max())
                    
                    # Extend range slightly
                    range_extend = (max_val - min_val) * 0.2
                    slider_min = min_val - range_extend
                    slider_max = max_val + range_extend
                    
                    slider_values[feature] = st.slider(
                        f"{feature}",
                        min_value=slider_min,
                        max_value=slider_max,
                        value=float(current_value),
                        step=(slider_max - slider_min) / 100,
                        key=f"slider_{feature}"
                    )
                
                if st.button("🎚️ Apply Slider Values", key="apply_sliders"):
                    for feature, value in slider_values.items():
                        st.session_state.whatif_modified[feature] = value
                    st.success("Slider values applied!")
                    st.rerun()
        
        with tab3:
            st.markdown("**Apply batch modifications:**")
            
            # Percentage modifications
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Scale all features:**")
                scale_factor = st.slider(
                    "Scale factor",
                    min_value=0.1,
                    max_value=2.0,
                    value=1.0,
                    step=0.1,
                    key="scale_factor"
                )
                
                if st.button("📈 Apply Scaling", key="apply_scaling"):
                    st.session_state.whatif_modified = st.session_state.whatif_modified * scale_factor
                    st.success(f"All features scaled by {scale_factor}")
                    st.rerun()
            
            with col2:
                st.markdown("**Add noise:**")
                noise_level = st.slider(
                    "Noise level (%)",
                    min_value=0.0,
                    max_value=50.0,
                    value=5.0,
                    step=1.0,
                    key="noise_level"
                )
                
                if st.button("🎲 Add Random Noise", key="add_noise"):
                    noise = np.random.normal(0, noise_level/100, len(st.session_state.whatif_modified))
                    st.session_state.whatif_modified = st.session_state.whatif_modified * (1 + noise)
                    st.success(f"Added {noise_level}% noise")
                    st.rerun()
        
        # Save current state to history
        if st.button("💾 Save Current State", key="save_state"):
            current_pred = st.session_state.model.predict(
                st.session_state.whatif_modified.values.reshape(1, -1)
            )[0]
            
            state = {
                'features': st.session_state.whatif_modified.copy(),
                'prediction': current_pred,
                'timestamp': pd.Timestamp.now()
            }
            
            st.session_state.whatif_history.append(state)
            st.success("State saved to history!")
        
        # History section
        if st.session_state.whatif_history:
            st.subheader("📚 Modification History")
            
            # Display history table
            history_data = []
            for i, state in enumerate(st.session_state.whatif_history):
                history_data.append({
                    'Index': i,
                    'Prediction': state['prediction'],
                    'Timestamp': state['timestamp'].strftime("%H:%M:%S")
                })
            
            history_df = pd.DataFrame(history_data)
            
            # Add selection
            selected_history = st.selectbox(
                "Select a saved state to restore:",
                options=range(len(st.session_state.whatif_history)),
                format_func=lambda x: f"State {x}: Pred={st.session_state.whatif_history[x]['prediction']:.3f}",
                key="history_selector"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Restore Selected", key="restore_history"):
                    st.session_state.whatif_modified = st.session_state.whatif_history[selected_history]['features']
                    st.success(f"Restored state {selected_history}")
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Clear History", key="clear_history"):
                    st.session_state.whatif_history = []
                    st.success("History cleared")
                    st.rerun()
            
            with col3:
                # Download history
                if st.button("📥 Export History", key="export_history"):
                    history_export = []
                    for i, state in enumerate(st.session_state.whatif_history):
                        row = {'State_Index': i, 'Prediction': state['prediction']}
                        row.update(state['features'].to_dict())
                        history_export.append(row)
                    
                    history_csv = pd.DataFrame(history_export).to_csv(index=False)
                    st.download_button(
                        label="📄 Download History CSV",
                        data=history_csv,
                        file_name="whatif_analysis_history.csv",
                        mime="text/csv"
                    )
    
    else:
        st.info("👆 Please select and load a base instance to start what-if analysis.")