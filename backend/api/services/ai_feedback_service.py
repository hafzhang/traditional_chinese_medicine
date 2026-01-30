"""
AI Feedback Service
AI反馈服务层 - MVP
使用通义千问 (DashScope) API
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, date
import json
import os

try:
    import dashscope
    from dashscope import Generation
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

from api.models import UserCheckIn, User, ConstitutionResult
from api.services.checkin_service import CheckInService


class AIFeedbackService:
    """AI反馈服务类"""

    def __init__(self):
        if DASHSCOPE_AVAILABLE:
            dashscope.api_key = os.getenv("DASHSCOPE_API_KEY", "")
        self.checkin_service = CheckInService()

    def analyze_checkin_pattern(
        self,
        user_id: str,
        weeks_data: List[Dict[str, Any]],
        db: Session
    ) -> Dict[str, Any]:
        """
        分析用户打卡模式

        Args:
            user_id: 用户ID
            weeks_data: 多周打卡数据
            db: 数据库会话

        Returns:
            分析结果
        """
        if not weeks_data:
            return self._get_empty_analysis()

        # 获取用户体质信息
        user = db.query(User).filter(User.id == user_id).first()
        constitution_code = None
        if user:
            latest_result = db.query(ConstitutionResult).filter(
                ConstitutionResult.user_id == user_id
            ).order_by(ConstitutionResult.created_at.desc()).first()
            if latest_result:
                constitution_code = latest_result.primary_constitution

        # 如果DashScope不可用，使用规则分析
        if not DASHSCOPE_AVAILABLE or not dashscope.api_key:
            return self._rule_based_analysis(user_id, weeks_data, constitution_code, db)

        # 使用AI分析
        prompt = self._build_analysis_prompt(user_id, weeks_data, constitution_code, db)

        try:
            response = Generation.call(
                model="qwen-turbo",
                prompt=prompt,
                result_format='message',
                max_tokens=1500
            )

            if response.status_code == 200:
                result_text = response.output.text
                return self._parse_ai_response(result_text)
        except Exception as e:
            print(f"AI analysis failed: {e}")

        # 回退到规则分析
        return self._rule_based_analysis(user_id, weeks_data, constitution_code, db)

    def _build_analysis_prompt(
        self,
        user_id: str,
        weeks_data: List[Dict[str, Any]],
        constitution_code: Optional[str],
        db: Session
    ) -> str:
        """构建AI分析提示词"""
        constitution_info = ""
        if constitution_code:
            constitution_names = {
                "peace": "平和质", "qi_deficiency": "气虚质", "yang_deficiency": "阳虚质",
                "yin_deficiency": "阴虚质", "phlegm_damp": "痰湿质", "damp_heat": "湿热质",
                "blood_stasis": "血瘀质", "qi_depression": "气郁质", "special": "特禀质"
            }
            constitution_info = f"用户体质: {constitution_names.get(constitution_code, constitution_code)}"

        # 将数据转换为可读格式
        data_summary = []
        for week in weeks_data:
            data_summary.append(f"第{week.get('week_number', '?')}周: "
                              f"运动完成率{week.get('exercise_completion_rate', 0):.1f}%, "
                              f"作息遵守率{week.get('routine_adherence_rate', 0):.1f}%, "
                              f"情绪分{week.get('mood_score', 0):.1f}")

        prompt = f"""
你是一位专业的中医养生顾问。请分析用户的健康打卡数据并提供个性化建议。

{constitution_info}
用户近期打卡数据:
{chr(10).join(data_summary)}

请从以下方面分析:
1. 运动完成率趋势
2. 作息规律性
3. 情绪状态变化
4. 给出3条具体的养生建议

