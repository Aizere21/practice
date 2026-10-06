import re

text = "Apples, pears. grapes and melon"
pattern = r"[ ,. ]"  
print(re.sub(pattern, ":", text))

