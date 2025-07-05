#!/usr/bin/env python3
"""
📦 Script to create a compressed backup (`.tar.gz`) of selected project files,
excluding `.venv` and unnecessary folders.

✅ Includes only:
- Root YAML and dependency files
- `scripts/` folder
- `services/` folder (including lambdas, cognito, core-infra)

🧑‍💻 Author: Evert Escalante <eescal01>
📅 Updated: 2025-07-03
"""

import os
import tarfile
from datetime import datetime

# Archivos/directorios explícitamente permitidos
WHITELIST = {
    "packaged-root.yaml",
    "poetry.lock",
    "pyproject.toml",
    "requirements.txt",
    "root-layer-stack.yaml",
    "root-stack.yaml",
    "scripts",
    "services",
}

def should_include(path):
    parts = path.split(os.sep)
    return parts[0] in WHITELIST

def exclude_dot_venv(dirs):
    if ".venv" in dirs:
        dirs.remove(".venv")

def add_filtered_files(tar: tarfile.TarFile, root_dir: str):
    for root, dirs, files in os.walk(root_dir):
        # Exclude .venv from descent
        exclude_dot_venv(dirs)

        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, root_dir)

            if should_include(relative_path):
                tar.add(full_path, arcname=relative_path)
                print(f"📁 Added: {relative_path}")

if __name__ == "__main__":
    root_directory = '.'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_sans_venv_{timestamp}.tar.gz"

    print(f"🔄 Starting backup (excluding .venv) -> {backup_filename}")

    with tarfile.open(backup_filename, "w:gz") as tar:
        add_filtered_files(tar, root_directory)

    print(f"\n✅ Backup completed successfully: {backup_filename}")
