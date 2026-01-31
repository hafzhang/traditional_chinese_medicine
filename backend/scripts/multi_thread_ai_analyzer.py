#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
8线程并发AI食谱分析器
使用多线程并发处理，大幅提升AI处理速度
"""

import pandas as pd
import json
import re
import os
import sys
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

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

# 线程锁用于文件写入
file_lock = threading.Lock()


class ThreadSafeAIAnalyzer:
    """线程安全的AI分析器"""

    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.base_url = base_url or os.environ.get("ANTHROPIC_BASE_URL")
        self.use_ai = ANTHROPIC_AVAILABLE and self.api_key

        # 每个线程创建自己的客户端
        self.local = threading.local()

        if self.use_ai:
            if self.base_url:
                print(f"[OK] 8线程AI模式 (API: {self.base_url})")
            else:
                print("[OK] 8线程AI模式")
        else:
            print("[WARNING] API不可用")

    def _get_client(self):
        """获取线程本地的客户端"""
        if not hasattr(self.local, 'client'):
            if self.base_url:
                self.local.client = anthropic.Anthropic(api_key=self.api_key, base_url=self.base_url)
            else:
                self.local.client = anthropic.Anthropic(api_key=self.api_key)
        return self.local.client

    def analyze_batch(self, recipes_data, thread_id=0):
        """
        批量分析多条食谱（线程安全）

        Args:
            recipes_data: 食谱数据列表
            thread_id: 线程ID

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

            # 调用AI API（线程安全）
            client = self._get_client()
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
                timeout=60.0
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

                print(f"  [线程{thread_id}] 成功处理 {len(results)} 条")
                return results
            else:
                print(f"  [线程{thread_id}] 解析失败，使用备选方案")
                return self._fallback_analysis(recipes_data)

        except Exception as e:
            print(f"  [线程{thread_id}] API调用失败: {e}，使用备选方案")
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
            if any(kw in all_text for kw in ["祛湿", "冬瓜", "薏米"]):
                suitable.append("phlegm_damp")

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


def process_range_with_threads(start_idx, end_idx, analyzer, output_file, num_threads=8, batch_size=10):
    """
    使用多线程处理指定范围的食谱

    Args:
        start_idx: 起始索引
        end_idx: 结束索引
        analyzer: AIRecipeAnalyzer实例
        output_file: 输出文件路径
        num_threads: 线程数
        batch_size: 每批处理的食谱数
    """
    print(f"\n处理食谱 {start_idx+1}-{end_idx}，共 {end_idx-start_idx} 条")
    print(f"配置: {num_threads}线程, 每批{batch_size}条")

    # 读取数据
    df = pd.read_excel(output_file)

    # 准备批次
    batches = []
    for batch_start in range(start_idx, end_idx, batch_size):
        batch_end = min(batch_start + batch_size, end_idx)

        recipes_data = []
        for idx in range(batch_start, batch_end):
            recipes_data.append({
                'index': idx,
                'recipe': df.iloc[idx].to_dict()
            })

        batches.append((batch_start, batch_end, recipes_data))

    print(f"总共 {len(batches)} 个批次，使用 {num_threads} 个线程并发处理...")

    ai_count = 0
    sim_count = 0
    completed = 0

    # 使用线程池并发处理
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 提交所有任务
        future_to_batch = {}
        for i, (batch_start, batch_end, recipes_data) in enumerate(batches):
            thread_id = i % num_threads
            future = executor.submit(analyzer.analyze_batch, recipes_data, thread_id)
            future_to_batch[future] = (batch_start, batch_end, len(recipes_data))

        # 处理完成的任务
        for future in as_completed(future_to_batch):
            batch_start, batch_end, batch_size_actual = future_to_batch[future]

            try:
                results = future.result()

                # 更新DataFrame（线程安全）
                with file_lock:
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
                            ai_count += batch_size_actual
                        else:
                            sim_count += batch_size_actual

                    # 定期保存
                    completed += 1
                    if completed % max(1, len(batches) // 10) == 0 or completed == len(batches):
                        df.to_excel(output_file, index=False, engine='openpyxl')
                        progress_pct = (batch_end) / (end_idx - start_idx) * 100
                        print(f"  [进度] {completed}/{len(batches)} 批次完成, 已保存 (AI: {ai_count}, 模拟: {sim_count})")

            except Exception as e:
                print(f"  [ERROR] 批次 {batch_start}-{batch_end} 处理失败: {e}")

    # 最终保存
    df.to_excel(output_file, index=False, engine='openpyxl')

    avg_conf = df.iloc[start_idx:end_idx]['confidence'].mean()
    print(f"\n  [完成] AI: {ai_count}, 模拟: {sim_count}, 平均置信度: {avg_conf:.1f}%")

    return ai_count, sim_count


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='8线程并发AI食谱分析')
    parser.add_argument('--start', type=int, default=0, help='起始索引')
    parser.add_argument('--end', type=int, default=None, help='结束索引')
    parser.add_argument('--threads', type=int, default=8, help='线程数')
    parser.add_argument('--batch-size', type=int, default=10, help='每批处理的食谱数')
    parser.add_argument('--api-key', type=str, default=None, help='API密钥')
    parser.add_argument('--base-url', type=str, default=None, help='API基础URL')

    args = parser.parse_args()

    # 文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    input_file = os.path.join(project_root, 'source_data', 'dishes_list.xlsx')
    output_file = os.path.join(project_root, 'source_data', 'dishes_list_ai_filled.xlsx')

    print("=" * 70)
    print("8线程并发AI食谱分析器")
    print("=" * 70)

    # 读取数据
    print(f"\n读取文件: {input_file}")
    df_total = pd.read_excel(input_file)
    total = len(df_total)

    start_idx = args.start
    end_idx = args.end if args.end else total

    print(f"总食谱数: {total}")
    print(f"处理范围: {start_idx+1} - {end_idx}")
    print(f"线程数: {args.threads}")
    print(f"批量大小: {args.batch_size}")

    # 初始化分析器
    analyzer = ThreadSafeAIAnalyzer(api_key=args.api_key, base_url=args.base_url)

    # 添加列（如果不存在）
    df = pd.read_excel(output_file) if os.path.exists(output_file) else df_total
    for col in ['difficulty', 'suitable_constitutions', 'avoid_constitutions',
                'efficacy_tags', 'solar_terms', 'confidence', 'method']:
        if col not in df.columns:
            df[col] = None

    start_time = time.time()

    # 处理
    ai_total, sim_total = process_range_with_threads(
        start_idx, end_idx, analyzer, output_file,
        num_threads=args.threads,
        batch_size=args.batch_size
    )

    elapsed = time.time() - start_time

    print("\n" + "=" * 70)
    print(f"处理完成! 用时: {elapsed:.1f}秒")
    print(f"AI分析: {ai_total} 条")
    print(f"模拟分析: {sim_total} 条")
    print(f"速度: {(end_idx - start_idx) / elapsed:.1f} 条/秒")
    print(f"输出文件: {output_file}")
    print("=" * 70)


if __name__ == '__main__':
    main()
