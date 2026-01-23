# 穴位功能开发方案
# Acupoint Feature Development Plan

## 项目概述 / Project Overview

基于《穴位(312).xlsx》和 `272_pages_acupunture_point_chart` 图片资源，开发完整的穴位查找、展示和搜索功能。

**资源清单：**
- Excel数据文件：`穴位（312）.xlsx` - 包含312个穴位的详细信息
- 图片资源：`272_pages_acupunture_point_chart/`
  - **55个穴位图片**（56_new_acupunture_point/）
  - **14个经络GIF动画图**（GIF_meridian_collateral_diagram/）

---

## 数据结构分析 / Data Structure Analysis

### Excel文件字段 (14列)

| 序号 | 字段 | 描述 | 示例 |
|------|------|------|------|
| 1 | 穴位名称 | 标准名称 | 合谷穴 |
| 2 | 穴位位置其他 | 附加位置说明 | - |
| 3 | 穴位代码 | 标准代码 | LI4 |
| 4 | 穴位所属经络 | 所属经络 | 手阳明大肠经 |
| 5 | 穴位是否特定 | 特定/通用标志 | 特定 |
| 6 | 穴位主治功能概述 | 功能概述 | 通经活络、镇痛 |
| 7 | 穴位别名 | 别名列表 | - |
| 8 | 穴位定位与取穴方法 | 取穴方法 | 拇指食指合拢 |
| 9 | 穴位方法-艾灸 | 艾灸方法 | 艾灸3-7壮 |
| 10 | 穴位方法-按摩 | 按摩方法 | 指压按揉 |
| 11 | 穴位定位解剖结构 | 解剖位置 | 肌肉间隙 |
| 12 | 穴位主要治疗 | 主治病症 | 头痛、牙痛 |
| 13 | 穴位定位 | 标准定位位置 | 手背 |
| 14 | 其他信息 | 补充说明 | - |

---

## 当前系统状态 / Current System Status

### 已完成

| 功能 | 状态 | 说明 |
|------|------|------|
| 数据库模型 | ✅ 完成 | Acupoint模型包含所有必需字段 |
| 361标准穴位 | ✅ 完成 | 基于国家标准 |
| API接口 | ✅ 完成 | 7个RESTful端点 |
| 前端页面 | ✅ 完成 | 列表页和详情页 |
| 图片映射 | 🔄 更新中 | 55个图片文件（覆盖200+穴位） |
| 经络GIF | ✅ 完成 | 14个经络动画 |

### 待完成

| 功能 | 优先级 | 说明 |
|------|--------|------|
| Excel数据导入 | 🔴 高 | 导入312个穴位详细信息 |
| 图片完整映射 | 🔴 高 | 将55个图片映射到对应穴位 |
| 经络图展示 | 🟡 中 | 在详情页展示经络GIF |
| 搜索功能 | 🟡 中 | 实现关键词搜索 |
| 详情页增强 | 🟢 低 | 添加更多展示内容 |

---

## 图片资源完整清单 / Complete Image Resource List

### 单个穴位图片 (35个)

| 穴位名称 | 图片文件 | 经络 |
|---------|---------|------|
| 承山 | 承山.jpg | 足太阳膀胱经 |
| 尺泽 | 尺泽.jpg | 手太阴肺经 |
| 大陵 | 大陵.jpg | 手厥阴心包经 |
| 合谷 | 合谷.jpg | 手阳明大肠经 |
| 肩髎 | 肩髎.jpg | 手少阳三焦经 |
| 肩髃 | 肩髃.jpg | 手阳明大肠经 |
| 肩贞 | 肩贞.jpg | 手太阳小肠经 |
| 解溪 | 解溪.jpg | 足阳明胃经 |
| 孔最 | 孔最.jpg | 手太阴肺经 |
| 昆仑 | 昆仑.jpg | 足太阳膀胱经 |
| 劳宫 | 劳宫.jpg | 手厥阴心包经 |
| 列缺 | 列缺.jpg | 手太阴肺经 |
| 命门 | 命门.jpg | 督脉 |
| 内关 | 内关.jpg | 手厥阴心包经 |
| 内庭 | 内庭.jpg | 足阳明胃经 |
| 期门 | 期门.jpg | 足厥阴肝经 |
| 丘墟 | 丘墟.jpg | 足少阳胆经 |
| 曲池 | 曲池.jpg | 手阳明大肠经 |
| 曲泽 | 曲泽.jpg | 手厥阴心包经 |
| 三阴交 | 三阴交.jpg | 足太阴脾经 |
| 膻中 | 膻中.jpg | 任脉 |
| 神门 | 神门.jpg | 手少阴心经 |
| 肾俞 | 肾俞.jpg | 足太阳膀胱经 |
| 手三里 | 手三里.jpg | 手阳明大肠经 |
| 太溪 | 太溪.jpg | 足少阴肾经 |
| 外关 | 外关.jpg | 手少阳三焦经 |
| 腕骨 | 腕骨.jpg | 手太阳小肠经 |
| 委中 | 委中.jpg | 足太阳膀胱经 |
| 膝眼 | 膝眼.jpg | 经外奇穴 |
| 行间 | 行间.jpg | 足厥阴肝经 |
| 悬钟 | 悬钟.jpg | 足少阳胆经 |
| 血海 | 血海.jpg | 足太阴脾经 |
| 阳池 | 阳池.jpg | 手少阳三焦经 |
| 阳谷 | 阳谷.jpg | 手太阳小肠经 |
| 阳溪 | 阳溪.jpg | 手阳明大肠经 |
| 养老 | 养老.jpg | 手太阳小肠经 |
| 鱼际 | 鱼际.jpg | 手太阴肺经 |
| 涌泉 | 涌泉.jpg | 足少阴肾经 |
| 足三里 | 足三里.jpg | 足阳明胃经 |
| 巨阙 | 巨阙.jpg | 任脉 |
| 阴陵泉 | 阴陵泉.jpg | 足太阴脾经 |

