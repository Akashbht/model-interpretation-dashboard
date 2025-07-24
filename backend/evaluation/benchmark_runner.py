import uuid
import time
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from .metrics import MetricsCalculator

class BenchmarkRunner:
    """Runs benchmarks across multiple models and calculates metrics"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.results_store = {}  # In-memory store for results
        self.metrics_calculator = MetricsCalculator()
    
    def run_benchmark(self, prompts: List[str], model_ids: List[str], 
                     metrics: List[str] = None) -> Dict[str, Any]:
        """Run benchmark across selected models"""
        
        if metrics is None:
            metrics = ['latency', 'cost', 'quality']
        
        benchmark_id = str(uuid.uuid4())
        
        # Initialize results structure
        benchmark_results = {
            'id': benchmark_id,
            'timestamp': time.time(),
            'prompts': prompts,
            'model_ids': model_ids,
            'metrics': metrics,
            'results': {},
            'summary': {}
        }
        
        # Run tests for each model
        for model_id in model_ids:
            connector = self.model_manager.get_model_connector(model_id)
            if not connector:
                continue
            
            model_results = self._run_model_benchmark(
                connector, prompts, metrics, model_id
            )
            benchmark_results['results'][model_id] = model_results
        
        # Calculate summary statistics
        benchmark_results['summary'] = self._calculate_summary(
            benchmark_results['results'], metrics
        )
        
        # Store results
        self.results_store[benchmark_id] = benchmark_results
        
        return benchmark_results
    
    def _run_model_benchmark(self, connector, prompts: List[str], 
                           metrics: List[str], model_id: str) -> Dict[str, Any]:
        """Run benchmark for a single model"""
        
        model_info = connector.get_model_info()
        prompt_results = []
        
        for i, prompt in enumerate(prompts):
            prompt_result = self._evaluate_single_prompt(
                connector, prompt, metrics, model_info
            )
            prompt_result['prompt_index'] = i
            prompt_results.append(prompt_result)
        
        # Aggregate results across all prompts
        aggregated_metrics = self._aggregate_prompt_results(prompt_results, metrics)
        
        return {
            'model_id': model_id,
            'model_info': model_info,
            'prompt_results': prompt_results,
            'aggregated_metrics': aggregated_metrics
        }
    
    def _evaluate_single_prompt(self, connector, prompt: str, 
                              metrics: List[str], model_info: Dict) -> Dict[str, Any]:
        """Evaluate a single prompt with a model"""
        
        # Generate response
        response_data = connector.generate_response(prompt)
        
        # Calculate metrics
        calculated_metrics = {}
        
        if 'latency' in metrics:
            latency_score = self.metrics_calculator.calculate_latency_score(
                response_data.get('latency', 0)
            )
            calculated_metrics['latency'] = {
                'raw_value': response_data.get('latency', 0),
                'score': latency_score
            }
        
        if 'cost' in metrics:
            tokens_used = response_data.get('tokens_used', 0)
            cost_per_1k = model_info.get('cost_per_1k_tokens', 0)
            cost = (tokens_used / 1000) * cost_per_1k
            
            cost_score = self.metrics_calculator.calculate_cost_score(cost)
            calculated_metrics['cost'] = {
                'raw_value': cost,
                'tokens_used': tokens_used,
                'score': cost_score
            }
        
        if 'quality' in metrics:
            quality_score = self.metrics_calculator.calculate_quality_score(
                response_data.get('response', '')
            )
            calculated_metrics['quality'] = {
                'score': quality_score
            }
        
        if 'context_utilization' in metrics:
            prompt_length = len(prompt.split())
            max_context = model_info.get('max_context_length', 4096)
            context_score = self.metrics_calculator.calculate_context_utilization_score(
                prompt_length, max_context
            )
            calculated_metrics['context_utilization'] = {
                'prompt_length': prompt_length,
                'max_context': max_context,
                'score': context_score
            }
        
        return {
            'prompt': prompt,
            'response': response_data.get('response', ''),
            'success': response_data.get('success', False),
            'error': response_data.get('error'),
            'metrics': calculated_metrics
        }
    
    def _aggregate_prompt_results(self, prompt_results: List[Dict], 
                                metrics: List[str]) -> Dict[str, Any]:
        """Aggregate metrics across all prompts for a model"""
        
        aggregated = {}
        
        for metric in metrics:
            scores = []
            raw_values = []
            
            for result in prompt_results:
                if result['success'] and metric in result['metrics']:
                    metric_data = result['metrics'][metric]
                    scores.append(metric_data['score'])
                    if 'raw_value' in metric_data:
                        raw_values.append(metric_data['raw_value'])
            
            if scores:
                aggregated[metric] = {
                    'average_score': sum(scores) / len(scores),
                    'min_score': min(scores),
                    'max_score': max(scores),
                    'count': len(scores)
                }
                
                if raw_values:
                    aggregated[metric]['average_raw'] = sum(raw_values) / len(raw_values)
                    aggregated[metric]['min_raw'] = min(raw_values)
                    aggregated[metric]['max_raw'] = max(raw_values)
        
        # Calculate overall score
        if aggregated:
            metric_scores = {metric: data['average_score'] 
                           for metric, data in aggregated.items()}
            overall_score = self.metrics_calculator.aggregate_scores(metric_scores)
            aggregated['overall_score'] = overall_score
        
        return aggregated
    
    def _calculate_summary(self, results: Dict[str, Any], 
                         metrics: List[str]) -> Dict[str, Any]:
        """Calculate summary statistics across all models"""
        
        summary = {
            'rankings': {},
            'best_performers': {},
            'metric_averages': {}
        }
        
        # Collect scores for ranking
        model_scores = {}
        for model_id, model_data in results.items():
            if 'aggregated_metrics' in model_data:
                model_scores[model_id] = model_data['aggregated_metrics']
        
        # Rank models by overall score
        if model_scores:
            ranked_models = sorted(
                model_scores.items(),
                key=lambda x: x[1].get('overall_score', 0),
                reverse=True
            )
            
            summary['rankings']['overall'] = [
                {
                    'model_id': model_id,
                    'score': scores.get('overall_score', 0)
                }
                for model_id, scores in ranked_models
            ]
            
            # Rank by individual metrics
            for metric in metrics:
                metric_rankings = sorted(
                    [(mid, scores.get(metric, {}).get('average_score', 0)) 
                     for mid, scores in model_scores.items()],
                    key=lambda x: x[1],
                    reverse=True
                )
                
                summary['rankings'][metric] = [
                    {'model_id': model_id, 'score': score}
                    for model_id, score in metric_rankings
                ]
                
                # Best performer for this metric
                if metric_rankings:
                    summary['best_performers'][metric] = metric_rankings[0][0]
        
        return summary
    
    def get_results(self, benchmark_id: str) -> Dict[str, Any]:
        """Get results for a specific benchmark"""
        return self.results_store.get(benchmark_id)