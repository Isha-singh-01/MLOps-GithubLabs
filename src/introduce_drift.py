"""
Script to introduce data drift
"""
import sys
import os

# Add src to path
sys.path.append('src')
from generate_data import generate_sentiment_data

# Generate data with drift
df = generate_sentiment_data(n_samples=1000, drift=True)
os.makedirs('data', exist_ok=True)
df.to_csv('data/reviews.csv', index=False)

print("✅ Data with drift generated!")
print(f"\nSentiment distribution:")
print(df['sentiment'].value_counts())