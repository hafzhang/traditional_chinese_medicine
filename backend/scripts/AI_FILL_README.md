# AI填充食谱数据 - 使用说明

## 概述

使用智谱AI GLM-4.7模型填充 `dishes_list_ai_filled.xlsx` 中 `method="simulated"` 的食谱数据。

## 已创建的文件

| 文件 | 说明 |
|------|------|
| `backend/scripts/ai_fill_config.py` | 配置文件（API密钥、体质代码、功效标签等） |
| `backend/scripts/fill_recipes_with_ai.py` | 主脚本（AI填充逻辑） |

## 功能特性

- **批量处理**: 每批处理20条记录（可配置）
- **断点续传**: 支持中断后继续处理
- **自动备份**: 处理前自动备份原文件
- **进度跟踪**: 实时显示处理进度和预计剩余时间
- **错误重试**: API失败自动重试3次
- **测试模式**: 支持小批量测试

## 使用方法

### 1. 测试模式（推荐先运行）

仅处理前5条记录，验证AI响应质量：

```bash
cd backend
python scripts/fill_recipes_with_ai.py --test 5
```

### 2. 模拟运行

不修改文件，仅测试API连接：

```bash
python scripts/fill_recipes_with_ai.py --dry-run --test 5
```

### 3. 正式运行（全部数据）

处理所有 `method="simulated"` 的记录：

```bash
python scripts/fill_recipes_with_ai.py
```

### 4. 自定义批处理大小

```bash
python scripts/fill_recipes_with_ai.py --batch-size 50
```

### 5. 重新开始（清除进度）

```bash
python scripts/fill_recipes_with_ai.py --clear-progress
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--file`, `-f` | Excel文件路径 | `../source_data/dishes_list_ai_filled.xlsx` |
| `--batch-size`, `-b` | 批处理大小 | 20 |
| `--no-resume` | 不从断点续传 | False |
| `--dry-run` | 模拟运行，不修改文件 | False |
| `--clear-progress` | 清除进度文件 | False |
| `--test`, `-t` N | 测试模式，仅处理前N条 | None |

## 填充的字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `suitable_constitutions` | 适合体质 | `["qi_deficiency", "peace"]` |
| `avoid_constitutions` | 禁忌体质 | `["phlegm_damp"]` |
| `efficacy_tags` | 功效标签 | `["健脾", "养胃"]` |
| `solar_terms` | 节气 | `["立春", "春季"]` |
| `confidence` | 置信度 | `85` |
| `method` | 从"simulated"改为"AI" | `"AI"` |

## 进度文件

处理进度保存在：`backend/scripts/ai_fill_progress.json`

如需重新开始，使用 `--clear-progress` 参数或手动删除此文件。

## 备份文件

处理前会自动备份原文件到：`dishes_list_ai_filled.xlsx.backup`

## 验证步骤

### 1. 格式验证

脚本会自动验证：
- 体质代码是否有效
- 功效标签是否在预定义列表中
- 节气是否有效
- 置信度是否在0-100范围内

### 2. 内容验证

随机抽查10-20行，检查AI填充内容是否合理。

### 3. 导入测试

```bash
cd backend
python scripts/import_recipes.py --dry-run --limit 100
```

## 注意事项

1. **API成本**: 5000+行调用智谱API，会产生相应费用
2. **处理时间**: 预计需要1-3小时（取决于API响应速度）
3. **网络连接**: 需要稳定的网络连接访问智谱API
4. **数据备份**: 脚本会自动备份原文件

## 故障排除

### API连接失败

检查：
1. 网络连接是否正常
2. API密钥是否正确（`ai_fill_config.py` 中的 `ZHIPU_API_KEY`）
3. API URL是否可访问

### JSON解析失败

AI返回的JSON格式可能不规范，脚本会：
1. 尝试去除代码块标记（```json ... ```）
2. 记录失败的原始响应用于调试

### 进度文件损坏

使用 `--clear-progress` 清除进度文件重新开始。

## 输出示例

```
============================================================
批处理: 1-20 / 5065
============================================================

[1] 处理: 红枣山药粥...
[OK] 成功: 红枣山药粥... (置信度: 85%)

[2] 处理: 枸杞银耳汤...
[OK] 成功: 枸杞银耳汤... (置信度: 88%)

...

============================================================
处理摘要
============================================================
总数:       5065
成功:       5060
跳过:       0
失败:       5
耗时:       7200.00 秒
平均耗时:   1.42 秒/条
```
