#!/usr/bin/env python3
"""
Comprehensive test suite for the Model Interpretation Dashboard
"""

import unittest
import sys
import os
import tempfile
import json

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from models.model_manager import ModelManager
from models.base_connector import BaseModelConnector
from evaluation.metrics import MetricsCalculator
from evaluation.benchmark_runner import BenchmarkRunner
from evaluation.leaderboard import Leaderboard

class MockConnector(BaseModelConnector):
    """Mock connector for testing"""
    
    def __init__(self, api_key=None, model_name="mock-model"):
        super().__init__(model_name)
        self.api_key = api_key
        self.call_count = 0
    
    def generate_response(self, prompt, **kwargs):
        self.call_count += 1
        return {
            'response': f"Mock response to: {prompt[:50]}...",
            'latency': 1.5,
            'tokens_used': 150,
            'model': self.model_name,
            'success': True
        }
    
    def get_model_info(self):
        return {
            'name': self.model_name,
            'provider': 'Mock',
            'max_context_length': 4096,
            'cost_per_1k_tokens': 0.01,
            'modalities': ['text']
        }

class TestMetricsCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calc = MetricsCalculator()
    
    def test_latency_score(self):
        # Test perfect score for fast response
        self.assertEqual(self.calc.calculate_latency_score(0.5), 100.0)
        
        # Test zero score for slow response
        self.assertEqual(self.calc.calculate_latency_score(15.0), 0.0)
        
        # Test mid-range score
        score = self.calc.calculate_latency_score(5.0)
        self.assertGreater(score, 0)
        self.assertLess(score, 100)
    
    def test_cost_score(self):
        # Test perfect score for free response
        self.assertEqual(self.calc.calculate_cost_score(0), 100.0)
        
        # Test decreasing scores for higher costs
        score_low = self.calc.calculate_cost_score(0.01)
        score_high = self.calc.calculate_cost_score(0.05)
        self.assertGreater(score_low, score_high)
    
    def test_quality_score(self):
        # Test empty response
        self.assertEqual(self.calc.calculate_quality_score(""), 0.0)
        
        # Test good response
        good_response = "This is a comprehensive answer to your question. It provides detailed information and ends properly."
        score = self.calc.calculate_quality_score(good_response)
        self.assertGreater(score, 50)
        
        # Test incomplete response
        bad_response = "I apologize but I cannot"
        score_bad = self.calc.calculate_quality_score(bad_response)
        score_good = self.calc.calculate_quality_score(good_response)
        self.assertGreater(score_good, score_bad)
    
    def test_aggregate_scores(self):
        scores = {
            'latency': 80.0,
            'cost': 70.0,
            'quality': 90.0
        }
        
        # Test default weights
        agg_score = self.calc.aggregate_scores(scores)
        self.assertGreater(agg_score, 0)
        self.assertLessEqual(agg_score, 100)
        
        # Test custom weights
        weights = {'latency': 0.5, 'cost': 0.3, 'quality': 0.2}
        agg_score_custom = self.calc.aggregate_scores(scores, weights)
        self.assertGreater(agg_score_custom, 0)
        self.assertLessEqual(agg_score_custom, 100)

class TestModelManager(unittest.TestCase):
    
    def setUp(self):
        # Create temporary config file
        self.temp_dir = tempfile.mkdtemp()
        os.environ['HOME'] = self.temp_dir
        self.manager = ModelManager()
    
    def test_initialization(self):
        self.assertIsInstance(self.manager, ModelManager)
        self.assertIsInstance(self.manager.models, dict)
    
    def test_get_available_models(self):
        models = self.manager.get_available_models()
        self.assertIsInstance(models, list)
    
    def test_add_custom_model(self):
        config = {
            'name': 'test-model',
            'api_key': 'test-key',
            'endpoint': 'https://test.com'
        }
        result = self.manager.add_model(config)
        self.assertTrue(result.get('success', False))
        self.assertIn('model_id', result)

class TestBenchmarkRunner(unittest.TestCase):
    
    def setUp(self):
        self.manager = ModelManager()
        # Add mock connector for testing
        self.manager.models['mock_test'] = {
            'connector_class': MockConnector,
            'api_key': 'test',
            'model_name': 'test-model',
            'enabled': True
        }
        self.runner = BenchmarkRunner(self.manager)
    
    def test_initialization(self):
        self.assertIsInstance(self.runner, BenchmarkRunner)
        self.assertIsInstance(self.runner.results_store, dict)
    
    def test_run_benchmark(self):
        prompts = ["Test prompt 1", "Test prompt 2"]
        model_ids = ["mock_test"]
        metrics = ["latency", "cost", "quality"]
        
        results = self.runner.run_benchmark(prompts, model_ids, metrics)
        
        self.assertIn('id', results)
        self.assertIn('results', results)
        self.assertIn('summary', results)
        self.assertEqual(len(results['prompts']), 2)
        self.assertIn('mock_test', results['results'])

class TestLeaderboard(unittest.TestCase):
    
    def setUp(self):
        self.leaderboard = Leaderboard()
    
    def test_initialization(self):
        self.assertIsInstance(self.leaderboard, Leaderboard)
    
    def test_get_rankings(self):
        rankings = self.leaderboard.get_rankings()
        self.assertIn('rankings', rankings)
        self.assertIn('last_updated', rankings)
        self.assertIsInstance(rankings['rankings'], list)
    
    def test_different_metrics(self):
        overall = self.leaderboard.get_rankings('overall')
        latency = self.leaderboard.get_rankings('latency')
        cost = self.leaderboard.get_rankings('cost')
        quality = self.leaderboard.get_rankings('quality')
        
        # Should all return valid rankings
        for ranking in [overall, latency, cost, quality]:
            self.assertIn('rankings', ranking)
            self.assertIsInstance(ranking['rankings'], list)

class TestIntegration(unittest.TestCase):
    """Integration tests for the full workflow"""
    
    def test_full_workflow(self):
        # Test the complete workflow
        manager = ModelManager()
        runner = BenchmarkRunner(manager)
        leaderboard = Leaderboard()
        
        # Add mock model
        manager.models['integration_test'] = {
            'connector_class': MockConnector,
            'api_key': 'test',
            'model_name': 'integration-model',
            'enabled': True
        }
        
        # Run benchmark
        prompts = ["What is AI?"]
        model_ids = ["integration_test"]
        results = runner.run_benchmark(prompts, model_ids)
        
        # Verify results structure
        self.assertIn('id', results)
        self.assertIn('results', results)
        self.assertIn('integration_test', results['results'])
        
        # Test leaderboard still works
        rankings = leaderboard.get_rankings()
        self.assertIsInstance(rankings['rankings'], list)

def run_all_tests():
    """Run all tests and display results"""
    print("🧪 Running Model Interpretation Dashboard Test Suite")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestMetricsCalculator,
        TestModelManager,
        TestBenchmarkRunner,
        TestLeaderboard,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")
    
    if result.errors:
        print("\nErrors:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed! Dashboard is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the output above.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)