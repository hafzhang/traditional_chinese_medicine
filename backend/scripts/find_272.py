import os

root = r"e:\a_shangzhan\traditional_chinese_medicine"
print(f"Scanning {root} for '272'...")

for root_dir, dirs, files in os.walk(root):
    for d in dirs:
        if d.startswith("272"):
            print(f"FOUND DIR: {os.path.join(root_dir, d)}")
