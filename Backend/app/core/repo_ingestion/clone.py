import os
import subprocess
from urllib.parse import urlparse
from logger import logger

def get_repo_name(repo_url):
    """Extract repo name from URL, e.g. metta-moses.git → metta-moses"""
    return os.path.splitext(os.path.basename(urlparse(repo_url).path))[0]

def clone_repo(repo_url, temp_dir):
    repo_name = get_repo_name(repo_url)
    repo_path = os.path.join(temp_dir, repo_name)

    if os.path.exists(repo_path):
        logger.info(f"Repo already exists at {repo_path}, removing...")
        subprocess.run(["rm", "-rf", repo_path], shell=True)
    logger.info(f"Cloning {repo_url} into {repo_path}")
    subprocess.run(["git", "clone", repo_url, repo_path], check=True)

    return repo_path
