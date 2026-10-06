import re

pattern = r"a.*b"  
examples = ["a123b", "ab", "a and b", "baab"]

for word in examples:
    result = re.fullmatch(pattern, word)
    print(word, "— подходит" if result else "— не подходит")

