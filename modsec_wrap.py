from wafamole.models.modsec_wrapper import PyModSecurityWrapper
import sqlparse
''' '''
# Split a string containing two SQL statements:
attacks = open('wafamole_dataset/attacks.sql', 'r').read()
statements = sqlparse.split(attacks)
print(statements) 


test = PyModSecurityWrapper(rules_path='conf')
result = test.classify("'OR'1=1'")

print(result)

