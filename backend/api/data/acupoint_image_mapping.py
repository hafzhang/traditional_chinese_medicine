"""
Acupoint Image Mapping
穴位图片映射 - 将图片文件名映射到穴位代码
"""

# 图片文件到穴位代码的映射
# 基于文件名中的关键词匹配
IMAGE_MAPPING = {
    # 单个穴位图片
    "合谷.jpg": "LI4",
    "曲池.jpg": "LI11",
    "手三里.jpg": "LI10",
    "阳溪.jpg": "LI5",
    "阳谷.jpg": "LI6",
    "阳池.jpg": "TE4",
    "外关.jpg": "TE5",
    "腕骨.jpg": "SI4",
    "养老.jpg": "SI6",
    "尺泽.jpg": "LU5",
    "孔最.jpg": "LU6",
    "列缺.jpg": "LU7",
    "鱼际.jpg": "LU10",
    "大陵.jpg": "PC7",
    "内关.jpg": "PC6",
    "劳宫.jpg": "PC8",
    "曲泽.jpg": "PC3",
    "神门.jpg": "HT7",
    "三阴交.jpg": "SP6",
    "血海.jpg": "SP10",
    "阴陵泉.jpg": "SP9",
    "足三里.jpg": "ST36",
    "解溪.jpg": "ST41",
    "内庭.jpg": "ST44",
    "太冲.jpg": "LR3",
    "行间.jpg": "LR2",
    "期门.jpg": "LR14",
    "太溪.jpg": "KI3",
    "涌泉.jpg": "KI1",
    "昆仑.jpg": "BL60",
    "委中.jpg": "BL40",
    "承山.jpg": "BL57",
    "悬钟.jpg": "GB39",
    "丘墟.jpg": "GB40",
    "肩髃.jpg": "LI15",
    "肩髎.jpg": "TE14",
    "肩贞.jpg": "SI9",
    "膝眼.jpg": "EX-LE1",  # 经外奇穴

    # 腹部穴位（组合图）
    "膻中.jpg": "CV17",
    "中脘.jpg": "CV12",  # 从"膻中 中庭 上中下脘 神阙.jpg"映射
    "气海.jpg": "CV6",    # 从"神阙 气海 关元 中极.jpg"映射
    "关元.jpg": "CV4",    # 从"神阙 气海 关元 中极.jpg"映射
    "神阙.jpg": "CV8",    # 从多个组合图映射
    "天枢.jpg": "ST25",   # 从"天枢 神阙.jpg"映射
    "巨阙.jpg": "CV14",

    # 背部穴位
    "大椎.jpg": "GV14",   # 从多个组合图映射
    "命门.jpg": "GV4",
    "肾俞.jpg": "BL23",   # 从"志室 肾俞 命门.jpg"映射
    "腰阳关.jpg": "GV3",  # 从"腰阳关 腰眼 大肠俞.jpg"映射

    # 其他
    "风池.jpg": "GB20",
}

# 经络图片GIF映射
MERIDIAN_GIF_MAPPING = {
    "手太阴肺经.gif": "LU",
    "手阳明大肠经.gif": "LI",
    "足阳明胃经.gif": "ST",
    "足太阴脾经.gif": "SP",
    "手少阴心经.gif": "HT",
    "手太阳小肠经.gif": "SI",
    "足太阳膀胱经.gif": "BL",
    "足少阴肾经.gif": "KI",
    "手厥阴心包经.gif": "PC",
    "手少阳三焦经.gif": "TE",
    "足少阳胆经.gif": "GB",
    "足厥阴肝经.gif": "LR",
    "督脉.gif": "GV",
    "任脉.gif": "CV",
}

# 穴位代码到图片文件名的映射（反向查找）
CODE_TO_IMAGE = {}
for image_file, code in IMAGE_MAPPING.items():
    if code not in CODE_TO_IMAGE:
        CODE_TO_IMAGE[code] = []
    CODE_TO_IMAGE[code].append(image_file)

# 特殊处理：一些组合图片包含多个穴位
COMPOSITE_IMAGES = {
    "大椎 膈俞 至阳.jpg": ["GV14", "BL17", "GV9"],
    "大椎 肩井.jpg": ["GV14", "GB21"],
    "大椎至腰关 风门至大肠俞.jpg": ["GV14", "GV3", "BL12", "BL25"],
    "犊鼻 足三里 上巨 丰隆 条口 下巨.jpg": ["ST35", "ST36", "ST37", "ST40", "ST38", "ST39"],
    "解溪 太冲.jpg": ["ST41", "LR3"],
    "膻中 中庭 上中下脘 神阙.jpg": ["CV17", "CV16", "CV12", "CV11", "CV10", "CV8"],
    "神阙 气海 关元 中极.jpg": ["CV8", "CV6", "CV4", "CV3"],
    "天枢 神阙.jpg": ["ST25", "CV8"],
    "腰阳关 腰眼 大肠俞.jpg": ["GV3", "EX-B7", "BL25"],
    "志室 肾俞 命门.jpg": ["BL52", "BL23", "GV4"],
    "志室 身柱.jpg": ["BL52", "GV12"],
    "身柱 风门 肺俞.jpg": ["GV12", "BL12", "BL13"],
    "中庭 上中下脘 神阙.jpg": ["CV16", "CV12", "CV11", "CV10", "CV8"],
}


def get_image_for_acupoint(code: str) -> str:
    """
    根据穴位代码获取图片文件名

    Args:
        code: 穴位代码，如 "LI4"

    Returns:
        图片文件名，如果没有找到返回默认图片
    """
    if code in CODE_TO_IMAGE and CODE_TO_IMAGE[code]:
        # 返回第一个匹配的图片
        return CODE_TO_IMAGE[code][0]

    # 尝试通过组合图片匹配
    for composite_file, codes in COMPOSITE_IMAGES.items():
        if code in codes:
            return composite_file

    # 没有找到对应图片
    return "default.png"


def get_meridian_gif(meridian_code: str) -> str:
    """
    根据经络代码获取GIF文件名

    Args:
        meridian_code: 经络代码，如 "LU"

    Returns:
        GIF文件名
    """
    for gif_name, code in MERIDIAN_GIF_MAPPING.items():
        if code == meridian_code:
            return gif_name
    return "default.gif"


if __name__ == "__main__":
    print("Acupoint Image Mapping")
    print("=" * 50)
    print(f"Total single acupoint images: {len(IMAGE_MAPPING)}")
    print(f"Total composite images: {len(COMPOSITE_IMAGES)}")
    print(f"Total meridian GIFs: {len(MERIDIAN_GIF_MAPPING)}")
    print()

    # Test some acupoints
    test_codes = ["LI4", "ST36", "CV17", "GV14"]
    for code in test_codes:
        image = get_image_for_acupoint(code)
        print(f"{code} -> {image}")
