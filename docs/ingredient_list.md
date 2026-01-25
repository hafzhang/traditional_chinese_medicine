# 食材档案

本文档列出了中医养生平台中的食材示例数据。

---

## 数据结构

| 字段 | 说明 | 示例 |
|------|------|------|
| name | 食材名称 | 山药 |
| category | 分类 | 蔬菜类/谷类/水果类/肉类等 |
| nature | 性味 | 寒/凉/平/温/热 |
| taste | 味道 | 酸/苦/甘/辛/咸 |
| efficacy | 功效描述 | 补脾养胃，生津益肺，补肾涩精 |
| nutritional_value | 营养价值 | 含黏液蛋白、维生素、淀粉等 |
| contraindications | 禁忌人群 | 湿盛中满者慎用 |
| suitable_constitutions | 适合体质 | ["qi_deficiency", "yang_deficiency"] |
| avoid_constitutions | 禁忌体质 | ["phlegm_damp"] |
| aliases | 别名数组 | ["怀山药", "淮山", "薯蓣"] |
| image_url | 图片URL | /static/ingredients/山药.jpg |

---

## 食材列表

### 1. 山药

| 字段 | 值 |
|------|-----|
| **name** | 山药 |
| **category** | 蔬菜类 |
| **nature** | 平 |
| **taste** | 甘 |
| **efficacy** | 补脾养胃，生津益肺，补肾涩精。用于脾虚食少、久泻不止、肺虚喘咳、肾虚遗精、带下、尿频、虚热消渴。 |
| **nutritional_value** | 含黏液蛋白、维生素、淀粉、淀粉酶、皂苷、游离氨基酸、多酚氧化酶等物质，具有滋补作用。 |
| **contraindications** | 湿盛中满或有实邪、积滞者慎用。 |
| **suitable_constitutions** | `["qi_deficiency", "yang_deficiency", "yin_deficiency"]` |
| **avoid_constitutions** | `["phlegm_damp"]` |
| **aliases** | `["怀山药", "淮山", "薯蓣", "山芋"]` |
| **image_url** | /static/ingredients/山药.jpg |

---

### 2. 枸杞子

| 字段 | 值 |
|------|-----|
| **name** | 枸杞子 |
| **category** | 果实类 |
| **nature** | 平 |
| **taste** | 甘 |
| **efficacy** | 滋补肝肾，益精明目。用于虚劳精亏、腰膝酸痛、眩晕耳鸣、内热消渴、血虚萎黄、目昏不明。 |
| **nutritional_value** | 含枸杞多糖、甜菜碱、胡萝卜素、维生素A、B1、B2、C、钙、磷、铁等，具有增强免疫力、抗氧化作用。 |
| **contraindications** | 外邪实热、脾虚有湿及泄泻者忌服。 |
| **suitable_constitutions** | `["yin_deficiency", "yang_deficiency", "blood_stasis"]` |
| **avoid_constitutions** | `["phlegm_damp", "damp_heat"]` |
| **aliases** | `["枸杞", "杞子", "红耳坠"]` |
| **image_url** | /static/ingredients/枸杞子.jpg |

---

### 3. 红枣

| 字段 | 值 |
|------|-----|
| **name** | 红枣 |
| **category** | 果实类 |
| **nature** | 温 |
| **taste** | 甘 |
| **efficacy** | 补中益气，养血安神。用于脾虚食少、乏力便溏、妇人脏躁。 |
| **nutritional_value** | 含蛋白质、糖类、有机酸、维生素A、维生素C、多种微量钙和氨基酸等，具有增强免疫力、保护肝脏作用。 |
| **contraindications** | 湿盛脘腹胀满、食积、虫积、龋齿作痛，以及痰热咳嗽者忌服。 |
| **suitable_constitutions** | `["qi_deficiency", "blood_stasis", "yang_deficiency"]` |
| **avoid_constitutions** | `["phlegm_damp", "damp_heat"]` |
| **aliases** | `["大枣", "枣子"]` |
| **image_url** | /static/ingredients/红枣.jpg |

---

### 4. 生姜

