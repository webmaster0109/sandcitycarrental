import os

def list_files_and_folders(directory):
    files_and_folders = []
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path):
            files_and_folders.append((item, 'File'))
        elif os.path.isdir(full_path):
            files_and_folders.append((item, 'Folder'))
    return files_and_folders

if __name__ == "__main__":
    directory_path = '/home/sanjubross'
    if os.path.exists(directory_path):
        files_and_folders = list_files_and_folders(directory_path)
        for name, type in files_and_folders:
            print(f"{name}: {type}")
    else:
        print("Directory does not exist.")
