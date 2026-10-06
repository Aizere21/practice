import re

text = "SplitAtUppercaseLetters"
parts = re.split(r"(?=[A-Z])", text)


words = []
for part in parts:
    if part != "":
        words.append(part)

print("Слова:", words)
