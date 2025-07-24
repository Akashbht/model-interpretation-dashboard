import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box,
  Typography,
  TableSortLabel,
  Chip,
  LinearProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import axios from 'axios';

const Leaderboard = ({ apiBaseUrl, refreshTrigger }) => {
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortMetric, setSortMetric] = useState('overall');
  const [orderBy, setOrderBy] = useState('score');
  const [order, setOrder] = useState('desc');

  useEffect(() => {
    fetchLeaderboard();
  }, [sortMetric, refreshTrigger]);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${apiBaseUrl}/api/leaderboard?metric=${sortMetric}`);
      setRankings(response.data.rankings || []);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const sortedRankings = React.useMemo(() => {
    return [...rankings].sort((a, b) => {
      let aVal = a[orderBy];
      let bVal = b[orderBy];
      
      if (orderBy === 'model_id') {
        aVal = a.model_id.split('_')[1] || a.model_id;
        bVal = b.model_id.split('_')[1] || b.model_id;
      }
      
      if (order === 'desc') {
        return bVal > aVal ? 1 : -1;
      } else {
        return aVal > bVal ? 1 : -1;
      }
    });
  }, [rankings, order, orderBy]);

  const getProviderColor = (modelId) => {
    if (modelId.includes('openai')) return 'primary';
    if (modelId.includes('anthropic')) return 'secondary';
    return 'default';
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'error';
  };

  const formatModelName = (modelId) => {
    const parts = modelId.split('_');
    if (parts.length > 1) {
      const provider = parts[0];
      const model = parts.slice(1).join('_');
      return { provider, model };
    }
    return { provider: 'Custom', model: modelId };
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">Model Leaderboard</Typography>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Metric</InputLabel>
          <Select
            value={sortMetric}
            label="Metric"
            onChange={(e) => setSortMetric(e.target.value)}
          >
            <MenuItem value="overall">Overall</MenuItem>
            <MenuItem value="latency">Latency</MenuItem>
            <MenuItem value="cost">Cost</MenuItem>
            <MenuItem value="quality">Quality</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {loading && <LinearProgress sx={{ mb: 2 }} />}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>
                <TableSortLabel
                  active={orderBy === 'model_id'}
                  direction={orderBy === 'model_id' ? order : 'asc'}
                  onClick={() => handleSort('model_id')}
                >
                  Rank
                </TableSortLabel>
              </TableCell>
              <TableCell>Model</TableCell>
              <TableCell>Provider</TableCell>
              <TableCell align="right">
                <TableSortLabel
                  active={orderBy === 'score'}
                  direction={orderBy === 'score' ? order : 'asc'}
                  onClick={() => handleSort('score')}
                >
                  Score
                </TableSortLabel>
              </TableCell>
              {sortMetric === 'latency' && (
                <TableCell align="right">Avg Latency (s)</TableCell>
              )}
              {sortMetric === 'cost' && (
                <TableCell align="right">Avg Cost ($)</TableCell>
              )}
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedRankings.map((model, index) => {
              const { provider, model: modelName } = formatModelName(model.model_id);
              return (
                <TableRow key={model.model_id} hover>
                  <TableCell>
                    <Typography variant="h6" color="primary">
                      #{index + 1}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body1" fontWeight="medium">
                      {modelName}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={provider}
                      color={getProviderColor(model.model_id)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
                      <Chip
                        label={model.score.toFixed(1)}
                        color={getScoreColor(model.score)}
                        variant="filled"
                      />
                    </Box>
                  </TableCell>
                  {sortMetric === 'latency' && model.avg_latency && (
                    <TableCell align="right">
                      {model.avg_latency.toFixed(2)}s
                    </TableCell>
                  )}
                  {sortMetric === 'cost' && model.avg_cost && (
                    <TableCell align="right">
                      ${model.avg_cost.toFixed(4)}
                    </TableCell>
                  )}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      {rankings.length === 0 && !loading && (
        <Paper sx={{ p: 3, textAlign: 'center', mt: 2 }}>
          <Typography color="text.secondary">
            No benchmark results available. Run a benchmark to see the leaderboard.
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default Leaderboard;