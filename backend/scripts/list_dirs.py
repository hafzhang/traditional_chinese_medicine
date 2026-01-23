import os

start_dir = r"e:\a_shangzhan\traditional_chinese_medicine\frontend\src"
print(f"Listing {start_dir}")

try:
    items = os.listdir(start_dir)
    for item in items:
        print(f" - {item}")
        full_path = os.path.join(start_dir, item)
        if os.path.isdir(full_path):
             print(f"   (DIR) {item}")
             try:
                 sub_items = os.listdir(full_path)
                 print(f"   Contains {len(sub_items)} items")
             except Exception as e:
                 print(f"   Error accessing subdir: {e}")

except Exception as e:
    print(f"Error: {e}")
