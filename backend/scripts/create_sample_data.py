"""
创建 Phase 1 示例数据
Create sample data for Phase 1 features
"""

from api.database import SessionLocal, Base, engine
from api.models import (
    Ingredient, Recipe, Acupoint, SymptomAcupoint,
    TongueDiagnosisRecord, Course
)


def create_sample_ingredients():
    """创建示例食材数据"""
    ingredients = [
        Ingredient(
            name="山药",
            aliases=["怀山药", "淮山", "土山药"],
            category="药材",
            nature="平",
            flavor="甘",
            meridians=["脾", "肺", "肾"],
            suitable_constitutions=["qi_deficiency", "yin_deficiency"],
            avoid_constitutions=["phlegm_damp"],
            efficacy="健脾养胃、补肺益肾、固精止带",
            nutrition="含黏液质、维生素、淀粉、胆碱、皂苷等",
            cooking_methods=["蒸", "煮", "炖", "炒"],
            daily_dosage="50-100g",
            best_time="早晚餐",
            precautions="便秘者不宜多食",
            compatible_with=["莲子", "枸杞", "红枣"],
            incompatible_with=["碱性食物", "鲤鱼"],
            description="山药是常见的药食同源食材，具有健脾养胃、补肺益肾的功效"
        ),
        Ingredient(
            name="枸杞",
            aliases=["枸杞子", "宁夏枸杞"],
            category="药材",
            nature="平",
            flavor="甘",
            meridians=["肝", "肾", "肺"],
            suitable_constitutions=["yin_deficiency", "blood_stasis"],
            avoid_constitutions=["damp_heat", "phlegm_damp"],
            efficacy="滋补肝肾、明目、润肺",
            nutrition="含胡萝卜素、维生素、钙、铁等",
            cooking_methods=["泡茶", "煮粥", "炖汤"],
            daily_dosage="10-20g",
            best_time="任何时间",
            precautions="外邪实热、脾虚湿滞者不宜食用",
            compatible_with=["菊花", "红枣", "山药"],
            incompatible_with=["绿茶"],
            description="枸杞是常用的滋补药材，具有滋补肝肾、明目的功效"
        ),
        Ingredient(
            name="红枣",
            aliases=["大枣", "干枣"],
            category="药材",
            nature="温",
            flavor="甘",
            meridians=["脾", "胃", "心"],
            suitable_constitutions=["qi_deficiency", "blood_stasis", "yang_deficiency"],
            avoid_constitutions=["damp_heat", "yin_deficiency"],
            efficacy="补中益气、养血安神",
            nutrition="含糖类、维生素、有机酸等",
            cooking_methods=["煮粥", "炖汤", "泡茶"],
            daily_dosage="3-5颗",
            best_time="任何时间",
            precautions="糖尿病患者慎用",
            compatible_with=["枸杞", "桂圆", "生姜"],
            incompatible_with=["萝卜", "葱"],
            description="红枣是常用的补益药材，具有补中益气、养血安神的功效"
        ),
        Ingredient(
            name="生姜",
            aliases=["姜", "鲜姜"],
            category="调料品",
            nature="温",
            flavor="辛",
            meridians=["肺", "脾", "胃"],
            suitable_constitutions=["yang_deficiency", "phlegm_damp", "blood_stasis"],
            avoid_constitutions=["yin_deficiency", "damp_heat"],
            efficacy="发汗解表、温中止呕、温肺止咳",
            nutrition="含姜辣素、姜烯酮、膳食纤维等",
            cooking_methods=["煮汤", "炒菜", "泡茶"],
            daily_dosage="3-5片",
            best_time="早餐或风寒时",
            precautions="阴虚内热者不宜多食",
            compatible_with=["红糖", "红枣", "葱白"],
            incompatible_with=["芹菜", "兔肉"],
            description="生姜是常用的调味品，具有发汗解表、温中止呕的功效"
        ),
        Ingredient(
            name="薏米",
            aliases=["薏苡仁", "薏仁"],
            category="谷物",
            nature="凉",
            flavor="甘、淡",
            meridians=["脾", "肺", "肾"],
            suitable_constitutions=["phlegm_damp", "damp_heat"],
            avoid_constitutions=["yang_deficiency", "qi_deficiency"],
            efficacy="健脾利湿、清热排脓",
            nutrition="含蛋白质、脂肪、碳水化合物、维生素B等",
            cooking_methods=["煮粥", "煮汤", "打豆浆"],
            daily_dosage="30-50g",
            best_time="任何时间",
            precautions="孕妇慎用、津液不足者不宜多食",
            compatible_with=["红豆", "山药", "莲子"],
            incompatible_with=["海带"],
            description="薏米是常用的祛湿食材，具有健脾利湿的功效"
        )
    ]
    return ingredients


