# Troubleshooting Guide

## Common Installation Issues

### 1. Python Version Compatibility
**Problem**: Package installation fails with Python version errors.
**Solution**: Ensure you're using Python 3.8 or higher:
```bash
python3 --version
```

### 2. Permission Errors During Installation
**Problem**: `Permission denied` errors when installing packages.
**Solution**: Use user installation:
```bash
pip3 install --user -r requirements.txt
```

### 3. Memory Issues with Large Models
**Problem**: Application crashes when loading large models or datasets.
**Solutions**:
- Use smaller sample sizes for SHAP background data
- Close other applications to free memory
- Consider using a machine with more RAM

### 4. SHAP Installation Issues
**Problem**: SHAP fails to install due to compilation errors.
**Solutions**:
- Install build tools: `sudo apt-get install build-essential` (Linux)
- Update pip: `pip3 install --upgrade pip`
- Try conda installation: `conda install -c conda-forge shap`

### 5. Streamlit Port Issues
**Problem**: "Port 8501 is already in use" error.
**Solutions**:
```bash
# Kill existing streamlit processes
pkill -f streamlit

# Or use a different port
streamlit run app.py --server.port 8502
```

## Runtime Issues

### 1. Model Loading Errors
**Symptoms**: "Invalid model" or "Model has no predict method" errors.
**Solutions**:
- Ensure model is saved with joblib or pickle
- Verify model was trained with compatible scikit-learn version
- Check that model object has `predict()` method

### 2. Data Processing Errors
**Symptoms**: CSV loading fails or data preprocessing errors.
**Solutions**:
- Check CSV file encoding (should be UTF-8)
- Ensure no completely empty columns
- Verify data types are compatible

### 3. Explanation Generation Timeouts
**Symptoms**: SHAP or LIME takes too long or crashes.
**Solutions**:
- Reduce dataset size for explanations
- Use TreeExplainer for tree-based models (faster)
- Increase background data sample size gradually

### 4. Visualization Errors
**Symptoms**: Plotly charts don't display or show errors.
**Solutions**:
- Update browser to latest version
- Clear browser cache
- Try a different browser

## Performance Optimization

### 1. Large Datasets
- Sample data for background/training: Use 100-500 samples
- Process data in chunks for very large files
- Consider data preprocessing before upload

### 2. Complex Models
- Use TreeExplainer for RandomForest, XGBoost models
- Reduce number of features for explanations
- Cache explainer objects when possible

### 3. Memory Management
- Clear session state periodically using Reset button
- Avoid keeping multiple large datasets in memory
- Close browser tabs when not needed

## Getting Help

If you encounter issues not covered here:

1. **Check the error messages** - they often contain helpful information
2. **Verify your Python environment** - ensure all dependencies are installed
3. **Test with sample data** - use the provided sample models and datasets
4. **Check browser console** - for frontend-related issues
5. **Try in incognito mode** - to rule out browser cache issues

## Reporting Issues

When reporting issues, please include:
- Python version (`python3 --version`)
- Operating system
- Full error message or stack trace
- Steps to reproduce the problem
- Sample data/model if possible (ensure no sensitive information)