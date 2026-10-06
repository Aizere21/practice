import re

text = "InsertSpacesBetweenCapitalizedWords"
pattern = r"(?<=[a-z])(?=[A-Z])"  
result = re.sub(pattern, " ", text)
print("Результат:", result)
