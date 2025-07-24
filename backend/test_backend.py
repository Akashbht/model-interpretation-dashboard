#!/usr/bin/env python3
"""
Simple test script to verify the backend functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test imports
try:
    from models.model_manager import ModelManager
    from evaluation.benchmark_runner import BenchmarkRunner
    from evaluation.leaderboard import Leaderboard
    from evaluation.metrics import MetricsCalculator
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test ModelManager
print("\n🧪 Testing ModelManager...")
try:
    model_manager = ModelManager()
    available_models = model_manager.get_available_models()
    print(f"✅ ModelManager works. Found {len(available_models)} models")
    for model in available_models:
        print(f"   - {model.get('name', 'Unknown')} ({model.get('provider', 'Unknown')})")
except Exception as e:
    print(f"❌ ModelManager error: {e}")

# Test BenchmarkRunner
print("\n🧪 Testing BenchmarkRunner...")
try:
    benchmark_runner = BenchmarkRunner(model_manager)
    print("✅ BenchmarkRunner initialized successfully")
except Exception as e:
    print(f"❌ BenchmarkRunner error: {e}")

# Test Leaderboard
print("\n🧪 Testing Leaderboard...")
try:
    leaderboard = Leaderboard()
    rankings = leaderboard.get_rankings()
    print(f"✅ Leaderboard works. Found {len(rankings.get('rankings', []))} ranked models")
except Exception as e:
    print(f"❌ Leaderboard error: {e}")

# Test MetricsCalculator
print("\n🧪 Testing MetricsCalculator...")
try:
    calc = MetricsCalculator()
    
    # Test latency score
    latency_score = calc.calculate_latency_score(2.5)
    print(f"✅ Latency score for 2.5s: {latency_score:.1f}")
    
    # Test cost score
    cost_score = calc.calculate_cost_score(0.02)
    print(f"✅ Cost score for $0.02: {cost_score:.1f}")
    
    # Test quality score
    quality_score = calc.calculate_quality_score("This is a good response to the prompt.")
    print(f"✅ Quality score for sample text: {quality_score:.1f}")
    
except Exception as e:
    print(f"❌ MetricsCalculator error: {e}")

print("\n🎉 Backend test complete!")