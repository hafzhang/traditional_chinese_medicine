"""
Comprehensive Acupoints Data (361 Standard Points)
穴位数据完整版（361个标准穴位）
包含所有标准穴位的详细信息、解剖图参考、经络图参考
"""

# 经络信息与对应的GIF动画图
MERIDIANS = {
    "LU": {"name": "手太阴肺经", "name_en": "Lung Meridian", "count": 11, "part": "上肢", "gif": "手太阴肺经.gif"},
    "LI": {"name": "手阳明大肠经", "name_en": "Large Intestine Meridian", "count": 20, "part": "上肢", "gif": "手阳明大肠经.gif"},
    "ST": {"name": "足阳明胃经", "name_en": "Stomach Meridian", "count": 45, "part": "下肢", "gif": "足阳明胃经.gif"},
    "SP": {"name": "足太阴脾经", "name_en": "Spleen Meridian", "count": 21, "part": "下肢", "gif": "足太阴脾经.gif"},
    "HT": {"name": "手少阴心经", "name_en": "Heart Meridian", "count": 9, "part": "上肢", "gif": "手少阴心经.gif"},
    "SI": {"name": "手太阳小肠经", "name_en": "Small Intestine Meridian", "count": 19, "part": "上肢", "gif": "手太阳小肠经.gif"},
    "BL": {"name": "足太阳膀胱经", "name_en": "Bladder Meridian", "count": 67, "part": "背部", "gif": "足太阳膀胱经.gif"},
    "KI": {"name": "足少阴肾经", "name_en": "Kidney Meridian", "count": 27, "part": "下肢", "gif": "足少阴肾经.gif"},
    "PC": {"name": "手厥阴心包经", "name_en": "Pericardium Meridian", "count": 9, "part": "上肢", "gif": "手厥阴心包经.gif"},
    "TE": {"name": "手少阳三焦经", "name_en": "Triple Energizer Meridian", "count": 23, "part": "上肢", "gif": "手少阳三焦经.gif"},
    "GB": {"name": "足少阳胆经", "name_en": "Gallbladder Meridian", "count": 44, "part": "下肢", "gif": "足少阳胆经.gif"},
    "LR": {"name": "足厥阴肝经", "name_en": "Liver Meridian", "count": 14, "part": "下肢", "gif": "足厥阴肝经.gif"},
    "GV": {"name": "督脉", "name_en": "Governor Vessel", "count": 28, "part": "背部", "gif": "督脉.gif"},
    "CV": {"name": "任脉", "name_en": "Conception Vessel", "count": 24, "part": "胸腹部", "gif": "任脉.gif"},
}

# 可用的穴位图像（从272_pages_acupunture_point_chart目录）
AVAILABLE_IMAGES = {
    "合谷": "合谷.jpg",
    "曲池": "曲池.jpg",
    "迎香": "迎香.jpg",  # 可能需要
    "内关": "内关.jpg",
    "外关": "外关.jpg",
    "列缺": "列缺.jpg",
    "神门": "神门.jpg",
    "后溪": "后溪.jpg",  # 可能需要
    "太溪": "太溪.jpg",
    "昆仑": "昆仑.jpg",
    "委中": "委中.jpg",
    "足三里": "足三里.jpg",
    "三阴交": "三阴交.jpg",
    "血海": "血海.jpg",
    "涌泉": "涌泉.jpg",
    "太冲": "太冲.jpg",  # 可能需要（解溪 太冲.jpg包含）
    "膻中": "膻中.jpg",
    "中脘": "膻中 中庭 上中下脘 神阙.jpg",  # 组合图
    "关元": "神阙 气海 关元 中极.jpg",  # 组合图
    "气海": "神阙 气海 关元 中极.jpg",  # 组合图
    "神阙": "神阙 气海 关元 中极.jpg",  # 组合图
    "天枢": "天枢 神阙.jpg",  # 组合图
    "肾俞": "肾俞.jpg",
    "命门": "命门.jpg",
    "大椎": "大椎 膈俞 至阳.jpg",  # 组合图
    "风池": "风池.jpg",  # 可能需要
    "百会": "百会.jpg",  # 可能需要
    "太阳": "太阳.jpg",  # 可能需要
    "四神聪": "四神聪.jpg",  # 可能需要
    "劳宫": "劳宫.jpg",
    "阳池": "阳池.jpg",
    "阳溪": "阳溪.jpg",
    "阳谷": "阳谷.jpg",
    "阴陵泉": "阴陵泉.jpg",
    "阳陵泉": "阳陵泉.jpg",  # 可能需要
    "悬钟": "悬钟.jpg",
    "行间": "行间.jpg",
    "期门": "期门.jpg",
    "肩髃": "肩髃.jpg",
    "肩髎": "肩髎.jpg",
    "肩贞": "肩贞.jpg",
    "手三里": "手三里.jpg",
    "孔最": "孔最.jpg",
    "尺泽": "尺泽.jpg",
    "鱼际": "鱼际.jpg",
    "腕骨": "腕骨.jpg",
    "养老": "养老.jpg",
    "大陵": "大陵.jpg",
    "曲泽": "曲泽.jpg",
    "承山": "承山.jpg",
    "解溪": "解溪.jpg",
    "内庭": "内庭.jpg",
    "膝眼": "膝眼.jpg",
    "中府": "中府.jpg",  # 可能需要
    "云门": "云门.jpg",  # 可能需要
    "膺窗": "膺窗.jpg",  # 可能需要
}

