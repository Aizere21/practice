import re

text = "Alice met Bob and McDonald"
pattern = r"\b[A-Z][a-z]+\b"

print("Найденные слова:", re.findall(pattern, text))

