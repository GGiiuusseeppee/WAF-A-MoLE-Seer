from wafamole.models.modsec_wrapper import PyModSecurityWrapper
import sqlparse

# Split a string containing two SQL statements:
attacks = open('sqli.txt', 'r').read()
statements = sqlparse.split(attacks)
#print(statements) 


test = PyModSecurityWrapper(rules_path='conf')
feature = test.extract_features(statements)
result = test.classify(statements)
print(result)


