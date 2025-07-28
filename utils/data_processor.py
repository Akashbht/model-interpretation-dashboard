import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class DataProcessor:
    """Utility class for processing and preparing data"""
    
    def __init__(self):
        self.label_encoders = {}
        self.feature_names = []
        self.target_column = None
        
    @staticmethod
    def load_data(uploaded_file):
        """
        Load data from uploaded CSV file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            pandas DataFrame or None if failed
        """
        try:
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            
            # Basic validation
            if df.empty:
                st.error("Uploaded CSV file is empty.")
                return None
            
            if df.shape[1] < 2:
                st.error("Dataset must have at least 2 columns (features and target).")
                return None
            
            return df
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None
    
    def prepare_features(self, df, target_column=None):
        """
        Prepare features for model prediction and explanation
        
        Args:
            df: pandas DataFrame
            target_column: Name of target column (optional)
            
        Returns:
            Tuple of (X, y, feature_names) where y is None if no target
        """
        try:
            # Identify target column
            if target_column:
                if target_column not in df.columns:
                    st.error(f"Target column '{target_column}' not found in dataset.")
                    return None, None, []
                
                X = df.drop(columns=[target_column])
                y = df[target_column]
                self.target_column = target_column
            else:
                X = df.copy()
                y = None
            
            # Store original feature names
            self.feature_names = list(X.columns)
            
            # Handle categorical variables
            X_processed = X.copy()
            for column in X.columns:
                if X[column].dtype == 'object':
                    # Use label encoding for categorical variables
                    le = LabelEncoder()
                    X_processed[column] = le.fit_transform(X[column].astype(str))
                    self.label_encoders[column] = le
            
            # Handle missing values
            X_processed = X_processed.fillna(X_processed.mean())
            
            return X_processed, y, self.feature_names
            
        except Exception as e:
            st.error(f"Error preparing features: {str(e)}")
            return None, None, []
    
    def get_data_info(self, df):
        """
        Get information about the dataset
        
        Args:
            df: pandas DataFrame
            
        Returns:
            Dictionary with dataset information
        """
        info = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'categorical_columns': list(df.select_dtypes(include=['object']).columns),
            'numerical_columns': list(df.select_dtypes(include=[np.number]).columns)
        }
        
        return info
    
    def reverse_encode_features(self, X, feature_names=None):
        """
        Reverse label encoding for display purposes
        
        Args:
            X: Feature matrix
            feature_names: List of feature names
            
        Returns:
            DataFrame with original categorical values
        """
        if feature_names is None:
            feature_names = self.feature_names
        
        X_display = pd.DataFrame(X, columns=feature_names)
        
        for column, le in self.label_encoders.items():
            if column in X_display.columns:
                try:
                    X_display[column] = le.inverse_transform(X_display[column].astype(int))
                except:
                    pass  # Keep encoded values if inverse transform fails
        
        return X_display