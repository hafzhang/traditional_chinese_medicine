#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量AI食谱分析器 - 一次API调用处理多条食谱
大幅提升处理速度
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

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# 批量分析提示词
BATCH_ANALYSIS_PROMPT = """你是一位经验丰富的中医食疗专家。请分析以下{count}条食谱，为每条食谱填写元数据。

食谱信息：
{recipes_info}

请以JSON数组格式返回分析结果，格式如下：
[
  {{
    "index": 0,
    "difficulty": "难度等级（简单/中等/较难/困难）",
    "suitable_constitutions": ["适合的体质代码"],
    "avoid_constitutions": ["禁忌的体质代码"],
    "efficacy_tags": ["功效标签"],
    "solar_terms": ["适合的节气"]
  }},
  ...
]

体质代码：peace, qi_deficiency, yang_deficiency, yin_deficiency, phlegm_damp, damp_heat, blood_stasis, qi_depression, special
功效标签：补气,补血,滋阴,助阳,健脾,养胃,润肺,止咳,祛湿,清热,解表,安神,消食,理气,活血,美容,减肥,增强免疫,补肾,疏肝,养心,润肠,明目,强筋骨
节气：立春,雨水,惊蛰,春分,清明,谷雨,立夏,小满,芒种,夏至,小暑,大暑,立秋,处暑,白露,秋分,寒露,霜降,立冬,小雪,大雪,冬至,小寒,大寒

只返回JSON数组，不要其他内容。
"""


