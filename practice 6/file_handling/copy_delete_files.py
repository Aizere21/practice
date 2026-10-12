
import os
import shutil

source = "example.txt"
backup = "backup_example.txt"
copy_file = "copy_example.txt"


if os.path.isfile(source):
    shutil.copy(source, backup)
    shutil.copy(source, copy_file)
    print("Backup and copy created.")
else:
    print("Source file does not exist. Run read_files.py first.")


print("Exists:", os.path.exists(source))
print("Readable:", os.access(source, os.R_OK))
print("Writable:", os.access(source, os.W_OK))
print("Executable:", os.access(source, os.X_OK))


if os.path.isfile(copy_file):
    try:
        os.remove(copy_file)
        print("Copy file deleted.")
    except OSError as error:
        print("Could not delete file:", error)
else:
    print("There is no copy file to delete.")