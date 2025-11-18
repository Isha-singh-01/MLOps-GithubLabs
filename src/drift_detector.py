"""
Data drift detection using statistical tests
"""
import pandas as pd
import numpy as np
from scipy import stats
import json
from datetime import datetime
import os

class DriftDetector:
    def __init__(self, threshold=0.05):
        """
        Initialize drift detector
        
        Args:
            threshold: P-value threshold for drift detection
        """
        self.threshold = threshold
        self.drift_detected = False
        self.drift_metrics = {}
    
    def detect_label_drift(self, old_data, new_data):
        """
        Detect drift in label distribution using Chi-square test
        """
        old_dist = old_data['sentiment'].value_counts().sort_index()
        new_dist = new_data['sentiment'].value_counts().sort_index()
        
        # Ensure same categories
        for label in [0, 1, 2]:
            if label not in old_dist.index:
                old_dist[label] = 0
            if label not in new_dist.index:
                new_dist[label] = 0
        
        old_dist = old_dist.sort_index()
        new_dist = new_dist.sort_index()
        
        # Chi-square test
        chi2, p_value = stats.chisquare(new_dist, old_dist)
        
        # Convert numpy types to Python native types for JSON serialization
        drift_detected = bool(p_value < self.threshold)
        
        self.drift_metrics['label_drift'] = {
            'chi2_statistic': float(chi2),
            'p_value': float(p_value),
            'drift_detected': drift_detected,
            'old_distribution': {int(k): int(v) for k, v in old_dist.to_dict().items()},
            'new_distribution': {int(k): int(v) for k, v in new_dist.to_dict().items()}
        }
        
        return drift_detected
    
    def detect_text_length_drift(self, old_data, new_data):
        """
        Detect drift in text length distribution using KS test
        """
        old_lengths = old_data['review'].str.len()
        new_lengths = new_data['review'].str.len()
        
        # Kolmogorov-Smirnov test
        ks_stat, p_value = stats.ks_2samp(old_lengths, new_lengths)
        
        # Convert numpy types to Python native types for JSON serialization
        drift_detected = bool(p_value < self.threshold)
        
        self.drift_metrics['text_length_drift'] = {
            'ks_statistic': float(ks_stat),
            'p_value': float(p_value),
            'drift_detected': drift_detected,
            'old_mean_length': float(old_lengths.mean()),
            'new_mean_length': float(new_lengths.mean())
        }
        
        return drift_detected
    
    def check_drift(self, old_data_path, new_data_path):
        """
        Check for drift between old and new datasets
        """
        old_data = pd.read_csv(old_data_path)
        new_data = pd.read_csv(new_data_path)
        
        label_drift = self.detect_label_drift(old_data, new_data)
        text_drift = self.detect_text_length_drift(old_data, new_data)
        
        self.drift_detected = label_drift or text_drift
        self.drift_metrics['overall_drift'] = bool(self.drift_detected)
        self.drift_metrics['timestamp'] = datetime.now().isoformat()
        
        return self.drift_detected
    
    def save_report(self, output_path):
        """Save drift detection report"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(self.drift_metrics, f, indent=4)
        
        print(f"Drift report saved to {output_path}")
        print(f"Drift detected: {self.drift_detected}")
        
        # Print summary
        if 'label_drift' in self.drift_metrics:
            print(f"\nLabel Drift:")
            print(f"  P-value: {self.drift_metrics['label_drift']['p_value']:.4f}")
            print(f"  Detected: {self.drift_metrics['label_drift']['drift_detected']}")
            
        if 'text_length_drift' in self.drift_metrics:
            print(f"\nText Length Drift:")
            print(f"  P-value: {self.drift_metrics['text_length_drift']['p_value']:.4f}")
            print(f"  Detected: {self.drift_metrics['text_length_drift']['drift_detected']}")

if __name__ == "__main__":
    # Import here to avoid circular import
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.generate_data import generate_sentiment_data
    
    print("Generating datasets for drift detection test...")
    os.makedirs('data', exist_ok=True)
    
    # Generate baseline data (no drift)
    print("\n1. Generating baseline data (no drift)...")
    old_data = generate_sentiment_data(n_samples=1000, drift=False)
    old_data.to_csv('data/old_reviews.csv', index=False)
    print(f"   Distribution: {dict(old_data['sentiment'].value_counts().sort_index())}")
    
    # Generate new data with drift
    print("\n2. Generating new data (with drift)...")
    new_data = generate_sentiment_data(n_samples=1000, drift=True)
    new_data.to_csv('data/new_reviews.csv', index=False)
    print(f"   Distribution: {dict(new_data['sentiment'].value_counts().sort_index())}")
    
    # Test drift detection
    print("\n3. Running drift detection...")
    detector = DriftDetector(threshold=0.05)
    drift_detected = detector.check_drift('data/old_reviews.csv', 'data/new_reviews.csv')
    
    os.makedirs('metrics', exist_ok=True)
    detector.save_report('metrics/drift_report.json')
    
    print("\n" + "="*50)
    print("✅ Drift detection test complete!")
    print(f"Overall drift detected: {drift_detected}")
    print("="*50)