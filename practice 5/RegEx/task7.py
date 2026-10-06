import re


def make_next_letter_big(match):
    
    return match.group(1).upper()


text = "this_is_snake_case"
pattern = r"_([a-z])"  
result = re.sub(pattern, make_next_letter_big, text)
print("Результат:", result)

