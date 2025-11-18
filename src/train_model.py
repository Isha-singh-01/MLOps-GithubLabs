"""
Train sentiment analysis model
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib
import json
from datetime import datetime
import os

def train_sentiment_model(data_path, model_output_path, metrics_output_path):
    """
    Train a sentiment analysis model
    """
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['review'], df['sentiment'], 
        test_size=0.2, 
        random_state=42,
        stratify=df['sentiment']
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Create pipeline
    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', MultinomialNB(alpha=0.1))
    ])
    
    print("Training model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Train accuracy: {train_score:.4f}")
    print(f"Test accuracy: {test_score:.4f}")
    
    # Save model
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(model, model_output_path)
    print(f"Model saved to {model_output_path}")
    
    # Save metrics
    metrics = {
        'train_accuracy': float(train_score),
        'test_accuracy': float(test_score),
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'timestamp': datetime.now().isoformat(),
        'model_path': model_output_path
    }
    
    os.makedirs(os.path.dirname(metrics_output_path), exist_ok=True)
    with open(metrics_output_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    
    print(f"Metrics saved to {metrics_output_path}")
    
    return metrics

if __name__ == "__main__":
    # Generate data first
    from generate_data import generate_sentiment_data
    
    os.makedirs('data', exist_ok=True)
    df = generate_sentiment_data(n_samples=1000, drift=False)
    df.to_csv('data/reviews.csv', index=False)
    
    # Train model
    metrics = train_sentiment_model(
        data_path='data/reviews.csv',
        model_output_path='models/sentiment_model.pkl',
        metrics_output_path='metrics/training_metrics.json'
    )