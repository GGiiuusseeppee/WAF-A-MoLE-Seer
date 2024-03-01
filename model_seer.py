import re
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model import LogisticRegression

class RegexClassifier():
    

    def __init__(self, regex_patterns):
        
        self.model = LogisticRegression()
        self.regex_patterns = regex_patterns

    def extract_features(self, payloads):
        
        features = np.array([[1 if re.search(pattern, payload) else 0 for pattern in self.regex_patterns] for payload in payloads])
        
        
        '''
        feature_vector = np.array([int(bool(re.search(regex, payload))) for regex in self.regex_patterns])
        return feature_vector
        '''
        return features
        
    def fit(self, X, y):    
    
        features = self.extract_features(X)
        self.model.fit(features, y)
        
        '''
        feature_vectors = np.array([self.extract_features(payload) for payload in X])

        
        malicious_indices = np.where(y == 1)[0]  
        self.threshold = np.mean(np.sum(feature_vectors[malicious_indices], axis=1))

        print(f"Optimal threshold set to: {self.threshold}")
        '''

    def predict(self, X):
        
        '''
        feature_vectors = np.array([self.extract_features(payload) for payload in X])

        predictions = np.sum(feature_vectors, axis=1) > len(self.regex_patterns) / 2  # Example threshold

        return predictions
        '''
        features = self.extract_features(X)
        return self.model.predict(features)