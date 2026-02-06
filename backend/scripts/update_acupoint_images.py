#!/usr/bin/env python3
"""
Update Acupoint Image URLs in Database
更新数据库中的穴位图片URL - 支持多穴位图片映射
"""
import sys
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import SessionLocal
from api.models import Acupoint
from api.data.acupoint_image_mapping import get_image_for_acupoint, COMPOSITE_IMAGES

# 图片源目录
SOURCE_IMAGE_DIR = Path("E:/a_shangzhan/traditional_chinese_medicine/source_data/272_pages_acupunture_point_chart/228_pages_acupunture_point")

# 静态文件目标目录
STATIC_DIR = Path("E:/a_shangzhan/traditional_chinese_medicine/backend/static/acupoints")


def ensure_directories():
    """确保静态文件目录存在"""
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] 静态文件目录: {STATIC_DIR}")


def copy_composite_images():
    """
    复制多穴位组合图片到静态目录
    返回复制的文件数量
    """
    print("\n" + "=" * 50)
    print("[+] Copying Composite Images")
    print("=" * 50)

    copied = 0
    skipped = 0
    errors = 0

    for composite_file in COMPOSITE_IMAGES.keys():
        source_path = SOURCE_IMAGE_DIR / composite_file

        # 检查源文件是否存在
        if not source_path.exists():
            print(f"  [ERROR] Source file not found: {composite_file}")
            errors += 1
            continue

        # 目标路径（替换空格为下划线）
        target_filename = composite_file.replace(' ', '_').replace('-', '_')
        target_path = STATIC_DIR / target_filename

        # 复制文件
        if target_path.exists():
            print(f"  [SKIP] Already exists: {target_filename}")
            skipped += 1
        else:
            try:
                shutil.copy2(source_path, target_path)
                print(f"  [COPY] {composite_file} -> {target_filename}")
                copied += 1
            except Exception as e:
                print(f"  [ERROR] Failed to copy {composite_file}: {e}")
                errors += 1

    print(f"\n  Copied: {copied}, Skipped: {skipped}, Errors: {errors}")
    return copied, skipped, errors


def update_acupoint_images(force_composite=False):
    """更新数据库中的穴位图片URL"""
    print("=" * 50)
    print("[+] Updating Acupoint Image URLs")
    print("=" * 50)

    # 首先复制组合图片
    ensure_directories()
    copy_composite_images()

    db = SessionLocal()

    try:
        # 获取所有穴位
        acupoints = db.query(Acupoint).all()
        total = len(acupoints)
        updated = 0
        skipped = 0
        composite_count = 0

        # 构建组合图片中的穴位代码集合
        composite_codes = set()
        for codes in COMPOSITE_IMAGES.values():
            composite_codes.update(codes)

        print(f"\nFound {total} acupoints in database")
        print(f"Found {len(composite_codes)} acupoints in composite images")
        print("\nUpdating image URLs...")

        for acupoint in acupoints:
            code = acupoint.code
            old_url = acupoint.image_url

            # 获取正确的图片URL
            image_file = get_image_for_acupoint(code)

            # 处理组合图片（使用下划线替换空格的文件名）
            if ' ' in image_file:
                image_file = image_file.replace(' ', '_').replace('-', '_')
                composite_count += 1

            new_url = f"/static/acupoints/{image_file}"

            # 检查是否需要更新
            if old_url != new_url:
                acupoint.image_url = new_url
                updated += 1
                if composite_count <= 5 or updated <= 10:
                    print(f"  [UPDATE] {code} {acupoint.name}: {old_url} -> {new_url}")
            elif force_composite and code in composite_codes:
                # 强制更新组合图片中的穴位（即使URL看起来一样）
                acupoint.image_url = new_url
                updated += 1
                print(f"  [FORCE] {code} {acupoint.name}: {old_url} -> {new_url}")
            else:
                skipped += 1

        # 提交更改
        db.commit()

        print("\n" + "=" * 50)
        print("[OK] Update Completed")
        print("=" * 50)
        print(f"\nSummary:")
        print(f"  Total acupoints: {total}")
        print(f"  Updated: {updated}")
        print(f"  Skipped: {skipped}")
        print(f"  Composite images used: {composite_count}")

        # 显示使用组合图片的穴位
        print(f"\nAcupoints using composite images:")
        all_composite_acupoints = []
        for composite_file, codes in COMPOSITE_IMAGES.items():
            for code in codes:
                point = db.query(Acupoint).filter(Acupoint.code == code).first()
                if point:
                    all_composite_acupoints.append(point)

        for a in all_composite_acupoints[:15]:
            print(f"  {a.code} {a.name}: {a.image_url}")

        if len(all_composite_acupoints) > 15:
            print(f"  ... and {len(all_composite_acupoints) - 15} more")

        return 0

    except Exception as e:
        print(f"\n[ERROR] {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return 1
    finally:
        db.close()


def verify_composite_mappings():
    """验证多穴位图片映射"""
    print("=" * 50)
    print("[+] Verifying Composite Image Mappings")
    print("=" * 50)

    db = SessionLocal()

    try:
        print("\nComposite Images and their Acupoints:")
        print("-" * 50)

        for composite_file, codes in COMPOSITE_IMAGES.items():
            print(f"\n  Image: {composite_file}")
            target_filename = composite_file.replace(' ', '_').replace('-', '_')
            expected_url = f"/static/acupoints/{target_filename}"

            for code in codes:
                acupoint = db.query(Acupoint).filter(Acupoint.code == code).first()
                if acupoint:
                    status = "OK" if acupoint.image_url == expected_url else "MISMATCH"
                    print(f"    [{status}] {code} {acupoint.name}: {acupoint.image_url}")
                else:
                    print(f"    [NOT FOUND] {code}")

    finally:
        db.close()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='更新穴位图片URL')
    parser.add_argument('--verify', action='store_true', help='仅验证映射')
    parser.add_argument('--force-composite', action='store_true', help='强制更新组合图片中的穴位')
    args = parser.parse_args()

    if args.verify:
        verify_composite_mappings()
    else:
        return update_acupoint_images(force_composite=args.force_composite)


if __name__ == "__main__":
    sys.exit(main() or 0)
