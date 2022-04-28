"""Validators for Resource Allocation App."""

import os

def is_file_exists(parent_dir: str, filename: str) -> bool:
    """If file exists at the path constructed from parent_dir and filename
    :param parent_dir: Parent directory of the file
    :type parent_dir: str
    :param filename: File name
    :type filename: str
    :return: True if file exists, else False
    :rtype: bool
    """
    
    filepath = os.path.join(parent_dir, filename)
    return os.path.exists(filepath)