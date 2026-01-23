#!/usr/bin/env python3
"""
Copy Acupoint Images to Static Folder
复制穴位图片到静态文件夹
"""
import sys
import os
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.data.acupoint_image_mapping import (
    IMAGE_MAPPING,
    COMPOSITE_IMAGES,
    MERIDIAN_GIF_MAPPING,
    get_image_for_acupoint,
    get_meridian_gif
)


def copy_acupoint_images():
    """复制穴位图片到静态文件夹"""
    print("=" * 50)
    print("[+] Copying Acupoint Images")
    print("=" * 50)

    # 源目录
    source_dir = Path(__file__).parent.parent.parent / "272_pages_acupunture_point_chart"
    acupoint_images_dir = source_dir / "56_new_acupunture_point"
    meridian_gif_dir = source_dir / "GIF_meridian_collateral_diagram"

    # 目标目录
    backend_static = Path(__file__).parent.parent / "static"
    acupoint_target_dir = backend_static / "acupoints"
    meridian_target_dir = backend_static / "meridians"

    # 创建目标目录
    acupoint_target_dir.mkdir(parents=True, exist_ok=True)
    meridian_target_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nSource directories:")
    print(f"  Acupoint images: {acupoint_images_dir}")
    print(f"  Meridian GIFs: {meridian_gif_dir}")

    print(f"\nTarget directories:")
    print(f"  Acupoint images: {acupoint_target_dir}")
    print(f"  Meridian GIFs: {meridian_target_dir}")

    # 1. 复制单个穴位图片
    print("\n[1] Copying single acupoint images...")
    count_single = 0

    for image_file, code in IMAGE_MAPPING.items():
        source_file = acupoint_images_dir / image_file
        if source_file.exists():
            # 使用穴位代码作为文件名，保持原扩展名
            ext = source_file.suffix
            target_file = acupoint_target_dir / f"{code}{ext}"

            try:
                shutil.copy2(source_file, target_file)
                print(f"  [OK] {image_file} -> {target_file.name}")
                count_single += 1
            except Exception as e:
                print(f"  [ERROR] Failed to copy {image_file}: {e}")
        else:
            print(f"  [WARN] Source file not found: {image_file}")

    print(f"\n  Copied {count_single} single acupoint images")

    # 2. 复制组合图片
    print("\n[2] Copying composite acupoint images...")
    count_composite = 0

    for composite_file, codes in COMPOSITE_IMAGES.items():
        source_file = acupoint_images_dir / composite_file
        if source_file.exists():
            # 为组合图片创建副本，使用主要穴位代码命名
            primary_code = codes[0]
            ext = source_file.suffix
            target_file = acupoint_target_dir / f"{primary_code}_composite{ext}"

            try:
                shutil.copy2(source_file, target_file)
                print(f"  [OK] {composite_file} -> {target_file.name}")
                count_composite += 1
            except Exception as e:
                print(f"  [ERROR] Failed to copy {composite_file}: {e}")
        else:
            print(f"  [WARN] Source file not found: {composite_file}")

    print(f"\n  Copied {count_composite} composite images")

    # 3. 复制经络GIF
    print("\n[3] Copying meridian GIF files...")
    count_gif = 0

    for gif_file, code in MERIDIAN_GIF_MAPPING.items():
        source_file = meridian_gif_dir / gif_file
        if source_file.exists():
            target_file = meridian_target_dir / gif_file

            try:
                shutil.copy2(source_file, target_file)
                print(f"  [OK] {gif_file} -> {target_file.name}")
                count_gif += 1
            except Exception as e:
                print(f"  [ERROR] Failed to copy {gif_file}: {e}")
        else:
            print(f"  [WARN] Source file not found: {gif_file}")

    print(f"\n  Copied {count_gif} meridian GIF files")

    # 4. 创建默认占位图片
    print("\n[4] Creating placeholder images...")

    # 创建简单的PNG占位图
    import base64
    png_data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )

    default_acupoint = acupoint_target_dir / "default.png"
    with open(default_acupoint, "wb") as f:
        f.write(png_data)

    default_meridian = meridian_target_dir / "default.gif"
    with open(default_meridian, "wb") as f:
        f.write(png_data)

    print(f"  [OK] Created default placeholder images")

    # 统计
    print("\n" + "=" * 50)
    print("[OK] Image Copy Completed")
    print("=" * 50)
    print(f"\nSummary:")
    print(f"  Single acupoint images: {count_single}")
    print(f"  Composite images: {count_composite}")
    print(f"  Meridian GIFs: {count_gif}")
    print(f"  Total files copied: {count_single + count_composite + count_gif}")
    print(f"\nTarget directories:")
    print(f"  {acupoint_target_dir}")
    print(f"  {meridian_target_dir}")


def main():
    """主函数"""
    try:
        copy_acupoint_images()
        return 0
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
