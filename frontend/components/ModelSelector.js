import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  ListItemText,
  OutlinedInput,
  Box,
  Chip,
  Typography,
  Alert
} from '@mui/material';
import axios from 'axios';

const ModelSelector = ({ selectedModels, onModelChange, apiBaseUrl }) => {
  const [availableModels, setAvailableModels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAvailableModels();
  }, []);

  const fetchAvailableModels = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${apiBaseUrl}/api/models`);
      setAvailableModels(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch available models');
      console.error('Error fetching models:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleModelChange = (event) => {
    const value = event.target.value;
    onModelChange(typeof value === 'string' ? value.split(',') : value);
  };

  const renderModelValue = (selected) => (
    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
      {selected.map((modelId) => {
        const model = availableModels.find(m => m.id === modelId);
        return (
          <Chip
            key={modelId}
            label={model ? `${model.provider} ${model.name}` : modelId}
            size="small"
            color={model?.connected ? 'success' : 'error'}
          />
        );
      })}
    </Box>
  );

  if (loading) {
    return <Typography>Loading models...</Typography>;
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box>
      <FormControl fullWidth margin="normal">
        <InputLabel>Select Models to Compare</InputLabel>
        <Select
          multiple
          value={selectedModels}
          onChange={handleModelChange}
          input={<OutlinedInput label="Select Models to Compare" />}
          renderValue={renderModelValue}
        >
          {availableModels.map((model) => (
            <MenuItem key={model.id} value={model.id}>
              <Checkbox checked={selectedModels.indexOf(model.id) > -1} />
              <ListItemText
                primary={`${model.provider} ${model.name}`}
                secondary={
                  <Box>
                    <Typography variant="caption" display="block">
                      Context: {model.max_context_length} tokens
                    </Typography>
                    <Typography variant="caption" display="block">
                      Cost: ${model.cost_per_1k_tokens}/1K tokens
                    </Typography>
                    <Typography variant="caption" display="block">
                      Status: {model.connected ? '✅ Connected' : '❌ Not Connected'}
                    </Typography>
                  </Box>
                }
              />
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      
      {availableModels.length === 0 && (
        <Alert severity="warning" sx={{ mt: 2 }}>
          No models available. Please configure your API keys in the environment variables.
        </Alert>
      )}
    </Box>
  );
};

export default ModelSelector;