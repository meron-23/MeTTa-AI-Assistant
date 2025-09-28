import os

def get_all_files(repo_dir):
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(repo_dir)
        for file in files
    ]
