#!/usr/bin/env python3
"""
Quick visualization script to demonstrate dashboard metrics
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_demo_visualization():
    """Create demo charts showing model comparison"""
    
    # Sample data for demonstration
    models = ['GPT-4', 'Claude-3-Opus', 'Claude-3-Sonnet', 'GPT-3.5-Turbo', 'Claude-3-Haiku']
    overall_scores = [85.2, 83.7, 79.1, 74.3, 71.8]
    latency_scores = [75.4, 68.9, 82.3, 87.6, 92.1]
    cost_scores = [62.1, 45.3, 78.4, 93.2, 95.8]
    quality_scores = [91.7, 90.2, 85.6, 78.9, 76.4]
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Model Interpretation Dashboard - Demo Results', fontsize=16, fontweight='bold')
    
    # 1. Overall Performance Bar Chart
    bars1 = ax1.bar(models, overall_scores, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    ax1.set_title('Overall Performance Ranking')
    ax1.set_ylabel('Score')
    ax1.set_ylim(0, 100)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, score in zip(bars1, overall_scores):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{score:.1f}', ha='center', va='bottom')
    
    # 2. Radar Chart for Top 3 Models
    categories = ['Latency', 'Cost', 'Quality', 'Overall']
    top_3_models = models[:3]
    top_3_data = [
        [latency_scores[0], cost_scores[0], quality_scores[0], overall_scores[0]],
        [latency_scores[1], cost_scores[1], quality_scores[1], overall_scores[1]], 
        [latency_scores[2], cost_scores[2], quality_scores[2], overall_scores[2]]
    ]
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    
    ax2 = plt.subplot(2, 2, 2, projection='polar')
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, (model, data) in enumerate(zip(top_3_models, top_3_data)):
        data_closed = data + [data[0]]
        ax2.plot(angles, data_closed, 'o-', linewidth=2, label=model, color=colors[i])
        ax2.fill(angles, data_closed, alpha=0.25, color=colors[i])
    
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(categories)
    ax2.set_ylim(0, 100)
    ax2.set_title('Top 3 Models - Multi-Metric Comparison')
    ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    # 3. Cost vs Quality Scatter
    ax3.scatter(cost_scores, quality_scores, s=100, c=overall_scores, cmap='viridis', alpha=0.7)
    for i, model in enumerate(models):
        ax3.annotate(model, (cost_scores[i], quality_scores[i]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    ax3.set_xlabel('Cost Efficiency Score')
    ax3.set_ylabel('Quality Score')
    ax3.set_title('Cost vs Quality Analysis')
    ax3.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(ax3.collections[0], ax=ax3)
    cbar.set_label('Overall Score')
    
    # 4. Latency Performance
    bars4 = ax4.barh(models, latency_scores, color=['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6'])
    ax4.set_title('Response Speed (Latency Scores)')
    ax4.set_xlabel('Latency Score (Higher = Faster)')
    ax4.set_xlim(0, 100)
    
    # Add value labels
    for bar, score in zip(bars4, latency_scores):
        ax4.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                f'{score:.1f}', va='center')
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('/tmp/dashboard_demo.png', dpi=300, bbox_inches='tight')
    print("📊 Demo visualization saved to /tmp/dashboard_demo.png")
    
    # Create a summary table
    df = pd.DataFrame({
        'Model': models,
        'Overall Score': overall_scores,
        'Latency Score': latency_scores,
        'Cost Score': cost_scores,
        'Quality Score': quality_scores
    })
    
    print("\n📋 Model Comparison Summary:")
    print(df.to_string(index=False))
    
    return fig

if __name__ == "__main__":
    try:
        create_demo_visualization()
        print("\n🎯 Dashboard Features Demonstrated:")
        print("   ✅ Multi-metric model comparison")
        print("   ✅ Performance ranking and scoring")
        print("   ✅ Cost vs Quality analysis")
        print("   ✅ Latency benchmarking")
        print("   ✅ Visual dashboard components")
    except ImportError as e:
        print(f"⚠️  Visualization requires matplotlib and pandas: {e}")
        print("   Install with: pip install matplotlib pandas")
    except Exception as e:
        print(f"❌ Error creating visualization: {e}")