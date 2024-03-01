import pandas as pd
import json
import re
import numpy as np



class DataLoader:
    def __init__(self, malicious_path, benign_path):
        self.malicious_path=malicious_path
        self.benign_path = benign_path

        self.data = None

    def load_data(self):

      malicious_data = []

      with open(self.malicious_path, 'r') as file:
          for line in file:
              malicious_data.append(line.strip())
      malicious_labels = [1] * len(malicious_data)

      benign_data = []
      with open(self.benign_path, 'r') as file:
          for line in file:
              benign_data.append(line.strip())
      benign_labels = [0]*len(benign_data)

      combined_data = malicious_data + benign_data
      combined_labels = malicious_labels + benign_labels

      return pd.DataFrame({'payloads': combined_data, 'label': combined_labels})


class FeatureExtractor:
    def __init__(self, regex_patterns_path):
        self.regex_patterns_path = regex_patterns_path
        self.patterns = self._load_regex_patterns()

    def _load_regex_patterns(self):
        patterns = []
        with open(self.regex_patterns_path, 'r') as file:
            for line in file:
                patterns.append(line.strip())
        return patterns

    def extract_features(self, texts):
        features = []
        labels = texts['label']
        texts = texts.drop('label', axis=1)['payloads']
        for text in texts:

          payload_features = [1 if re.search(pattern, text) else 0 for pattern in self.patterns]
          features.append(payload_features)
        return np.array(features), np.array(labels)

    def save_features(self, features, save_path):
        np.save(save_path, features)
        print(f"Features saved to {save_path}")







