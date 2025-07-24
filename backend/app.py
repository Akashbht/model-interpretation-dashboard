from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from models.model_manager import ModelManager
from evaluation.benchmark_runner import BenchmarkRunner
from evaluation.leaderboard import Leaderboard

app = Flask(__name__)
CORS(app)

# Initialize components
model_manager = ModelManager()
benchmark_runner = BenchmarkRunner(model_manager)
leaderboard = Leaderboard()

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list of available models"""
    return jsonify(model_manager.get_available_models())

@app.route('/api/models', methods=['POST'])
def add_model():
    """Add a new model configuration"""
    data = request.json
    result = model_manager.add_model(data)
    return jsonify(result)

@app.route('/api/benchmark', methods=['POST'])
def run_benchmark():
    """Run benchmark across selected models"""
    data = request.json
    prompts = data.get('prompts', [])
    model_ids = data.get('model_ids', [])
    metrics = data.get('metrics', ['latency', 'cost', 'quality'])
    
    results = benchmark_runner.run_benchmark(prompts, model_ids, metrics)
    return jsonify(results)

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get current model leaderboard"""
    return jsonify(leaderboard.get_rankings())

@app.route('/api/results/<benchmark_id>', methods=['GET'])
def get_benchmark_results(benchmark_id):
    """Get detailed results for a specific benchmark"""
    results = benchmark_runner.get_results(benchmark_id)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)