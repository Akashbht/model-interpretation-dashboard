import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Create sample classification dataset
def create_classification_dataset():
    """Create a sample classification dataset"""
    # Generate synthetic data
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=8,
        n_redundant=2,
        n_classes=3,
        random_state=42
    )
    
    # Create feature names
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    
    # Create DataFrame
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    # Add some categorical features
    df['category_A'] = np.random.choice(['Type1', 'Type2', 'Type3'], size=len(df))
    df['category_B'] = np.random.choice(['Small', 'Medium', 'Large'], size=len(df))
    
    return df

# Create sample regression dataset
def create_regression_dataset():
    """Create a sample regression dataset"""
    # Generate synthetic data
    X, y = make_regression(
        n_samples=1000,
        n_features=8,
        n_informative=6,
        noise=0.1,
        random_state=42
    )
    
    # Create feature names
    feature_names = [f'numeric_feature_{i}' for i in range(X.shape[1])]
    
    # Create DataFrame
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    # Add some categorical features
    df['region'] = np.random.choice(['North', 'South', 'East', 'West'], size=len(df))
    df['size_category'] = np.random.choice(['XS', 'S', 'M', 'L', 'XL'], size=len(df))
    
    return df

# Train and save models
def train_and_save_models():
    """Train sample models and save them"""
    
    # Classification model
    print("Creating classification dataset and model...")
    class_df = create_classification_dataset()
    
    # Prepare features for model training
    X_class = class_df.drop(['target'], axis=1)
    y_class = class_df['target']
    
    # Encode categorical variables
    le_dict = {}
    for col in ['category_A', 'category_B']:
        le = LabelEncoder()
        X_class[col] = le.fit_transform(X_class[col])
        le_dict[col] = le
    
    # Train classification model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_class, y_class)
    
    # Save classification model and data
    joblib.dump(clf, 'sample_models/classification_model.joblib')
    class_df.to_csv('sample_data/classification_data.csv', index=False)
    
    # Regression model
    print("Creating regression dataset and model...")
    reg_df = create_regression_dataset()
    
    # Prepare features for model training
    X_reg = reg_df.drop(['target'], axis=1)
    y_reg = reg_df['target']
    
    # Encode categorical variables
    for col in ['region', 'size_category']:
        le = LabelEncoder()
        X_reg[col] = le.fit_transform(X_reg[col])
    
    # Train regression model
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_reg, y_reg)
    
    # Save regression model and data
    joblib.dump(reg, 'sample_models/regression_model.joblib')
    reg_df.to_csv('sample_data/regression_data.csv', index=False)
    
    print("Sample models and datasets created successfully!")
    print("Files created:")
    print("- sample_models/classification_model.joblib")
    print("- sample_models/regression_model.joblib") 
    print("- sample_data/classification_data.csv")
    print("- sample_data/regression_data.csv")

if __name__ == "__main__":
    train_and_save_models()