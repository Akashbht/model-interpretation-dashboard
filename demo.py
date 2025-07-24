#!/usr/bin/env python3
"""
Demo script to showcase the Model Interpretation Dashboard functionality
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5000"

def demonstrate_api():
    print("🎭 Model Interpretation Dashboard - API Demonstration")
    print("=" * 60)
    
    # Test 1: Get available models
    print("\n1. 📋 Checking available models...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/models")
        models = response.json()
        print(f"✅ Found {len(models)} models:")
        for model in models:
            status = "🟢 Connected" if model.get('connected') else "🔴 Not Connected"
            print(f"   • {model.get('provider', 'Unknown')} {model.get('name', 'Unknown')} - {status}")
            print(f"     Context: {model.get('max_context_length', 'Unknown')} tokens")
            print(f"     Cost: ${model.get('cost_per_1k_tokens', 'Unknown')}/1K tokens")
    except Exception as e:
        print(f"❌ Error fetching models: {e}")
        print("💡 Make sure the Flask server is running (python backend/app.py)")
    
    # Test 2: Get leaderboard
    print("\n2. 🏆 Checking current leaderboard...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/leaderboard")
        leaderboard = response.json()
        rankings = leaderboard.get('rankings', [])
        print(f"✅ Current top performers:")
        for i, model in enumerate(rankings[:3], 1):
            print(f"   {i}. {model.get('model_id', 'Unknown')} - Score: {model.get('score', 0):.1f}")
    except Exception as e:
        print(f"❌ Error fetching leaderboard: {e}")
    
    # Test 3: Add a custom model (demo)
    print("\n3. ➕ Adding a custom model (demo)...")
    try:
        custom_model = {
            "name": "demo-model",
            "api_key": "demo-key-123",
            "endpoint": "https://api.example.com/v1"
        }
        response = requests.post(f"{API_BASE_URL}/api/models", json=custom_model)
        result = response.json()
        if result.get('success'):
            print(f"✅ Custom model added: {result.get('model_id')}")
        else:
            print(f"⚠️  Custom model addition: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error adding custom model: {e}")
    
    # Test 4: Run a small benchmark (if models are available)
    print("\n4. 🧪 Running demo benchmark...")
    try:
        # First check if we have any models
        response = requests.get(f"{API_BASE_URL}/api/models")
        models = response.json()
        available_models = [m['id'] for m in models if m.get('connected')]
        
        if not available_models:
            print("⚠️  No connected models available for benchmarking")
            print("💡 To run real benchmarks, add your API keys to .env file")
            return
        
        # Run benchmark with available models
        benchmark_data = {
            "prompts": [
                "What is artificial intelligence?",
                "Explain machine learning in simple terms."
            ],
            "model_ids": available_models[:2],  # Use first 2 available models
            "metrics": ["latency", "cost", "quality"]
        }
        
        print(f"   Running benchmark with {len(benchmark_data['model_ids'])} models...")
        response = requests.post(f"{API_BASE_URL}/api/benchmark", json=benchmark_data)
        results = response.json()
        
        if 'id' in results:
            print(f"✅ Benchmark completed! ID: {results['id']}")
            print(f"   Tested {len(results.get('prompts', []))} prompts")
            print(f"   Compared {len(results.get('results', {}))} models")
            
            # Show summary
            summary = results.get('summary', {})
            overall_rankings = summary.get('rankings', {}).get('overall', [])
            if overall_rankings:
                print("   🏆 Top performer:", overall_rankings[0].get('model_id'))
        else:
            print(f"❌ Benchmark failed: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error running benchmark: {e}")
    
    print("\n🎉 Demo complete!")
    print("\n💻 To explore the full dashboard:")
    print("   1. Start the backend: cd backend && python app.py")
    print("   2. Start the frontend: cd frontend && npm start") 
    print("   3. Open http://localhost:3000 in your browser")
    print("\n🔑 For full functionality, add your API keys to .env file")

if __name__ == "__main__":
    demonstrate_api()