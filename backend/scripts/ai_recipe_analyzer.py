#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI驱动的食谱元数据填充脚本

使用AI API分析食谱，基于中医理论填充元数据字段：
- difficulty: 难度 (简单/中等/较难/困难)
- suitable_constitutions: 适合体质 (9种体质的JSON数组)
- avoid_constitutions: 禁忌体质 (JSON数组)
- efficacy_tags: 功效标签 (JSON数组)
- solar_terms: 节气标签 (24节气的JSON数组)
"""

import pandas as pd
import json
import re
import os
import sys
import time
from datetime import datetime

# 添加scripts目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 尝试导入 anthropic (如果可用)
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic package not installed. Install with: pip install anthropic")

# 9种体质常量
CONSTITUTIONS = {
    "peace": "平和质",
    "qi_deficiency": "气虚质",
    "yang_deficiency": "阳虚质",
    "yin_deficiency": "阴虚质",
    "phlegm_damp": "痰湿质",
    "damp_heat": "湿热质",
    "blood_stasis": "血瘀质",
    "qi_depression": "气郁质",
    "special": "特禀质"
}

# 24节气
SOLAR_TERMS = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
]

# 功效标签
EFFICACY_TAGS = [
    "补气", "补血", "滋阴", "助阳", "健脾", "养胃",
    "润肺", "止咳", "祛湿", "清热", "解表", "安神",
    "消食", "理气", "活血", "美容", "减肥", "增强免疫",
    "补肾", "疏肝", "养心", "润肠", "明目", "强筋骨"
]

# AI分析提示词
ANALYSIS_PROMPT = """你是一位经验丰富的中医食疗专家。请分析以下食谱信息，根据中医理论填写元数据。

食谱信息：
- 菜名：{title}
- 食材：{ingredients}
- 描述：{description}
- 烹饪时间：{cooking_time}
- 制作步骤：{steps}
- 分类：{categories}

请以JSON格式返回以下字段：

{{
  "difficulty": "难度等级（简单/中等/较难/困难），根据烹饪时间、步骤复杂度、处理技巧综合判断",
  "suitable_constitutions": ["适合的体质代码", "从以下选择: peace, qi_deficiency, yang_deficiency, yin_deficiency, phlegm_damp, damp_heat, blood_stasis, qi_depression, special"],
  "avoid_constitutions": ["禁忌的体质代码", "同上列表"],
  "efficacy_tags": ["功效标签", "从以下选择: 补气,补血,滋阴,助阳,健脾,养胃,润肺,止咳,祛湿,清热,解表,安神,消食,理气,活血,美容,减肥,增强免疫,补肾,疏肝,养心,润肠,明目,强筋骨"],
  "solar_terms": ["适合的节气", "从24节气中选择"],
  "reasoning": "简要说明分析依据"
}}

判断依据：
1. 体质：根据食材的性味归经（寒热温凉）、功效综合判断
2. 功效：根据主要食材的功效叠加
3. 节气：根据食材的季节性判断
4. 难度：综合考虑烹饪时间、步骤数、处理技巧

