import os
import sys
from PIL import Image

target_dir = r"C:\Users\Administrator\Documents\claude过滤蔬菜图"
target_size_kb = 200
target_size_bytes = target_size_kb * 1024

jpg_files = [f for f in os.listdir(target_dir) if f.lower().endswith('.jpg')]
total_files = len(jpg_files)

print("=" * 50)
print("JPG Image Compression Task")
print("=" * 50)
print(f"Directory: {target_dir}")
print(f"Total files: {total_files}")
print(f"Target size: {target_size_kb} KB")
print("=" * 50)
print()

files_compressed = 0
files_skipped = 0
total_original_size = 0
total_compressed_size = 0

for filename in jpg_files:
    filepath = os.path.join(target_dir, filename)
    original_size = os.path.getsize(filepath)
    total_original_size += original_size
    original_size_kb = round(original_size / 1024, 2)
    
    if original_size > target_size_bytes:
        print(f"[{files_compressed + 1}] Processing: {filename} - {original_size_kb} KB")
        
        try:
            img = Image.open(filepath)
            
            # Convert to RGB if necessary (for RGBA images)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Try different quality levels
            success = False
            for quality in range(75, 34, -5):
                temp_path = filepath + '.tmp'
                
                # Save with current quality
                img.save(temp_path, 'JPEG', quality=quality, optimize=True)
                
                # Check file size
                new_size = os.path.getsize(temp_path)
                new_size_kb = round(new_size / 1024, 2)
                
                if new_size <= target_size_bytes:
                    # Success - replace original
                    os.remove(filepath)
                    os.rename(temp_path, filepath)
                    
                    saved_percent = round((original_size - new_size) / original_size * 100, 1)
                    total_compressed_size += new_size
                    files_compressed += 1
                    
                    print(f"    SUCCESS: {new_size_kb} KB (Quality: {quality}, Saved: {saved_percent}%)")
                    success = True
                    break
                else:
                    # Clean up temp file and try lower quality
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            
            if not success:
                # Could not compress enough - keep original
                total_compressed_size += original_size
                print(f"    FAILED: Could not compress under target size")
                
            img.close()
            
        except Exception as e:
            total_compressed_size += original_size
            print(f"    ERROR: {e}")
    else:
        total_compressed_size += original_size
        files_skipped += 1
        print(f"  SKIP: {filename} - {original_size_kb} KB (already OK)")

print()
print("=" * 50)
print("COMPRESSION REPORT")
print("=" * 50)
print(f"Total files: {total_files}")
print(f"Files compressed: {files_compressed}")
print(f"Files skipped: {files_skipped}")
print()

original_mb = round(total_original_size / (1024 * 1024), 2)
compressed_mb = round(total_compressed_size / (1024 * 1024), 2)
saved_mb = round((total_original_size - total_compressed_size) / (1024 * 1024), 2)
saved_percent = round((total_original_size - total_compressed_size) / total_original_size * 100, 1)

print(f"Original total size: {original_mb} MB")
print(f"Compressed total size: {compressed_mb} MB")
print(f"Space saved: {saved_mb} MB ({saved_percent}%)")
print("=" * 50)