def create_sample_recipes():
    """创建示例食谱数据"""
    recipes = [
        Recipe(
            name="山药莲子粥",
            type="粥类",
            difficulty="简单",
            cook_time=60,
            servings=2,
            suitable_constitutions=["qi_deficiency"],
            symptoms=["食欲不振", "疲劳乏力", "脾胃虚弱"],
            suitable_seasons=["春", "秋", "冬"],
            ingredients={
                "main": [
                    {"name": "山药", "amount": "100g"},
                    {"name": "糯米", "amount": "50g"}
                ],
                "auxiliary": [
                    {"name": "莲子", "amount": "20g"},
                    {"name": "枸杞", "amount": "10g"}
                ],
                "seasoning": [
                    {"name": "冰糖", "amount": "适量"}
                ]
            },
            steps=[
                "山药去皮切小块，糯米提前浸泡2小时",
                "锅中加水，放入糯米大火煮开",
                "加入山药、莲子转小火煮30分钟",
                "最后加入枸杞、冰糖煮5分钟即可"
            ],
            efficacy="健脾养胃、补肺益气",
            health_benefits="适合脾胃虚弱、食欲不振者食用",
            precautions="糖尿病患者慎用",
            tags=["健脾养胃", "补气", "早餐"],
            description="经典健脾养胃粥，适合脾胃虚弱人群"
        ),
        Recipe(
            name="当归生姜羊肉汤",
            type="汤类",
            difficulty="中等",
            cook_time=90,
            servings=3,
            suitable_constitutions=["yang_deficiency", "blood_stasis"],
            symptoms=["畏寒肢冷", "痛经", "腰膝酸软"],
            suitable_seasons=["冬"],
            ingredients={
                "main": [
                    {"name": "羊肉", "amount": "500g"},
                    {"name": "当归", "amount": "10g"}
                ],
                "auxiliary": [
                    {"name": "生姜", "amount": "30g"},
                    {"name": "红枣", "amount": "10颗"}
                ],
                "seasoning": [
                    {"name": "盐", "amount": "适量"},
                    {"name": "料酒", "amount": "2勺"}
                ]
            },
            steps=[
                "羊肉洗净切块，焯水去血沫",
                "当归、生姜洗净切片",
                "锅中加水，放入羊肉、当归、生姜大火煮开",
                "转小火炖煮1小时，加盐调味即可"
            ],
            efficacy="温中散寒、补血活血",
            health_benefits="适合阳虚体质、寒性人群食用",
            precautions="阴虚火旺者不宜食用",
            tags=["温阳散寒", "补血", "冬季养生"],
            description="经典温补汤品，适合冬季进补"
        )
    ]
    return recipes