只返回JSON，不要其他内容。
"""


class AIRecipeAnalyzer:
    """AI驱动的食谱分析器"""

    def __init__(self, api_key=None, base_url=None):
        """
        初始化分析器

        Args:
            api_key: Anthropic API密钥。如果为None，则使用模拟模式
            base_url: API基础URL，用于自定义API端点（如智谱AI）
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.base_url = base_url or os.environ.get("ANTHROPIC_BASE_URL")
        self.use_ai = ANTHROPIC_AVAILABLE and self.api_key

        if self.use_ai:
            if self.base_url:
                self.client = anthropic.Anthropic(api_key=self.api_key, base_url=self.base_url)
                print(f"[OK] 使用AI模式分析食谱 (自定义API: {self.base_url})")
            else:
                self.client = anthropic.Anthropic(api_key=self.api_key)
                print("[OK] 使用AI模式分析食谱")
        else:
            print("[WARNING] 使用模拟模式分析食谱（数据质量较低）")
            print("  要启用AI模式，请设置ANTHROPIC_API_KEY环境变量")

    def analyze_recipe(self, row):
        """
        分析单条食谱

        Args:
            row: DataFrame的行数据

        Returns:
            dict: 分析结果
        """
        # 提取食谱信息
        title = str(row.get('title', ''))
        ingredients = str(row.get('QuantityIngredients', ''))[:500]  # 限制长度
        description = str(row.get('desc', ''))[:200]
        cooking_time = str(row.get('costtime', ''))
        steps = str(row.get('steptext', ''))[:500]
        categories = str(row.get('cid', ''))

        if self.use_ai:
            return self._analyze_with_ai(title, ingredients, description, cooking_time, steps, categories)
        else:
            return self._analyze_simulated(title, ingredients, description, cooking_time, steps, categories)

    def _analyze_with_ai(self, title, ingredients, description, cooking_time, steps, categories):
        """使用AI API分析"""
        try:
            prompt = ANALYSIS_PROMPT.format(
                title=title,
                ingredients=ingredients,
                description=description,
                cooking_time=cooking_time,
                steps=steps,
                categories=categories
            )

            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text

            # 提取JSON
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                result = json.loads(json_match.group())
                result['confidence'] = 90  # AI分析置信度高
                result['method'] = 'AI'
                return result
            else:
                return self._analyze_simulated(title, ingredients, description, cooking_time, steps, categories)

        except Exception as e:
            print(f"  AI分析失败: {e}，使用模拟模式")
            return self._analyze_simulated(title, ingredients, description, cooking_time, steps, categories)

    def _analyze_simulated(self, title, ingredients, description, cooking_time, steps, categories):
        """模拟分析（当AI不可用时）"""
        # 基于规则的简化分析
        all_text = f"{title} {ingredients} {description} {categories}"

        # 难度判断
        difficulty = self._estimate_difficulty(cooking_time, steps)

        # 体质判断（简化版）
        suitable = self._estimate_constitutions(all_text)
        avoid = self._estimate_avoid(all_text)

        # 功效标签
        efficacy = self._estimate_efficacy(all_text)

        # 节气
        solar = self._estimate_solar_terms(all_text)

        return {
            "difficulty": difficulty,
            "suitable_constitutions": suitable,
            "avoid_constitutions": avoid,
            "efficacy_tags": efficacy,
            "solar_terms": solar,
            "reasoning": "基于规则的简化分析",
            "confidence": 50,
            "method": "simulated"
        }

    def _estimate_difficulty(self, cooking_time, steps):
        """估算难度"""
        # 解析时间
        numbers = re.findall(r'\d+', str(cooking_time))
        if numbers:
            max_time = max(int(n) for n in numbers)
            if max_time > 90: return "困难"
            elif max_time > 40: return "较难"
            elif max_time > 15: return "中等"
        return "简单"

    def _estimate_constitutions(self, text):
        """估算适合体质（简化版）"""
        suitable = ["peace"]  # 默认平和质

        # 关键词映射
        keywords_map = {
            "qi_deficiency": ["补气", "气虚", "人参", "黄芪", "山药", "红枣"],
            "yang_deficiency": ["温补", "阳虚", "羊肉", "生姜", "辣椒"],
            "yin_deficiency": ["滋阴", "阴虚", "梨", "百合", "银耳"],
            "phlegm_damp": ["祛湿", "冬瓜", "薏米", "红豆"],
            "damp_heat": ["清热", "苦瓜", "黄瓜", "绿豆"],
            "blood_stasis": ["活血", "当归", "红花"],
            "qi_depression": ["理气", "陈皮", "玫瑰"],
        }

        for constitution, keywords in keywords_map.items():
            if any(kw in text for kw in keywords):
                if constitution not in suitable:
                    suitable.append(constitution)

        return suitable

    def _estimate_avoid(self, text):
        """估算禁忌体质"""
        avoid = []

        # 寒凉食物
        if any(kw in text for kw in ["绿豆", "苦瓜", "黄瓜", "西瓜", "梨"]):
            avoid.append("yang_deficiency")

        # 辛辣食物
        if any(kw in text for kw in ["辣椒", "胡椒", "羊肉"]):
            avoid.extend(["yin_deficiency", "damp_heat"])

        return list(set(avoid))

    def _estimate_efficacy(self, text):
        """估算功效"""
        efficacy_map = {
            "补气": ["补气", "人参", "黄芪"],
            "补血": ["补血", "当归", "红枣"],
            "滋阴": ["滋阴", "百合", "银耳", "梨"],
            "健脾": ["健脾", "山药"],
            "养胃": ["养胃", "小米"],
            "清热": ["清热", "绿豆", "苦瓜"],
            "祛湿": ["祛湿", "薏米", "红豆"],
            "活血": ["活血", "当归"],
        }

        tags = []
        for tag, keywords in efficacy_map.items():
            if any(kw in text for kw in keywords):
                tags.append(tag)

        return tags[:5] if tags else []

    def _estimate_solar_terms(self, text):
        """估算节气"""
        seasonal = {
            "春季": ["春笋", "韭菜", "菠菜"],
            "夏季": ["西瓜", "苦瓜", "黄瓜", "绿豆"],
            "秋季": ["梨", "百合", "银耳", "螃蟹"],
            "冬季": ["羊肉", "萝卜", "白菜"],
        }

        terms = []
        for season, ingredients in seasonal.items():
            if any(ing in text for ing in ingredients):
                if season == "春季":
                    terms.extend(["立春", "春分", "清明"])
                elif season == "夏季":
                    terms.extend(["立夏", "夏至", "大暑"])
                elif season == "秋季":
                    terms.extend(["立秋", "秋分", "霜降"])
                elif season == "冬季":
                    terms.extend(["立冬", "冬至", "大寒"])
                break

        return list(set(terms))[:3]


