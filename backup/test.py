import os

file_path = '/static/file/avatar-1.jpg'

# Split the file path into its components
path_parts = file_path.split(os.sep)

# Remove one folder from the path
if len(path_parts) >= 2:
    path_parts.pop(-2)  # Remove the second-to-last element (folder)

# Reconstruct the file path
new_file_path = os.sep.join(path_parts)

print(new_file_path)
