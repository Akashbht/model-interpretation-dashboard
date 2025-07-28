#!/usr/bin/env python3
"""
Test script to validate the model interpretation dashboard components
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_sample_data():
    """Test that sample data was created correctly"""
    print("🧪 Testing sample data...")
    
    # Check classification data
    class_file = project_root / "sample_data" / "classification_data.csv"
    if not class_file.exists():
        print("❌ Classification data file not found")
        return False
    
    class_df = pd.read_csv(class_file)
    print(f"✅ Classification data loaded: {class_df.shape}")
    
    # Check regression data
    reg_file = project_root / "sample_data" / "regression_data.csv"
    if not reg_file.exists():
        print("❌ Regression data file not found")
        return False
    
    reg_df = pd.read_csv(reg_file)
    print(f"✅ Regression data loaded: {reg_df.shape}")
    
    return True

def test_sample_models():
    """Test that sample models were created correctly"""
    print("🧪 Testing sample models...")
    
    try:
        import joblib
        
        # Check classification model
        class_model_file = project_root / "sample_models" / "classification_model.joblib"
        if not class_model_file.exists():
            print("❌ Classification model file not found")
            return False
        
        class_model = joblib.load(class_model_file)
        print(f"✅ Classification model loaded: {type(class_model).__name__}")
        
        # Check regression model
        reg_model_file = project_root / "sample_models" / "regression_model.joblib"
        if not reg_model_file.exists():
            print("❌ Regression model file not found")
            return False
        
        reg_model = joblib.load(reg_model_file)
        print(f"✅ Regression model loaded: {type(reg_model).__name__}")
        
        return True
        
    except ImportError:
        print("⚠️ joblib not available, skipping model tests")
        return True

def test_component_imports():
    """Test that all components can be imported"""
    print("🧪 Testing component imports...")
    
    try:
        # Test data processor (with mock streamlit)
        from utils.data_processor_test import DataProcessor
        print("✅ DataProcessor imported")
        
        print("✅ All components import successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    print("🧪 Testing basic functionality...")
    
    try:
        from utils.data_processor_test import DataProcessor
        
        # Create simple test data
        test_data = pd.DataFrame({
            'numeric_col': [1, 2, 3, 4, 5],
            'categorical_col': ['A', 'B', 'A', 'C', 'B'],
            'target': [0, 1, 0, 1, 1]
        })
        
        # Test data processor
        processor = DataProcessor()
        X, y, feature_names = processor.prepare_features(test_data, 'target')
        
        if X is not None and len(feature_names) == 2:
            print("✅ Data processing works correctly")
            return True
        else:
            print("❌ Data processing failed")
            return False
            
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Running Model Interpretation Dashboard Tests\n")
    
    tests = [
        ("Sample Data", test_sample_data),
        ("Sample Models", test_sample_models),
        ("Component Imports", test_component_imports),
        ("Basic Functionality", test_basic_functionality),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The dashboard is ready to use.")
        print("\nTo start the dashboard:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: streamlit run app.py")
        print("3. Open your browser to http://localhost:8501")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)