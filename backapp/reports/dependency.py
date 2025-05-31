# Read the Python dependency tree file
from collections import defaultdict
import re

python_file_path = "python-dependencies.txt"

# Try reading with utf-8 first, fallback to utf-16 if error occurs
try:
    with open(python_file_path, "r", encoding="utf-8") as f:
        python_lines = f.readlines()
except UnicodeDecodeError:
    with open(python_file_path, "r", encoding="utf-16") as f:
        python_lines = f.readlines()

# Extract all package names using regex and count them
python_dependency_count = defaultdict(int)
python_package_regex = re.compile(r'^\s*([a-zA-Z0-9._-]+)==[\d.]+'
                                  r'|[├└│ ]+([a-zA-Z0-9._-]+) \[required')

for line in python_lines:
    match = python_package_regex.search(line)
    if match:
        package = match.group(1) if match.group(1) else match.group(2)
        if package:
            python_dependency_count[package] += 1

# Count total unique dependencies
total_python_dependencies = len(python_dependency_count)

# Write the result to a text file
output_file_path = "python-dependency-count.txt"
with open(output_file_path, "w", encoding="utf-8") as out_file:
    out_file.write(f"Total Unique Python Dependencies: {total_python_dependencies}\n")
    for package, count in sorted(python_dependency_count.items(), key=lambda x: -x[1]):
        out_file.write(f"{package}: {count}\n")

output_file_path