def create_sample_acupoints():
    """创建示例穴位数据"""
    acupoints = [
        Acupoint(
            name="足三里",
            code="ST36",
            meridian="足阳明胃经",
            body_part="下肢",
            location="犊鼻下3寸，胫骨前缘外一横指",
            simple_location="膝盖骨外侧下方凹陷往下四横指",
            efficacy=["健脾和胃", "扶正培元", "调理气血"],
            indications=["胃痛", "消化不良", "失眠", "疲劳", "便秘"],
            massage_method="用拇指指腹按压，做环形揉动",
            massage_duration="3-5分钟",
            massage_frequency="每日1-2次",
            precautions="孕妇慎用，饭后1小时内不宜按压",
            suitable_constitutions=["qi_deficiency", "yang_deficiency"],
            constitution_benefit="健脾和胃，增强体质，改善消化功能"
        ),
        Acupoint(
            name="合谷",
            code="LI4",
            meridian="手阳明大肠经",
            body_part="上肢",
            location="手背，第一、二掌骨之间，约平第二掌骨中点处",
            simple_location="手背虎口处，按压有酸胀感",
            efficacy=["镇静止痛", "通经活络", "解表散热"],
            indications=["头痛", "牙痛", "发热", "面瘫", "痛经"],
            massage_method="用拇指指腹按压，做环形揉动",
            massage_duration="2-3分钟",
            massage_frequency="每日2-3次",
            precautions="孕妇禁用，有活血作用",
            suitable_constitutions=["qi_deficiency", "yang_deficiency", "blood_stasis"],
            constitution_benefit="调理气血，缓解疼痛"
        ),
        Acupoint(
            name="神门",
            code="HT7",
            meridian="手少阴心经",
            body_part="上肢",
            location="腕横纹尺侧端，尺侧腕屈肌腱桡侧凹陷处",
            simple_location="手腕横纹小指侧凹陷处",
            efficacy=["安神定志", "清心泻火", "调理心气"],
            indications=["失眠", "健忘", "心悸", "焦虑"],
            massage_method="用拇指指腹轻轻按压",
            massage_duration="2-3分钟",
            massage_frequency="每晚睡前",
            precautions="轻柔按压，不可用力过重",
            suitable_constitutions=["yin_deficiency", "qi_depression", "special"],
            constitution_benefit="安神助眠，缓解焦虑失眠"
        ),
        Acupoint(
            name="太冲",
            code="LR3",
            meridian="足厥阴肝经",
            body_part="下肢",
            location="足背侧，第一、二跖骨结合部之前凹陷处",
            simple_location="脚背大拇趾和二趾之间的凹陷处",
            efficacy=["疏肝解郁", "调理气血", "平肝息风"],
            indications=["头痛", "眩晕", "月经不调", "抑郁", "高血压"],
            massage_method="用拇指指腹按压，做上下推按",
            massage_duration="3-5分钟",
            massage_frequency="每日1-2次",
            precautions="孕妇慎用，有活血作用",
            suitable_constitutions=["qi_depression", "blood_stasis", "yang_deficiency"],
            constitution_benefit="疏肝理气，缓解压力和焦虑"
        ),
        Acupoint(
            name="关元",
            code="CV4",
            meridian="任脉",
            body_part="胸腹部",
            location="前正中线上，脐下3寸",
            simple_location="肚脐正下方四横指处",
            efficacy=["培元固本", "温阳益气", "调理脾胃"],
            indications=["阳痿", "遗精", "月经不调", "腹泻", "虚劳"],
            massage_method="用掌心揉动或用艾灸",
            massage_duration="3-5分钟",
            massage_frequency="每日1-2次",
            precautions="孕妇慎用，可配合艾灸",
            suitable_constitutions=["qi_deficiency", "yang_deficiency"],
            constitution_benefit="培补元气，增强体质，改善阳虚症状"
        )
    ]
    return acupoints