def process_recipes_in_range(df, start_idx, end_idx, analyzer, output_file):
    """
    处理指定范围的食谱

    Args:
        df: DataFrame
        start_idx: 起始索引
        end_idx: 结束索引
        analyzer: AIRecipeAnalyzer实例
        output_file: 输出文件路径
    """
    print(f"\n处理食谱 {start_idx+1}-{end_idx}，共 {end_idx-start_idx} 条")

    save_batch_size = 20  # 每20条保存一次
    results = []

    for idx in range(start_idx, end_idx):
        try:
            row = df.iloc[idx]

            # 显示进度
            if (idx - start_idx + 1) % 5 == 0 or idx == start_idx:
                print(f"  进度: {idx - start_idx + 1}/{end_idx - start_idx} (食谱 {idx+1})...", flush=True)

            # 分析食谱
            result = analyzer.analyze_recipe(row)

            results.append({
                'difficulty': result.get('difficulty', '简单'),
                'suitable_constitutions': json.dumps(result.get('suitable_constitutions', ["peace"]), ensure_ascii=False),
                'avoid_constitutions': json.dumps(result.get('avoid_constitutions', []), ensure_ascii=False),
                'efficacy_tags': json.dumps(result.get('efficacy_tags', []), ensure_ascii=False),
                'solar_terms': json.dumps(result.get('solar_terms', []), ensure_ascii=False),
                'confidence': result.get('confidence', 50),
                'method': result.get('method', 'simulated')
            })

            # 定期保存
            if len(results) >= save_batch_size or idx == end_idx - 1:
                # 更新DataFrame
                for i, result in enumerate(results):
                    df_idx = start_idx + idx - start_idx - len(results) + 1 + i
                    df.at[df_idx, 'difficulty'] = result['difficulty']
                    df.at[df_idx, 'suitable_constitutions'] = result['suitable_constitutions']
                    df.at[df_idx, 'avoid_constitutions'] = result['avoid_constitutions']
                    df.at[df_idx, 'efficacy_tags'] = result['efficacy_tags']
                    df.at[df_idx, 'solar_terms'] = result['solar_terms']
                    df.at[df_idx, 'confidence'] = result['confidence']
                    df.at[df_idx, 'method'] = result['method']

                # 保存
                df.to_excel(output_file, index=False, engine='openpyxl')
                results.clear()

            # 避免API限流（AI模式）
            if analyzer.use_ai:
                time.sleep(0.3)

        except Exception as e:
            print(f"  [ERROR] 食谱 {idx+1} 处理失败: {e}")
            # 使用模拟模式作为备选
            results.append({
                'difficulty': '简单',
                'suitable_constitutions': '["peace"]',
                'avoid_constitutions': '[]',
                'efficacy_tags': '[]',
                'solar_terms': '[]',
                'confidence': 30,
                'method': 'fallback'
            })

    # 最终统计
    ai_count = (df.iloc[start_idx:end_idx]['method'] == 'AI').sum()
    avg_conf = df.iloc[start_idx:end_idx]['confidence'].mean()
    print(f"\n  [OK] 完成! 平均置信度: {avg_conf:.1f}%, AI分析: {ai_count} 条")

    return results


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='AI驱动的食谱元数据填充')
    parser.add_argument('--start', type=int, default=0, help='起始索引')
    parser.add_argument('--end', type=int, default=None, help='结束索引')
    parser.add_argument('--api-key', type=str, default=None, help='Anthropic API密钥')
    parser.add_argument('--base-url', type=str, default=None, help='API基础URL（如智谱AI）')
    parser.add_argument('--batch-size', type=int, default=500, help='每批处理数量')

    args = parser.parse_args()

    # 文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    input_file = os.path.join(project_root, 'source_data', 'dishes_list.xlsx')
    output_file = os.path.join(project_root, 'source_data', 'dishes_list_ai_filled.xlsx')

    print("=" * 60)
    print("AI驱动的食谱元数据填充")
    print("=" * 60)

    # 读取数据
    print(f"\n读取文件: {input_file}")
    df = pd.read_excel(input_file)
    total = len(df)

    # 确定处理范围
    start_idx = args.start
    end_idx = args.end if args.end else min(start_idx + args.batch_size, total)

    print(f"总食谱数: {total}")
    print(f"处理范围: {start_idx+1} - {end_idx}")

    # 检查是否是增量处理
    if os.path.exists(output_file):
        print(f"发现已有文件: {output_file}")
        existing_df = pd.read_excel(output_file)
        if len(existing_df) == total and 'method' in existing_df.columns:
            # 检查哪些已处理
            processed = existing_df['method'].notna().sum()
            print(f"已处理: {processed} 条")
            if processed > 0:
                df = existing_df  # 使用已有数据继续

    # 初始化分析器
    analyzer = AIRecipeAnalyzer(api_key=args.api_key, base_url=args.base_url)

    # 添加新列（如果不存在）
    for col in ['difficulty', 'suitable_constitutions', 'avoid_constitutions',
                'efficacy_tags', 'solar_terms', 'confidence', 'method']:
        if col not in df.columns:
            df[col] = None

    # 处理
    start_time = time.time()
    process_recipes_in_range(df, start_idx, end_idx, analyzer, output_file)
    elapsed = time.time() - start_time

    print(f"\n完成! 用时: {elapsed:.1f}秒")
    print(f"输出文件: {output_file}")

    # 显示示例
    print("\n示例数据:")
    for i in range(start_idx, min(start_idx + 3, end_idx)):
        print(f"\n【{df['title'].iloc[i]}】")
        print(f"  难度: {df['difficulty'].iloc[i]}")
        print(f"  适合体质: {df['suitable_constitutions'].iloc[i]}")
        print(f"  置信度: {df['confidence'].iloc[i]}%")


if __name__ == '__main__':
    main()
