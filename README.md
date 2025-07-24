# Model Interpretation Dashboard

A comprehensive dashboard for benchmarking, comparing, and ranking advanced AI models (GPT-4, Claude, Sonnet, Opus, and more) across qualitative and quantitative metrics.

## Features

### 🤖 Model Support
- **Pre-integrated models**: OpenAI GPT series, Anthropic Claude series
- **Custom endpoints**: Add your own models via API key or custom endpoint
- **Real-time connectivity**: Check model availability and connection status

### 📊 Comprehensive Metrics
- **Latency**: Response speed measurement
- **Cost Efficiency**: Cost per 1K tokens calculation
- **Response Quality**: Automated quality scoring using multiple factors
- **Context Utilization**: How effectively models use their context window
- **Custom Metrics**: Extensible framework for user-defined metrics

### 🧪 Evaluation & Workflow
- **Interactive Prompt Input**: Upload or create test prompts
- **Side-by-side Comparison**: Run prompts across multiple models simultaneously
- **Detailed Analytics**: Aggregate scores and performance visualization
- **Historical Tracking**: Track model performance over time

### 📈 Dashboard Features
- **Interactive Leaderboard**: Real-time model rankings
- **Advanced Visualizations**: Bar charts, radar plots, and performance graphs
- **Drill-down Analysis**: Review individual model responses per prompt
- **Filter & Sort**: Comprehensive filtering by metrics and performance
- **Export Results**: Share and export benchmark results

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- API keys for OpenAI and/or Anthropic (optional but recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Akashbht/model-interpretation-dashboard.git
cd model-interpretation-dashboard
```

2. **Run setup script**
```bash
./setup.sh
```

3. **Configure API keys**
```bash
cp .env.example .env
# Edit .env file with your API keys
```

4. **Start the backend**
```bash
cd backend
source venv/bin/activate
python app.py
```

5. **Start the frontend** (in a new terminal)
```bash
cd frontend
npm start
```

6. **Access the dashboard**
   - Open http://localhost:3000 in your browser
   - Backend API runs on http://localhost:5000

## Architecture

### Backend Structure
```
backend/
├── app.py                 # Flask API server
├── requirements.txt       # Python dependencies
├── models/               # Model connectors
│   ├── base_connector.py # Base connector interface
│   ├── gpt_connector.py  # OpenAI GPT connector
│   ├── claude_connector.py # Anthropic Claude connector
│   └── model_manager.py  # Model management
└── evaluation/           # Evaluation system
    ├── metrics.py        # Metrics calculation
    ├── benchmark_runner.py # Benchmark execution
    └── leaderboard.py    # Rankings and leaderboard
```

### Frontend Structure
```
frontend/
├── src/
│   ├── App.js            # Main application
│   └── index.js          # Entry point
├── components/           # React components
│   ├── ModelSelector.js  # Model selection interface
│   ├── PromptInput.js    # Prompt input and management
│   ├── Leaderboard.js    # Rankings display
│   └── ResponseViewer.js # Results visualization
└── package.json          # Node.js dependencies
```

## API Documentation

### Core Endpoints

#### Get Available Models
```
GET /api/models
```
Returns list of configured models with connection status.

#### Add Custom Model
```
POST /api/models
Content-Type: application/json

{
  "name": "custom-model",
  "api_key": "your-api-key",
  "endpoint": "https://api.example.com" // optional
}
```

#### Run Benchmark
```
POST /api/benchmark
Content-Type: application/json

{
  "prompts": ["What is AI?", "Explain quantum computing"],
  "model_ids": ["openai_gpt-4", "anthropic_claude-3-sonnet"],
  "metrics": ["latency", "cost", "quality"]
}
```

#### Get Leaderboard
```
GET /api/leaderboard?metric=overall
```
Returns current model rankings for specified metric.

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Application Configuration
REACT_APP_API_URL=http://localhost:5000
FLASK_ENV=development
FLASK_DEBUG=true
```

### Adding New Models

1. **For API-compatible models**: Use the "Add Model" feature in the dashboard
2. **For custom connectors**: Create a new connector class extending `BaseModelConnector`

Example custom connector:
```python
from models.base_connector import BaseModelConnector

class CustomConnector(BaseModelConnector):
    def generate_response(self, prompt, **kwargs):
        # Implement your model's API call
        pass
    
    def get_model_info(self):
        # Return model information
        pass
```

## Metrics Explained

### Latency Score
- Measures response time from request to completion
- Score: 100 (≤1s) to 0 (≥10s)
- Lower latency = higher score

### Cost Score  
- Calculated based on tokens used and model pricing
- Normalized against maximum cost threshold
- Lower cost = higher score

### Quality Score
- Multi-factor assessment including:
  - Response completeness
  - Length appropriateness  
  - Coherence indicators
  - Error detection
- Base score modified by response characteristics

### Context Utilization
- Measures how effectively models use available context
- Optimal range: 20-80% of context window
- Penalizes both under and over-utilization

## Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests  
cd frontend
npm test
```

### Building for Production
```bash
# Build frontend
cd frontend
npm run build

# Production deployment
# Backend: Use gunicorn or similar WSGI server
# Frontend: Serve build/ directory with nginx or similar
```

## Extending the Dashboard

### Adding New Metrics
1. Implement metric calculation in `evaluation/metrics.py`
2. Update `BenchmarkRunner` to collect metric data
3. Add metric selection in frontend

### Adding Visualizations
1. Create new React component in `frontend/components/`
2. Integrate with Chart.js or Recharts
3. Add to main dashboard interface

### Custom Model Integrations
1. Create connector extending `BaseModelConnector`
2. Register in `ModelManager`
3. Update frontend model selection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review API endpoints and examples

## Roadmap

- [ ] Additional model providers (Cohere, AI21, etc.)
- [ ] Advanced visualization options
- [ ] Batch processing for large prompt sets
- [ ] Model fine-tuning integration
- [ ] Custom evaluation datasets
- [ ] Team collaboration features
- [ ] Export to popular ML platforms