def create_sample_courses():
    """创建示例课程数据"""
    courses = [
        Course(
            title="气虚质怎么调理？中医师教你4招改善",
            description="详细讲解气虚质的成因、表现和调理方法，包括饮食、运动、穴位按摩等",
            category="constitution",
            subcategory="qi_deficiency",
            content_type="video",
            content_url="https://example.com/video/qi_deficiency.mp4",
            suitable_constitutions=["qi_deficiency"],
            tags=["气虚质", "健脾", "养生", "调理"],
            duration=300,
            cover_image="https://example.com/images/qi_deficiency.jpg",
            author="王医师",
            author_title="中医执业医师 20年经验"
        ),
        Course(
            title="阳虚体质的人冬天应该吃什么？",
            description="介绍阳虚体质的特点和冬季进补方法，推荐适合的食材和食谱",
            category="constitution",
            subcategory="yang_deficiency",
            content_type="article",
            content_url="https://example.com/article/yang_deficiency_winter.html",
            suitable_constitutions=["yang_deficiency"],
            tags=["阳虚质", "冬季养生", "饮食", "进补"],
            duration=180,
            cover_image="https://example.com/images/yang_deficiency.jpg",
            author="李营养师",
            author_title="注册营养师"
        ),
        Course(
            title="春季养生：疏肝理气正当时",
            description="春季是肝气生发的季节，讲解如何通过饮食和穴位按摩疏肝理气",
            category="season",
            subcategory="spring",
            content_type="video",
            content_url="https://example.com/video/spring_health.mp4",
            suitable_constitutions=["qi_depression", "blood_stasis"],
            tags=["春季养生", "疏肝", "节气"],
            duration=240,
            cover_image="https://example.com/images/spring.jpg",
            author="张医师",
            author_title="中医执业医师"
        ),
        Course(
            title="三伏天养生：冬病夏治正当时",
            description="讲解三伏天的养生原理和方法，如何利用三伏天调理阳虚、寒湿体质",
            category="season",
            subcategory="summer",
            content_type="video",
            content_url="https://example.com/video/sanfu.mp4",
            suitable_constitutions=["yang_deficiency", "phlegm_damp"],
            tags=["夏季养生", "冬病夏治", "三伏贴"],
            duration=360,
            cover_image="https://example.com/images/summer.jpg",
            author="刘医师",
            author_title="中医执业医师"
        )
    ]
    return courses


def create_sample_data():
    """创建所有示例数据"""
    print("开始创建示例数据...")

    # 创建表
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        # 创建食材
        ingredients = create_sample_ingredients()
        for ing in ingredients:
            session.add(ing)
        print(f"✓ 创建了 {len(ingredients)} 个食材")

        # 创建食谱
        recipes = create_sample_recipes()
        for recipe in recipes:
            session.add(recipe)
        print(f"✓ 创建了 {len(recipes)} 个食谱")

        # 创建穴位
        acupoints_data = create_sample_acupoints()
        for acupoint in acupoints_data:
            session.add(acupoint)
        # 刷新会话以获取生成的ID
        session.flush()
        print(f"✓ 创建了 {len(acupoints_data)} 个穴位")

        # 创建课程
        courses = create_sample_courses()
        for course in courses:
            session.add(course)
        print(f"✓ 创建了 {len(courses)} 个课程")

        # 创建症状-穴位关联（此时穴位已有ID）
        acupoints_map = {a.name: a.id for a in acupoints_data}
        symptom_acupoints = [
            SymptomAcupoint(symptom_name="胃痛", acupoint_id=acupoints_map["足三里"], priority=1),
            SymptomAcupoint(symptom_name="胃痛", acupoint_id=acupoints_map["合谷"], priority=2),
            SymptomAcupoint(symptom_name="失眠", acupoint_id=acupoints_map["神门"], priority=1),
            SymptomAcupoint(symptom_name="头痛", acupoint_id=acupoints_map["合谷"], priority=1),
            SymptomAcupoint(symptom_name="头痛", acupoint_id=acupoints_map["太冲"], priority=2),
            SymptomAcupoint(symptom_name="焦虑", acupoint_id=acupoints_map["太冲"], priority=1),
            SymptomAcupoint(symptom_name="痛经", acupoint_id=acupoints_map["合谷"], priority=1),
            SymptomAcupoint(symptom_name="疲劳", acupoint_id=acupoints_map["足三里"], priority=1),
        ]
        for sa in symptom_acupoints:
            session.add(sa)
        print(f"✓ 创建了 {len(symptom_acupoints)} 个症状-穴位关联")

        session.commit()
        print("\n✅ 示例数据创建完成！")

    except Exception as e:
        print(f"\n❌ 创建数据时出错: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    create_sample_data()
