
import os
import shutil

source = "example.txt"
destination_folder = "destination"

os.makedirs(destination_folder, exist_ok=True)

if os.path.isfile(source):
    
    shutil.copy(source, os.path.join(destination_folder, "example_copy.txt"))
    print("File copied to destination folder.")

    
else:
    print("example.txt does not exist. Run file_handling/read_files.py first.")


path = os.path.abspath(source)
if os.path.exists(path):
    print("Path exists.")
    print("Filename:", os.path.basename(path))
    print("Directory:", os.path.dirname(path))
else:
    print("Path does not exist.")


for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    filename = letter + ".txt"
    with open(os.path.join(destination_folder, filename), "w") as file:
        file.write("This is file " + filename)

print("Created A.txt to Z.txt inside destination.")
