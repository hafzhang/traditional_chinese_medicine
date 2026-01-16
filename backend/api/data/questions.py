"""
Questions Data
体质测试题目数据 - 基于CCMQ标准简化版
"""

# 30个问题，涵盖9种体质类型
# 每个问题答案: 1=没有, 2=很少, 3=有时, 4=经常, 5=总是

QUESTIONS_DATA = [
    # 平和质 (1-4)
    {
        "number": 1,
        "content": "您精力充沛吗？",
        "constitution_type": "peace"
    },
    {
        "number": 2,
        "content": "您说话声音低弱无力吗？",
        "constitution_type": "peace"
    },
    {
        "number": 3,
        "content": "您容易疲乏吗？",
        "constitution_type": "peace"
    },
    {
        "number": 4,
        "content": "您面色晦暗或容易出现褐斑吗？",
        "constitution_type": "peace"
    },
    # 气虚质 (5-8)
    {
        "number": 5,
        "content": "您容易疲乏吗？",
        "constitution_type": "qi_deficiency"
    },
    {
        "number": 6,
        "content": "您容易气短（呼吸短促，接不上气）吗？",
        "constitution_type": "qi_deficiency"
    },
    {
        "number": 7,
        "content": "您比一般人容易感冒吗？",
        "constitution_type": "qi_deficiency"
    },
    {
        "number": 8,
        "content": "您喜欢安静、不喜欢说话吗？",
        "constitution_type": "qi_deficiency"
    },
    # 阳虚质 (9-12)
    {
        "number": 9,
        "content": "您手脚发凉吗？",
        "constitution_type": "yang_deficiency"
    },
    {
        "number": 10,
        "content": "您胃、胳膊、膝盖怕冷吗？",
        "constitution_type": "yang_deficiency"
    },
    {
        "number": 11,
        "content": "您比一般人怕冷吗？",
        "constitution_type": "yang_deficiency"
    },
    {
        "number": 12,
        "content": "您吃凉东西会感到不舒服或怕吃凉的吗？",
        "constitution_type": "yang_deficiency"
    },
    # 阴虚质 (13-16)
    {
        "number": 13,
        "content": "您感到口干咽燥、总想喝水吗？",
        "constitution_type": "yin_deficiency"
    },
    {
        "number": 14,
        "content": "您手心脚心发热吗？",
        "constitution_type": "yin_deficiency"
    },
    {
        "number": 15,
        "content": "您皮肤或口唇干吗？",
        "constitution_type": "yin_deficiency"
    },
    {
        "number": 16,
        "content": "您便秘或大便干燥吗？",
        "constitution_type": "yin_deficiency"
    },
    # 痰湿质 (17-19)
    {
        "number": 17,
        "content": "您感到胸闷或腹部胀满吗？",
        "constitution_type": "phlegm_damp"
    },
    {
        "number": 18,
        "content": "您感到身体沉重不轻松或不爽快吗？",
        "constitution_type": "phlegm_damp"
    },
    {
        "number": 19,
        "content": "您腹部肥满松软吗？",
        "constitution_type": "phlegm_damp"
    },
    # 湿热质 (20-22)
    {
        "number": 20,
        "content": "您面部或鼻部有油腻感或者油亮发光吗？",
        "constitution_type": "damp_heat"
    },
    {
        "number": 21,
        "content": "您容易生痤疮或疮疖吗？",
        "constitution_type": "damp_heat"
    },
    {
        "number": 22,
        "content": "您感到口苦或嘴里有异味吗？",
        "constitution_type": "damp_heat"
    },
    # 血瘀质 (23-25)
    {
        "number": 23,
        "content": "您的皮肤在不知不觉中会出现青紫瘀斑吗？",
        "constitution_type": "blood_stasis"
    },
    {
        "number": 24,
        "content": "您的两颧部有细微红丝吗？",
        "constitution_type": "blood_stasis"
    },
    {
        "number": 25,
        "content": "您身体上有哪里疼痛，而且疼痛部位固定吗？",
        "constitution_type": "blood_stasis"
    },
    # 气郁质 (26-28)
    {
        "number": 26,
        "content": "您感到闷闷不乐、情绪低沉吗？",
        "constitution_type": "qi_depression"
    },
    {
        "number": 27,
        "content": "您容易精神紧张、焦虑不安吗？",
        "constitution_type": "qi_depression"
    },
    {
        "number": 28,
        "content": "您无缘无故叹气吗？",
        "constitution_type": "qi_depression"
    },
    # 特禀质 (29-30)
    {
        "number": 29,
        "content": "您没有感冒也会打喷嚏吗？",
        "constitution_type": "special"
    },
    {
        "number": 30,
        "content": "您没有感冒也会鼻塞、流鼻涕吗？",
        "constitution_type": "special"
    }
]