### 组合图片 (20个，覆盖多个穴位)

| 图片文件 | 包含穴位 | 数量 |
|---------|---------|------|
| 大椎 膈俞 至阳.jpg | 大椎、膈俞、至阳 | 3 |
| 大椎 肩井.jpg | 大椎、肩井 | 2 |
| 大椎至腰关 风门至大肠俞.jpg | 大椎至腰关、风门至大肠俞 | 多个 |
| 犊鼻 足三里 上巨 丰隆 条口 下巨.jpg | 犊鼻、足三里、上巨虚、丰隆、条口、下巨虚 | 6 |
| 解溪 太冲.jpg | 解溪、太冲 | 2 |
| 膻中 中庭 上中下脘 神阙.jpg | 膻中、中庭、上脘、中脘、下脘、神阙 | 6 |
| 身柱 风门 肺俞.jpg | 身柱、风门、肺俞 | 3 |
| 神阙 气海 关元 中极.jpg | 神阙、气海、关元、中极 | 4 |
| 天枢 神阙.jpg | 天枢、神阙 | 2 |
| 腰阳关 腰眼 大肠俞.jpg | 腰阳关、腰眼、大肠俞 | 3 |
| 志室 身柱.jpg | 志室、身柱 | 2 |
| 志室 肾俞 命门.jpg | 志室、肾俞、命门 | 3 |
| 中庭 上中下脘 神阙.jpg | 中庭、上脘、中脘、下脘、神阙 | 5 |

**组合图片覆盖穴位总数：约200+个**

### 经络GIF动画图 (14个)

| 经络名称 | GIF文件 | 状态 |
|---------|---------|------|
| 手太阴肺经 | 手太阴肺经.gif | ✅ |
| 手阳明大肠经 | 手阳明大肠经.gif | ✅ |
| 足阳明胃经 | 足阳明胃经.gif | ✅ |
| 足太阴脾经 | 足太阴脾经.gif | ✅ |
| 手少阴心经 | 手少阴心经.gif | ✅ |
| 手太阳小肠经 | 手太阳小肠经.gif | ✅ |
| 足太阳膀胱经 | 足太阳膀胱经.gif | ✅ |
| 足少阴肾经 | 足少阴肾经.gif | ✅ |
| 手厥阴心包经 | 手厥阴心包经.gif | ✅ |
| 手少阳三焦经 | 手少阳三焦经.gif | ✅ |
| 足少阳胆经 | 足少阳胆经.gif | ✅ |
| 足厥阴肝经 | 足厥阴肝经.gif | ✅ |
| 督脉 | 督脉.gif | ✅ |
| 任脉 | 任脉.gif | ✅ |

---

## Excel数据导入方案 / Excel Import Plan

### 导入脚本结构

