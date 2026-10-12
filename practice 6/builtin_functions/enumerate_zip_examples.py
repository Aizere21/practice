

names = ["Ali", "Aida", "Dana"]
grades = [85, 90, 95]

print("Names with indexes:")
for index, name in enumerate(names, start=1):
    print(index, name)

print("\nNames paired with grades:")
for name, grade in zip(names, grades):
    print(name, grade)