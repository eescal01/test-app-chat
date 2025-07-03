#!/usr/bin/env python3
"""
📦 Script to create a compressed backup (`.tar.gz`) of the current directory,
excluding all `.venv` folders.

✅ Use case:
- This script helps you archive your working directory while skipping heavy virtual environments,
  which are typically not needed for source backups.

🧑‍💻 Author: Evert Escalante <eescal01>
📅 Last updated: 2025-07-03
"""

import os
import tarfile
from datetime import datetime

def exclude_venvs(tar: tarfile.TarFile, root_dir: str):
    """
    Recursively adds files and folders to the tar archive, skipping any `.venv` directories.

    Args:
        tar (tarfile.TarFile): The open tar archive to write to.
        root_dir (str): The root directory to start archiving from.

    Behavior:
        - If a `.venv` folder is encountered, it's excluded from the archive.
        - All other files and folders are added with relative paths.
    """
    for root, dirs, files in os.walk(root_dir):
        # Skip descending into `.venv` folders
        if '.venv' in dirs:
            dirs.remove('.venv')  # Prevent entering the .venv directory

        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, root_dir)
            tar.add(full_path, arcname=relative_path)
            print(f"📁 Added: {relative_path}")

if __name__ == "__main__":
    # Root directory for backup (current directory)
    root_directory = '.'

    # Generate dynamic backup filename using current timestamp
    backup_filename = f"backup_sans_venv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"

    print(f"🔄 Starting backup (excluding .venv) -> {backup_filename}")

    # Create tar.gz archive and exclude virtual environments
    with tarfile.open(backup_filename, "w:gz") as tar:
        exclude_venvs(tar, root_directory)

    print(f"\n✅ Backup completed successfully: {backup_filename}")
