
MERIDIANS = {
    "LU": {"name": "手太阴肺经", "count": 11, "part": "上肢"},
    "LI": {"name": "手阳明大肠经", "count": 20, "part": "上肢"},
    "ST": {"name": "足阳明胃经", "count": 45, "part": "下肢"},
    "SP": {"name": "足太阴脾经", "count": 21, "part": "下肢"},
    "HT": {"name": "手少阴心经", "count": 9, "part": "上肢"},
    "SI": {"name": "手太阳小肠经", "count": 19, "part": "上肢"},
    "BL": {"name": "足太阳膀胱经", "count": 67, "part": "背部"},
    "KI": {"name": "足少阴肾经", "count": 27, "part": "下肢"},
    "PC": {"name": "手厥阴心包经", "count": 9, "part": "上肢"},
    "TE": {"name": "手少阳三焦经", "count": 23, "part": "上肢"},
    "GB": {"name": "足少阳胆经", "count": 44, "part": "下肢"},
    "LR": {"name": "足厥阴肝经", "count": 14, "part": "下肢"},
    "GV": {"name": "督脉", "count": 28, "part": "背部"},
    "CV": {"name": "任脉", "count": 24, "part": "胸腹部"},
}

# Known points with details (Top ~50 commonly used)
KNOWN_POINTS = {
    "GV20": {"name": "百会", "location": "后发际正中直上7寸，当两耳尖直上，头顶正中。", "simple_location": "两耳尖连线中点，头顶正中央。", "efficacy": ["升阳举陷", "益气固脱", "安神醒脑"], "indications": ["头痛", "眩晕", "失眠", "健忘", "中风", "脱肛"], "massage": "用指腹或掌心按揉，力度适中。"},
    "EX-HN1": {"name": "四神聪", "location": "在头顶部，当百会前后左右各1寸，共4穴。", "simple_location": "百会穴前后左右各1拇指宽处。", "efficacy": ["镇静安神", "清头明目"], "indications": ["头痛", "眩晕", "失眠", "健忘", "癫痫"], "massage": "用手指逐一按揉或四指同时按揉。"},
    "GB20": {"name": "风池", "location": "在项部，当枕骨之下，与风府相平，胸锁乳突肌与斜方肌上端之间的凹陷处。", "simple_location": "后脑勺下方，颈部肌肉外侧凹陷处。", "efficacy": ["疏风解表", "清头明目"], "indications": ["感冒", "头痛", "颈椎病", "视力下降"], "massage": "双手拇指按揉，有酸胀感为宜。"},
    "CV12": {"name": "中脘", "location": "在上腹部，前正中线上，当脐中上4寸。", "simple_location": "肚脐正上方4横指处（3寸+1寸）。", "efficacy": ["健脾和胃", "补中益气"], "indications": ["胃痛", "腹胀", "呕吐", "消化不良"], "massage": "用掌心或指腹顺时针按揉。"},
    "CV4": {"name": "关元", "location": "在下腹部，前正中线上，当脐中下3寸。", "simple_location": "肚脐正下方4横指处。", "efficacy": ["培元固本", "补益下焦"], "indications": ["月经不调", "痛经", "阳痿", "遗精", "虚劳"], "massage": "用掌心温热按揉，或艾灸。"},
    "LI4": {"name": "合谷", "location": "在手背，第1、2掌骨间，当第二掌骨桡侧的中点处。", "simple_location": "拇指、食指合拢，肌肉最高处。", "efficacy": ["镇痛通络", "清热解表"], "indications": ["头痛", "牙痛", "感冒", "面瘫"], "massage": "用拇指指腹用力按压，有酸胀感。"},
    "PC6": {"name": "内关", "location": "在前臂掌侧，当曲泽与大陵的连线上，腕横纹上2寸，掌长肌腱与桡侧腕屈肌腱之间。", "simple_location": "手腕横纹往上3横指，两筋之间。", "efficacy": ["宁心安神", "理气止痛"], "indications": ["心悸", "胸闷", "胃痛", "恶心呕吐"], "massage": "用拇指指甲垂直按压。"},
    "ST36": {"name": "足三里", "location": "在小腿前外侧，当犊鼻下3寸，距胫骨前缘一横指（中指）。", "simple_location": "外膝眼下4横指，胫骨旁开1横指。", "efficacy": ["健脾和胃", "扶正培元", "通经活络"], "indications": ["胃痛", "呕吐", "腹胀", "消化不良", "虚劳"], "massage": "用拇指指腹按揉，或艾灸。"},
    "SP6": {"name": "三阴交", "location": "小腿内侧，当足内踝尖上3寸，胫骨内侧缘后方。", "simple_location": "内踝尖直上4横指，胫骨后缘。", "efficacy": ["健脾益胃", "调肝补肾", "调经止带"], "indications": ["月经不调", "痛经", "带下", "不孕", "失眠", "腹胀", "消化不良"], "massage": "用拇指指腹按揉，力度适中，有酸胀感为宜。"},
    "LR3": {"name": "太冲", "location": "足背侧，第一、二跖骨结合部之前凹陷处。", "simple_location": "大脚趾和二脚趾缝间向上推，推到骨头结合处的凹陷。", "efficacy": ["疏肝理气", "平肝潜阳", "清利头目"], "indications": ["头痛", "眩晕", "失眠", "高血压", "月经不调", "情绪烦躁"], "massage": "用拇指指腹向脚趾方向推按，或者点按。"},
    "KI1": {"name": "涌泉", "location": "足底部，卷足时足前部凹陷处，约当足底第2、3趾趾缝纹头端与足跟连线的前1/3与后2/3交点上。", "simple_location": "脚底前1/3处，弯曲脚趾时的凹陷中。", "efficacy": ["滋阴益肾", "平肝熄风", "安神定志"], "indications": ["头痛", "眩晕", "失眠", "高血压", "咽喉肿痛", "便秘"], "massage": "用拇指指腹用力按揉，或者用手掌心搓热后摩擦。"},
    "GV14": {"name": "大椎", "location": "后正中线上，第七颈椎棘突下凹陷中。", "simple_location": "低头时颈后最突出的骨头下方。", "efficacy": ["清热解表", "截疟止痫", "益气壮阳"], "indications": ["感冒", "发热", "咳嗽", "颈椎病", "肩背痛"], "massage": "用手掌心搓热后摩擦，或者用中指按揉。"},
    "BL23": {"name": "肾俞", "location": "腰部，当第2腰椎棘突下，旁开1.5寸。", "simple_location": "肚脐正对后背位置，脊柱旁开两指宽处。", "efficacy": ["补肾益气", "强腰利水", "聪耳明目"], "indications": ["腰痛", "遗精", "阳痿", "月经不调", "耳鸣", "耳聋"], "massage": "用双手拇指按揉，或者用手掌摩擦腰部。"},
    "CV6": {"name": "气海", "location": "下腹部，前正中线上，当脐中下1.5寸。", "simple_location": "肚脐直下1.5寸（约两横指）。", "efficacy": ["益气助阳", "调经固经"], "indications": ["腹痛", "泄泻", "便秘", "遗尿", "阳痿", "月经不调"], "massage": "用手掌心轻柔按揉。"},
    "LU1": {"name": "中府", "location": "在胸前壁的外上方，云门下1寸，平第1肋间隙，距前正中线6寸。", "simple_location": "锁骨外端下方凹陷直下1寸。", "efficacy": ["止咳平喘", "清肺化痰"], "indications": ["咳嗽", "气喘", "胸痛", "肩背痛"], "massage": "用拇指按揉。"},
    "LU7": {"name": "列缺", "location": "在前臂桡侧缘，桡骨茎突上方，腕横纹上1.5寸。", "simple_location": "两手虎口交叉，食指尖所指凹陷处。", "efficacy": ["宣肺解表", "通经活络"], "indications": ["咳嗽", "气喘", "头痛", "颈项强痛", "牙痛"], "massage": "用拇指按揉。"},
    "LI11": {"name": "曲池", "location": "在肘横纹外侧端，屈肘，当尺泽与肱骨外上髁连线中点。", "simple_location": "屈肘成直角，肘横纹外侧端。", "efficacy": ["清热解表", "调和气血"], "indications": ["发热", "咽喉肿痛", "手臂肿痛", "高血压"], "massage": "用拇指按揉。"},
    "LI20": {"name": "迎香", "location": "在鼻翼外缘中点旁，当鼻唇沟中。", "simple_location": "鼻翼旁开约1厘米皱纹中。", "efficacy": ["通利鼻窍", "疏风散热"], "indications": ["鼻塞", "鼻渊", "面痒", "口歪"], "massage": "用食指指腹按揉。"},
    "ST25": {"name": "天枢", "location": "在腹中部，距脐中2寸。", "simple_location": "肚脐旁开3指宽。", "efficacy": ["理气止痛", "通便"], "indications": ["腹痛", "腹胀", "便秘", "泄泻", "痛经"], "massage": "用拇指或掌根按揉。"},
    "SP10": {"name": "血海", "location": "屈膝，在大腿内侧，髌底内侧端上2寸，当股四头肌内侧头的隆起处。", "simple_location": "坐在椅子上，腿绷直，膝盖内侧上方肌肉隆起最高处。", "efficacy": ["活血化瘀", "补血养血"], "indications": ["月经不调", "痛经", "皮肤瘙痒", "贫血"], "massage": "用拇指按揉。"},
    "HT7": {"name": "神门", "location": "在腕部，腕掌侧横纹尺侧端，尺侧腕屈肌腱的桡侧凹陷处。", "simple_location": "手腕横纹小指侧端凹陷处。", "efficacy": ["宁心安神", "清火凉血"], "indications": ["失眠", "健忘", "心悸", "心烦"], "massage": "用拇指按揉。"},
    "SI3": {"name": "后溪", "location": "在手掌尺侧，微握拳，当第5掌指关节后的远侧掌横纹头赤白肉际。", "simple_location": "握拳，小指侧掌横纹突起处。", "efficacy": ["清心安神", "通督脉"], "indications": ["头项强痛", "腰背痛", "手指麻木", "耳聋"], "massage": "用拇指指甲掐按。"},
    "BL40": {"name": "委中", "location": "在腘横纹中点，当股二头肌腱与半腱肌腱的中间。", "simple_location": "膝盖后窝正中点。", "efficacy": ["舒筋活络", "凉血解毒"], "indications": ["腰痛", "下肢痿痹", "腹痛", "吐泻"], "massage": "用拇指按揉。"},
    "BL60": {"name": "昆仑", "location": "在足部外踝后方，当外踝尖与跟腱之间的凹陷处。", "simple_location": "外踝尖与脚跟腱连线中点凹陷处。", "efficacy": ["安神清热", "舒筋活络"], "indications": ["头痛", "项强", "腰骶痛", "足跟肿痛"], "massage": "用拇指按揉。"},
    "KI3": {"name": "太溪", "location": "在足内侧，内踝后方，当内踝尖与跟腱之间的凹陷处。", "simple_location": "内踝尖与脚跟腱连线中点凹陷处。", "efficacy": ["滋阴益肾", "壮阳强腰"], "indications": ["月经不调", "失眠", "腰痛", "耳鸣", "牙痛"], "massage": "用拇指按揉。"},
    "PC8": {"name": "劳宫", "location": "在手掌心，当第2、3掌骨之间偏于第3掌骨，握拳屈指时中指尖处。", "simple_location": "握拳，中指指尖触到的手掌心处。", "efficacy": ["清心火", "安神"], "indications": ["心痛", "心烦", "口疮", "口臭"], "massage": "用拇指按揉。"},
    "TE5": {"name": "外关", "location": "在前臂背侧，当阳池与肘尖的连线上，腕背横纹上2寸，尺骨与桡骨之间。", "simple_location": "手腕背横纹上3横指，两骨之间。", "efficacy": ["清热解表", "通经活络"], "indications": ["头痛", "颊痛", "耳聋", "耳鸣", "落枕"], "massage": "用拇指按揉。"},
    "GB34": {"name": "阳陵泉", "location": "在小腿外侧，当腓骨头前下方凹陷处。", "simple_location": "膝盖外下方，腓骨小头前下方凹陷。", "efficacy": ["疏肝利胆", "舒筋活络"], "indications": ["黄疸", "口苦", "胁肋痛", "下肢痿痹"], "massage": "用拇指按揉。"},
    "LR14": {"name": "期门", "location": "在胸部，当乳头直下，第6肋间隙，前正中线旁开4寸。", "simple_location": "乳头直下，第六肋间隙。", "efficacy": ["疏肝理气", "健脾和胃"], "indications": ["胸胁胀痛", "呕吐", "呃逆", "乳痈"], "massage": "用掌根推揉。"},
    "GV26": {"name": "水沟", "location": "在面部，当人中沟的上1/3与中1/3交点处。", "simple_location": "人中沟上1/3处。", "efficacy": ["开窍醒神", "消肿止痛"], "indications": ["昏迷", "晕厥", "中暑", "腰脊强痛"], "massage": "用拇指指甲掐按。"},
    "CV17": {"name": "膻中", "location": "在胸部，前正中线上，平第4肋间，两乳头连线的中点。", "simple_location": "两乳头连线中点。", "efficacy": ["宽胸理气", "止咳平喘"], "indications": ["胸闷", "心痛", "咳嗽", "气喘", "乳少"], "massage": "用拇指或掌根按揉。"},
}

