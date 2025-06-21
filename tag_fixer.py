import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config.env")

# Get vault path
vault_path = os.getenv("VAULT_PATH")

# Pattern to match Obsidian-style tags (e.g., #Some-Tag/Value)
tag_pattern = re.compile(r'#([\w/-]+)')

# Function to normalize tag to lowercase with hyphens
def normalize_tag(tag):
    return re.sub(r'[^a-z0-9]+', '-', tag.lower()).strip('-')

# Replacer function with mutable flag
def replacer(match, modified_flag):
    original = match.group(1)
    fixed = normalize_tag(original)
    if fixed != original:
        modified_flag[0] = True
        return f"#{fixed}"
    return match.group(0)

# Walk through all markdown files and fix tags
for root, _, files in os.walk(vault_path):
    for file in files:
        if not file.endswith(".md"):
            continue

        full_path = os.path.join(root, file)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        modified_flag = [False]
        new_content = tag_pattern.sub(lambda m: replacer(m, modified_flag), content)

        if modified_flag[0]:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated tags in: {full_path}")

print("Tag normalization complete.")
