import os
import sys
from PIL import Image

target_dir = r"C:\Users\Administrator\Documents\claude过滤蔬菜图"
target_size_kb = 200
target_size_bytes = target_size_kb * 1024

jpg_files = [f for f in os.listdir(target_dir) if f.lower().endswith('.jpg')]
total_files = len(jpg_files)

print("=" * 50)
print("JPG Image Compression Task V2")
print("=" * 50)
print(f"Directory: {target_dir}")
print(f"Total files: {total_files}")
print(f"Target size: {target_size_kb} KB")
print("=" * 50)
print()

files_compressed = 0
files_skipped = 0
files_failed = 0
total_original_size = 0
total_compressed_size = 0
failed_list = []

for filename in jpg_files:
    filepath = os.path.join(target_dir, filename)
    original_size = os.path.getsize(filepath)
    total_original_size += original_size
    original_size_kb = round(original_size / 1024, 2)
    
    if original_size > target_size_bytes:
        print(f"[{files_compressed + 1}] Processing: {filename} - {original_size_kb} KB")
        
        try:
            img = Image.open(filepath)
            original_width, original_height = img.size
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Strategy 1: Try quality reduction first
            success = False
            temp_path = filepath + '.tmp'
            
            for quality in range(75, 34, -5):
                img.save(temp_path, 'JPEG', quality=quality, optimize=True)
                new_size = os.path.getsize(temp_path)
                if new_size <= target_size_bytes:
                    os.remove(filepath)
                    os.rename(temp_path, filepath)
                    new_size_kb = round(new_size / 1024, 2)
                    saved_percent = round((original_size - new_size) / original_size * 100, 1)
                    total_compressed_size += new_size
                    files_compressed += 1
                    print(f"    SUCCESS: {new_size_kb} KB (Quality: {quality}, Saved: {saved_percent}%)")
                    success = True
                    break
                else:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            
            # Strategy 2: If quality reduction didn't work, resize the image
            if not success:
                print(f"    Quality reduction insufficient, trying resize...")
                for scale_factor in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]:
                    new_width = int(original_width * scale_factor)
                    new_height = int(original_height * scale_factor)
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    for quality in [75, 65, 55, 45]:
                        resized_img.save(temp_path, 'JPEG', quality=quality, optimize=True)
                        new_size = os.path.getsize(temp_path)
                        
                        if new_size <= target_size_bytes:
                            resized_img.close()
                            img.close()
                            os.remove(filepath)
                            os.rename(temp_path, filepath)
                            new_size_kb = round(new_size / 1024, 2)
                            saved_percent = round((original_size - new_size) / original_size * 100, 1)
                            total_compressed_size += new_size
                            files_compressed += 1
                            print(f"    SUCCESS: {new_size_kb} KB (Resize: {scale_factor*100:.0f}%, Quality: {quality}, Saved: {saved_percent}%)")
                            success = True
                            break
                        else:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                    
                    if success:
                        break
                    
                    resized_img.close()
                
                if not success:
                    img.close()
                    total_compressed_size += original_size
                    files_failed += 1
                    failed_list.append(f"{filename} ({original_size_kb} KB)")
                    print(f"    FAILED: Could not compress under target size")
            else:
                img.close()
            
        except Exception as e:
            total_compressed_size += original_size
            files_failed += 1
            failed_list.append(f"{filename} - {str(e)}")
            print(f"    ERROR: {e}")
            try:
                img.close()
            except:
                pass
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
print(f"Files failed: {files_failed}")
print()

original_mb = round(total_original_size / (1024 * 1024), 2)
compressed_mb = round(total_compressed_size / (1024 * 1024), 2)
saved_mb = round((total_original_size - total_compressed_size) / (1024 * 1024), 2)
saved_percent = round((total_original_size - total_compressed_size) / total_original_size * 100, 1)

print(f"Original total size: {original_mb} MB")
print(f"Compressed total size: {compressed_mb} MB")
print(f"Space saved: {saved_mb} MB ({saved_percent}%)")

if failed_list:
    print()
    print("Failed files:")
    for f in failed_list:
        print(f"  - {f}")

print("=" * 50)