| 字段 | 值 |
|------|-----|
| **name** | 生姜 |
| **category** | 调味蔬菜类 |
| **nature** | 温 |
| **taste** | 辛 |
| **efficacy** | 解表散寒，温中止呕，化痰止咳。用于风寒感冒、胃寒呕吐、寒痰咳嗽。 |
| **nutritional_value** | 含姜辣素、姜烯酮、姜油酮、淀粉、纤维等，具有促进血液循环、发汗解表作用。 |
| **contraindications** | 阴虚内热及实热证者忌服。 |
| **suitable_constitutions** | `["yang_deficiency", "phlegm_damp"]` |
| **avoid_constitutions** | `["yin_deficiency", "damp_heat"]` |
| **aliases** | `["姜", "鲜姜"]` |
| **image_url** | /static/ingredients/生姜.jpg |

---

### 5. 山楂

| 字段 | 值 |
|------|-----|
| **name** | 山楂 |
| **category** | 水果类 |
| **nature** | 温 |
| **taste** | 酸、甘 |
| **efficacy** | 消食健胃，行气散瘀，化浊降脂。用于肉食积滞、胃脘胀痛、泻痢腹痛、瘀血经闭、产后瘀阻、心腹刺痛、胸痹心痛、疝气疼痛、高脂血症。 |
| **nutritional_value** | 含山楂酸、酒石酸、柠檬酸、黄酮类、维生素C等，具有促进消化、降低血脂作用。 |
| **contraindications** | 脾胃虚弱者慎服，孕妇慎用。 |
| **suitable_constitutions** | `["phlegm_damp", "blood_stasis", "qi_depression"]` |
| **avoid_constitutions** | `["qi_deficiency", "yang_deficiency"]` |
| **aliases** | `["山里红", "酸楂"]` |
| **image_url** | /static/ingredients/山楂.jpg |

---

### 6. 薏米

| 字段 | 值 |
|------|-----|
| **name** | 薏米 |
| **category** | 谷类 |
| **nature** | 凉 |
| **taste** | 甘、淡 |
| **efficacy** | 利水渗湿，健脾止泻，除痹，排脓，解毒散结。用于水肿、脚气、小便不利、脾虚泄泻、湿热痹痛、脓疱疮、赘疣。 |
| **nutritional_value** | 含薏苡仁油、薏苡仁酯、甾醇、氨基酸、糖类、维生素B1等，具有增强免疫力、抗肿瘤作用。 |
| **contraindications** | 孕妇慎用，津液不足者慎用。 |
| **suitable_constitutions** | `["phlegm_damp", "damp_heat"]` |
| **avoid_constitutions** | `["yang_deficiency"]` |
| **aliases** | `["薏苡仁", "薏仁", "六谷米"]` |
| **image_url** | /static/ingredients/薏米.jpg |

---

### 7. 银耳

| 字段 | 值 |
|------|-----|
| **name** | 银耳 |
| **category** | 菌菇类 |
| **nature** | 平 |
| **taste** | 甘、淡 |
| **efficacy** | 滋阴润肺，养胃生津。用于虚劳咳嗽、痰中带血、津少口渴、病后体虚、气短乏力。 |
| **nutritional_value** | 含蛋白质、脂肪、碳水化合物、粗纤维、硫、磷、铁、镁、钙、钾、钠等，具有增强免疫力、抗衰老作用。 |
| **contraindications** | 外感风寒、出血症患者忌服。 |
| **suitable_constitutions** | `["yin_deficiency", "qi_deficiency"]` |
| **avoid_constitutions** | `["phlegm_damp"]` |
| **aliases** | `["白木耳", "雪耳"]` |
| **image_url** | /static/ingredients/银耳.jpg |

---

### 8. 人参

| 字段 | 值 |
|------|-----|
| **name** | 人参 |
| **category** | 药材类 |
| **nature** | 微温 |
| **taste** | 甘、微苦 |
| **efficacy** | 大补元气，复脉固脱，补脾益肺，生津养血，安神益智。用于体虚欲脱、肢冷脉微、脾虚食少、气短喘促、津伤口渴、内热消渴、气血亏虚、久病虚羸、惊悸失眠、阳痿宫冷。 |
| **nutritional_value** | 含人参皂苷、人参多糖、多种氨基酸、维生素等，具有增强免疫力、抗疲劳、抗休克作用。 |
| **contraindications** | 实热证、湿热证及正气不虚者忌服。不宜与藜芦、五灵脂同用。 |
| **suitable_constitutions** | `["qi_deficiency", "yang_deficiency"]` |
| **avoid_constitutions** | `["yin_deficiency", "damp_heat", "phlegm_damp"]` |
| **aliases** | `["吉林参", "高丽参", "人参"]` |
| **image_url** | /static/ingredients/人参.jpg |

