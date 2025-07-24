import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Button,
  Grid,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormGroup,
  FormControlLabel,
  Checkbox
} from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import axios from 'axios';

import ModelSelector from './components/ModelSelector';
import PromptInput from './components/PromptInput';
import Leaderboard from './components/Leaderboard';
import ResponseViewer from './components/ResponseViewer';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [selectedModels, setSelectedModels] = useState([]);
  const [prompts, setPrompts] = useState([]);
  const [selectedMetrics, setSelectedMetrics] = useState(['latency', 'cost', 'quality']);
  const [benchmarkResults, setBenchmarkResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [leaderboardRefresh, setLeaderboardRefresh] = useState(0);

  const steps = [
    {
      label: 'Select Models',
      description: 'Choose the AI models you want to compare',
    },
    {
      label: 'Configure Test Prompts',
      description: 'Add prompts to test the models with',
    },
    {
      label: 'Choose Metrics',
      description: 'Select which metrics to evaluate',
    },
    {
      label: 'Run Benchmark',
      description: 'Execute the benchmark and view results',
    },
  ];

  const availableMetrics = [
    { id: 'latency', label: 'Latency (Response Speed)', description: 'How quickly the model responds' },
    { id: 'cost', label: 'Cost Efficiency', description: 'Cost per 1K tokens' },
    { id: 'quality', label: 'Response Quality', description: 'Overall quality of responses' },
    { id: 'context_utilization', label: 'Context Utilization', description: 'How well the model uses its context window' }
  ];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    setBenchmarkResults(null);
    setError(null);
  };

  const canProceedFromStep = (step) => {
    switch (step) {
      case 0: return selectedModels.length > 0;
      case 1: return prompts.length > 0;
      case 2: return selectedMetrics.length > 0;
      default: return true;
    }
  };

  const runBenchmark = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/benchmark`, {
        prompts,
        model_ids: selectedModels,
        metrics: selectedMetrics
      });
      
      setBenchmarkResults(response.data);
      setLeaderboardRefresh(prev => prev + 1);
      handleNext();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to run benchmark');
    } finally {
      setLoading(false);
    }
  };

  const handleMetricChange = (metricId) => {
    setSelectedMetrics(prev => 
      prev.includes(metricId)
        ? prev.filter(m => m !== metricId)
        : [...prev, metricId]
    );
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <ModelSelector
            selectedModels={selectedModels}
            onModelChange={setSelectedModels}
            apiBaseUrl={API_BASE_URL}
          />
        );
      case 1:
        return (
          <PromptInput
            prompts={prompts}
            onPromptsChange={setPrompts}
          />
        );
      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Select Evaluation Metrics
            </Typography>
            <FormGroup>
              {availableMetrics.map((metric) => (
                <FormControlLabel
                  key={metric.id}
                  control={
                    <Checkbox
                      checked={selectedMetrics.includes(metric.id)}
                      onChange={() => handleMetricChange(metric.id)}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant="body1">{metric.label}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {metric.description}
                      </Typography>
                    </Box>
                  }
                />
              ))}
            </FormGroup>
          </Box>
        );
      case 3:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Review and Run Benchmark
            </Typography>
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Selected Models ({selectedModels.length})
                  </Typography>
                  {selectedModels.map(modelId => (
                    <Typography key={modelId} variant="body2">
                      • {modelId.split('_').slice(1).join('_')}
                    </Typography>
                  ))}
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Test Prompts ({prompts.length})
                  </Typography>
                  {prompts.slice(0, 3).map((prompt, index) => (
                    <Typography key={index} variant="body2" noWrap>
                      • {prompt.length > 50 ? `${prompt.substring(0, 50)}...` : prompt}
                    </Typography>
                  ))}
                  {prompts.length > 3 && (
                    <Typography variant="body2" color="text.secondary">
                      ... and {prompts.length - 3} more
                    </Typography>
                  )}
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Metrics ({selectedMetrics.length})
                  </Typography>
                  {selectedMetrics.map(metric => (
                    <Typography key={metric} variant="body2">
                      • {availableMetrics.find(m => m.id === metric)?.label || metric}
                    </Typography>
                  ))}
                </Paper>
              </Grid>
            </Grid>

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button
                variant="contained"
                onClick={runBenchmark}
                disabled={loading}
                size="large"
              >
                {loading ? <CircularProgress size={24} /> : 'Run Benchmark'}
              </Button>
            </Box>
          </Box>
        );
      default:
        return 'Unknown step';
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Model Interpretation Dashboard
        </Typography>
        <Typography variant="h6" component="h2" gutterBottom align="center" color="text.secondary">
          Benchmark and Compare Advanced AI Models
        </Typography>

        <Grid container spacing={4} sx={{ mt: 2 }}>
          {/* Main Workflow */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 3 }}>
              <Stepper activeStep={activeStep} orientation="vertical">
                {steps.map((step, index) => (
                  <Step key={step.label}>
                    <StepLabel>
                      <Typography variant="h6">{step.label}</Typography>
                    </StepLabel>
                    <StepContent>
                      <Typography sx={{ mb: 2 }}>{step.description}</Typography>
                      <Box sx={{ mb: 2 }}>
                        {getStepContent(index)}
                      </Box>
                      <Box sx={{ mb: 1 }}>
                        <div>
                          <Button
                            variant="contained"
                            onClick={index === steps.length - 1 ? runBenchmark : handleNext}
                            sx={{ mt: 1, mr: 1 }}
                            disabled={!canProceedFromStep(index) || loading}
                          >
                            {index === steps.length - 1 ? 'Run Benchmark' : 'Continue'}
                          </Button>
                          <Button
                            disabled={index === 0 || loading}
                            onClick={handleBack}
                            sx={{ mt: 1, mr: 1 }}
                          >
                            Back
                          </Button>
                        </div>
                      </Box>
                    </StepContent>
                  </Step>
                ))}
              </Stepper>

              {activeStep === steps.length && (
                <Paper square elevation={0} sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Benchmark Complete!
                  </Typography>
                  <Typography sx={{ mb: 2 }}>
                    Your benchmark has been completed. View the results below.
                  </Typography>
                  <Button onClick={handleReset} sx={{ mt: 1, mr: 1 }}>
                    Run Another Benchmark
                  </Button>
                </Paper>
              )}
            </Paper>

            {/* Results Viewer */}
            {benchmarkResults && (
              <Box sx={{ mt: 3 }}>
                <ResponseViewer benchmarkResults={benchmarkResults} />
              </Box>
            )}
          </Grid>

          {/* Sidebar */}
          <Grid item xs={12} md={4}>
            <Leaderboard 
              apiBaseUrl={API_BASE_URL}
              refreshTrigger={leaderboardRefresh}
            />
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}

export default App;