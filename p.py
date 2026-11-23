import re
import json

users = json.loads(input())

pattern = r"^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.(edu|com)$"

for user in users:
    if re.match(pattern , user["email"]):
        print(user["name"] , user["email"])



from datetime import datetime

date1 = input()
date2 = input()
date3 = input()
date4 = input()

date1 = datetime.strptime(date1, "%Y-%m-%d")
date2 = datetime.strptime(date2, "%Y-%m-%d")
date3 = datetime.strptime(date3, "%Y-%m-%d")
date4 = datetime.strptime(date4, "%Y-%m-%d")

print((date2 - date1).days)
print((date3 - date1).days)
print((date4 - date1).days)




import math

x1 = float(input())
y1 = float(input())

x2 = float(input())
y2 = float(input())

x3 = float(input())
y3 = float(input())

d1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

d2 = math.sqrt((x3 - x2)**2 + (y3 - y2)**2)

print(d1 + d2)


