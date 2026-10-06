import re


text = "camelCaseString"
pattern = r"([a-z])([A-Z])"  
text_with_underscores = re.sub(pattern, r"\1_\2", text)
result = text_with_underscores.lower()

print("Результат:", result)
