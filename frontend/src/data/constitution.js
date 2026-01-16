/**
 * 体质信息数据
 * Constitution Information Data
 * 基于王琦院士 CCMQ 标准的九种体质详细信息
 */

export const CONSTITUTION_INFO = {
  peace: {
    type: 'peace',
    name: '平和质',
    icon: '☯',
    color: '#52c41a',
    description: '阴阳气血调和，体态适中，面色红润，精力充沛',
    characteristics: {
      overall: [
        '体型匀称健壮',
        '面色、肤色润泽',
        '头发稠密有光泽',
        '目光有神，鼻色明润',
        '嗅觉通利，唇色红润',
        '精力充沛，不易疲劳',
        '耐受寒热，睡眠良好',
        '胃纳佳，二便正常'
      ],
      mental: ['性格随和开朗']
    },
    regulation: {
      diet: [
        '饮食有节，不要过饥过饱',
        '食物搭配要多样化',
        '清淡饮食，避免过饱'
      ],
      exercise: ['适度运动，劳逸结合'],
      lifestyle: [
        '规律作息，避免熬夜',
        '保持心情舒畅'
      ]
    },
    taboos: ['避免暴饮暴食', '避免长期偏食']
  },
  qi_deficiency: {
    type: 'qi_deficiency',
    name: '气虚质',
    icon: '气',
    color: '#faad14',
    description: '元气不足，气息低弱，机体功能状态低下',
    characteristics: {
      overall: [
        '肌肉松软，容易疲劳',
        '面色苍白，目光少神',
        '气短懒言，容易出汗',
        '易感冒，尤其怕风'
      ],
      mental: ['性格内向，不喜冒险']
    },
    regulation: {
      diet: [
        '宜吃补气健脾的食物',
        '如：山药、莲子、大枣、小米、糯米、鸡肉、牛肉',
        '忌吃破气耗气的食物',
        '如：山楂、大蒜、香菜、芥菜'
      ],
      exercise: ['温和运动为主，如散步、太极拳、八段锦'],
      lifestyle: [
        '避免过度劳累',
        '保证充足睡眠',
        '注意保暖，避免出汗受风'
      ],
      emotion: ['保持心情愉快，避免过度思虑']
    },
    taboos: ['忌剧烈运动', '忌过度用脑', '忌食寒凉']
  },
  yang_deficiency: {
    type: 'yang_deficiency',
    name: '阳虚质',
    icon: '阳',
    color: '#1890ff',
    description: '阳气不足，身体失于温煦，畏寒怕冷',
    characteristics: {
      overall: [
        '肌肉松软，容易水肿',
        '面色发白，手足发凉',
        '怕冷喜热，精神不振',
        '易大便溏薄'
      ],
      mental: ['性格多沉静、内向']
    },
    regulation: {
      diet: [
        '宜吃温补阳气的食物',
        '如：羊肉、韭菜、辣椒、生姜、花椒、桂圆',
        '少吃生冷寒凉的食物',
        '如：冰镇饮料、生冷瓜果'
      ],
      exercise: ['适度运动，以身体发热为度，如慢跑、快走'],
      lifestyle: [
        '注意保暖，尤其是腰腹和脚部',
        '避免长期处于寒冷环境',
        '多晒太阳'
      ],
      emotion: ['保持积极乐观的心态']
    },
    taboos: ['忌食生冷', '避免长期受寒', '忌冷水澡']
  },
  yin_deficiency: {
    type: 'yin_deficiency',
    name: '阴虚质',
    icon: '阴',
    color: '#eb2f96',
    description: '阴液亏少，以干燥失润、虚热内扰为主要特征',
    characteristics: {
      overall: [
        '体形多偏瘦',
        '面色潮红，有烘热感',
        '口燥咽干，手足心热',
        '易心烦失眠，大便干燥'
      ],
      mental: ['性格急躁易怒，外向活泼']
    },
    regulation: {
      diet: [
        '宜吃滋阴润燥的食物',
        '如：百合、银耳、梨、鸭肉、桑葚、枸杞',
        '少吃辛辣燥热的食物',
        '如：辣椒、胡椒、羊肉、狗肉'
      ],
      exercise: ['中小强度的运动，避免剧烈运动，如游泳、瑜伽'],
      lifestyle: [
        '注意休息，避免熬夜',
        '保持室内适宜湿度',
        '多饮水'
      ],
      emotion: ['学会调节情绪，避免动怒']
    },
    taboos: ['忌辛辣燥热', '忌熬夜', '忌高温环境']
  },
  phlegm_damp: {
    type: 'phlegm_damp',
    name: '痰湿质',
    icon: '痰',
    color: '#722ed1',
    description: '水液内停而痰湿凝聚，以黏滞重浊为主要特征',
    characteristics: {
      overall: [
        '体型肥胖，腹部肥满松软',
        '面部皮肤油脂较多',
        '多汗且黏，胸闷痰多',
        '口黏腻或甜，身重不爽'
      ],
      mental: ['性格偏温和，稳重多谋']
    },
    regulation: {
      diet: [
        '宜吃健脾利湿、化痰祛湿的食物',
        '如：冬瓜、赤小豆、荷叶、白萝卜、薏米',
        '少吃甜、黏、油腻的食物',
        '如：糖果、糯米、肥肉、油炸食品'
      ],
      exercise: ['长期坚持运动，如快走、慢跑、太极拳'],
      lifestyle: [
        '控制饮食量',
        '保持居住环境干燥',
        '保持大便通畅'
      ],
      emotion: ['保持心情舒畅']
    },
    taboos: ['忌甜腻肥厚', '忌少动久坐', '忌居住潮湿']
  },
  damp_heat: {
    type: 'damp_heat',
    name: '湿热质',
    icon: '湿',
    color: '#fa541c',
    description: '湿热内蕴，以湿热内蕴为主要特征',
    characteristics: {
      overall: [
        '容易长痤疮、粉刺',
        '面垢油光，易口苦口干',
        '身重困倦，大便黏滞不畅',
        '小便短赤，男性易阴囊潮湿'
      ],
      mental: ['容易心烦急躁']
    },
    regulation: {
      diet: [
        '宜吃清热利湿的食物',
        '如：绿豆、苦瓜、黄瓜、芹菜、西瓜、冬瓜',
        '少吃辛辣燥烈、大热大补的食物',
        '如：辣椒、狗肉、羊肉、白酒'
      ],
      exercise: ['中等强度运动，如中长跑、游泳、爬山'],
      lifestyle: [
        '保持环境通风干燥',
        '避免熬夜',
        '注意个人卫生'
      ],
      emotion: ['保持心态平和']
    },
    taboos: ['忌辛辣油腻', '忌饮酒', '忌高温环境']
  },
  blood_stasis: {
    type: 'blood_stasis',
    name: '血瘀质',
    icon: '瘀',
    color: '#f5222d',
    description: '血行不畅，以肤色晦黯、舌质紫黯为主要特征',
    characteristics: {
      overall: [
        '肤色晦黯，色素沉着',
        '容易出现瘀斑',
        '口唇黯淡或紫',
        '舌质黯淡或有瘀点'
      ],
      mental: ['性格心情烦闷，容易健忘']
    },
    regulation: {
      diet: [
        '宜吃活血化瘀的食物',
        '如：黑豆、山楂、醋、玫瑰花茶、黑木耳',
        '少吃寒凉、收涩的食物',
        '如：柿子、石榴'
      ],
      exercise: ['适度运动，促进血液循环，如跑步、跳绳'],
      lifestyle: [
        '注意保暖，避免寒邪侵袭',
        '保持心情舒畅',
        '避免久坐'
      ],
      emotion: ['保持心情愉悦，避免抑郁']
    },
    taboos: ['忌寒凉收涩', '忌久坐不动', '忌受寒']
  },
  qi_depression: {
    type: 'qi_depression',
    name: '气郁质',
    icon: '郁',
    color: '#13c2c2',
    description: '气机郁滞，以神情抑郁、忧虑脆弱为主要特征',
    characteristics: {
      overall: [
        '表情多郁闷、不开心',
        '胸胁胀满，或走窜疼痛',
        '善太息，嗳气呃逆',
        '咽喉异物感，乳房胀痛'
      ],
      mental: ['性格内向不稳定，敏感多虑']
    },
    regulation: {
      diet: [
        '宜吃疏肝理气的食物',
        '如：柑橘、柚子、陈皮、玫瑰花、菊花',
        '少吃生冷、油腻的食物'
      ],
      exercise: ['增加户外运动，如踏青、登山、游泳'],
      lifestyle: [
        '多与人交流',
        '培养兴趣爱好',
        '保持规律作息'
      ],
      emotion: ['学会疏解情绪，保持心情舒畅']
    },
    taboos: ['忌思虑过度', '忌长期郁结', '忌独处']
  },
  special: {
    type: 'special',
    name: '特禀质',
    icon: '特',
    color: '#52c41a',
    description: '先天失常，以生理缺陷、过敏反应等为主要特征',
    characteristics: {
      overall: [
        '容易过敏（花粉、食物、药物）',
        '不感冒也容易打喷嚏、流鼻涕',
        '容易患哮喘、荨麻疹等',
        '皮肤容易起荨麻疹、湿疹'
      ],
      mental: ['性格因情况而异']
    },
    regulation: {
      diet: [
        '宜吃清淡、均衡的食物',
        '避免食用已知的过敏食物',
        '少吃腥膻发物',
        '如：鱼、虾、蟹、羊肉'
      ],
      exercise: ['适度运动，增强体质，如散步、瑜伽'],
      lifestyle: [
        '避免接触过敏原',
        '保持室内清洁',
        '勤换洗衣物'
      ],
      emotion: ['保持心态平和']
    },
    taboos: ['忌接触过敏原', '忌食用过敏食物', '忌养宠物']
  }
}

