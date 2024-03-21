from wafamole.models.modsec_wrapp_mod import PyModSecurityWrapperMod
from wafamole.models.modsec_wrapper import PyModSecurityWrapper
import sqlparse
import numpy as np

# Split a string containing two SQL statements:
#attacks = open('sqli.txt', 'r').read()
#statements = sqlparse.split(attacks)
#print(statements) 

test = PyModSecurityWrapperMod(rules_path='../conf')
'''
test1 = PyModSecurityWrapper(rules_path='../conf')

total_score = test1.classify('p=x%27%20OR%20full_name%20LIKE%20%27%Bob%')
print(total_score)
'''

file_path = '../dataset/sqli_1.txt'
file_ben = '../dataset/legitimates/legitimate_1.txt'
triggered_rules_set = set() 




# Open the file and read each payload
with open(file_path, 'r') as file:
    for line in file:
        payload = line.strip()
        if payload:  
            feature_vector, total_score = test.classify(payload)

            triggered_rules = [rule_id for rule_id, triggered in feature_vector.items() if triggered]
            triggered_rules_set.update(triggered_rules)

            
            print(f"Payload: {payload}, Total Score: {total_score}")
            
print(f"All unique triggered rules: {triggered_rules_set}")

unique_rules_list = sorted(list(triggered_rules_set))


with open(file_path, 'r') as file:
    payloads = [line.strip() for line in file if line.strip()]


features = np.zeros((len(payloads), len(unique_rules_list)), dtype=int)


for i, payload in enumerate(payloads):
    feature_vector, _ = test.classify(payload)
    
    
    for rule_id, triggered in feature_vector.items():
        if triggered:
            
            rule_index = unique_rules_list.index(rule_id)
            features[i, rule_index] = 1


print(features.shape)            

import json

def save_unique_rules_to_json(unique_rules_list, file_path):
    """Save the unique rules list to a JSON file.

    Args:
        unique_rules_list (list): The list of unique rules.
        file_path (str): The path to the file where the JSON should be saved.
    """
    data = {"rules_ids": unique_rules_list}
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


json_file_path = '../dataset/unique_rules_list.json'
save_unique_rules_to_json(unique_rules_list, json_file_path)

print(f"Unique rules list saved to {json_file_path}")


