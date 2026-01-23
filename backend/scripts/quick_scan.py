import os

roots_to_check = [
    r"e:\a_shangzhan\traditional_chinese_medicine\frontend",
    r"e:\a_shangzhan\traditional_chinese_medicine"
]

target_name = "百会"

print("Quick scan...")
for root_dir in roots_to_check:
    if not os.path.exists(root_dir):
        continue
        
    print(f"Checking {root_dir}")
    try:
        items = os.listdir(root_dir)
        for item in items:
            full_path = os.path.join(root_dir, item)
            if os.path.isdir(full_path):
                if item == "node_modules" or item == ".git":
                    continue
                # Check inside this dir
                try:
                    subitems = os.listdir(full_path)
                    for sub in subitems:
                        if target_name in sub:
                            print(f"FOUND in subdir: {os.path.join(full_path, sub)}")
                        # Check if this subitem is a directory that looks like the long name
                        if "272" in sub or "人体穴位" in sub:
                             print(f"SUSPICIOUS DIR: {os.path.join(full_path, sub)}")
                except:
                    pass
            elif target_name in item:
                print(f"FOUND in root: {full_path}")
            
            if "272" in item or "人体穴位" in item:
                print(f"SUSPICIOUS ITEM: {full_path}")
    except Exception as e:
        print(f"Error: {e}")
