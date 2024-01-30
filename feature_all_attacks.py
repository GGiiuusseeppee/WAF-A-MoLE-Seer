import re
import random
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


def load_regex_patterns(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

regex_file_path = 'regex_sql.txt'
regex_patterns = load_regex_patterns(regex_file_path)


def extract_features(payload, regex_patterns):
    features = [int(bool(re.search(pattern, payload))) for pattern in regex_patterns]
    return features

def read_payloads(file_path, delimiter):
    with open(file_path, 'r') as file:
        file_content = file.read()
        payloads = file_content.split(delimiter)
        return [payload.strip() for payload in payloads if payload.strip()]




def process_payloads(payloads_file_path, regex_patterns):
    payloads = read_payloads(payloads_file_path, delimiter)
    #print('payload one', payloads[0])
    return [extract_features(payload, regex_patterns) for payload in payloads]

delimiter = '\n' 

attacks_path = 'payload_xxe.txt'
benign_path = 'wafamole_dataset/sane.sql.02'

mal_payloads = read_payloads(attacks_path, delimiter)
ben_payloads = read_payloads(benign_path, delimiter)
#print('mal payloads:', mal_payloads)
#print('ben payloads:', ben_payloads)

all_payloads = mal_payloads+ben_payloads
random.shuffle(all_payloads)

features = process_payloads(benign_path, regex_patterns)


print('regex:\n',regex_patterns)
print(features)
'''
for i, vector in enumerate(features):
    print(f"Payload {i+1}: Feature Vector = {vector}")  
'''