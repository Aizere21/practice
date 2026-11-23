
 
with open("values.txt", "w") as f:
    f.write("10\n")
    f.write("3.5\n")
    f.write("7\n")
    f.write("hello\n")


with open("values.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    value = line.strip()
    print(value, type(value))


with open("values.txt", "a") as f:
    f.write("42\n")


numbers = []

with open("values.txt", "r") as f:
    for line in f:
        value = line.strip()

        try:
            number = int(value)
        except ValueError:
            try:
                number = float(value)
            except ValueError:
                continue

        numbers.append(number)


print("Numbers:", numbers)
print("Total:", sum(numbers))
print("Smallest:", min(numbers))
print("Largest:", max(numbers))
print("How many numbers:", len(numbers))

import os
os.remove("values.txt")








import math
a , b , c = list(map(int , input(). split()))
d = b**2 - 4*a*c
d1 = math.sqrt(d)

print(float(d))
print(float(d1))





from datetime import datetime
date1 = input()
date2 = input()
date1 = datetime.strptime(date1 , "%Y-%m-%d %H:%M")
date2 = datetime.strptime(date2 , "%Y-%m-%d %H:%M")
difference = date2 - date1 
minutes = difference.total_seconds() / 60
print(int(minutes))



import re
import json

users = json.loads(input())

pattern = r"^a[a-z]*_[a-z_]*$"

for user in users:
    if re.match(pattern, user["handle"]):
        print(user["user_id"])



