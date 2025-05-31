# Try reading the file with an alternative encoding due to UnicodeDecodeError
with open("npm-dependency-tree.txt", "r", encoding="utf-16") as f:
    lines = f.readlines()

# Re-parse using the same logic
from collections import defaultdict
import re

dependency_count = defaultdict(int)
package_regex = re.compile(r'[\s|`+\\-]*([@a-zA-Z0-9/._-]+)@[\d.]+')

for line in lines:
    match = package_regex.search(line)
    if match:
        package = match.group(1)
        dependency_count[package] += 1

# Convert to DataFrame and sort by count
import pandas as pd

df = pd.DataFrame(list(dependency_count.items()), columns=["Dependency", "Count"])
df_sorted = df.sort_values(by="Count", ascending=False).reset_index(drop=True)

import ace_tools as tools; tools.display_dataframe_to_user(name="Full Dependency Count", dataframe=df_sorted)


# Calculate total number of unique dependencies
total_dependencies = len(dependency_count)

# Add a summary row to the dataframe
summary_row = pd.DataFrame([["Total Unique Dependencies", total_dependencies]], columns=["Dependency", "Count"])
df_with_summary = pd.concat([df_sorted, summary_row], ignore_index=True)

import ace_tools as tools; tools.display_dataframe_to_user(name="Dependency Count with Total", dataframe=df_with_summary)
