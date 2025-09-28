import os
import hashlib
import json
import shutil
from logger import logger

def hash_file_content(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def process_metta_files(file_paths, output_dir, repo_root=None, json_path="../metta_index.json"):
    """
    file_paths: list of all files in the repo
    output_dir: where to store hashed .metta files (flat)
    repo_root: path to the root of the cloned repo (used for relative paths in index)
    json_path: name of JSON file mapping hash → relative path
    """
    os.makedirs(output_dir, exist_ok=True)
    index = {}

    repo_name = os.path.basename(os.path.normpath(repo_root)) if repo_root else "repo"

    for file in file_paths:
        if file.endswith(".metta"):
            file_hash = hash_file_content(file)
            new_name = f"{file_hash}.metta"

            rel_path_inside_repo = os.path.relpath(file, repo_root).replace("\\", "/") if repo_root else os.path.basename(file)
            index[file_hash] = f"{repo_name}/{rel_path_inside_repo}"

            dest_path = os.path.join(output_dir, new_name)
            shutil.copy(file, dest_path)

            logger.info(f"Processed {rel_path_inside_repo} → {new_name}")
    os.system(f"rd /s /q {repo_root}")
    json_full_path = os.path.join(output_dir, json_path)
    with open(json_full_path, "w") as f:
        json.dump(index, f, indent=2)

    logger.info(f"Index saved at {json_full_path}")
