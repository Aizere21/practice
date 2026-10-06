import re

text = "first_part and second_piece; invalid_Name"
pattern = r"\b[a-z]+_[a-z]+\b"

matches = re.findall(pattern, text)
print("Найденные слова:", matches)