class BatchAIRecipeAnalyzer:
    """批量AI食谱分析器"""

    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.base_url = base_url or os.environ.get("ANTHROPIC_BASE_URL")
        self.use_ai = ANTHROPIC_AVAILABLE and self.api_key

        if self.use_ai:
            if self.base_url:
                self.client = anthropic.Anthropic(api_key=self.api_key, base_url=self.base_url)
                print(f"[OK] 使用批量AI模式 (API: {self.base_url})")
            else:
                self.client = anthropic.Anthropic(api_key=self.api_key)
                print("[OK] 使用批量AI模式")
        else:
            print("[WARNING] API不可用")

    def analyze_batch(self, recipes_data):
        """
        批量分析多条食谱

        Args:
            recipes_data: 食谱数据列表，每个元素包含索引和食谱信息

        Returns:
            list: 分析结果列表
        """
        if not self.use_ai:
            return self._fallback_analysis(recipes_data)

        try:
            # 构建批量食谱信息
            recipes_info = ""
            for item in recipes_data:
                idx = item['index']
                recipe = item['recipe']
                recipes_info += f"""
食谱 {idx + 1}:
- 菜名：{recipe.get('title', '')}
- 食材：{str(recipe.get('QuantityIngredients', ''))[:300]}
- 描述：{str(recipe.get('desc', ''))[:150]}
- 烹饪时间：{recipe.get('costtime', '')}
"""

            prompt = BATCH_ANALYSIS_PROMPT.format(
                count=len(recipes_data),
                recipes_info=recipes_info
            )

            # 调用AI API
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text

            # 解析JSON结果
            json_match = re.search(r'\[[\s\S]*\]', result_text)
            if json_match:
                results = json.loads(json_match.group())

                # 添加置信度和方法
                for result in results:
                    result['confidence'] = 90
                    result['method'] = 'AI'

                return results
            else:
                print("  [WARNING] 无法解析AI响应，使用备选方案")
                return self._fallback_analysis(recipes_data)

        except Exception as e:
            print(f"  [ERROR] AI批量分析失败: {e}，使用备选方案")
            return self._fallback_analysis(recipes_data)

    def _fallback_analysis(self, recipes_data):
        """备选分析（基于规则）"""
        results = []
        for item in recipes_data:
            idx = item['index']
            recipe = item['recipe']

            # 简化的规则分析
            all_text = f"{recipe.get('title', '')} {str(recipe.get('QuantityIngredients', ''))} {str(recipe.get('desc', ''))}"

            # 难度
            costtime = str(recipe.get('costtime', ''))
            numbers = re.findall(r'\d+', costtime)
            if numbers:
                max_time = max(int(n) for n in numbers)
                if max_time > 90: difficulty = "困难"
                elif max_time > 40: difficulty = "较难"
                elif max_time > 15: difficulty = "中等"
                else: difficulty = "简单"
            else:
                difficulty = "简单"

            # 体质
            suitable = ["peace"]
            if any(kw in all_text for kw in ["补气", "气虚", "山药", "红枣"]):
                suitable.append("qi_deficiency")
            if any(kw in all_text for kw in ["温补", "羊肉", "生姜"]):
                suitable.append("yang_deficiency")
            if any(kw in all_text for kw in ["滋阴", "梨", "百合"]):
                suitable.append("yin_deficiency")

            results.append({
                "index": idx,
                "difficulty": difficulty,
                "suitable_constitutions": suitable,
                "avoid_constitutions": [],
                "efficacy_tags": [],
                "solar_terms": [],
                "confidence": 50,
                "method": "simulated"
            })

        return results


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='批量AI食谱分析')
    parser.add_argument('--start', type=int, default=0, help='起始索引')
    parser.add_argument('--end', type=int, default=None, help='结束索引')
    parser.add_argument('--batch-size', type=int, default=15, help='每批处理的食谱数')
    parser.add_argument('--api-key', type=str, default=None, help='API密钥')
    parser.add_argument('--base-url', type=str, default=None, help='API基础URL')

    args = parser.parse_args()

    # 文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    input_file = os.path.join(project_root, 'source_data', 'dishes_list.xlsx')
    output_file = os.path.join(project_root, 'source_data', 'dishes_list_ai_filled.xlsx')

    print("=" * 60)
    print("批量AI食谱分析器")
    print("=" * 60)

    # 读取数据
    print(f"\n读取文件: {input_file}")
    df = pd.read_excel(input_file)
    total = len(df)

    start_idx = args.start
    end_idx = args.end if args.end else min(start_idx + 500, total)

    print(f"总食谱数: {total}")
    print(f"处理范围: {start_idx+1} - {end_idx}")
    print(f"批量大小: {args.batch_size} 条/批")

    # 加载已有数据
    if os.path.exists(output_file):
        existing_df = pd.read_excel(output_file)
        if len(existing_df) == total:
            df = existing_df

    # 初始化分析器
    analyzer = BatchAIRecipeAnalyzer(api_key=args.api_key, base_url=args.base_url)

    # 添加列
    for col in ['difficulty', 'suitable_constitutions', 'avoid_constitutions',
                'efficacy_tags', 'solar_terms', 'confidence', 'method']:
        if col not in df.columns:
            df[col] = None

    # 批量处理
    total_batches = (end_idx - start_idx + args.batch_size - 1) // args.batch_size
    ai_count = 0
    start_time = time.time()

    for batch_num in range(total_batches):
        batch_start = start_idx + batch_num * args.batch_size
        batch_end = min(batch_start + args.batch_size, end_idx)

        if batch_start >= end_idx:
            break

        print(f"\n批次 {batch_num + 1}/{total_batches} (食谱 {batch_start+1}-{batch_end})...")

        # 准备批量数据
        recipes_data = []
        for idx in range(batch_start, batch_end):
            recipes_data.append({
                'index': idx,
                'recipe': df.iloc[idx].to_dict()
            })

        # 批量分析
        try:
            results = analyzer.analyze_batch(recipes_data)

            # 更新DataFrame
            for result in results:
                idx = result['index']
                df.at[idx, 'difficulty'] = result.get('difficulty', '简单')
                df.at[idx, 'suitable_constitutions'] = json.dumps(result.get('suitable_constitutions', ["peace"]), ensure_ascii=False)
                df.at[idx, 'avoid_constitutions'] = json.dumps(result.get('avoid_constitutions', []), ensure_ascii=False)
                df.at[idx, 'efficacy_tags'] = json.dumps(result.get('efficacy_tags', []), ensure_ascii=False)
                df.at[idx, 'solar_terms'] = json.dumps(result.get('solar_terms', []), ensure_ascii=False)
                df.at[idx, 'confidence'] = result.get('confidence', 50)
                df.at[idx, 'method'] = result.get('method', 'simulated')

                if result.get('method') == 'AI':
                    ai_count += 1

            # 定期保存
            if (batch_num + 1) % 3 == 0 or batch_num == total_batches - 1:
                df.to_excel(output_file, index=False, engine='openpyxl')
                print(f"  [保存] 进度: {batch_end}/{end_idx}, AI分析: {ai_count} 条")

        except Exception as e:
            print(f"  [ERROR] 批次处理失败: {e}")

    # 最终保存
    df.to_excel(output_file, index=False, engine='openpyxl')

    elapsed = time.time() - start_time
    avg_conf = df.iloc[start_idx:end_idx]['confidence'].mean()

    print(f"\n" + "=" * 60)
    print(f"完成! 用时: {elapsed:.1f}秒")
    print(f"AI分析: {ai_count} 条")
    print(f"平均置信度: {avg_conf:.1f}%")
    print(f"输出文件: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
