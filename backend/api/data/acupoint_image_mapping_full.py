"""
Complete Acupoint Image Mapping
完整穴位图片映射 - 55个图片文件映射到穴位
"""

# 单个穴位图片直接映射（使用文件名中的穴位名称）
SINGLE_ACUPOINT_IMAGES = {
    "承山": "承山.jpg",
    "尺泽": "尺泽.jpg",
    "大陵": "大陵.jpg",
    "合谷": "合谷.jpg",
    "肩髎": "肩髎.jpg",
    "肩髃": "肩髃.jpg",
    "肩贞": "肩贞.jpg",
    "解溪": "解溪.jpg",
    "孔最": "孔最.jpg",
    "昆仑": "昆仑.jpg",
    "劳宫": "劳宫.jpg",
    "列缺": "列缺.jpg",
    "命门": "命门.jpg",
    "内关": "内关.jpg",
    "内庭": "内庭.jpg",
    "期门": "期门.jpg",
    "丘墟": "丘墟.jpg",
    "曲池": "曲池.jpg",
    "曲泽": "曲泽.jpg",
    "三阴交": "三阴交.jpg",
    "膻中": "膻中.jpg",
    "神门": "神门.jpg",
    "肾俞": "肾俞.jpg",
    "手三里": "手三里.jpg",
    "太溪": "太溪.jpg",
    "外关": "外关.jpg",
    "腕骨": "腕骨.jpg",
    "委中": "委中.jpg",
    "膝眼": "膝眼.jpg",
    "行间": "行间.jpg",
    "悬钟": "悬钟.jpg",
    "血海": "血海.jpg",
    "阳池": "阳池.jpg",
    "阳谷": "阳谷.jpg",
    "阳溪": "阳溪.jpg",
    "养老": "养老.jpg",
    "鱼际": "鱼际.jpg",
    "涌泉": "涌泉.jpg",
    "足三里": "足三里.jpg",
    "巨阙": "巨阙.jpg",
    "阴陵泉": "阴陵泉.jpg",
}

# 组合图片映射（一个图片包含多个穴位）
COMPOSITE_ACUPOINT_IMAGES = {
    "大椎 膈俞 至阳.jpg": ["大椎", "膈俞", "至阳"],
    "大椎 肩井.jpg": ["大椎", "肩井"],
    "大椎至腰关 风门至大肠俞.jpg": ["大椎", "腰阳关", "风门", "肺俞", "厥阴俞", "心俞", "督俞", "膈俞", "肝俞", "胆俞", "脾俞", "胃俞", "三焦俞", "肾俞", "气海俞", "大肠俞"],
    "犊鼻 足三里 上巨 丰隆 条口 下巨.jpg": ["犊鼻", "足三里", "上巨虚", "丰隆", "条口", "下巨虚"],
    "解溪 太冲.jpg": ["解溪", "太冲"],
    "膻中 中庭 上中下脘 神阙.jpg": ["膻中", "中庭", "上脘", "中脘", "下脘", "神阙"],
    "身柱 风门 肺俞.jpg": ["身柱", "风门", "肺俞"],
    "神阙 气海 关元 中极.jpg": ["神阙", "气海", "关元", "中极"],
    "天枢 神阙.jpg": ["天枢", "神阙"],
    "腰阳关 腰眼 大肠俞.jpg": ["腰阳关", "腰眼", "大肠俞"],
    "志室 身柱.jpg": ["志室", "身柱"],
    "志室 肾俞 命门.jpg": ["志室", "肾俞", "命门"],
    "中庭 上中下脘 神阙.jpg": ["中庭", "上脘", "中脘", "下脘", "神阙"],
    "曲泽穴.jpg": ["曲泽"],  # 单个穴位，文件名带"穴"字
}

# 经络GIF映射
MERIDIAN_GIF_IMAGES = {
    "手太阴肺经": "手太阴肺经.gif",
    "手阳明大肠经": "手阳明大肠经.gif",
    "足阳明胃经": "足阳明胃经.gif",
    "足太阴脾经": "足太阴脾经.gif",
    "手少阴心经": "手少阴心经.gif",
    "手太阳小肠经": "手太阳小肠经.gif",
    "足太阳膀胱经": "足太阳膀胱经.gif",
    "足少阴肾经": "足少阴肾经.gif",
    "手厥阴心包经": "手厥阴心包经.gif",
    "手少阳三焦经": "手少阳三焦经.gif",
    "足少阳胆经": "足少阳胆经.gif",
    "足厥阴肝经": "足厥阴肝经.gif",
    "督脉": "督脉.gif",
    "任脉": "任脉.gif",
}


def get_image_url_by_name(name: str) -> str:
    """
    根据穴位名称获取图片URL

    Args:
        name: 穴位名称（不含"穴"字）

    Returns:
        图片URL路径
    """
    # 首先检查单个穴位图片
    if name in SINGLE_ACUPOINT_IMAGES:
        return f"/static/acupoints/{SINGLE_ACUPOINT_IMAGES[name]}"

    # 检查组合图片
    for image_file, acupoints in COMPOSITE_ACUPOINT_IMAGES.items():
        if name in acupoints:
            return f"/static/acupoints/{image_file}"

    # 检查带"穴"字的图片
    name_with_suffix = name + "穴"
    if name_with_suffix in SINGLE_ACUPOINT_IMAGES:
        return f"/static/acupoints/{SINGLE_ACUPOINT_IMAGES[name_with_suffix]}"

    # 默认占位图
    return "/static/acupoints/default.png"


def get_meridian_gif_url(meridian_name: str) -> str:
    """
    根据经络名称获取GIF动画URL

    Args:
        meridian_name: 经络名称

    Returns:
        GIF动画URL路径
    """
    if meridian_name in MERIDIAN_GIF_IMAGES:
        return f"/static/meridians/{MERIDIAN_GIF_IMAGES[meridian_name]}"
    return "/static/meridians/default.gif"


def get_all_image_mappings():
    """
    获取所有图片映射信息
    用于调试和验证
    """
    mappings = {
        "single_count": len(SINGLE_ACUPOINT_IMAGES),
        "composite_count": len(COMPOSITE_ACUPOINT_IMAGES),
        "meridian_gif_count": len(MERIDIAN_GIF_IMAGES),
        "single_images": SINGLE_ACUPOINT_IMAGES,
        "composite_images": COMPOSITE_ACUPOINT_IMAGES,
        "meridian_gifs": MERIDIAN_GIF_IMAGES
    }

    # 计算组合图片覆盖的穴位总数
    composite_coverage = set()
    for acupoints in COMPOSITE_ACUPOINT_IMAGES.values():
        composite_coverage.update(acupoints)

    mappings["composite_coverage_count"] = len(composite_coverage)
    mappings["total_coverage"] = len(SINGLE_ACUPOINT_IMAGES) + len(composite_coverage)

    return mappings


if __name__ == "__main__":
    mappings = get_all_image_mappings()
    print("=" * 50)
    print("穴位图片映射统计")
    print("=" * 50)
    print(f"单个穴位图片: {mappings['single_count']}")
    print(f"组合图片: {mappings['composite_count']}")
    print(f"经络GIF: {mappings['meridian_gif_count']}")
    print(f"组合图片覆盖穴位数: {mappings['composite_coverage_count']}")
    print(f"总覆盖穴位数: {mappings['total_coverage']}")
    print()

    # 显示组合图片覆盖的穴位
    print("组合图片覆盖的穴位:")
    for image_file, acupoints in COMPOSITE_ACUPOINT_IMAGES.items():
        print(f"  {image_file}: {len(acupoints)}个穴位 - {acupoints}")
