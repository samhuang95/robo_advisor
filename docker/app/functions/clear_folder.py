import os

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename == 'dummy':
            continue
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