---

### 9. 菊花

| 字段 | 值 |
|------|-----|
| **name** | 菊花 |
| **category** | 花茶类 |
| **nature** | 微寒 |
| **taste** | 甘、苦、辛 |
| **efficacy** | 散风清热，平肝明目，清热解毒。用于风热感冒、头痛眩晕、目赤肿痛、眼目昏花、疮痈肿毒。 |
| **nutritional_value** | 含挥发油、菊甙、氨基酸、维生素、微量元素等，具有扩张冠状动脉、增加冠脉流量作用。 |
| **contraindications** | 气虚胃寒、食少泄泻者慎用。 |
| **suitable_constitutions** | `["damp_heat", "yin_deficiency"]` |
| **avoid_constitutions** | `["yang_deficiency", "qi_deficiency"]` |
| **aliases** | `["白菊花", "杭菊", "贡菊"]` |
| **image_url** | /static/ingredients/菊花.jpg |

---

### 10. 当归

| 字段 | 值 |
|------|-----|
| **name** | 当归 |
| **category** | 药材类 |
| **nature** | 温 |
| **taste** | 甘、辛 |
| **efficacy** | 补血活血，调经止痛，润肠通便。用于血虚萎黄、眩晕心悸、月经不调、经闭痛经、虚寒腹痛、风湿痹痛、跌扑损伤、痈疽疮疡、肠燥便秘。 |
| **nutritional_value** | 含藁本内酯、阿魏酸、多糖、氨基酸、维生素等，具有促进造血、增强免疫力、抗炎作用。 |
| **contraindications** | 湿盛中满、大便溏泄者慎用。 |
| **suitable_constitutions** | `["blood_stasis", "qi_deficiency", "yang_deficiency"]` |
| **avoid_constitutions** | `["phlegm_damp", "damp_heat"]` |
| **aliases** | `["秦归", "云归", "西归"]` |
| **image_url** | /static/ingredients/当归.jpg |

---

### 11. 黄芪

| 字段 | 值 |
|------|-----|
| **name** | 黄芪 |
| **category** | 药材类 |
| **nature** | 微温 |
| **taste** | 甘 |
| **efficacy** | 补气升阳，固表止汗，利水消肿，生津养血，行滞通痹，托毒排脓，敛疮生肌。用于气虚乏力、食少便溏、中气下陷、久泻脱肛、便血崩漏、表虚自汗、气虚水肿、痈疽难溃、久溃不敛。 |
| **nutritional_value** | 含黄芪甲苷、黄芪多糖、氨基酸、叶酸等，具有增强免疫力、抗疲劳、促进造血作用。 |
| **contraindications** | 表实邪盛、气滞湿阻、食积停滞、痈疽初起或溃后热毒尚盛者忌服。 |
| **suitable_constitutions** | `["qi_deficiency", "yang_deficiency"]` |
| **avoid_constitutions** | `["phlegm_damp", "damp_heat"]` |
| **aliases** | `["绵芪", "北芪"]` |
| **image_url** | /static/ingredients/黄芪.jpg |

---

### 12. 莲子

| 字段 | 值 |
|------|-----|
| **name** | 莲子 |
| **category** | 坚果类 |
| **nature** | 平 |
| **taste** | 甘、涩 |
| **efficacy** | 补脾止泻，止带，益肾涩精，养心安神。用于脾虚泄泻、带下、遗精、心悸失眠。 |
| **nutritional_value** | 含蛋白质、脂肪、碳水化合物、钙、磷、铁等，具有养心安神、增强记忆力作用。 |
| **contraindications** | 中满痞胀及大便燥结者忌服。 |
| **suitable_constitutions** | `["qi_deficiency", "yin_deficiency", "yang_deficiency"]` |
| **avoid_constitutions** | `["phlegm_damp"]` |
| **aliases** | `["莲肉", "莲实"]` |
| **image_url** | /static/ingredients/莲子.jpg |

---

### 13. 百合

| 字段 | 值 |
|------|-----|
| **name** | 百合 |
| **category** | 蔬菜类 |
| **nature** | 寒 |
| **taste** | 甘 |
| **efficacy** | 养阴润肺，清心安神。用于阴虚燥咳、劳嗽咳血、虚烦惊悸、失眠多梦、精神恍惚。 |
| **nutritional_value** | 含秋水仙碱、多种生物碱、淀粉、蛋白质、脂肪等，具有润肺止咳、宁心安神作用。 |
| **contraindications** | 风寒咳嗽及中寒便溏者忌服。 |
| **suitable_constitutions** | `["yin_deficiency", "qi_depression"]` |
| **avoid_constitutions** | `["yang_deficiency", "phlegm_damp"]` |
| **aliases** | `["白百合", "蒜脑薯"]` |
| **image_url** | /static/ingredients/百合.jpg |