```python
# backend/scripts/import_acupoints_from_excel.py

from openpyxl import load_workbook
from api.database import SessionLocal
from api.models import Acupoint
import uuid

def import_from_excel(file_path: str):
    """从Excel文件导入312个穴位数据"""
    wb = load_workbook(file_path, data_only=True)
    sheet = wb.active

    db = SessionLocal()
    count = 0

    for row in range(2, sheet.max_row + 1):
        # 读取Excel数据
        name = sheet.cell(row, 1).value           # 穴位名称
        code = sheet.cell(row, 3).value           # 穴位代码
        meridian = sheet.cell(row, 4).value       # 所属经络
        location = sheet.cell(row, 8).value       # 取穴方法
        massage = sheet.cell(row, 10).value       # 按摩方法
        indications = sheet.cell(row, 14).value   # 主要治疗

        # 检查是否已存在
        existing = db.query(Acupoint).filter(Acupoint.code == code).first()
        if existing:
            # 更新现有记录
            existing.location = location
            existing.massage_method = massage
            existing.indications = parse_indications(indications)
        else:
            # 创建新记录
            acupoint = Acupoint(
                id=str(uuid.uuid4()),
                name=name,
                code=code,
                meridian=meridian,
                location=location,
                simple_location=extract_simple_location(location),
                massage_method=massage,
                indications=parse_indications(indications),
                image_url=get_image_url(code)
            )
            db.add(acupoint)

        count += 1

    db.commit()
    print(f"Imported {count} acupoints")
    return count
```

---

## 前端展示设计 / Frontend Design

### 1. 穴位列表页

```
┌─────────────────────────────────────┐
│     [经脉] [部位]                   │  Tabs
├──────────┬──────────────────────────┤
│          │                          │
│ 手太阴   │  ┌─────┐  ┌─────┐       │
│ 手阳明   │  │图片 │  │图片 │       │
│ 足阳明   │  └─────┘  └─────┘       │
│ ...      │  合谷   足三里           │
├──────────┴──────────────────────────┤
│         穴位卡片网格 (2列)          │
└─────────────────────────────────────┘
```

### 2. 穴位详情页 - 增强版

```
┌─────────────────────────────────────┐
│         穴位大图 (可预览/放大)      │
│  [合谷穴] 手阳明大肠经             │
├─────────────────────────────────────┤
│  [3D图解] [AR取穴] [按摩计时]       │
├─────────────────────────────────────┤
│  📍 取穴定位                        │
│     简易取穴：拇指食指合拢...       │
├─────────────────────────────────────┤
│  📊 经络解剖图                      │  ← 新增
│     [手阳明大肠经.gif动画图]        │
├─────────────────────────────────────┤
│  ✨ 功效作用                        │
│     [通经活络] [镇痛解表]          │
├─────────────────────────────────────┤
│  🏥 主治病症                        │
│     [头痛] [牙痛] [发热]           │
├─────────────────────────────────────┤
│  🙌 按摩方法                        │
│     手法：指压按揉                  │
│     💡建议每次3-5分钟               │
├─────────────────────────────────────┤
│  🎯 体质调理                        │
│     [气虚质] [血瘀质]               │
└─────────────────────────────────────┘
```

### 3. 经络图展示组件

```vue
<template>
  <view class="meridian-diagram">
    <text class="section-title">经络走向</text>
    <image
      :src="meridianGifUrl"
      class="meridian-gif"
      mode="aspectFit"
    />
    <text class="meridian-name">{{ acupoint.meridian }}</text>
  </view>
</template>
```

---

## 图片加载优化 / Image Loading

### 懒加载实现

```vue
<image
  :src="acupoint.image_url"
  loading="lazy"
  @error="handleError"
  mode="aspectFill"
/>
```

### 经络GIF自动播放

```vue
<image
  :src="anatomicalImageUrl"
  class="meridian-gif"
  mode="aspectFit"
/>
<!-- GIF在支持的平台会自动播放 -->
```

---

## 数据库图片URL更新 / Database Image URL Update

### 图片文件命名规则

**单个穴位：** 使用标准拼音或文件原名
```
合谷.jpg → hegu.jpg 或保持原名
足三里.jpg → zusanli.jpg 或保持原名
```

**组合图片：** 使用主穴位+_composite
```
大椎 膈俞 至阳.jpg → GV14_composite.jpg
```

### 批量更新脚本

```python
# backend/scripts/update_all_acupoint_images.py

def update_all_image_urls():
    """更新所有穴位图片URL"""
    import os
    import shutil
    from pathlib import Path

    source_dir = Path("272_pages_acupunture_point_chart/56_new_acupunture_point")
    target_dir = Path("backend/static/acupoints")

    # 复制所有图片
    for img_file in source_dir.glob("*.jpg"):
        shutil.copy2(img_file, target_dir / img_file.name)
        print(f"Copied: {img_file.name}")
```

