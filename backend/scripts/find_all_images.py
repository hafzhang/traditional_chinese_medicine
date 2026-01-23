import os

root_dir = r"e:\a_shangzhan\traditional_chinese_medicine"
print(f"Scanning {root_dir} for image directories...")

image_dirs = {}

for root, dirs, files in os.walk(root_dir):
    # Skip .git, node_modules, etc to speed up
    if '.git' in root or 'node_modules' in root or '__pycache__' in root:
        continue
        
    jpg_count = sum(1 for f in files if f.lower().endswith('.jpg'))
    if jpg_count > 0:
        image_dirs[root] = jpg_count
        # If we find a specific file, print it
        for f in files:
            if "百会" in f:
                print(f"FOUND MATCH: {os.path.join(root, f)}")

# Sort by count descending
sorted_dirs = sorted(image_dirs.items(), key=lambda x: x[1], reverse=True)

print("\nTop directories with images:")
for d, count in sorted_dirs[:10]:
    print(f"{count} images in: {d}")
