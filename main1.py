import numpy as np
from Waf_dataset_processing import DataLoader, FeatureExtractor
from Waf_classification import SeerBox
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

def main():

    data_loader = DataLoader(malicious_path='dataset/true-positives.txt', benign_path='dataset/false-positives.txt' )
    data = data_loader.load_data()
    data.head()
    regex_patterns_path = 'regex_xss.txt'
    feature_extractor = FeatureExtractor(regex_patterns_path)

    X, y = feature_extractor.extract_features(data)
    seer = SeerBox(X,y, model=SVC())
    seer.run()
    

if __name__ == "__main__":
    main()
