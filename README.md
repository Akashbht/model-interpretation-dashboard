# 🔍 Model Interpretation Dashboard

An interactive dashboard to visualize and interpret black-box ML model predictions using SHAP and LIME explanations.

## 🚀 Features

- **📁 Model & Data Upload**: Support for scikit-learn and XGBoost models (`.pkl`, `.joblib`) and CSV datasets
- **📊 Predictions View**: Comprehensive prediction analysis with distribution plots and data tables
- **🔍 Global Explanations**: SHAP-based global feature importance analysis
- **🎯 Local Explanations**: SHAP and LIME local explanations for individual predictions
- **🔄 What-If Analysis**: Interactive feature modification with real-time prediction updates
- **📥 Export Capabilities**: Download predictions, explanations, and analysis results

## 🛠️ Tech Stack

- **Backend/Frontend**: Streamlit (unified approach)
- **ML Interpretability**: SHAP, LIME
- **Data Processing**: pandas, numpy, scikit-learn
- **Visualization**: Plotly, matplotlib, seaborn
- **Model Support**: scikit-learn, XGBoost

## 🏃‍♂️ Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Akashbht/model-interpretation-dashboard.git
   cd model-interpretation-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:8501`

### Quick Demo with Sample Data

The repository includes sample models and datasets for immediate testing:

1. **Run the sample data generator** (optional, already included):
   ```bash
   python create_sample_data.py
   ```

2. **Try the demo**:
   - Start the app: `streamlit run app.py`
   - Upload `sample_models/classification_model.joblib` as your model
   - Upload `sample_data/classification_data.csv` as your dataset
   - Select `target` as the target column
   - Explore the different tabs!

## 📖 Usage Guide

### 1. Upload Model and Data

- **Sidebar → Configuration**: Upload your trained model and dataset
- **Supported Models**: scikit-learn, XGBoost (pickled/joblib format)
- **Supported Data**: CSV files with numerical and categorical features
- **Target Column**: Optionally specify a target column to exclude from features

### 2. View Predictions

- **Predictions Tab**: Analyze model predictions on your dataset
- View prediction statistics and distribution plots
- Select individual instances for detailed analysis
- Export predictions as CSV

### 3. Global Explanations

- **Global Explanations Tab**: Understand overall feature importance
- SHAP-based global feature importance rankings
- Interactive visualizations showing which features matter most
- Export importance rankings

### 4. Local Explanations

- **Local Explanations Tab**: Analyze individual prediction explanations
- Choose between SHAP and LIME explanations
- View feature contributions for specific predictions
- Compare different explanation methods side-by-side

### 5. What-If Analysis

- **What-If Analysis Tab**: Interactive feature manipulation
- Load any instance and modify feature values
- See real-time prediction changes
- Multiple modification approaches:
  - Manual value editing
  - Slider controls
  - Batch modifications (scaling, noise)
- Save and restore analysis states
- Export modification history

## 📁 Project Structure

```
model-interpretation-dashboard/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore patterns
├── create_sample_data.py          # Sample data generator
│
├── utils/                         # Utility modules
│   ├── model_loader.py           # Model loading and validation
│   ├── data_processor.py         # Data processing and preparation
│   └── explainer.py              # SHAP and LIME explanation management
│
├── components/                    # UI components
│   ├── upload_section.py         # File upload interface
│   ├── prediction_panel.py       # Predictions display
│   ├── explanation_panel.py      # Explanation visualizations
│   └── whatif_analysis.py        # What-if analysis interface
│
├── sample_models/                 # Sample trained models
│   ├── classification_model.joblib
│   └── regression_model.joblib
│
└── sample_data/                   # Sample datasets
    ├── classification_data.csv
    └── regression_data.csv
```

## 🔧 Supported Model Types

### Classification Models
- Scikit-learn classifiers (RandomForest, SVM, LogisticRegression, etc.)
- XGBoost classifiers
- Any model with `predict()` and optionally `predict_proba()` methods

### Regression Models
- Scikit-learn regressors (RandomForest, LinearRegression, etc.)
- XGBoost regressors
- Any model with `predict()` method

### Model Requirements
- Models must be saved in pickle (`.pkl`) or joblib (`.joblib`) format
- Models must implement sklearn-compatible interface
- Feature names should be consistent between training and inference data

## 📊 Supported Data Formats

### Input Data
- **Format**: CSV files
- **Features**: Numerical and categorical columns
- **Missing Values**: Automatically handled (filled with mean/mode)
- **Categorical Encoding**: Automatic label encoding for string columns

### Data Processing
- Automatic categorical variable detection and encoding
- Missing value imputation
- Feature name preservation for interpretability
- Target column handling (optional exclusion from features)

## 🎯 Explanation Methods

### SHAP (SHapley Additive exPlanations)
- **Global Importance**: Mean absolute SHAP values across all instances
- **Local Explanations**: Feature attribution for individual predictions
- **Tree Explainer**: Optimized for tree-based models (RandomForest, XGBoost)
- **Kernel Explainer**: Universal fallback for any model type

### LIME (Local Interpretable Model-Agnostic Explanations)
- **Local Explanations**: Feature importance for individual predictions
- **Model-Agnostic**: Works with any model type
- **Tabular Explainer**: Specialized for structured/tabular data
- **Discretization**: Handles continuous features intelligently

## 🚨 Troubleshooting

### Common Issues

**1. Model Loading Errors**
- Ensure model is saved in `.pkl` or `.joblib` format
- Verify model has `predict()` method
- Check that model was trained with compatible scikit-learn version

**2. Data Processing Errors**
- Ensure CSV file is properly formatted
- Check for column name consistency
- Verify data types are compatible

**3. Explanation Errors**
- Large datasets may take time for SHAP initialization
- Try reducing dataset size for faster processing
- LIME may require more time for complex models

**4. Memory Issues**
- For large datasets, consider sampling
- Close other applications to free memory
- Use smaller background datasets for SHAP

### Performance Tips

- **Large Models**: Use TreeExplainer for tree-based models (faster)
- **Large Datasets**: Sample data for background/training sets
- **Complex Models**: Prefer SHAP over LIME for consistency
- **Real-time Analysis**: Use smaller feature sets for what-if analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Enhancements

- [ ] Support for additional model formats (ONNX, TensorFlow)
- [ ] Advanced visualization options (dependency plots, interaction effects)
- [ ] Batch what-if analysis capabilities
- [ ] Integration with MLflow for model tracking
- [ ] Custom explanation method integration
- [ ] Performance optimization for large datasets
- [ ] API endpoints for programmatic access