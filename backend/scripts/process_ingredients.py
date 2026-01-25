#!/usr/bin/env python3
"""
食材数据处理脚本
- 读取CSV并修复JSON数组格式
- 复制图片到backend/static/ingredients/
- 生成SQL导入脚本
"""

import csv
import os
import shutil
import json
from pathlib import Path

# Constitution code mapping (Chinese name to code)
CONSTITUTION_MAP = {
    "平和质": "peace",
    "气虚质": "qi_deficiency",
    "阳虚质": "yang_deficiency",
    "阴虚质": "yin_deficiency",
    "痰湿质": "phlegm_damp",
    "湿热质": "damp_heat",
    "血瘀质": "blood_stasis",
    "气郁质": "qi_depression",
    "特禀质": "special",
}

# Reverse mapping for validation
CONSTITUTION_CODE_TO_NAME = {v: k for k, v in CONSTITUTION_MAP.items()}

# Paths
BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = BASE_DIR.parent / "source_data" / "ingredients"
STATIC_DIR = BASE_DIR / "static" / "ingredients"
CSV_FILE = SOURCE_DIR / "ingredients_data.csv"

def parse_json_array(value):
    """Safely parse JSON array string to list"""
    if not value or value.strip() == "":
        return []
    try:
        # Handle string format like '["平和质","气虚质"]'
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return []

def convert_constitution_names_to_codes(names):
    """Convert Chinese constitution names to codes"""
    if not names:
        return []
    codes = []
    for name in names:
        code = CONSTITUTION_MAP.get(name)
        if code:
            codes.append(code)
    return codes

def copy_images():
    """Copy ingredient images to static directory"""
    print(f"Copying images from {SOURCE_DIR} to {STATIC_DIR}...")

    # Create directory if not exists
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

    image_files = list(SOURCE_DIR.glob("*.jpg")) + list(SOURCE_DIR.glob("*.jpeg")) + list(SOURCE_DIR.glob("*.png"))

    # Exclude non-ingredient images
    exclude_files = {"蔬菜集锦.jpg"}
    copied = 0
    for img in image_files:
        if img.name not in exclude_files:
            dest = STATIC_DIR / img.name
            if not dest.exists():
                shutil.copy2(img, dest)
                copied += 1
            else:
                # File exists, skip
                pass

    print(f"Copied {copied} new images. Total in static: {len(list(STATIC_DIR.glob('*')))}")
    return len(list(STATIC_DIR.glob("*")))

def process_csv():
    """Process CSV file and fix data"""
    print(f"Processing CSV file: {CSV_FILE}")

    with open(CSV_FILE, 'r', encoding='gbk') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Total rows in CSV: {len(rows)}")

    # Process each row
    processed_data = []
    issues = []

    for i, row in enumerate(rows):
        item = {
            'name': row['name'].strip(),
            'category': row['category'].strip() if row['category'] else None,
            'nature': row['nature'].strip() if row['nature'] else None,
            'flavor': row['taste'].strip() if row['taste'] else None,  # CSV taste -> model flavor
            'efficacy': row['efficacy'].strip() if row['efficacy'] else None,
            'nutrition': row['nutritional_value'].strip() if row['nutritional_value'] else None,
            'precautions': row['contraindications'].strip() if row['contraindications'] else None,
        }

        # Parse JSON arrays
        suitable_constitutions = parse_json_array(row.get('suitable_constitutions', ''))
        avoid_constitutions = parse_json_array(row.get('avoid_constitutions', ''))
        aliases = parse_json_array(row.get('aliases', ''))

        # Convert Chinese names to codes
        item['suitable_constitutions'] = convert_constitution_names_to_codes(suitable_constitutions)
        item['avoid_constitutions'] = convert_constitution_names_to_codes(avoid_constitutions)
        item['aliases'] = aliases

        # Image URL
        img_path = STATIC_DIR / f"{item['name']}.jpg"
        if img_path.exists():
            item['image_url'] = f"/static/ingredients/{item['name']}.jpg"
        else:
            item['image_url'] = None
            if i < 10:  # Only log first few
                issues.append(f"No image for: {item['name']}")

        # 新增字段映射
        # usage_guide -> description
        usage_guide = row.get('usage_guide', '').strip()
        description = row.get('description', '').strip()

        # 组合描述：如果有原有描述和使用指导，合并显示
        if description and usage_guide:
            item['description'] = f"{description}\n\n使用指导：{usage_guide}"
        elif usage_guide:
            item['description'] = usage_guide
        elif description:
            item['description'] = description
        else:
            item['description'] = None

        # compatibility -> 解析为compatible_foods和incompatible_foods
        compatibility = row.get('compatibility', '').strip()
        if compatibility:
            # 解析格式："宜配：...；忌配：..."
            compatible_foods = []
            incompatible_foods = []

            if '宜配：' in compatibility or '宜配:' in compatibility:
                parts = compatibility.split('忌配：' if '忌配：' in compatibility else '忌配:')
                compatible_part = parts[0].replace('宜配：', '').replace('宜配:', '').strip()
                if compatible_part and compatible_part != '无特殊禁忌':
                    compatible_foods.append({
                        'name': '通用',
                        'reason': compatible_part,
                        'benefit': '营养互补'
                    })

            if '忌配：' in compatibility or '忌配:' in compatibility:
                parts = compatibility.split('忌配：' if '忌配：' in compatibility else '忌配:')
                if len(parts) > 1:
                    incompatible_part = parts[1].strip()
                    if incompatible_part and incompatible_part != '无特殊禁忌':
                        incompatible_foods.append({
                            'name': '通用',
                            'reason': incompatible_part,
                            'effect': '可能影响健康或营养吸收'
                        })

            item['compatible_foods'] = compatible_foods if compatible_foods else None
            item['incompatible_foods'] = incompatible_foods if incompatible_foods else None
        else:
            item['compatible_foods'] = None
            item['incompatible_foods'] = None

        # Validate required fields
        if not item['name']:
            issues.append(f"Row {i+1}: Missing name")
            continue

        processed_data.append(item)

    print(f"Processed {len(processed_data)} items")
    if issues:
        print(f"\nIssues found ({len(issues)}):")
        for issue in issues[:20]:  # Show first 20
            print(f"  - {issue}")

    return processed_data

