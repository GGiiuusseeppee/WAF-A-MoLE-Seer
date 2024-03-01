import os
import re
from os import listdir
from os.path import isfile, join
import numpy as np


class WAFDatasetProcessingextr:
    def __init__(self, payloads_path, regex_patterns_path):
        self.payloads_path = payloads_path
        self.regex_patterns_path = regex_patterns_path
        self.payload_texts = []  
        self.features = [] 
        self.labels = []
        self.vectorized_data = None
        
        

    def _find_payloads(self):
        with open(self.payloads_path, 'r') as file:
            self.payload_texts = file.readlines()
        
    def create_label_vector(self, label):
        with open(join(self.payloads_path), 'r') as file:
            for _ in file:
                self.labels.append(label)
            self.labels = np.array(self.labels)
           

    def _load_regex_patterns(self):
        
        patterns = []
        with open(self.regex_patterns_path, 'r') as file:
            for line in file:
                patterns.append(line.strip())
        return patterns

    def _extract_features(self, patterns):
        
        for text in self.payload_texts:
            payload_features = [0] * len(patterns)
            for i, pattern in enumerate(patterns):
                if re.search(pattern, text):
                    payload_features[i] = 1
            self.features.append(payload_features)
        

    def _vectorize_features(self):
        
        self.vectorized_data = np.array(self.features)
        

    def process(self):
        self._find_payloads()
        patterns = self._load_regex_patterns()
        self._extract_features(patterns)
        self._vectorize_features()
        
