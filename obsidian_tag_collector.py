import os
import re
from dotenv import load_dotenv

load_dotenv("config.env")

# Set this to the root folder of your Obsidian vault
vault_path = os.getenv("VAULT_PATH")

# Pattern to match Obsidian-style tags
tag_pattern = re.compile(r'#([\w/-]+)')

found_tags = set()

for root, _, files in os.walk(vault_path):
    for file in files:
        if file.endswith(".md"):
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()
                found_tags.update(tag_pattern.findall(content))

# Sort and format the tag list
sorted_tags = sorted(found_tags)
with open(f"{vault_path}{os.getenv("TAGS_FILE_PATH")}", "w", encoding="utf-8") as out_file:
    for tag in sorted_tags:
        out_file.write(f"{tag}\n")

print(f"Extracted {len(sorted_tags)} unique tags into obsidian_tags.md")