def generate_data():
    data = []
    
    # Generate standard points
    for meridian_code, info in MERIDIANS.items():
        count = info["count"]
        meridian_name = info["name"]
        default_part = info["part"]
        
        for i in range(1, count + 1):
            code = f"{meridian_code}{i}"
            
            # Use known info if available
            if code in KNOWN_POINTS:
                point = KNOWN_POINTS[code]
                # Try to add "穴" to name if not present (optional, but consistent)
                name = point["name"]
                if not name.endswith("穴"):
                    name += "穴"
                
                entry = {
                    "name": name,
                    "code": code,
                    "meridian": meridian_name,
                    "body_part": default_part, # Can be refined if we had more data
                    "location": point["location"],
                    "simple_location": point["simple_location"],
                    "efficacy": point["efficacy"],
                    "indications": point["indications"],
                    "massage_method": point["massage"],
                    "image_url": f"/static/acupoints/{point['name'].replace('穴','')}.jpg" # Try to match pinyin later or just use name
                }
                
                # Correction for image url to use pinyin if we can (hardcoded for now)
                # But for the generated file, we'll keep it simple or fix specific ones
                # We already have a pinyin mapping in previous steps, but here we generate the file.
                # Let's just use a standard placeholder or specific ones we know.
                
            else:
                # Generic entry
                entry = {
                    "name": f"{meridian_name}第{i}穴", # Placeholder name
                    "code": code,
                    "meridian": meridian_name,
                    "body_part": default_part,
                    "location": "定位数据待完善",
                    "simple_location": "暂无简易取穴法",
                    "efficacy": ["待补充"],
                    "indications": ["待补充"],
                    "massage_method": "一般按摩方法：按揉或点按。",
                    "image_url": "/static/acupoints/default.png"
                }
            
            data.append(entry)
            
    # Add Extra Points (EX) if needed, we have some in KNOWN_POINTS
    for code, point in KNOWN_POINTS.items():
        if code.startswith("EX"):
            name = point["name"]
            if not name.endswith("穴"):
                name += "穴"
            entry = {
                "name": name,
                "code": code,
                "meridian": "经外奇穴",
                "body_part": "其他",
                "location": point["location"],
                "simple_location": point["simple_location"],
                "efficacy": point["efficacy"],
                "indications": point["indications"],
                "massage_method": point["massage"],
                "image_url": f"/static/acupoints/{point['name'].replace('穴','')}.jpg"
            }
            # Check if already added (unlikely since EX codes are not in standard loops)
            data.append(entry)

    # Sort by code
    return data

if __name__ == "__main__":
    import json
    data = generate_data()
    
    with open(r"e:\a_shangzhan\traditional_chinese_medicine\backend\api\data\full_acupoints.py", "w", encoding="utf-8") as f:
        f.write('"""\nFull Acupoints Data (Generated)\n"""\n\n')
        f.write("ACUPOINTS_DATA = [\n")
        for item in data:
            f.write(f"    {json.dumps(item, ensure_ascii=False)},\n")
        f.write("]\n")
    
    print("Done generating full_acupoints.py")