# 已知的详细穴位数据（约30个）
KNOWN_POINTS = {
    "GV20": {
        "name": "百会",
        "location": "后发际正中直上7寸，当两耳尖直上，头顶正中。",
        "simple_location": "两耳尖连线中点，头顶正中央。",
        "efficacy": ["升阳举陷", "益气固脱", "安神醒脑"],
        "indications": ["头痛", "眩晕", "失眠", "健忘", "中风", "脱肛"],
        "massage": "用指腹或掌心按揉，力度适中。",
        "has_image": False
    },
    "EX-HN1": {
        "name": "四神聪",
        "location": "在头顶部，当百会前后左右各1寸，共4穴。",
        "simple_location": "百会穴前后左右各1拇指宽处。",
        "efficacy": ["镇静安神", "清头明目"],
        "indications": ["头痛", "眩晕", "失眠", "健忘", "癫痫"],
        "massage": "用手指逐一按揉或四指同时按揉。",
        "has_image": False
    },
    "EX-HN5": {
        "name": "太阳",
        "location": "在颞部，当眉梢与目外眦之间，向后约一横指的凹陷处。",
        "simple_location": "眉梢与眼角之间向后约1指宽的凹陷处。",
        "efficacy": ["清热明目", "通络止痛"],
        "indications": ["偏头痛", "目赤肿痛", "牙痛"],
        "massage": "用拇指或食指指腹按揉。",
        "has_image": False
    },
    "GB20": {
        "name": "风池",
        "location": "在项部，当枕骨之下，与风府相平，胸锁乳突肌与斜方肌上端之间的凹陷处。",
        "simple_location": "后脑勺下方，颈部肌肉外侧凹陷处。",
        "efficacy": ["疏风解表", "清头明目"],
        "indications": ["感冒", "头痛", "颈椎病", "视力下降"],
        "massage": "双手拇指按揉，有酸胀感为宜。",
        "has_image": False
    },
    "CV12": {
        "name": "中脘",
        "location": "在上腹部，前正中线上，当脐中上4寸。",
        "simple_location": "肚脐正上方4横指处。",
        "efficacy": ["健脾和胃", "补中益气"],
        "indications": ["胃痛", "腹胀", "呕吐", "消化不良"],
        "massage": "用掌心或指腹顺时针按揉。",
        "has_image": True
    },
    "CV4": {
        "name": "关元",
        "location": "在下腹部，前正中线上，当脐中下3寸。",
        "simple_location": "肚脐正下方4横指处。",
        "efficacy": ["培元固本", "补益下焦"],
        "indications": ["月经不调", "痛经", "阳痿", "遗精", "虚劳"],
        "massage": "用掌心温热按揉，或艾灸。",
        "has_image": True
    },
    "LI4": {
        "name": "合谷",
        "location": "在手背，第1、2掌骨间，当第二掌骨桡侧的中点处。",
        "simple_location": "拇指、食指合拢，肌肉最高处。",
        "efficacy": ["镇痛通络", "清热解表"],
        "indications": ["头痛", "牙痛", "感冒", "面瘫"],
        "massage": "用拇指指腹用力按压，有酸胀感。",
        "has_image": True
    },
    "PC6": {
        "name": "内关",
        "location": "在前臂掌侧，当曲泽与大陵的连线上，腕横纹上2寸，掌长肌腱与桡侧腕屈肌腱之间。",
        "simple_location": "手腕横纹往上3横指，两筋之间。",
        "efficacy": ["宁心安神", "理气止痛"],
        "indications": ["心悸", "胸闷", "胃痛", "恶心呕吐"],
        "massage": "用拇指指甲垂直按压。",
        "has_image": True
    },
    "ST36": {
        "name": "足三里",
        "location": "在小腿前外侧，当犊鼻下3寸，距胫骨前缘一横指（中指）。",
        "simple_location": "外膝眼下4横指，胫骨旁开1横指。",
        "efficacy": ["健脾和胃", "扶正培元", "通经活络"],
        "indications": ["胃痛", "呕吐", "腹胀", "消化不良", "虚劳"],
        "massage": "用拇指指腹按揉，或艾灸。",
        "has_image": True
    },
    "SP6": {
        "name": "三阴交",
        "location": "小腿内侧，当足内踝尖上3寸，胫骨内侧缘后方。",
        "simple_location": "内踝尖直上4横指，胫骨后缘。",
        "efficacy": ["健脾益胃", "调肝补肾", "调经止带"],
        "indications": ["月经不调", "痛经", "带下", "不孕", "失眠", "腹胀", "消化不良"],
        "massage": "用拇指指腹按揉，力度适中，有酸胀感为宜。",
        "has_image": True
    },
    "LR3": {
        "name": "太冲",
        "location": "足背侧，第一、二跖骨结合部之前凹陷处。",
        "simple_location": "大脚趾和二脚趾缝间向上推，推到骨头结合处的凹陷。",
        "efficacy": ["疏肝理气", "平肝潜阳", "清利头目"],
        "indications": ["头痛", "眩晕", "失眠", "高血压", "月经不调", "情绪烦躁"],
        "massage": "用拇指指腹向脚趾方向推按，或者点按。",
        "has_image": True
    },
    "KI1": {
        "name": "涌泉",
        "location": "足底部，卷足时足前部凹陷处，约当足底第2、3趾趾缝纹头端与足跟连线的前1/3与后2/3交点上。",
        "simple_location": "脚底前1/3处，弯曲脚趾时的凹陷中。",
        "efficacy": ["滋阴益肾", "平肝熄风", "安神定志"],
        "indications": ["头痛", "眩晕", "失眠", "高血压", "咽喉肿痛", "便秘"],
        "massage": "用拇指指腹用力按揉，或者用手掌心搓热后摩擦。",
        "has_image": True
    },
    "GV14": {
        "name": "大椎",
        "location": "后正中线上，第七颈椎棘突下凹陷中。",
        "simple_location": "低头时颈后最突出的骨头下方。",
        "efficacy": ["清热解表", "截疟止痫", "益气壮阳"],
        "indications": ["感冒", "发热", "咳嗽", "颈椎病", "肩背痛"],
        "massage": "用手掌心搓热后摩擦，或者用中指按揉。",
        "has_image": True
    },
    "BL23": {
        "name": "肾俞",
        "location": "腰部，当第2腰椎棘突下，旁开1.5寸。",
        "simple_location": "肚脐正对后背位置，脊柱旁开两指宽处。",
        "efficacy": ["补肾益气", "强腰利水", "聪耳明目"],
        "indications": ["腰痛", "遗精", "阳痿", "月经不调", "耳鸣", "耳聋"],
        "massage": "用双手拇指按揉，或者用手掌摩擦腰部。",
        "has_image": True
    },
    "CV6": {
        "name": "气海",
        "location": "下腹部，前正中线上，当脐中下1.5寸。",
        "simple_location": "肚脐直下1.5寸（约两横指）。",
        "efficacy": ["益气助阳", "调经固经"],
        "indications": ["腹痛", "泄泻", "便秘", "遗尿", "阳痿", "月经不调"],
        "massage": "用手掌心轻柔按揉。",
        "has_image": True
    },
    "LU1": {
        "name": "中府",
        "location": "在胸前壁的外上方，云门下1寸，平第1肋间隙，距前正中线6寸。",
        "simple_location": "锁骨外端下方凹陷直下1寸。",
        "efficacy": ["止咳平喘", "清肺化痰"],
        "indications": ["咳嗽", "气喘", "胸痛", "肩背痛"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "LU7": {
        "name": "列缺",
        "location": "在前臂桡侧缘，桡骨茎突上方，腕横纹上1.5寸。",
        "simple_location": "两手虎口交叉，食指尖所指凹陷处。",
        "efficacy": ["宣肺解表", "通经活络"],
        "indications": ["咳嗽", "气喘", "头痛", "颈项强痛", "牙痛"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "LI11": {
        "name": "曲池",
        "location": "在肘横纹外侧端，屈肘，当尺泽与肱骨外上髁连线中点。",
        "simple_location": "屈肘成直角，肘横纹外侧端。",
        "efficacy": ["清热解表", "调和气血"],
        "indications": ["发热", "咽喉肿痛", "手臂肿痛", "高血压"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "LI20": {
        "name": "迎香",
        "location": "在鼻翼外缘中点旁，当鼻唇沟中。",
        "simple_location": "鼻翼旁开约1厘米皱纹中。",
        "efficacy": ["通利鼻窍", "疏风散热"],
        "indications": ["鼻塞", "鼻渊", "面痒", "口歪"],
        "massage": "用食指指腹按揉。",
        "has_image": False
    },
    "ST25": {
        "name": "天枢",
        "location": "在腹中部，距脐中2寸。",
        "simple_location": "肚脐旁开3指宽。",
        "efficacy": ["理气止痛", "通便"],
        "indications": ["腹痛", "腹胀", "便秘", "泄泻", "痛经"],
        "massage": "用拇指或掌根按揉。",
        "has_image": True
    },
    "SP10": {
        "name": "血海",
        "location": "屈膝，在大腿内侧，髌底内侧端上2寸，当股四头肌内侧头的隆起处。",
        "simple_location": "坐在椅子上，腿绷直，膝盖内侧上方肌肉隆起最高处。",
        "efficacy": ["活血化瘀", "补血养血"],
        "indications": ["月经不调", "痛经", "皮肤瘙痒", "贫血"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "HT7": {
        "name": "神门",
        "location": "在腕部，腕掌侧横纹尺侧端，尺侧腕屈肌腱的桡侧凹陷处。",
        "simple_location": "手腕横纹小指侧端凹陷处。",
        "efficacy": ["宁心安神", "清火凉血"],
        "indications": ["失眠", "健忘", "心悸", "心烦"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "SI3": {
        "name": "后溪",
        "location": "在手掌尺侧，微握拳，当第5掌指关节后的远侧掌横纹头赤白肉际。",
        "simple_location": "握拳，小指侧掌横纹突起处。",
        "efficacy": ["清心安神", "通督脉"],
        "indications": ["头项强痛", "腰背痛", "手指麻木", "耳聋"],
        "massage": "用拇指指甲掐按。",
        "has_image": False
    },
    "BL40": {
        "name": "委中",
        "location": "在腘横纹中点，当股二头肌腱与半腱肌腱的中间。",
        "simple_location": "膝盖后窝正中点。",
        "efficacy": ["舒筋活络", "凉血解毒"],
        "indications": ["腰痛", "下肢痿痹", "腹痛", "吐泻"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "BL60": {
        "name": "昆仑",
        "location": "在足部外踝后方，当外踝尖与跟腱之间的凹陷处。",
        "simple_location": "外踝尖与脚跟腱连线中点凹陷处。",
        "efficacy": ["安神清热", "舒筋活络"],
        "indications": ["头痛", "项强", "腰骶痛", "足跟肿痛"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "KI3": {
        "name": "太溪",
        "location": "在足内侧，内踝后方，当内踝尖与跟腱之间的凹陷处。",
        "simple_location": "内踝尖与脚跟腱连线中点凹陷处。",
        "efficacy": ["滋阴益肾", "壮阳强腰"],
        "indications": ["月经不调", "失眠", "腰痛", "耳鸣", "牙痛"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "PC8": {
        "name": "劳宫",
        "location": "在手掌心，当第2、3掌骨之间偏于第3掌骨，握拳屈指时中指尖处。",
        "simple_location": "握拳，中指指尖触到的手掌心处。",
        "efficacy": ["清心火", "安神"],
        "indications": ["心痛", "心烦", "口疮", "口臭"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "TE5": {
        "name": "外关",
        "location": "在前臂背侧，当阳池与肘尖的连线上，腕背横纹上2寸，尺骨与桡骨之间。",
        "simple_location": "手腕背横纹上3横指，两骨之间。",
        "efficacy": ["清热解表", "通经活络"],
        "indications": ["头痛", "颊痛", "耳聋", "耳鸣", "落枕"],
        "massage": "用拇指按揉。",
        "has_image": True
    },
    "GB34": {
        "name": "阳陵泉",
        "location": "在小腿外侧，当腓骨头前下方凹陷处。",
        "simple_location": "膝盖外下方，腓骨小头前下方凹陷。",
        "efficacy": ["疏肝利胆", "舒筋活络"],
        "indications": ["黄疸", "口苦", "胁肋痛", "下肢痿痹"],
        "massage": "用拇指按揉。",
        "has_image": False
    },
    "LR14": {
        "name": "期门",
        "location": "在胸部，当乳头直下，第6肋间隙，前正中线旁开4寸。",
        "simple_location": "乳头直下，第六肋间隙。",
        "efficacy": ["疏肝理气", "健脾和胃"],
        "indications": ["胸胁胀痛", "呕吐", "呃逆", "乳痈"],
        "massage": "用掌根推揉。",
        "has_image": True
    },
    "GV26": {
        "name": "水沟",
        "location": "在面部，当人中沟的上1/3与中1/3交点处。",
        "simple_location": "人中沟上1/3处。",
        "efficacy": ["开窍醒神", "消肿止痛"],
        "indications": ["昏迷", "晕厥", "中暑", "腰脊强痛"],
        "massage": "用拇指指甲掐按。",
        "has_image": False
    },
    "CV17": {
        "name": "膻中",
        "location": "在胸部，前正中线上，平第4肋间，两乳头连线的中点。",
        "simple_location": "两乳头连线中点。",
        "efficacy": ["宽胸理气", "止咳平喘"],
        "indications": ["胸闷", "心痛", "咳嗽", "气喘", "乳少"],
        "massage": "用拇指或掌根按揉。",
        "has_image": True
    },
}

# 361标准穴位名称完整列表（WHO标准）
STANDARD_ACUPOINT_NAMES = {
    # 手太阴肺经 (11穴)
    "LU1": "中府", "LU2": "云门", "LU3": "天府", "LU4": "侠白", "LU5": "尺泽",
    "LU6": "孔最", "LU7": "列缺", "LU8": "经渠", "LU9": "太渊", "LU10": "鱼际", "LU11": "少商",

    # 手阳明大肠经 (20穴)
    "LI1": "商阳", "LI2": "二间", "LI3": "三间", "LI4": "合谷", "LI5": "阳溪",
    "LI6": "偏历", "LI7": "温溜", "LI8": "下廉", "LI9": "上廉", "LI10": "手三里",
    "LI11": "曲池", "LI12": "肘髎", "LI13": "手五里", "LI14": "臂臑", "LI15": "肩髃",
    "LI16": "巨骨", "LI17": "天鼎", "LI18": "扶突", "LI19": "口禾髎", "LI20": "迎香",

    # 足阳明胃经 (45穴)
    "ST1": "承泣", "ST2": "四白", "ST3": "巨髎", "ST4": "地仓", "ST5": "大迎",
    "ST6": "颊车", "ST7": "下关", "ST8": "头维", "ST9": "人迎", "ST10": "水突",
    "ST11": "气舍", "ST12": "缺盆", "ST13": "气户", "ST14": "库房", "ST15": "屋翳",
    "ST16": "膺窗", "ST17": "乳中", "ST18": "乳根", "ST19": "不容", "ST20": "承满",
    "ST21": "梁门", "ST22": "关门", "ST23": "太乙", "ST24": "滑肉门", "ST25": "天枢",
    "ST26": "外陵", "ST27": "大巨", "ST28": "水道", "ST29": "归来", "ST30": "气冲",
    "ST31": "髀关", "ST32": "伏兔", "ST33": "阴市", "ST34": "梁丘", "ST35": "犊鼻",
    "ST36": "足三里", "ST37": "上巨虚", "ST38": "条口", "ST39": "下巨虚", "ST40": "丰隆",
    "ST41": "解溪", "ST42": "冲阳", "ST43": "陷谷", "ST44": "内庭", "ST45": "厉兑",

    # 足太阴脾经 (21穴)
    "SP1": "隐白", "SP2": "大都", "SP3": "太白", "SP4": "公孙", "SP5": "商丘",
    "SP6": "三阴交", "SP7": "漏谷", "SP8": "地机", "SP9": "阴陵泉", "SP10": "血海",
    "SP11": "箕门", "SP12": "冲门", "SP13": "府舍", "SP14": "腹结", "SP15": "大横",
    "SP16": "腹哀", "SP17": "食窦", "SP18": "天溪", "SP19": "胸乡", "SP20": "周荣", "SP21": "大包",

    # 手少阴心经 (9穴)
    "HT1": "极泉", "HT2": "青灵", "HT3": "少海", "HT4": "灵道", "HT5": "通里",
    "HT6": "阴郄", "HT7": "神门", "HT8": "少府", "HT9": "少冲",

    # 手太阳小肠经 (19穴)
    "SI1": "少泽", "SI2": "前谷", "SI3": "后溪", "SI4": "腕骨", "SI5": "阳谷",
    "SI6": "养老", "SI7": "支正", "SI8": "小海", "SI9": "肩贞", "SI10": "臑俞",
    "SI11": "天宗", "SI12": "秉风", "SI13": "曲垣", "SI14": "肩外俞", "SI15": "肩中俞",
    "SI16": "天窗", "SI17": "天容", "SI18": "颧髎", "SI19": "听宫",

    # 足太阳膀胱经 (67穴)
    "BL1": "睛明", "BL2": "攒竹", "BL3": "眉冲", "BL4": "曲差", "BL5": "五处",
    "BL6": "承光", "BL7": "通天", "BL8": "络却", "BL9": "玉枕", "BL10": "天柱",
    "BL11": "大杼", "BL12": "风门", "BL13": "肺俞", "BL14": "厥阴俞", "BL15": "心俞",
    "BL16": "督俞", "BL17": "膈俞", "BL18": "肝俞", "BL19": "胆俞", "BL20": "脾俞",
    "BL21": "胃俞", "BL22": "三焦俞", "BL23": "肾俞", "BL24": "气海俞", "BL25": "大肠俞",
    "BL26": "关元俞", "BL27": "小肠俞", "BL28": "膀胱俞", "BL29": "中膂俞", "BL30": "白环俞",
    "BL31": "上髎", "BL32": "次髎", "BL33": "中髎", "BL34": "下髎", "BL35": "会阳",
    "BL36": "承扶", "BL37": "殷门", "BL38": "浮郄", "BL39": "委阳", "BL40": "委中",
    "BL41": "附分", "BL42": "魄户", "BL43": "膏肓", "BL44": "神堂", "BL45": "譩譆",
    "BL46": "膈关", "BL47": "魂门", "BL48": "阳纲", "BL49": "意舍", "BL50": "胃仓",
    "BL51": "肓门", "BL52": "志室", "BL53": "胞肓", "BL54": "秩边", "BL55": "合阳",
    "BL56": "承筋", "BL57": "承山", "BL58": "飞扬", "BL59": "跗阳", "BL60": "昆仑",
    "BL61": "仆参", "BL62": "申脉", "BL63": "金门", "BL64": "京骨", "BL65": "束骨",
    "BL66": "足通谷", "BL67": "至阴",

    # 足少阴肾经 (27穴)
    "KI1": "涌泉", "KI2": "然谷", "KI3": "太溪", "KI4": "大钟", "KI5": "水泉",
    "KI6": "照海", "KI7": "复溜", "KI8": "交信", "KI9": "筑宾", "KI10": "阴谷",
    "KI11": "横骨", "KI12": "大赫", "KI13": "气穴", "KI14": "四满", "KI15": "中注",
    "KI16": "肓俞", "KI17": "商曲", "KI18": "石关", "KI19": "阴都", "KI20": "腹通谷",
    "KI21": "幽门", "KI22": "步廊", "KI23": "神封", "KI24": "灵墟", "KI25": "神藏",
    "KI26": "彧中", "KI27": "俞府",

    # 手厥阴心包经 (9穴)
    "PC1": "天池", "PC2": "天泉", "PC3": "曲泽", "PC4": "郄门", "PC5": "间使",
    "PC6": "内关", "PC7": "大陵", "PC8": "劳宫", "PC9": "中冲",

    # 手少阳三焦经 (23穴)
    "TE1": "关冲", "TE2": "液门", "TE3": "中渚", "TE4": "阳池", "TE5": "外关",
    "TE6": "支沟", "TE7": "会宗", "TE8": "三阳络", "TE9": "四渎", "TE10": "天井",
    "TE11": "清冷渊", "TE12": "消泺", "TE13": "臑会", "TE14": "肩髎", "TE15": "天髎",
    "TE16": "天牖", "TE17": "翳风", "TE18": "瘈脉", "TE19": "颅息", "TE20": "角孙",
    "TE21": "耳门", "TE22": "和髎", "TE23": "丝竹空",

    # 足少阳胆经 (44穴)
    "GB1": "瞳子髎", "GB2": "听会", "GB3": "上关", "GB4": "颔厌", "GB5": "悬颅",
    "GB6": "悬厘", "GB7": "曲鬓", "GB8": "率谷", "GB9": "天冲", "GB10": "浮白",
    "GB11": "头窍阴", "GB12": "完骨", "GB13": "本神", "GB14": "阳白", "GB15": "头临泣",
    "GB16": "目窗", "GB17": "正营", "GB18": "承灵", "GB19": "脑空", "GB20": "风池",
    "GB21": "肩井", "GB22": "渊腋", "GB23": "辄筋", "GB24": "日月", "GB25": "京门",
    "GB26": "带脉", "GB27": "五枢", "GB28": "维道", "GB29": "居髎", "GB30": "环跳",
    "GB31": "风市", "GB32": "中渎", "GB33": "膝阳关", "GB34": "阳陵泉", "GB35": "阳交",
    "GB36": "外丘", "GB37": "光明", "GB38": "阳辅", "GB39": "悬钟", "GB40": "丘墟",
    "GB41": "足临泣", "GB42": "地五会", "GB43": "侠溪", "GB44": "足窍阴",

    # 足厥阴肝经 (14穴)
    "LR1": "大敦", "LR2": "行间", "LR3": "太冲", "LR4": "中封", "LR5": "蠡沟",
    "LR6": "中都", "LR7": "膝关", "LR8": "曲泉", "LR9": "阴包", "LR10": "足五里",
    "LR11": "阴廉", "LR12": "急脉", "LR13": "章门", "LR14": "期门",

    # 督脉 (28穴)
    "GV1": "长强", "GV2": "腰俞", "GV3": "腰阳关", "GV4": "命门", "GV5": "悬枢",
    "GV6": "脊中", "GV7": "中枢", "GV8": "筋缩", "GV9": "至阳", "GV10": "灵台",
    "GV11": "神道", "GV12": "身柱", "GV13": "陶道", "GV14": "大椎", "GV15": "哑门",
    "GV16": "风府", "GV17": "脑户", "GV18": "强间", "GV19": "后顶", "GV20": "百会",
    "GV21": "前顶", "GV22": "囟会", "GV23": "上星", "GV24": "神庭", "GV25": "素髎",
    "GV26": "水沟", "GV27": "兑端", "GV28": "龈交",

    # 任脉 (24穴)
    "CV1": "会阴", "CV2": "曲骨", "CV3": "中极", "CV4": "关元", "CV5": "石门",
    "CV6": "气海", "CV7": "阴交", "CV8": "神阙", "CV9": "水分", "CV10": "下脘",
    "CV11": "建里", "CV12": "中脘", "CV13": "上脘", "CV14": "巨阙", "CV15": "鸠尾",
    "CV16": "中庭", "CV17": "膻中", "CV18": "玉堂", "CV19": "紫宫", "CV20": "华盖",
    "CV21": "璇玑", "CV22": "天突", "CV23": "廉泉", "CV24": "承浆",
}

# 经外奇穴（部分常用）
EXTRA_POINTS = {
    "EX-HN1": "四神聪",
    "EX-HN5": "太阳",
}


def _get_image_url(code: str, name: str) -> str:
    """获取穴位图片URL"""
    # 首先尝试通过代码查找图片
    try:
        from .acupoint_image_mapping import get_image_for_acupoint
        image_file = get_image_for_acupoint(code)
        if image_file and image_file != "default.png":
            return f"/static/acupoints/{image_file}"
    except ImportError:
        pass

    # 回退到通过名称查找
    if name in AVAILABLE_IMAGES:
        return f"/static/acupoints/{AVAILABLE_IMAGES[name]}"
    return "/static/acupoints/default.png"


def _get_anatomical_image_url(meridian_code: str) -> str:
    """获取经络解剖图URL"""
    if meridian_code in MERIDIANS:
        gif_name = MERIDIANS[meridian_code]["gif"]
        return f"/static/meridians/{gif_name}"
    return "/static/meridians/default.gif"


def generate_comprehensive_acupoints():
    """生成361个标准穴位完整数据"""
    data = []

    # 1. 生成十四经穴 (361个)
    for meridian_code, info in MERIDIANS.items():
        count = info["count"]
        meridian_name = info["name"]
        body_part = info["part"]
        meridian_gif = info["gif"]

        for i in range(1, count + 1):
            code = f"{meridian_code}{i}"

            # 获取标准名称
            if code in STANDARD_ACUPOINT_NAMES:
                name = STANDARD_ACUPOINT_NAMES[code]
            else:
                name = f"{meridian_name}第{i}穴"

            # 检查是否是已知详细穴位
            if code in KNOWN_POINTS:
                point = KNOWN_POINTS[code]
                entry = {
                    "name": f"{name}穴" if not name.endswith("穴") else name,
                    "code": code,
                    "meridian": meridian_name,
                    "body_part": body_part,
                    "location": point["location"],
                    "simple_location": point["simple_location"],
                    "efficacy": point["efficacy"],
                    "indications": point["indications"],
                    "massage_method": point["massage"],
                    "image_url": _get_image_url(code, name),
                    "anatomical_image_url": f"/static/meridians/{meridian_gif}",
                    "model_3d_url": ""
                }
            else:
                # 生成标准占位数据
                entry = {
                    "name": f"{name}穴" if not name.endswith("穴") else name,
                    "code": code,
                    "meridian": meridian_name,
                    "body_part": body_part,
                    "location": f"{name}的定位待完善",
                    "simple_location": "暂无简易取穴法",
                    "efficacy": ["待补充"],
                    "indications": ["待补充"],
                    "massage_method": "一般按摩方法：按揉或点按。",
                    "image_url": _get_image_url(code, name),
                    "anatomical_image_url": f"/static/meridians/{meridian_gif}",
                    "model_3d_url": ""
                }

            data.append(entry)

    # 2. 添加经外奇穴
    for code, name in EXTRA_POINTS.items():
        if code in KNOWN_POINTS:
            point = KNOWN_POINTS[code]
            entry = {
                "name": f"{name}穴" if not name.endswith("穴") else name,
                "code": code,
                "meridian": "经外奇穴",
                "body_part": "其他",
                "location": point["location"],
                "simple_location": point["simple_location"],
                "efficacy": point["efficacy"],
                "indications": point["indications"],
                "massage_method": point["massage"],
                "image_url": _get_image_url(code, name),
                "anatomical_image_url": "/static/meridians/default.gif",
                "model_3d_url": ""
            }
        else:
            entry = {
                "name": f"{name}穴" if not name.endswith("穴") else name,
                "code": code,
                "meridian": "经外奇穴",
                "body_part": "其他",
                "location": f"{name}的定位待完善",
                "simple_location": "暂无简易取穴法",
                "efficacy": ["待补充"],
                "indications": ["待补充"],
                "massage_method": "一般按摩方法：按揉或点按。",
                "image_url": _get_image_url(code, name),
                "anatomical_image_url": "/static/meridians/default.gif",
                "model_3d_url": ""
            }
        data.append(entry)

    return data


# 导出生成的列表
ACUPOINTS_DATA = generate_comprehensive_acupoints()

# 打印统计信息
if __name__ == "__main__":
    print(f"Total acupoints: {len(ACUPOINTS_DATA)}")
    print(f"Standard meridian points: {sum(m['count'] for m in MERIDIANS.values())}")
    print(f"Extra points: {len(EXTRA_POINTS)}")
    print(f"\nMeridian breakdown:")
    for code, info in MERIDIANS.items():
        print(f"  {code} ({info['name']}): {info['count']} points")
