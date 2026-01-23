import os

root = r"e:\a_shangzhan\traditional_chinese_medicine\frontend\src"
print(f"Scanning {root}...")
for item in os.listdir(root):
    print(item)
