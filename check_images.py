import os
import re

posts_dir = "content/posts"
files = os.listdir(posts_dir)

en_files = [f for f in files if f.endswith(".en.md")]

for en_file in en_files:
    zh_file = en_file.replace(".en.md", ".zh.md")
    if zh_file in files:
        en_path = os.path.join(posts_dir, en_file)
        zh_path = os.path.join(posts_dir, zh_file)
        
        with open(en_path, "r") as f:
            en_content = f.read()
        with open(zh_path, "r") as f:
            zh_content = f.read()
            
        en_imgs = re.findall(r"!\[.*?\]\(.*?\)|<img.*?>", en_content, re.IGNORECASE | re.DOTALL)
        zh_imgs = re.findall(r"!\[.*?\]\(.*?\)|<img.*?>", zh_content, re.IGNORECASE | re.DOTALL)
        
        if len(en_imgs) != len(zh_imgs):
            print(f"Mismatch: {en_file} ({len(en_imgs)}) vs {zh_file} ({len(zh_imgs)})")