---

### 14. 茯苓

| 字段 | 值 |
|------|-----|
| **name** | 茯苓 |
| **category** | 菌菇类 |
| **nature** | 平 |
| **taste** | 甘、淡 |
| **efficacy** | 利水渗湿，健脾，宁心。用于水肿尿少、痰饮眩悸、脾虚食少、便溏泄泻、心神不安、惊悸失眠。 |
| **nutritional_value** | 含茯苓多糖、茯苓酸、蛋白质、脂肪、卵磷脂等，具有增强免疫力、抗肿瘤、保肝作用。 |
| **contraindications** | 阴虚而无湿热、虚寒滑精者慎用。 |
| **suitable_constitutions** | `["phlegm_damp", "qi_deficiency"]` |
| **avoid_constitutions** | `["yin_deficiency"]` |
| **aliases** | `["云苓", "松苓"]` |
| **image_url** | /static/ingredients/茯苓.jpg |

---

### 15. 陈皮

| 字段 | 值 |
|------|-----|
| **name** | 陈皮 |
| **category** | 调味类 |
| **nature** | 温 |
| **taste** | 苦、辛 |
| **efficacy** | 理气健脾，燥湿化痰。用于脘腹胀满、食少吐泻、咳嗽痰多。 |
| **nutritional_value** | 含挥发油、橙皮甙、维生素B、C等，具有促进消化、祛痰止咳作用。 |
| **contraindications** | 气虚体燥、阴虚燥咳、吐血及内有实热者慎用。 |
| **suitable_constitutions** | `["phlegm_damp", "qi_depression"]` |
| **avoid_constitutions** | `["yin_deficiency", "qi_deficiency"]` |
| **aliases** | `["橘皮", "红皮"]` |
| **image_url** | /static/ingredients/陈皮.jpg |

---

## 体质代码对照

| 代码 | 名称 |
|------|------|
| `peace` | 平和质 |
| `qi_deficiency` | 气虚质 |
| `yang_deficiency` | 阳虚质 |
| `yin_deficiency` | 阴虚质 |
| `phlegm_damp` | 痰湿质 |
| `damp_heat` | 湿热质 |
| `blood_stasis` | 血瘀质 |
| `qi_depression` | 气郁质 |
| `special` | 特禀质 |

---

## 分类说明

| 分类 | 说明 |
|------|------|
| 蔬菜类 | 根茎类、叶菜类蔬菜 |
| 谷类 | 粮食、杂粮 |
| 水果类 | 鲜果、干果 |
| 肉类 | 畜禽、水产 |
| 菌菇类 | 食用菌、药用菌 |
| 药材类 | 中药材、药食同源 |
| 调味类 | 调料、香辛料 |
| 坚果类 | 坚果、种子 |
| 花茶类 | 花草茶、代用茶 |
| 果实类 | 干果、蜜饯 |

---

## 性味说明

| 性味 | 特性 |
|------|------|
| 寒 | 清热、泻火、解毒 |
| 凉 | 清热、润燥 |
| 平 | 补益、和缓 |
| 温 | 温中、散寒 |
| 热 | 散寒、回阳 |

---

## 导入数据库示例

```python
from api.models import Ingredient
from sqlalchemy.orm import Session

def create_sample_ingredients(db: Session):
    ingredients = [
        Ingredient(
            name="山药",
            category="蔬菜类",
            nature="平",
            taste="甘",
            efficacy="补脾养胃，生津益肺，补肾涩精。",
            nutritional_value="含黏液蛋白、维生素、淀粉等。",
            contraindications="湿盛中满者慎用。",
            suitable_constitutions=["qi_deficiency", "yang_deficiency", "yin_deficiency"],
            avoid_constitutions=["phlegm_damp"],
            aliases=["怀山药", "淮山", "薯蓣", "山芋"],
            image_url="/static/ingredients/山药.jpg"
        ),
        # ... 其他食材
    ]

    for ingredient in ingredients:
        db.add(ingredient)
    db.commit()
```
