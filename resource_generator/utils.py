import os

def extract_file_name(file):
    base = os.path.basename(file)
    return os.path.splitext(base)[0]
