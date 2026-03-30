import os
import shutil

def flatten_directory(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if (file.endswith(".zip") or file == "Thumbs.db"):    # Ignore .zip files and Thumbs.db
                print(f"Ignoring {file}")
            else:
                file_path = os.path.join(root, file)
                if not os.path.exists(root_dir + '/' + file):
                    print(f"Moving {file_path} to {root_dir}")
                    shutil.move(file_path, root_dir)
                else:
                    #print(f"{file} already exists")
                    pass
# Some ways to handle try/except errors:
#                except shutil.SameFileError:
#                    print(f"Source and destination are the same file. No problem.")
#                except PermissionError:
#                    print(f"Permission denied.")
#                except shutil.Error as e:
#                    print(f"An error occurred: {e}")

    for root, dirs, _ in os.walk(root_dir, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            uselessFile = dir_path + "/Thumbs.db"
            if os.path.exists(uselessFile):
                os.remove(uselessFile)
            os.rmdir(dir_path)

# Example usage
#flatten_directory("/path/to/your/directory")
flatten_directory(".")