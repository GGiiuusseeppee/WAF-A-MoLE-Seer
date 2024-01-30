import re 
from sklearn.metrics import roc_curve, auc
import sqlparse
import matplotlib.pyplot as plt
import random


def read_regex_patterns(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def read_and_split(path, label):
    payloads = []
    file_content = open(path, 'r').read()
    statements = sqlparse.split(file_content)
    for statement in statements:
        payloads.append((statement, label))
    return payloads

def read_and_split_payloads(file_path, label):
    payloads = []
    with open(file_path, 'r') as file:
        file_content = file.read()
        statements = sqlparse.split(file_content)
        for statement in statements:
            if statement.strip():
                payloads.append((statement.strip(),label))
    return payloads

def classify_payloads_regex(rules, payloads):
    results = []
    labels = []
    for payload, label in payloads:
        matched = any(re.search(rule, payload) for rule in rules)
        #all_matches = [re.findall(rule, payload) for rule in rules]
        #matched_finds = [item for sublist in all_matches for item in sublist]
        results.append(1 if matched else 0)
        labels.append(label)
    print(f'payloads:\n{payloads[:15]}')
    print(f'results:{results[:15]}')
    print(f'labels: {labels[:15]}')
        #print(matched_finds)
    
    return results, labels

def what_match(rules, payloads):
    results = []
    match_details = []
    for payload, label in payloads:
        matched_rules = [rule for rule in rules if re.search(rule, payload)]
        results.append(1 if matched_rules else 0)
        match_details.append((payload, matched_rules))
    return results, match_details

def calculate_roc(labels, scores):
    fpr, tpr, thresholds = roc_curve(labels, scores)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    #plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.savefig('roc_curve.png')
    plt.show()

attack_label = 1
benign_label = 0
attacks_path = 'wafamole_dataset/attacks.sql.12'
sane_path = 'wafamole_dataset/sane.sql.03'

mal_payloads = read_and_split_payloads(attacks_path, attack_label)
ben_payloads = read_and_split_payloads(sane_path, benign_label)
print(f'MALICIOUSSSS\n{mal_payloads[0]}')
print(len(mal_payloads))
print(f'BENIGNNNN \n {ben_payloads[0]}')
print(len(ben_payloads))

all_payloads = mal_payloads+ben_payloads
#random.shuffle(all_payloads)
#print(all_payloads)

#print(all_payloads[32409])
regex_rules = [
    r'(OR\s+1=1|UNION\s+SELECT|(--|#|/\*)|xp_cmdshell|\b(WAITFOR\s+DELAY|SELECT\s+PG_SLEEP|SLEEP)\b)',
    r"(?i)\b(or|and)\b.*=(['\"])(.*?)\2",
    r"(?i)\bunion\b.*\bselect\b",
    r"(\/\*.*?\*\/|--[^\r\n]*|#)",
    r"0x[0-9A-Fa-f]+",
    r"\bselect\b.*\bfrom\b.*\bselect\b",
    r"(?i)\b(xp_|sp_|exec)\b",
    r"(?i)\bconcat\b|\bchar\b|\bcast\b|\bconvert\b",
    r"(?i)\band\b.*\b=\b|\bor\b.*\b=\b"
]

results, true_labels = classify_payloads_regex(regex_rules, all_payloads)
verify = results==true_labels

'''
for payload, matched_rules in match_details:
    print(f"Payload: {payload}\nMatched Rules: {matched_rules}\n")
'''

print(verify)
print(f'len results with ones:{results.count(1)}')
print(f'len true label with ones: {true_labels.count(1)}')
calculate_roc(true_labels, results)