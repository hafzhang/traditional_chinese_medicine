import os

start_dir = r"e:\a_shangzhan\traditional_chinese_medicine\frontend\src"
print(f"Walking {start_dir}")

found = False
for root, dirs, files in os.walk(start_dir):
    if "百会.jpg" in files:
        print(f"FOUND IT IN: {root}")
        found = True
        break

if not found:
    print("Could not find '百会.jpg' anywhere.")
