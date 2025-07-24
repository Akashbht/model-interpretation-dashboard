from typing import Dict, Any, List
import re
import statistics

class MetricsCalculator:
    """Calculate various evaluation metrics for model responses"""
    
    @staticmethod
    def calculate_latency_score(latency: float) -> float:
        """Calculate latency score (lower latency = higher score)"""
        # Score from 0-100, with 1 second = 100, 10+ seconds = 0
        if latency <= 1.0:
            return 100.0
        elif latency >= 10.0:
            return 0.0
        else:
            return max(0, 100 * (10 - latency) / 9)
    
    @staticmethod
    def calculate_cost_score(cost: float, max_cost: float = 0.1) -> float:
        """Calculate cost score (lower cost = higher score)"""
        if cost <= 0:
            return 100.0
        
        normalized_cost = min(cost / max_cost, 1.0)
        return (1 - normalized_cost) * 100
    
    @staticmethod
    def calculate_quality_score(response: str, reference: str = None) -> float:
        """Calculate response quality score based on various factors"""
        if not response:
            return 0.0
        
        score = 50.0  # Base score
        
        # Length appropriateness (not too short, not excessively long)
        length = len(response.split())
        if 10 <= length <= 500:
            score += 20
        elif 5 <= length < 10 or 500 < length <= 1000:
            score += 10
        
        # Coherence indicators
        sentences = response.split('.')
        if len(sentences) > 1:
            score += 10
        
        # Check for completeness (ends properly)
        if response.strip().endswith('.') or response.strip().endswith('!') or response.strip().endswith('?'):
            score += 10
        
        # Check for obvious errors or incomplete responses
        if "I apologize" in response or "I cannot" in response:
            score -= 10
        
        # If reference provided, calculate similarity
        if reference:
            similarity = MetricsCalculator._calculate_text_similarity(response, reference)
            score = (score + similarity * 100) / 2
        
        return min(100.0, max(0.0, score))
    
    @staticmethod
    def _calculate_text_similarity(text1: str, text2: str) -> float:
        """Simple text similarity calculation"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    @staticmethod
    def calculate_context_utilization_score(prompt_length: int, max_context: int) -> float:
        """Calculate how well the model utilizes its context window"""
        if max_context <= 0:
            return 50.0
        
        utilization = min(prompt_length / max_context, 1.0)
        
        # Optimal utilization is around 20-80% of context
        if 0.2 <= utilization <= 0.8:
            return 100.0
        elif utilization < 0.2:
            return utilization * 500  # Scale up low utilization
        else:
            return max(0, 100 - (utilization - 0.8) * 500)  # Penalize over-utilization
    
    @staticmethod
    def aggregate_scores(scores: Dict[str, float], weights: Dict[str, float] = None) -> float:
        """Aggregate multiple metric scores into a single score"""
        if not scores:
            return 0.0
        
        if weights is None:
            weights = {
                'latency': 0.3,
                'cost': 0.2,
                'quality': 0.4,
                'context_utilization': 0.1
            }
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric, score in scores.items():
            weight = weights.get(metric, 0.1)
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0