// 题目到体质的映射
export const QUESTION_TYPE_MAPPING = {
  1: 'peace', 2: 'peace', 3: 'peace', 4: 'peace',
  5: 'qi_deficiency', 6: 'qi_deficiency', 7: 'qi_deficiency', 8: 'qi_deficiency',
  9: 'yang_deficiency', 10: 'yang_deficiency', 11: 'yang_deficiency', 12: 'yang_deficiency',
  13: 'yin_deficiency', 14: 'yin_deficiency', 15: 'yin_deficiency', 16: 'yin_deficiency',
  17: 'phlegm_damp', 18: 'phlegm_damp', 19: 'phlegm_damp',
  20: 'damp_heat', 21: 'damp_heat', 22: 'damp_heat',
  23: 'blood_stasis', 24: 'blood_stasis', 25: 'blood_stasis',
  26: 'qi_depression', 27: 'qi_depression', 28: 'qi_depression',
  29: 'special', 30: 'special'
}

// 体质题目分组
export const QUESTION_GROUPS = {
  peace: { start: 1, end: 4, name: '平和质' },
  qi_deficiency: { start: 5, end: 8, name: '气虚质' },
  yang_deficiency: { start: 9, end: 12, name: '阳虚质' },
  yin_deficiency: { start: 13, end: 16, name: '阴虚质' },
  phlegm_damp: { start: 17, end: 19, name: '痰湿质' },
  damp_heat: { start: 20, end: 22, name: '湿热质' },
  blood_stasis: { start: 23, end: 25, name: '血瘀质' },
  qi_depression: { start: 26, end: 28, name: '气郁质' },
  special: { start: 29, end: 30, name: '特禀质' }
}

export default CONSTITUTION_INFO
