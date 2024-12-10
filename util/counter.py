import os
from collections import defaultdict


def count_files_by_root_folder(root_path):
    folder_totals = defaultdict(int)  # Dictionary to store totals per immediate folder

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Get the immediate root folder (first-level child of `root_path`)
        relative_path = os.path.relpath(dirpath, root_path)
        immediate_root = relative_path.split(os.sep)[0]  # Get the top-level folder name

        # Add file count to the respective immediate root folder
        folder_totals[immediate_root] += len(filenames)

    # Print the totals
    for folder, total in folder_totals.items():
        print(f"Folder: {folder} | Total Files: {total}")


# Set the root directory (adjust this path to your root project directory)
root_dir = r"D:\Projects\citation-analysis\data\uk"
count_files_by_root_folder(root_dir)
