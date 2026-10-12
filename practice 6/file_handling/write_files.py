
with open("notes.txt", "w") as file:
    file.write("First line\n")
    file.write("Second line\n")


with open("notes.txt", "a") as file:
    file.write("Third line\n")


fruits = ["Apple", "Banana", "Orange"]
with open("fruits.txt", "w") as file:
    for fruit in fruits:
        file.write(fruit + "\n")

print("Files written successfully.")

with open("notes.txt", "r") as file:
    print(file.read())

with open("fruits.txt", "r") as file:
    print(file.read())


try:
    with open("new_file.txt", "x") as file:
        file.write("This file was created with mode x.")
    print("new_file.txt created.")
except FileExistsError:
    print("new_file.txt already exists.")




