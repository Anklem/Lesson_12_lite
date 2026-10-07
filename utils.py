import os
import time
from pathlib import Path


def log_file_action(action: str, file_path: str):
    with open("project_root/logs/log.txt", "a", encoding='utf-8') as log:
        log.write(f"{file_path}: {action}, {time.ctime(os.path.getmtime(file_path))}\n")

def get_dir_size(path):
    total_size = 0
    for file_path in Path(path).rglob('*'):
        if file_path.is_file(): total_size += file_path.stat().st_size
    return total_size
