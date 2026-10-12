
with open("example.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("I am learning Python.\n")
    file.write("File handling is useful.")


with open("example.txt", "r") as file:
    print("READ:")
    print(file.read())


with open("example.txt", "r") as file:
    print("FIRST LINE:")
    print(file.readline().strip())


with open("example.txt", "r") as file:
    print("ALL LINES:")
    print(file.readlines())


with open("example.txt", "r") as file:
    lines = file.readlines()
print("Number of lines:", len(lines))

