import os
import shutil

def flatten_directory(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            shutil.move(file_path, root_dir)

    for root, dirs, _ in os.walk(root_dir, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

# Example usage
#flatten_directory("/path/to/your/directory")
flatten_directory(".")