import os
from pathlib import Path


os.makedirs("Practice6_demo/files/documents", exist_ok=True)

path = "."

print("Current directory:", os.getcwd())
print("\nAll items in the current directory:")
print(os.listdir(path))

print("\nDirectories only:")
for name in os.listdir(path):
    full_path = os.path.join(path, name)
    if os.path.isdir(full_path):
        print(name)

print("\nFiles only:")
for name in os.listdir(path):
    full_path = os.path.join(path, name)
    if os.path.isfile(full_path):
        print(name)

print("\nAll nested directories and files:")
for root, directories, files in os.walk("Practice6_demo"):
    print("Folder:", root)
    print("Directories:", directories)
    print("Files:", files)

print("\nPython files in the current directory:")
for name in os.listdir(path):
    if name.endswith(".py"):
        print(name)


folder = Path("pathlib_demo")
folder.mkdir(exist_ok=True)
print("\npathlib folder exists:", folder.exists())
