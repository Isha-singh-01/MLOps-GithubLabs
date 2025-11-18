"""
Generate synthetic sentiment analysis dataset
"""
import pandas as pd
import numpy as np
from datetime import datetime
import os

def generate_sentiment_data(n_samples=1000, drift=False):
    """
    Generate synthetic product review data
    
    Args:
        n_samples: Number of samples to generate
        drift: If True, introduce data drift
    """
    np.random.seed(42 if not drift else 123)
    
    # Positive review templates
    positive_words = ['excellent', 'amazing', 'great', 'love', 'perfect', 
                     'wonderful', 'fantastic', 'best', 'awesome', 'outstanding']
    
    # Negative review templates
    negative_words = ['terrible', 'awful', 'worst', 'hate', 'poor', 
                     'disappointing', 'bad', 'horrible', 'useless', 'waste']
    
    # Neutral words
    neutral_words = ['okay', 'average', 'fine', 'decent', 'acceptable',
                    'normal', 'standard', 'typical', 'regular', 'ordinary']
    
    reviews = []
    sentiments = []
    
    for _ in range(n_samples):
        sentiment = np.random.choice([0, 1, 2], p=[0.3, 0.4, 0.3])  # neg, neu, pos
        
        if drift:
            # Introduce drift: more negative reviews
            sentiment = np.random.choice([0, 1, 2], p=[0.5, 0.3, 0.2])
        
        if sentiment == 2:  # Positive
            words = np.random.choice(positive_words, size=np.random.randint(5, 15))
            review = f"This product is {' '.join(words)}. Highly recommend!"
        elif sentiment == 0:  # Negative
            words = np.random.choice(negative_words, size=np.random.randint(5, 15))
            review = f"This product is {' '.join(words)}. Do not buy!"
        else:  # Neutral
            words = np.random.choice(neutral_words, size=np.random.randint(5, 15))
            review = f"This product is {' '.join(words)}. It's acceptable."
        
        reviews.append(review)
        sentiments.append(sentiment)
    
    df = pd.DataFrame({
        'review': reviews,
        'sentiment': sentiments,
        'timestamp': datetime.now()
    })
    
    return df

if __name__ == "__main__":
    # Generate training data
    df = generate_sentiment_data(n_samples=1000, drift=False)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/reviews.csv', index=False)
    print(f"Generated {len(df)} samples")
    print(f"Sentiment distribution:\n{df['sentiment'].value_counts()}")