请以JSON格式返回，严格遵循以下格式:
{{
    "trends": ["运动完成率呈上升趋势", "作息较为规律"],
    "risk_factors": ["情绪分数偏低", "运动量不足"],
    "recommendations": ["建议每天练习八段锦15分钟", "保持规律作息时间", "睡前进行冥想放松"],
    "motivational_message": "您本周的表现很棒，继续保持！"
}}
"""
        return prompt

    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """解析AI响应"""
        try:
            # 尝试提取JSON部分
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse AI response: {e}")

        # 如果解析失败，返回默认响应
        return {
            "trends": ["数据不足以分析趋势"],
            "risk_factors": [],
            "recommendations": ["继续保持健康习惯", "注意劳逸结合", "保持积极心态"],
            "motivational_message": "记录健康数据是养生的第一步！"
        }

    def _rule_based_analysis(
        self,
        user_id: str,
        weeks_data: List[Dict[str, Any]],
        constitution_code: Optional[str],
        db: Session
    ) -> Dict[str, Any]:
        """基于规则的分析（AI不可用时的回退方案）"""
        if not weeks_data:
            return self._get_empty_analysis()

        latest_week = weeks_data[0]
        exercise_rate = latest_week.get("exercise_completion_rate", 0)
        routine_rate = latest_week.get("routine_adherence_rate", 0)
        mood_score = latest_week.get("mood_score", 0)

        trends = []
        risk_factors = []
        recommendations = []

        # 分析运动完成率
        if exercise_rate >= 80:
            trends.append("运动习惯良好")
        elif exercise_rate >= 50:
            trends.append("运动频率适中")
            recommendations.append("建议增加运动频率，每周至少3-5次")
        else:
            risk_factors.append("运动量不足")
            recommendations.append("建议从简单的八段锦开始，每天练习10-15分钟")

        # 分析作息规律性
        if routine_rate >= 80:
            trends.append("作息规律")
        elif routine_rate >= 50:
            trends.append("作息较为规律")
            recommendations.append("保持规律作息时间")
        else:
            risk_factors.append("作息不规律")
            recommendations.append("建议固定起床和睡眠时间")

        # 分析情绪状态
        if mood_score >= 7:
            trends.append("情绪状态良好")
        elif mood_score >= 5:
            trends.append("情绪状态平稳")
        else:
            risk_factors.append("情绪状态需要关注")
            recommendations.append("建议进行冥想或呼吸练习来放松心情")

        # 根据体质给出建议
        if constitution_code:
            constitution_recommendations = self._get_constitution_recommendations(constitution_code)
            recommendations.extend(constitution_recommendations[:2])

        # 生成鼓励信息
        if exercise_rate >= 80 and routine_rate >= 80:
            motivational = "您本周的表现非常出色！继续保持这个好习惯！"
        elif exercise_rate >= 50 or routine_rate >= 50:
            motivational = "您正在建立良好的健康习惯，继续坚持！"
        else:
            motivational = "千里之行始于足下，每一天的进步都值得鼓励！"

        return {
            "trends": trends,
            "risk_factors": risk_factors,
            "recommendations": recommendations[:5],  # 限制建议数量
            "motivational_message": motivational
        }

    def _get_constitution_recommendations(self, constitution_code: str) -> List[str]:
        """根据体质获取建议"""
        recommendations_map = {
            "qi_deficiency": [
                "建议进行温和的运动如散步、太极",
                "避免过度劳累",
                "可以尝试练习补气功法"
            ],
            "yang_deficiency": [
                "建议选择上午阳光下运动",
                "注意保暖，避免受凉",
                "可以练习温阳功法"
            ],
            "yin_deficiency": [
                "建议进行中等强度运动",
                "避免大汗淋漓",
                "可以练习滋阴功法"
            ],
            "phlegm_damp": [
                "建议进行有氧运动",
                "运动强度可稍大",
                "坚持每天运动有助于祛湿"
            ],
            "damp_heat": [
                "建议选择清凉环境的运动",
                "运动后及时补充水分",
                "可练习清热祛湿功法"
            ],
            "blood_stasis": [
                "建议进行促进血液循环的运动",
                "可练习活血化瘀功法",
                "运动后注意拉伸"
            ],
            "qi_depression": [
                "建议进行户外运动",
                "可练习疏肝解郁功法",
                "运动有助于舒缓情绪"
            ],
            "special": [
                "根据过敏情况选择运动环境",
                "避免花粉较多的地方户外运动",
                "室内运动较为安全"
            ],
            "peace": [
                "保持目前的良好习惯",
                "可根据季节调整运动方案",
                "注重平衡运动"
            ]
        }
        return recommendations_map.get(constitution_code, [])

    def _get_empty_analysis(self) -> Dict[str, Any]:
        """返回空分析结果"""
        return {
            "trends": [],
            "risk_factors": [],
            "recommendations": ["开始记录您的健康数据吧！"],
            "motivational_message": "开始您的健康之旅！"
        }

    def generate_weekly_recommendations(
        self,
        checkin_id: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        生成周建议

        Args:
            checkin_id: 打卡记录ID
            db: 数据库会话

        Returns:
            周建议
        """
        checkin = self.checkin_service.get_checkin_by_id(checkin_id, db)
        if not checkin:
            return self._get_empty_analysis()

        # 获取历史数据
        user_checkins, _ = self.checkin_service.get_user_checkins(
            checkin.user_id, db, limit=4
        )

        weeks_data = []
        for c in user_checkins:
            weeks_data.append({
                "week_number": c.week_number,
                "exercise_completion_rate": c.exercise_completion_rate,
                "routine_adherence_rate": c.routine_adherence_rate,
                "mood_score": c.mood_score,
                "daily_entries": c.daily_entries
            })

        # 分析模式
        analysis = self.analyze_checkin_pattern(checkin.user_id, weeks_data, db)

        return analysis

    def generate_motivational_message(
        self,
        user_id: str,
        streak: int,
        db: Session
    ) -> str:
        """
        生成鼓励信息

        Args:
            user_id: 用户ID
            streak: 连续打卡天数
            db: 数据库会话

        Returns:
            鼓励信息
        """
        messages_by_streak = {
            0: "开始记录您的健康数据吧！",
            range(1, 7): "很好的开始！继续保持！",
            range(7, 14): "坚持了一周！您正在建立良好的健康习惯！",
            range(14, 30): "两周了！您的坚持令人钦佩！",
            range(30, 60): "一个月！健康的生活方式正在形成！",
            range(60, 999): "太棒了！您已经养成了健康的生活习惯！"
        }

        for streak_range, message in messages_by_streak.items():
            if isinstance(streak_range, range):
                if streak in streak_range:
                    return message
            elif streak == streak_range:
                return message

        return messages_by_streak[range(60, 999)]

    def identify_risk_factors(
        self,
        user_id: str,
        db: Session
    ) -> List[str]:
        """
        识别风险因素

        Args:
            user_id: 用户ID
            db: 数据库会话

        Returns:
            风险因素列表
        """
        # 获取最近的打卡数据
        checkins, _ = self.checkin_service.get_user_checkins(user_id, db, limit=2)

        if not checkins:
            return ["尚未开始记录健康数据"]

        latest = checkins[0]
        risk_factors = []

        # 检查运动完成率
        if latest.exercise_completion_rate < 30:
            risk_factors.append("运动量严重不足")
        elif latest.exercise_completion_rate < 50:
            risk_factors.append("运动频率偏低")

        # 检查作息规律性
        if latest.routine_adherence_rate < 30:
            risk_factors.append("作息严重不规律")
        elif latest.routine_adherence_rate < 50:
            risk_factors.append("作息需要调整")

        # 检查情绪状态
        if latest.mood_score and latest.mood_score < 4:
            risk_factors.append("情绪状态需要关注")

        # 检查连续打卡情况
        streak = self.checkin_service.calculate_progress_streak(user_id, db)
        if streak == 0 and latest.exercise_completion_rate > 0:
            risk_factors.append("需要保持打卡习惯")

        return risk_factors
