#!/usr/bin/env python3
"""
Update All Acupoint Image URLs
更新所有穴位的图片URL - 使用完整图片映射
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import SessionLocal
from api.models import Acupoint
from api.data.acupoint_image_mapping_full import (
    get_image_url_by_name,
    get_all_image_mappings
)


def update_all_acupoint_images():
    """更新所有穴位的图片URL"""
    print("=" * 50)
    print("[+] 更新所有穴位图片URL")
    print("=" * 50)

    # 显示映射统计
    mappings = get_all_image_mappings()
    print(f"\n图片映射统计:")
    print(f"  单个穴位图片: {mappings['single_count']}")
    print(f"  组合图片: {mappings['composite_count']}")
    print(f"  经络GIF: {mappings['meridian_gif_count']}")
    print(f"  组合图片覆盖穴位: {mappings['composite_coverage_count']}")
    print(f"  总覆盖穴位数: {mappings['total_coverage']}")

    db = SessionLocal()

    try:
        # 获取所有穴位
        acupoints = db.query(Acupoint).all()
        total = len(acupoints)
        updated = 0
        no_image = []

        print(f"\n数据库穴位总数: {total}")
        print("\n开始更新图片URL...")

        for acupoint in acupoints:
            # 从穴位名称中提取不含"穴"的基础名称
            base_name = acupoint.name.replace("穴", "").strip()
            old_url = acupoint.image_url

            # 获取新的图片URL
            new_url = get_image_url_by_name(base_name)

            # 检查是否需要更新
            if old_url != new_url:
                acupoint.image_url = new_url
                updated += 1
                status = "[更新]" if "default.png" not in new_url else "[默认]"
                print(f"  {status} {acupoint.code} {acupoint.name}: {old_url} -> {new_url}")
            else:
                if "default.png" in new_url:
                    no_image.append(acupoint.name)

        # 提交更改
        db.commit()

        print("\n" + "=" * 50)
        print("[OK] 更新完成")
        print("=" * 50)
        print(f"\n统计:")
        print(f"  总穴位数: {total}")
        print(f"  已更新: {updated}")
        print(f"  无变化: {total - updated}")
        print(f"  无图片: {len(no_image)}")

        if no_image:
            print(f"\n无图片的穴位（前20个）:")
            for name in no_image[:20]:
                print(f"  - {name}")

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
    return update_all_acupoint_images()


if __name__ == "__main__":
    sys.exit(main())
