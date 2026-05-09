import json
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

def train_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'agrobot_data', 'intents.json')
    
    if not os.path.exists(data_path):
        print(f"Error: Intents data not found at {data_path}")
        return

    with open(data_path, 'r') as f:
        data = json.load(f)
        
    X_train = []
    y_train = []
    
    for intent in data['intents']:
        for pattern in intent['patterns']:
            X_train.append(pattern)
            y_train.append(intent['tag'])
            
    print(f"Loaded {len(X_train)} training patterns across {len(set(y_train))} intents.")
    
    # Create an intent classification pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2))),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("Training the Agrobot model...")
    pipeline.fit(X_train, y_train)
    
    models_dir = os.path.join(base_dir, 'ml_models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'agrobot_model.pkl')
    joblib.dump(pipeline, model_path)
    
    print(f"Model saved successfully to {model_path}")

if __name__ == "__main__":
    train_model()
