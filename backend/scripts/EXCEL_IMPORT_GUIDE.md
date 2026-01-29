# 菜谱导入增强版 Excel 模板说明

## Excel 文件结构

### 文件位置
`source_data/ingredients_list_enhanced.xlsx`

### 工作表说明

#### Sheet1: 菜谱主数据

保持原有列，添加以下新列：

| 新增列名 | 说明 | 必填 | 示例值 | 默认值 |
|---------|------|------|--------|--------|
| meal_type | 餐次类型 | 否 | breakfast | 根据菜名推测 |
| difficulty | 难度等级 | 否 | easy | 根据时间推测 |
| suitable_constitutions | 适合体质 | 否 | 气虚质,平和质 | [] |
| avoid_constitutions | 禁忌体质 | 否 | 痰湿质 | [] |
| efficacy_tags | 功效标签 | 否 | 健脾,养胃 | [] |
| solar_terms | 节气标签 | 否 | 春季,立春 | [] |
| servings | 份量 | 否 | 2 | 2 |
| cover_image | 封面图片URL | 否 | https://... | NULL |

### 原有列保持不变：

| 列名 | 说明 | 示例 |
|------|------|------|
| cid | 分类ID | 1,2,3 |
| zid | 子分类ID | 10,20,30 |
| title | 菜谱名称 | 山药小米粥 |
| desc | 菜谱描述 | 健脾养胃... |
| costtime | 烹饪时间 | 10-30分钟 |
| tip | 小贴士 | 适合... |
| steptext | 制作步骤 | 1.步骤一\n2.步骤二 |
| QuantityIngredients | 食材用量 | 山药50g、枸杞20g |

---

## 字段值参考

### meal_type (餐次类型)

| 中文值 | 代码值 |
|--------|--------|
| 早餐 | breakfast |
| 午餐 | lunch |
| 晚餐 | dinner |
| 小食 | snack |
| 汤品 | soup |

### difficulty (难度等级)

| 中文值 | 代码值 | 预计时间 |
|--------|--------|----------|
| 简单 | easy | < 30分钟 |
| 中等 | medium | 30-60分钟 |
| 困难 | hard | > 60分钟 |

### 体质类型

| 中文值 | 代码值 |
|--------|--------|
| 平和质 | peace |
| 气虚质 | qi_deficiency |
| 阳虚质 | yang_deficiency |
| 阴虚质 | yin_deficiency |
| 痰湿质 | phlegm_damp |
| 湿热质 | damp_heat |
| 血瘀质 | blood_stasis |
| 气郁质 | qi_depression |
| 特禀质 | special |

### 功效标签

健脾、养胃、补气、补血、养阴、温阳、化痰、祛湿、活血、疏肝、安神、润肺、补肾、清热、解毒、止痛

### 节气标签

**四季**: 春季、夏季、秋季、冬季

**24节气**: 立春、雨水、惊蛰、春分、清明、谷雨、立夏、小满、芒种、夏至、小暑、大暑、立秋、处暑、白露、秋分、寒露、霜降、立冬、小雪、大雪、冬至、小寒、大寒

---

## 数据填写示例

### 示例 1: 山药小米粥

| 列名 | 填写内容 |
|------|----------|
| title | 山药小米粥 |
| desc | 健脾养胃的养生粥品，适合脾胃虚弱、消化不良的人群 |
| costtime | 10-30分钟 |
| meal_type | breakfast |
| difficulty | easy |
| suitable_constitutions | 气虚质,平和质 |
| avoid_constitutions | 痰湿质 |
| efficacy_tags | 健脾,养胃 |
| solar_terms | 春季,秋季 |
| servings | 2 |
| steptext | 1.将山药去皮切块，小米洗净备用#\n2.锅中加水烧开，放入小米煮15分钟#\n3.加入山药继续煮10分钟即可 |
| QuantityIngredients | 山药100g、小米50g、红枣3颗、枸杞适量 |

### 示例 2: 枸杞炖鸡汤

| 列名 | 填写内容 |
|------|----------|
| title | 枸杞炖鸡汤 |
| desc | 补血养气，适合气血两虚的人群 |
| costtime | 1-2小时 |
| meal_type | dinner |
| difficulty | medium |
| suitable_constitutions | 气虚质,血瘀质 |
| avoid_constitutions | 湿热质 |
| efficacy_tags | 补气,补血,养阴 |
| solar_terms | 冬季,立冬 |
| servings | 4 |
| steptext | 1.将鸡肉切块焯水#\n2.红枣、枸杞洗净备用#\n3.锅中加水，放入鸡肉、姜片炖煮1小时#\n4.加入红枣、枸杞继续炖30分钟#\n5.调味即可 |
| QuantityIngredients | 鸡肉500g、枸杞20g、红枣10颗、姜片5片 |

---

## 智能填充规则

### meal_type (餐次类型)
如果未填写，系统将根据菜名关键词自动推测：

| 关键词 | 推测类型 |
|--------|----------|
| 粥、汤、豆浆、牛奶、早餐、燕麦 | breakfast |
| 面、粉、饭、包、饺 | lunch |
| 甜品、糕点、小食 | snack |
| 汤、羹 | soup |
| 其他 | dinner |

### difficulty (难度等级)
如果未填写，系统将根据烹饪时间自动推测：

| 烹饪时间 | 推测难度 |
|----------|----------|
| ≤ 30分钟 | easy |
| 31-60分钟 | medium |
| > 60分钟 | hard |

### suitable_constitutions (适合体质)
系统会根据以下关键词自动匹配：

| 菜名关键词 | 推测体质 |
|-----------|----------|
| 健脾、养胃 | 气虚质、平和质 |
| 补血、养血 | 血瘀质、气虚质 |
| 清热、解毒 | 湿热质 |
| 祛湿、化痰 | 痰湿质 |
| 温阳、补肾 | 阳虚质 |
| 滋阴、养阴 | 阴虚质 |

---

## 导入命令

### 模拟运行（不实际导入）
```bash
cd backend
python scripts/import_recipes.py --file source_data/ingredients_list.xlsx --dry-run
```

### 正式导入
```bash
cd backend
python scripts/import_recipes.py --file source_data/ingredients_list.xlsx
```

### 测试导入（限制数量）
```bash
cd backend
python scripts/import_recipes.py --file source_data/ingredients_list.xlsx --limit 10 --dry-run
```

---

## 数据验证规则

1. **必填字段**: title (菜谱名称)
2. **枚举值验证**: meal_type, difficulty 必须是预定义的值
3. **体质验证**: 体质名称必须是9种体质之一
4. **食材验证**: 食材必须存在于 ingredients 表中
5. **编码处理**: 自动处理中文输入，转换为代码值

---

## 错误处理

导入过程中的错误会被记录：

| 错误类型 | 处理方式 |
|----------|----------|
| 菜谱已存在 | 跳过，记录到 skipped |
| 食材不存在 | 跳过该食材，继续导入 |
| 格式错误 | 记录错误，跳过该菜谱 |
| 数据库错误 | 回滚事务，记录错误 |

---

## 进度显示

导入过程中会显示：
- 总数 / 成功 / 跳过 / 失败
- 每10条或每100条显示一次进度
- 前5条失败详情
- 最终统计摘要