---

## 开发任务清单 / Development Checklist

### Phase 1: 图片资源完整导入 (🔴 高优先级)

- [ ] 复制所有55个图片文件到static目录
- [ ] 创建图片映射表（单个35个 + 组合20个）
- [ ] 更新数据库image_url字段
- [ ] 验证所有图片可访问

### Phase 2: 经络GIF展示 (🟡 中优先级)

- [ ] 确认14个GIF文件在正确位置
- [ ] 在详情页添加经络图展示组件
- [ ] 测试GIF动画播放效果
- [ ] 添加GIF加载错误处理

### Phase 3: Excel数据导入 (🟡 中优先级)

- [ ] 创建Excel导入脚本
- [ ] 解析312个穴位数据
- [ ] 导入数据库
- [ ] 验证数据完整性

### Phase 4: 前端优化 (🟢 低优先级)

- [ ] 图片预览功能
- [ ] 图片放大查看
- [ ] 相关穴位推荐
- [ ] 搜索功能增强

---

## API端点 / API Endpoints

### 已实现端点

| 端点 | 方法 | 功能 | 状态 |
|------|------|------|------|
| `/api/v1/acupoints` | GET | 获取穴位列表 | ✅ |
| `/api/v1/acupoints/{id}` | GET | 获取穴位详情 | ✅ |
| `/api/v1/acupoints/meridians/list` | GET | 获取经络列表 | ✅ |
| `/api/v1/acupoints/body-parts/list` | GET | 获取部位列表 | ✅ |
| `/api/v1/acupoints/recommend/{constitution}` | GET | 体质推荐 | ✅ |
| `/api/v1/acupoints/symptom/{symptom}` | GET | 症状搜索 | ✅ |

### 静态资源端点

| 资源 | 端点 | 状态 |
|------|------|------|
| 穴位图片 | `/static/acupoints/{filename}.jpg` | ✅ |
| 经络GIF | `/static/meridians/{经络名}.gif` | ✅ |

---

## 文件结构 / File Structure

```
backend/
├── api/
│   ├── data/
│   │   ├── acupoints_comprehensive.py      # 361标准穴位
│   │   ├── acupoint_image_mapping.py       # 图片映射
│   │   └── excel_acupoints.py              # Excel数据 (新增)
│   ├── models/__init__.py                  # 数据库模型
│   ├── services/acupoint_service.py        # 业务逻辑
│   └── routers/acupoints.py                # API路由
│
├── scripts/
│   ├── import_acupoints_from_excel.py      # Excel导入 (新增)
│   ├── copy_all_acupoint_images.py         # 批量复制图片 (新增)
│   └── update_acupoint_images.py           # URL更新
│
└── static/
    ├── acupoints/                          # 55个图片文件
    │   ├── 合谷.jpg
    │   ├── 足三里.jpg
    │   ├── 大椎 膈俞 至阳.jpg
    │   └── ...
    └── meridians/                          # 14个GIF文件
        ├── 手太阴肺经.gif
        ├── 手阳明大肠经.gif
        └── ...

frontend/src/
├── pages/acupoints/
│   ├── list.vue                            # 列表页 ✅
│   └── detail.vue                          # 详情页 ✅
└── api/acupoints.js                        # API客户端

docs/
└── point_development.md                    # 本文档
```

---

## 数据统计 / Statistics

| 项目 | 当前 | 目标 | 完成度 |
|------|------|------|--------|
| 穴位总数 | 363 | 361+ | 100% |
| 单个穴位图片 | 35 | 55 | 64% |
| 组合图片 | 0 | 20 | 0% |
| 经络GIF | 14 | 14 | 100% |
| Excel数据 | 0 | 312 | 0% |

**图片覆盖穴位数：约200+（通过组合图片）**

---

## 下一步行动 / Next Actions

### 立即执行

1. **复制所有图片到static目录**
   ```bash
   cp 272_pages_acupunture_point_chart/56_new_acupunture_point/*.jpg backend/static/acupoints/
   cp 272_pages_acupunture_point_chart/GIF_meridian_collateral_diagram/*.gif backend/static/meridians/
   ```

2. **创建完整图片映射表**
   - 35个单个穴位图片
   - 20个组合图片（包含穴位拆分）

3. **更新数据库URL**

### 本周完成

1. 在详情页展示经络GIF
2. 实现图片预览功能
3. 导入Excel数据

---

## 参考资料 / References

- 《经穴名称与定位》(GB/T 12346-2006)
- 王琦院士9种体质标准量表
- 国家中医药管理局标准
