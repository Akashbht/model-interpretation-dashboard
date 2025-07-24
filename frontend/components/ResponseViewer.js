import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Grid,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Card,
  CardContent,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button
} from '@mui/material';
import { ExpandMore } from '@mui/icons-material';

const ResponseViewer = ({ benchmarkResults }) => {
  const [selectedResponse, setSelectedResponse] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  if (!benchmarkResults || !benchmarkResults.results) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography color="text.secondary">
          No benchmark results to display. Run a benchmark to see responses.
        </Typography>
      </Paper>
    );
  }

  const handleResponseClick = (modelId, promptIndex, response) => {
    setSelectedResponse({
      modelId,
      promptIndex,
      response,
      prompt: benchmarkResults.prompts[promptIndex]
    });
    setDialogOpen(true);
  };

  const formatModelName = (modelId) => {
    const parts = modelId.split('_');
    if (parts.length > 1) {
      return parts.slice(1).join('_');
    }
    return modelId;
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'error';
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Benchmark Results
      </Typography>

      {/* Summary Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Models Tested
              </Typography>
              <Typography variant="h4">
                {Object.keys(benchmarkResults.results).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Prompts Used
              </Typography>
              <Typography variant="h4">
                {benchmarkResults.prompts.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Top Performer
              </Typography>
              <Typography variant="h6">
                {benchmarkResults.summary?.rankings?.overall?.[0] ? 
                  formatModelName(benchmarkResults.summary.rankings.overall[0].model_id) : 
                  'N/A'
                }
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Avg Overall Score
              </Typography>
              <Typography variant="h4">
                {benchmarkResults.summary?.rankings?.overall ? 
                  (benchmarkResults.summary.rankings.overall.reduce((sum, model) => sum + model.score, 0) / 
                   benchmarkResults.summary.rankings.overall.length).toFixed(1) : 
                  'N/A'
                }
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Detailed Results by Model */}
      {Object.entries(benchmarkResults.results).map(([modelId, modelResults]) => (
        <Accordion key={modelId} sx={{ mb: 1 }}>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
              <Typography variant="h6">
                {formatModelName(modelId)}
              </Typography>
              <Chip
                label={modelResults.model_info?.provider || 'Unknown'}
                size="small"
                color="primary"
              />
              {modelResults.aggregated_metrics?.overall_score && (
                <Chip
                  label={`Score: ${modelResults.aggregated_metrics.overall_score.toFixed(1)}`}
                  color={getScoreColor(modelResults.aggregated_metrics.overall_score)}
                  size="small"
                />
              )}
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            {/* Model Info */}
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Model Information
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="textSecondary">
                    Context Length
                  </Typography>
                  <Typography variant="body2">
                    {modelResults.model_info?.max_context_length?.toLocaleString() || 'N/A'} tokens
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="textSecondary">
                    Cost per 1K tokens
                  </Typography>
                  <Typography variant="body2">
                    ${modelResults.model_info?.cost_per_1k_tokens || 'N/A'}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="textSecondary">
                    Modalities
                  </Typography>
                  <Typography variant="body2">
                    {modelResults.model_info?.modalities?.join(', ') || 'N/A'}
                  </Typography>
                </Grid>
              </Grid>
            </Box>

            {/* Aggregated Metrics */}
            {modelResults.aggregated_metrics && (
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Performance Metrics
                </Typography>
                <TableContainer component={Paper} variant="outlined">
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Metric</TableCell>
                        <TableCell align="right">Average Score</TableCell>
                        <TableCell align="right">Best</TableCell>
                        <TableCell align="right">Worst</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {Object.entries(modelResults.aggregated_metrics).map(([metric, data]) => {
                        if (metric === 'overall_score') return null;
                        return (
                          <TableRow key={metric}>
                            <TableCell component="th" scope="row">
                              {metric.charAt(0).toUpperCase() + metric.slice(1).replace('_', ' ')}
                            </TableCell>
                            <TableCell align="right">
                              <Chip
                                label={data.average_score?.toFixed(1) || 'N/A'}
                                color={getScoreColor(data.average_score || 0)}
                                size="small"
                              />
                            </TableCell>
                            <TableCell align="right">{data.max_score?.toFixed(1) || 'N/A'}</TableCell>
                            <TableCell align="right">{data.min_score?.toFixed(1) || 'N/A'}</TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Box>
            )}

            {/* Individual Responses */}
            <Typography variant="subtitle2" gutterBottom>
              Responses by Prompt
            </Typography>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Prompt</TableCell>
                    <TableCell>Response Preview</TableCell>
                    <TableCell align="right">Success</TableCell>
                    <TableCell align="right">Action</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {modelResults.prompt_results?.map((result, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                          {result.prompt.length > 50 ? 
                            `${result.prompt.substring(0, 50)}...` : 
                            result.prompt
                          }
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" noWrap sx={{ maxWidth: 300 }}>
                          {result.response ? 
                            (result.response.length > 100 ? 
                              `${result.response.substring(0, 100)}...` : 
                              result.response
                            ) : 
                            result.error || 'No response'
                          }
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Chip
                          label={result.success ? 'Success' : 'Failed'}
                          color={result.success ? 'success' : 'error'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="right">
                        <Button
                          size="small"
                          onClick={() => handleResponseClick(modelId, index, result)}
                        >
                          View Full
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </AccordionDetails>
        </Accordion>
      ))}

      {/* Response Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Full Response - {selectedResponse ? formatModelName(selectedResponse.modelId) : ''}
        </DialogTitle>
        <DialogContent dividers>
          {selectedResponse && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Prompt:
              </Typography>
              <Paper sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}>
                <Typography variant="body2">
                  {selectedResponse.prompt}
                </Typography>
              </Paper>
              
              <Typography variant="subtitle2" gutterBottom>
                Response:
              </Typography>
              <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                  {selectedResponse.response.response || selectedResponse.response.error || 'No response'}
                </Typography>
              </Paper>

              {selectedResponse.response.metrics && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Metrics:
                  </Typography>
                  <Grid container spacing={2}>
                    {Object.entries(selectedResponse.response.metrics).map(([metric, data]) => (
                      <Grid item xs={6} md={4} key={metric}>
                        <Paper sx={{ p: 1 }}>
                          <Typography variant="caption" color="textSecondary">
                            {metric.charAt(0).toUpperCase() + metric.slice(1).replace('_', ' ')}
                          </Typography>
                          <Typography variant="body2">
                            Score: {data.score?.toFixed(1) || 'N/A'}
                          </Typography>
                          {data.raw_value && (
                            <Typography variant="caption" display="block">
                              Raw: {typeof data.raw_value === 'number' ? data.raw_value.toFixed(3) : data.raw_value}
                            </Typography>
                          )}
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ResponseViewer;