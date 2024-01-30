import re
import sqlparse

def read_regex_patterns(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def read_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        statements = sqlparse.split(file_content)
        return [statement.strip() for statement in statements if statement.strip()]

def create_feature_vector(query, regex_patterns):
    return [int(bool(re.search(pattern, query))) for pattern in regex_patterns]

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

regex_file_path = ''
#regex_patterns = read_regex_patterns(regex_file_path)

file_path = 'wafamole_dataset/attacks.sql.12'
queries = read_file(file_path)
print(queries[:5])

features = [create_feature_vector(query, regex_rules) for query in queries]

print(features[:5])