import re
import numpy as np


test_malicious_queries = ["UPDATE `tab` SET `col3` = 1 WHERE `col1` = 'z';", "SELECT `col2` FROM `tab` WHERE `col1` LIKE '%'g'%';", "DELETE FROM `tab` WHERE `col2` < ') AS YebR WHERE 4493=4493 OR 3408=(SELECT COUNT(*) FROM DOMAIN.DOMAINS AS T1,DOMAIN.COLUMNS AS T2,DOMAIN.TABLES AS T3)-- aXUa';",
"BEGIN DBMS_LOCK.SLEEP(5);"," END-- Sheb';"]  
test_benign_queries = ["DELETE FROM `tab` WHERE `col3` = 895025152 LIMIT -1055391744;", "INSERT INTO `tab` ( `col3` ) VALUES ( -1677524992 );", "DELETE FROM `tab` WHERE `col3` = 'ogkyjlp';",
"DELETE FROM `tab` WHERE `col2` LIKE '%'l'%' AND `col3` LIKE '%'kfy'%';", "INSERT INTO `tab` ( `col3` ) VALUES ( 2025062400 );", "UPDATE `tab` SET `col1` = 1 WHERE `col1` LIKE '%'yes'%' LIMIT -1862467584;"]
regex_patterns_path = 'regex_sql.txt'
patterns = []
with open(regex_patterns_path, 'r') as file:
    for line in file:
        patterns.append(line.strip())

print(patterns)
combined = test_malicious_queries + test_benign_queries
for query in combined:
    matches = [int(bool(re.search(pattern, query))) for pattern in patterns]
    print(f"Query: {query}\nMatches: {matches}\n")


features = []
for text in combined:

    payload_features = [1 if re.search(pattern, text) else 0 for pattern in patterns]
    features.append(payload_features)


ben_label = 0
mal_label = 1


vectorized_data = np.array(features)


def analyze_feature_distribution(vectorized_data):
    feature_sums = np.sum(vectorized_data, axis=0)
    print("Feature occurrence count:", feature_sums)
    
    threshold_high = len(vectorized_data) * 0.2  
    threshold_low = len(vectorized_data) * 0.1  
    
    too_common = np.where(feature_sums > threshold_high)[0]
    too_rare = np.where(feature_sums < threshold_low)[0]
    print("Too common features:", too_common)
    print("Too rare features:", too_rare)

analyze_feature_distribution(vectorized_data)


from sklearn.ensemble import RandomForestClassifier
X_train = vectorized_data
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
importances = clf.feature_importances_


for i, imp in enumerate(importances):
    print(f"Feature {i}: Importance {imp}")
