"""
体质测试 API 路由
"""
from fastapi import APIRouter, HTTPException
from typing import List
from loguru import logger

from app.schemas.constitution import QuizSubmitRequest, QuizResponse, QuestionItem
from app.services.constitution_service import constitution_service

router = APIRouter()

# 问卷题目（MVP 版本使用硬编码数据）
QUESTIONS = [
    # 平和质 (4题)
    {"id": "p1", "question_text": "您精力充沛吗？", "constitution_type": "peace", "order_index": 1},
    {"id": "p2", "question_text": "您说话声音低弱无力吗？(反向)", "constitution_type": "peace", "order_index": 2},
    {"id": "p3", "question_text": "您容易疲乏吗？(反向)", "constitution_type": "peace", "order_index": 3},
    {"id": "p4", "question_text": "您患有慢性疾病吗？(反向)", "constitution_type": "peace", "order_index": 4},

    # 气虚质 (4题)
    {"id": "qd1", "question_text": "您容易疲乏吗？", "constitution_type": "qi_deficiency", "order_index": 5},
    {"id": "qd2", "question_text": "您容易气短（呼吸短促，接不上气）吗？", "constitution_type": "qi_deficiency", "order_index": 6},
    {"id": "qd3", "question_text": "您比一般人容易感冒吗？", "constitution_type": "qi_deficiency", "order_index": 7},
    {"id": "qd4", "question_text": "您喜欢安静、不喜欢说话吗？", "constitution_type": "qi_deficiency", "order_index": 8},

    # 阳虚质 (4题)
    {"id": "yd1", "question_text": "您手脚发凉吗？", "constitution_type": "yang_deficiency", "order_index": 9},
    {"id": "yd2", "question_text": "您胃脘部、背部或腰膝部怕冷吗？", "constitution_type": "yang_deficiency", "order_index": 10},
    {"id": "yd3", "question_text": "您比一般人怕冷吗？", "constitution_type": "yang_deficiency", "order_index": 11},
    {"id": "yd4", "question_text": "您喜欢热饮吗？", "constitution_type": "yang_deficiency", "order_index": 12},

    # 阴虚质 (4题)
    {"id": "yix1", "question_text": "您感到口干咽燥、总想喝水吗？", "constitution_type": "yin_deficiency", "order_index": 13},
    {"id": "yix2", "question_text": "您手心脚心发热吗？", "constitution_type": "yin_deficiency", "order_index": 14},
    {"id": "yix3", "question_text": "您身体或脸上容易发热吗？", "constitution_type": "yin_deficiency", "order_index": 15},
    {"id": "yix4", "question_text": "您皮肤或口唇干吗？", "constitution_type": "yin_deficiency", "order_index": 16},

    # 痰湿质 (3题)
    {"id": "pt1", "question_text": "您感到胸闷或腹部胀满吗？", "constitution_type": "phlegm_damp", "order_index": 17},
    {"id": "pt2", "question_text": "您感到身体沉重不轻松或不爽快吗？", "constitution_type": "phlegm_damp", "order_index": 18},
    {"id": "pt3", "question_text": "您腹部肥满松软吗？", "constitution_type": "phlegm_damp", "order_index": 19},

    # 湿热质 (3题)
    {"id": "sr1", "question_text": "您面部或鼻部有油腻感或者油亮发光吗？", "constitution_type": "damp_heat", "order_index": 20},
    {"id": "sr2", "question_text": "您容易生痤疮或疮疖吗？", "constitution_type": "damp_heat", "order_index": 21},
    {"id": "sr3", "question_text": "您感到口苦或嘴里有异味吗？", "constitution_type": "damp_heat", "order_index": 22},

    # 血瘀质 (3题)
    {"id": "bs1", "question_text": "您的皮肤在不知不觉中会出现青紫瘀斑（皮下出血）吗？", "constitution_type": "blood_stasis", "order_index": 23},
    {"id": "bs2", "question_text": "您的两颧部有细微红丝吗？", "constitution_type": "blood_stasis", "order_index": 24},
    {"id": "bs3", "question_text": "您身体上有哪里疼痛（刺痛），而且位置固定吗？", "constitution_type": "blood_stasis", "order_index": 25},

    # 气郁质 (3题)
    {"id": "qy1", "question_text": "您感到闷闷不乐、情绪低沉吗？", "constitution_type": "qi_depression", "order_index": 26},
    {"id": "qy2", "question_text": "您容易精神紧张、焦虑不安吗？", "constitution_type": "qi_depression", "order_index": 27},
    {"id": "qy3", "question_text": "您无缘无故叹气吗？", "constitution_type": "qi_depression", "order_index": 28},

    # 特禀质 (2题)
    {"id": "tb1", "question_text": "您没有感冒时也会打喷嚏吗？", "constitution_type": "special", "order_index": 29},
    {"id": "tb2", "question_text": "您容易过敏（对药物、食物、气味、花粉等）吗？", "constitution_type": "special", "order_index": 30},
]


@router.get("/quiz/questions", response_model=QuizResponse)
async def get_questions():
    """获取问卷题目"""
    logger.info("获取问卷题目")
    return QuizResponse(
        code=0,
        message="success",
        data={
            "total": len(QUESTIONS),
            "estimated_time": "5-8分钟",
            "questions": QUESTIONS
        }
    )


@router.post("/quiz/submit", response_model=QuizResponse)
async def submit_quiz(data: QuizSubmitRequest):
    """
    提交体质测试问卷

    - **answers**: 答案列表，每个问题1-5分
    """
    logger.info(f"收到问卷提交，答案数量: {len(data.answers)}")

    # 验证答案数量
    if len(data.answers) != len(QUESTIONS):
        raise HTTPException(
            status_code=400,
            detail=f"答案数量不正确，应为{len(QUESTIONS)}题"
        )

    # 验证答案范围
    for i, answer in enumerate(data.answers):
        if answer < 1 or answer > 5:
            raise HTTPException(
                status_code=400,
                detail=f"第{i+1}题答案无效，应为1-5之间的整数"
            )

    # 分析体质
    try:
        result = await constitution_service.analyze(data.answers, QUESTIONS)

        return QuizResponse(
            code=0,
            message="success",
            data=result
        )
    except Exception as e:
        logger.error(f"分析体质时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/constitution/info")
async def get_constitution_info():
    """获取体质类型说明"""
    info = {
        "constitutions": [
            {
                "type": "peace",
                "name": "平和质",
                "description": "健康体质，阴阳气血调和"
            },
            {
                "type": "qi_deficiency",
                "name": "气虚质",
                "description": "元气不足，气息低弱"
            },
            {
                "type": "yang_deficiency",
                "name": "阳虚质",
                "description": "阳气不足，畏寒怕冷"
            },
            {
                "type": "yin_deficiency",
                "name": "阴虚质",
                "description": "阴液亏虚，口干咽燥"
            },
            {
                "type": "phlegm_damp",
                "name": "痰湿质",
                "description": "水湿内停，体形肥胖"
            },
            {
                "type": "damp_heat",
                "name": "湿热质",
                "description": "湿热内蕴，面垢油光"
            },
            {
                "type": "blood_stasis",
                "name": "血瘀质",
                "description": "血行不畅，面色晦暗"
            },
            {
                "type": "qi_depression",
                "name": "气郁质",
                "description": "气机郁滞，情绪抑郁"
            },
            {
                "type": "special",
                "name": "特禀质",
                "description": "先天失常，易过敏"
            }
        ]
    }
    return {"code": 0, "message": "success", "data": info}
