import os

start_dir = r"e:\a_shangzhan\traditional_chinese_medicine"
print(f"Walking {start_dir}")

for root, dirs, files in os.walk(start_dir):
    for d in dirs:
        if d.startswith("272"):
            print(f"FOUND DIR: {os.path.join(root, d)}")
