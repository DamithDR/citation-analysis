import os


def find_xml_files(directory):
    """
    Recursively find all XML files in the given directory and its subdirectories.

    Args:
        directory (str): The root directory to search for XML files.

    Returns:
        list: A list of paths to the XML files.
    """
    xml_files = []

    # Walk through all files and directories
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if the file has an .xml extension
            if file.lower().endswith('.xml'):
                # Construct the full file path
                full_path = os.path.join(root, file)
                xml_files.append(full_path)

    return xml_files
