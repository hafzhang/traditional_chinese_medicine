#!/usr/bin/env python3
"""
Update Acupoint Image URLs in Database
更新数据库中的穴位图片URL
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import SessionLocal
from api.models import Acupoint
from api.data.acupoint_image_mapping import get_image_for_acupoint


def update_acupoint_images():
    """更新数据库中的穴位图片URL"""
    print("=" * 50)
    print("[+] Updating Acupoint Image URLs")
    print("=" * 50)

    db = SessionLocal()

    try:
        # 获取所有穴位
        acupoints = db.query(Acupoint).all()
        total = len(acupoints)
        updated = 0
        skipped = 0

        print(f"\nFound {total} acupoints in database")
        print("\nUpdating image URLs...")

        for acupoint in acupoints:
            code = acupoint.code
            old_url = acupoint.image_url

            # 获取正确的图片URL
            image_file = get_image_for_acupoint(code)
            new_url = f"/static/acupoints/{image_file}"

            # 检查是否需要更新
            if old_url != new_url:
                acupoint.image_url = new_url
                updated += 1
                print(f"  [UPDATE] {code}: {old_url} -> {new_url}")
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

        # 显示一些示例
        print(f"\nSample acupoints with images:")
        sample = db.query(Acupoint).filter(
            Acupoint.image_url != "/static/acupoints/default.png"
        ).limit(10).all()

        for a in sample:
            print(f"  {a.code} {a.name}: {a.image_url}")

        return 0

    except Exception as e:
        print(f"\n[ERROR] {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return 1
    finally:
        db.close()


def main():
    """主函数"""
    return update_acupoint_images()


if __name__ == "__main__":
    sys.exit(main())
