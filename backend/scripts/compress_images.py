"""
图片压缩脚本
将 source_data/dishes_images 目录下的所有图片压缩到 200KB 以内
"""
import os
from pathlib import Path
from PIL import Image
import io

# 目标目录（从 backend 目录的上一级）
IMAGE_DIR = Path(__file__).parent.parent.parent / "source_data" / "dishes_images"
# 目标大小 (200KB = 200 * 1024 bytes)
TARGET_SIZE = 200 * 1024
# 质量步长
QUALITY_STEP = 5


def get_image_size(image_bytes):
    """获取图片字节数"""
    return len(image_bytes)


def compress_image(image_path, target_size=TARGET_SIZE):
    """
    压缩图片到目标大小以内

    Args:
        image_path: 图片路径
        target_size: 目标大小（字节），默认 200KB

    Returns:
        (success, original_size, compressed_size, quality_used)
    """
    try:
        # 获取原始文件大小
        original_size = image_path.stat().st_size

        # 如果已经小于目标大小，跳过
        if original_size <= target_size:
            return True, original_size, original_size, None

        # 打开图片
        img = Image.open(image_path)

        # 如果是 RGBA 模式，转换为 RGB（JPEG 不支持透明度）
        if img.mode == 'RGBA':
            # 创建白色背景
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 使用 alpha 通道作为 mask
            img = background
        elif img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')

        # 逐步降低质量直到满足大小要求
        quality = 95
        while quality >= 50:  # 最低质量 50
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            compressed_size = get_image_size(output.getvalue())

            if compressed_size <= target_size:
                # 保存压缩后的图片
                output.seek(0)
                with open(image_path, 'wb') as f:
                    f.write(output.getvalue())
                return True, original_size, compressed_size, quality

            quality -= QUALITY_STEP

        # 如果质量降到最低仍不能满足，尝试调整尺寸
        # 逐步缩小尺寸
        width, height = img.size
        scale_factor = 0.9

        while scale_factor >= 0.5:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            output = io.BytesIO()
            resized_img.save(output, format='JPEG', quality=75, optimize=True)
            compressed_size = get_image_size(output.getvalue())

            if compressed_size <= target_size:
                output.seek(0)
                with open(image_path, 'wb') as f:
                    f.write(output.getvalue())
                return True, original_size, compressed_size, f"scale_{scale_factor:.1f}_q75"

            scale_factor -= 0.05

        # 最后尝试：最小尺寸 + 最低质量
        resized_img = img.resize((int(width * 0.5), int(height * 0.5)), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        resized_img.save(output, format='JPEG', quality=50, optimize=True)
        compressed_size = get_image_size(output.getvalue())
        output.seek(0)
        with open(image_path, 'wb') as f:
            f.write(output.getvalue())
        return True, original_size, compressed_size, "scale_0.5_q50"

    except Exception as e:
        print(f"  错误: {e}")
        return False, 0, 0, None


def format_size(size_bytes):
    """格式化文件大小显示"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}MB"


def main():
    """主函数"""
    if not IMAGE_DIR.exists():
        print(f"错误: 目录不存在 {IMAGE_DIR}")
        return

    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}

    # 获取所有图片文件
    image_files = [f for f in IMAGE_DIR.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]

    if not image_files:
        print("没有找到图片文件")
        return

    print(f"找到 {len(image_files)} 个图片文件")
    print(f"目标大小: {format_size(TARGET_SIZE)}")
    print("-" * 80)

    # 统计信息
    stats = {
        'total': len(image_files),
        'skipped': 0,
        'compressed': 0,
        'failed': 0,
        'original_total': 0,
        'compressed_total': 0
    }

    # 按文件大小排序，先处理大文件
    image_files.sort(key=lambda x: x.stat().st_size, reverse=True)

    for i, image_path in enumerate(image_files, 1):
        original_size = image_path.stat().st_size
        stats['original_total'] += original_size

        print(f"[{i}/{stats['total']}] {image_path.name} ({format_size(original_size)})", end=" ... ")

        success, orig_sz, comp_sz, method = compress_image(image_path)

        if success:
            stats['compressed_total'] += comp_sz
            if orig_sz == comp_sz:
                print(f"已跳过 (已小于目标)")
                stats['skipped'] += 1
            else:
                print(f"已压缩 -> {format_size(comp_sz)} (方法: {method})")
                stats['compressed'] += 1
        else:
            print(f"失败")
            stats['failed'] += 1

    # 打印统计信息
    print("\n" + "=" * 80)
    print("压缩完成！")
    print(f"  总文件数: {stats['total']}")
    print(f"  已压缩: {stats['compressed']}")
    print(f"  已跳过: {stats['skipped']} (已小于目标大小)")
    print(f"  失败: {stats['failed']}")
    print(f"  原始总大小: {format_size(stats['original_total'])}")
    print(f"  压缩后总大小: {format_size(stats['compressed_total'])}")
    saved = stats['original_total'] - stats['compressed_total']
    print(f"  节省空间: {format_size(saved)} ({saved / stats['original_total'] * 100:.1f}%)")
    print("=" * 80)


if __name__ == "__main__":
    main()
