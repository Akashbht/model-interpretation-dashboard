import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip
} from '@mui/material';
import { Add, Delete } from '@mui/icons-material';

const PromptInput = ({ prompts, onPromptsChange }) => {
  const [newPrompt, setNewPrompt] = useState('');

  const addPrompt = () => {
    if (newPrompt.trim()) {
      onPromptsChange([...prompts, newPrompt.trim()]);
      setNewPrompt('');
    }
  };

  const removePrompt = (index) => {
    const updatedPrompts = prompts.filter((_, i) => i !== index);
    onPromptsChange(updatedPrompts);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      addPrompt();
    }
  };

  // Predefined test prompts for quick selection
  const predefinedPrompts = [
    "Explain quantum computing in simple terms.",
    "Write a short story about a robot learning to paint.",
    "Analyze the pros and cons of renewable energy.",
    "Describe the process of photosynthesis.",
    "What are the main causes of climate change?",
    "Explain the concept of machine learning to a 10-year-old.",
    "Write a professional email declining a job offer.",
    "Compare and contrast Python and JavaScript programming languages."
  ];

  const addPredefinedPrompt = (prompt) => {
    if (!prompts.includes(prompt)) {
      onPromptsChange([...prompts, prompt]);
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Test Prompts
      </Typography>
      
      {/* Add new prompt */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <TextField
          fullWidth
          multiline
          minRows={3}
          value={newPrompt}
          onChange={(e) => setNewPrompt(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter a test prompt..."
          label="New Prompt"
          variant="outlined"
        />
        <Box sx={{ mt: 1, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="contained"
            onClick={addPrompt}
            startIcon={<Add />}
            disabled={!newPrompt.trim()}
          >
            Add Prompt
          </Button>
        </Box>
      </Paper>

      {/* Predefined prompts */}
      <Box sx={{ mb: 2 }}>
        <Typography variant="subtitle2" gutterBottom>
          Quick Add - Predefined Prompts:
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {predefinedPrompts.map((prompt, index) => (
            <Chip
              key={index}
              label={prompt.length > 50 ? `${prompt.substring(0, 50)}...` : prompt}
              onClick={() => addPredefinedPrompt(prompt)}
              variant="outlined"
              clickable
              size="small"
            />
          ))}
        </Box>
      </Box>

      {/* Current prompts list */}
      {prompts.length > 0 && (
        <Paper sx={{ mt: 2 }}>
          <Typography variant="subtitle1" sx={{ p: 2, pb: 0 }}>
            Selected Prompts ({prompts.length})
          </Typography>
          <List>
            {prompts.map((prompt, index) => (
              <ListItem key={index} divider>
                <ListItemText
                  primary={prompt}
                  secondary={`${prompt.length} characters`}
                />
                <ListItemSecondaryAction>
                  <IconButton
                    edge="end"
                    onClick={() => removePrompt(index)}
                    color="error"
                  >
                    <Delete />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      {prompts.length === 0 && (
        <Paper sx={{ p: 3, textAlign: 'center', mt: 2 }}>
          <Typography color="text.secondary">
            No prompts added yet. Add some prompts to start benchmarking.
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default PromptInput;