def generate_import_script(data):
    """Generate Python script to import data to database"""
    output_file = BASE_DIR / "scripts" / "import_ingredients_to_db.py"

    # First, save data to a JSON file
    data_file = BASE_DIR / "scripts" / "ingredients_data.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    script_content = f'''#!/usr/bin/env python3
"""
自动生成的食材数据导入脚本
运行此脚本将食材数据导入数据库
"""

import sys
import json
sys.path.insert(0, str(r"{BASE_DIR}"))

from api.database import SessionLocal
from api.models import Ingredient
from datetime import datetime
from pathlib import Path

def import_ingredients():
    """Import ingredients from CSV data"""
    db = SessionLocal()
    try:
        # Load data from JSON file
        data_file = Path(r"{data_file}")
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        imported = 0
        for item in data:
            # Check if ingredient already exists
            existing = db.query(Ingredient).filter(Ingredient.name == item['name']).first()
            if existing:
                # Update existing
                for key, value in item.items():
                    setattr(existing, key, value)
                existing.updated_at = datetime.now()
            else:
                # Create new
                ingredient = Ingredient(**item)
                db.add(ingredient)

            imported += 1
            if imported % 100 == 0:
                db.commit()
                print(f"Imported {{imported}} items...")

        db.commit()
        print(f"Successfully imported {{imported}} ingredients!")

        # Show some stats
        total = db.query(Ingredient).count()
        with_images = db.query(Ingredient).filter(Ingredient.image_url != None).count()
        print(f"\\nTotal ingredients in DB: {{total}}")
        print(f"With images: {{with_images}}")

    except Exception as e:
        db.rollback()
        print(f"Error: {{e}}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_ingredients()
'''

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script_content)

    print(f"Generated import script: {output_file}")
    return output_file

def main():
    """Main processing function"""
    print("=" * 60)
    print("食材数据处理脚本")
    print("=" * 60)
    print()

    # Step 1: Copy images
    print("\n[Step 1] Copying images...")
    copy_images()

    # Step 2: Process CSV
    print("\n[Step 2] Processing CSV data...")
    data = process_csv()

    # Step 3: Generate import script
    print("\n[Step 3] Generating import script...")
    generate_import_script(data)

    # Step 4: Summary
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)
    print(f"""
Summary:
- Processed {len(data)} ingredients
- Images copied to: {STATIC_DIR}
- Import script generated at: {BASE_DIR}/scripts/import_ingredients_to_db.py

Next steps:
1. Run: cd backend && python scripts/import_ingredients_to_db.py
2. Test the API: GET /api/v1/ingredients
3. Check frontend display
    """)

if __name__ == "__main__":
    main()
