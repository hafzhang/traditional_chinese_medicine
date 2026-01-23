import os

path = r"e:\a_shangzhan\traditional_chinese_medicine\backend\static\acupoints"
os.makedirs(path, exist_ok=True)
print(f"Created {path}")

readme_content = """Acupoint Images Directory
穴位图片目录

请将穴位图片放置在此目录下。
建议命名规则：
- 使用拼音或英文名，如 baihui.jpg, zusanli.jpg
- 或者使用代码，如 GV20.jpg, ST36.jpg

目前数据库中的 image_url 指向 /static/acupoints/default.png 或 /static/acupoints/default_detail.png
如果添加了真实图片，请更新数据库或重命名图片以匹配（需修改代码逻辑）。

默认图片：
- default.png: 列表缩略图占位符
- default_detail.png: 详情页大图占位符
"""

with open(os.path.join(path, "README.txt"), "w", encoding="utf-8") as f:
    f.write(readme_content)

print("Created README.txt")
