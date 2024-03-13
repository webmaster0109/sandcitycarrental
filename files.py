import os

def find_files(root_folder):
    file_list = []
    for root, directories, files in os.walk(root_folder):
        for filename in files:
            file_list.append(os.path.join(root, filename))
    return file_list

if __name__ == "__main__":
    root_folder = '/home/sanjubross'
    if os.path.exists(root_folder):
        files = find_files(root_folder)
        for file in files:
            print(file)
    else:
        print("Root folder does not exist.")
