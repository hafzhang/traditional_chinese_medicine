"""
Foods Data
食物库数据 - 每种体质至少10条推荐食物
"""

FOODS_DATA = [
    # 气虚质推荐食物
    {
        "name": "山药",
        "name_en": "Chinese Yam",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["脾", "肺", "肾"],
        "suitable_constitutions": ["qi_deficiency", "peace"],
        "avoid_constitutions": [],
        "effects": ["补脾养胃", "生津益肺", "补肾涩精"],
        "recipes": ["山药炖排骨", "山药粥"]
    },
    {
        "name": "大枣",
        "name_en": "Jujube",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["脾", "胃", "心"],
        "suitable_constitutions": ["qi_deficiency", "yang_deficiency"],
        "avoid_constitutions": ["damp_heat", "phlegm_damp"],
        "effects": ["补中益气", "养血安神"],
        "recipes": ["红枣茶", "红枣桂圆粥"]
    },
    {
        "name": "黄芪",
        "name_en": "Astragalus",
        "nature": "微温",
        "flavor": "甘",
        "meridians": ["脾", "肺"],
        "suitable_constitutions": ["qi_deficiency"],
        "avoid_constitutions": ["yin_deficiency", "damp_heat"],
        "effects": ["补气升阳", "固表止汗", "利水消肿"],
        "recipes": ["黄芪炖鸡", "黄芪粥"]
    },
    {
        "name": "鸡肉",
        "name_en": "Chicken",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["脾", "胃"],
        "suitable_constitutions": ["qi_deficiency", "yang_deficiency"],
        "avoid_constitutions": ["damp_heat", "yin_deficiency"],
        "effects": ["温中益气", "补精填髓"],
        "recipes": ["清炖鸡汤", "黄芪蒸鸡"]
    },
    {
        "name": "糯米",
        "name_en": "Glutinous Rice",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["脾", "胃", "肺"],
        "suitable_constitutions": ["qi_deficiency", "yang_deficiency"],
        "avoid_constitutions": ["damp_heat", "phlegm_damp"],
        "effects": ["补中益气", "健脾止泻"],
        "recipes": ["糯米粥", "八宝饭"]
    },
    {
        "name": "牛肉",
        "name_en": "Beef",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["脾", "胃"],
        "suitable_constitutions": ["qi_deficiency", "yang_deficiency"],
        "avoid_constitutions": ["damp_heat"],
        "effects": ["补脾胃", "益气血", "强筋骨"],
        "recipes": ["红烧牛肉", "牛肉汤"]
    },
    {
        "name": "小米",
        "name_en": "Millet",
        "nature": "凉",
        "flavor": "甘、咸",
        "meridians": ["脾", "胃", "肾"],
        "suitable_constitutions": ["qi_deficiency", "peace"],
        "avoid_constitutions": [],
        "effects": ["健脾益胃", "养心安神"],
        "recipes": ["小米粥", "小米红枣粥"]
    },
    {
        "name": "莲子",
        "name_en": "Lotus Seed",
        "nature": "平",
        "flavor": "甘、涩",
        "meridians": ["脾", "肾", "心"],
        "suitable_constitutions": ["qi_deficiency", "peace"],
        "avoid_constitutions": ["phlegm_damp"],
        "effects": ["补脾止泻", "益肾固精", "养心安神"],
        "recipes": ["莲子百合粥", "银耳莲子汤"]
    },
    {
        "name": "香菇",
        "name_en": "Shiitake Mushroom",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["肝", "胃"],
        "suitable_constitutions": ["qi_deficiency", "peace"],
        "avoid_constitutions": ["phlegm_damp"],
        "effects": ["补气益胃", "托毒排毒"],
        "recipes": ["香菇炖鸡", "香菇青菜"]
    },
    {
        "name": "胡萝卜",
        "name_en": "Carrot",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["肺", "脾"],
        "suitable_constitutions": ["qi_deficiency", "peace"],
        "avoid_constitutions": [],
        "effects": ["健脾化滞", "补肝明目"],
        "recipes": ["胡萝卜排骨汤", "胡萝卜炒蛋"]
    },

    # 阳虚质推荐食物
    {
        "name": "羊肉",
        "name_en": "Mutton",
        "nature": "热",
        "flavor": "甘",
        "meridians": ["脾", "肾"],
        "suitable_constitutions": ["yang_deficiency", "qi_deficiency"],
        "avoid_constitutions": ["damp_heat", "yin_deficiency"],
        "effects": ["温中补虚", "补肾壮阳"],
        "recipes": ["当归生姜羊肉汤", "羊肉火锅"]
    },
    {
        "name": "韭菜",
        "name_en": "Chinese Chives",
        "nature": "温",
        "flavor": "辛",
        "meridians": ["肝", "胃", "肾"],
        "suitable_constitutions": ["yang_deficiency"],
        "avoid_constitutions": ["yin_deficiency", "damp_heat"],
        "effects": ["温补肝肾", "助阳固精"],
        "recipes": ["韭菜炒蛋", "韭菜盒子"]
    },
    {
        "name": "生姜",
        "name_en": "Ginger",
        "nature": "温",
        "flavor": "辛",
        "meridians": ["肺", "脾", "胃"],
        "suitable_constitutions": ["yang_deficiency", "qi_deficiency"],
        "avoid_constitutions": ["damp_heat", "yin_deficiency"],
        "effects": ["发汗解表", "温中止呕", "温肺止咳"],
        "recipes": ["生姜红糖水", "姜茶"]
    },
    {
        "name": "辣椒",
        "name_en": "Chili Pepper",
        "nature": "热",
        "flavor": "辛",
        "meridians": ["心", "脾"],
        "suitable_constitutions": ["yang_deficiency", "phlegm_damp"],
        "avoid_constitutions": ["yin_deficiency", "damp_heat"],
        "effects": ["温中散寒", "开胃消食"],
        "recipes": ["辣椒炒肉", "辣椒炒蛋"]
    },
    {
        "name": "花椒",
        "name_en": "Sichuan Pepper",
        "nature": "温",
        "flavor": "辛",
        "meridians": ["脾", "胃", "肾"],
        "suitable_constitutions": ["yang_deficiency", "phlegm_damp"],
        "avoid_constitutions": ["yin_deficiency"],
        "effects": ["温中止痛", "杀虫止痒"],
        "recipes": ["椒盐鸡", "花椒鱼"]
    },
    {
        "name": "肉桂",
        "name_en": "Cinnamon",
        "nature": "热",
        "flavor": "辛、甘",
        "meridians": ["肾", "脾", "心", "肝"],
        "suitable_constitutions": ["yang_deficiency"],
        "avoid_constitutions": ["yin_deficiency", "damp_heat", "blood_stasis"],
        "effects": ["补火助阳", "散寒止痛", "温通经脉"],
        "recipes": ["肉桂茶", "肉桂粥"]
    },
    {
        "name": "核桃仁",
        "name_en": "Walnut",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["肾", "肺", "大肠"],
        "suitable_constitutions": ["yang_deficiency", "qi_deficiency"],
        "avoid_constitutions": ["damp_heat", "phlegm_damp"],
        "effects": ["补肾温肺", "润肠通便"],
        "recipes": ["核桃粥", "琥珀核桃"]
    },
    {
        "name": "板栗",
        "name_en": "Chestnut",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["脾", "肾"],
        "suitable_constitutions": ["yang_deficiency", "qi_deficiency"],
        "avoid_constitutions": ["phlegm_damp"],
        "effects": ["健脾益肾", "强筋壮骨"],
        "recipes": ["板栗烧鸡", "糖炒板栗"]
    },
    {
        "name": "虾",
        "name_en": "Shrimp",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["肝", "肾"],
        "suitable_constitutions": ["yang_deficiency", "qi_deficiency"],
        "avoid_constitutions": ["special"],
        "effects": ["补肾壮阳", "通乳排毒"],
        "recipes": ["白灼虾", "虾仁炒蛋"]
    },
    {
        "name": "狗肉",
        "name_en": "Dog Meat",
        "nature": "温",
        "flavor": "咸、辛",
        "meridians": ["脾", "胃", "肾"],
        "suitable_constitutions": ["yang_deficiency"],
        "avoid_constitutions": ["yin_deficiency", "damp_heat"],
        "effects": ["温肾壮阳", "温补脾胃"],
        "recipes": ["红烧狗肉", "狗肉汤"]
    },

    # 阴虚质推荐食物
    {
        "name": "百合",
        "name_en": "Lily Bulb",
        "nature": "微寒",
        "flavor": "甘",
        "meridians": ["心", "肺"],
        "suitable_constitutions": ["yin_deficiency", "peace"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["养阴润肺", "清心安神"],
        "recipes": ["百合莲子粥", "西芹百合"]
    },
    {
        "name": "银耳",
        "name_en": "White Fungus",
        "nature": "平",
        "flavor": "甘、淡",
        "meridians": ["肺", "胃", "肾"],
        "suitable_constitutions": ["yin_deficiency", "peace"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["滋阴润肺", "养胃生津"],
        "recipes": ["银耳莲子汤", "冰糖银耳"]
    },
    {
        "name": "梨",
        "name_en": "Pear",
        "nature": "凉",
        "flavor": "甘、微酸",
        "meridians": ["肺", "胃"],
        "suitable_constitutions": ["yin_deficiency", "damp_heat", "peace"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["清热生津", "润燥化痰"],
        "recipes": ["冰糖雪梨", "银耳雪梨汤"]
    },
    {
        "name": "鸭肉",
        "name_en": "Duck Meat",
        "nature": "微寒",
        "flavor": "甘、咸",
        "meridians": ["肺", "脾", "肾"],
        "suitable_constitutions": ["yin_deficiency", "damp_heat"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["滋阴养胃", "利水消肿"],
        "recipes": ["老鸭汤", "啤酒鸭"]
    },
    {
        "name": "甲鱼",
        "name_en": "Soft-shelled Turtle",
        "nature": "微寒",
        "flavor": "甘",
        "meridians": ["肝", "肾"],
        "suitable_constitutions": ["yin_deficiency"],
        "avoid_constitutions": ["yang_deficiency", "phlegm_damp"],
        "effects": ["滋阴补肾", "清热凉血"],
        "recipes": ["清炖甲鱼", "甲鱼汤"]
    },
    {
        "name": "枸杞子",
        "name_en": "Goji Berry",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["肝", "肾", "肺"],
        "suitable_constitutions": ["yin_deficiency", "peace", "qi_deficiency"],
        "avoid_constitutions": ["phlegm_damp"],
        "effects": ["滋补肝肾", "益精明目"],
        "recipes": ["枸杞茶", "枸杞粥"]
    },
    {
        "name": "桑葚",
        "name_en": "Mulberry",
        "nature": "寒",
        "flavor": "甘、酸",
        "meridians": ["肝", "肾"],
        "suitable_constitutions": ["yin_deficiency", "blood_stasis"],
        "avoid_constitutions": ["yang_deficiency", "phlegm_damp"],
        "effects": ["滋阴补血", "生津润燥"],
        "recipes": ["桑葚酒", "桑葚粥"]
    },
    {
        "name": "绿豆",
        "name_en": "Mung Bean",
        "nature": "寒",
        "flavor": "甘",
        "meridians": ["心", "胃"],
        "suitable_constitutions": ["damp_heat", "yin_deficiency"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["清热解毒", "消暑利水"],
        "recipes": ["绿豆汤", "绿豆粥"]
    },
    {
        "name": "冬瓜",
        "name_en": "Winter Melon",
        "nature": "凉",
        "flavor": "甘、淡",
        "meridians": ["肺", "大肠", "膀胱"],
        "suitable_constitutions": ["damp_heat", "phlegm_damp", "yin_deficiency"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["清热利水", "消肿解毒"],
        "recipes": ["冬瓜排骨汤", "冬瓜炒肉"]
    },
    {
        "name": "豆腐",
        "name_en": "Tofu",
        "nature": "凉",
        "flavor": "甘",
        "meridians": ["脾", "胃", "大肠"],
        "suitable_constitutions": ["damp_heat", "yin_deficiency", "peace"],
        "avoid_constitutions": ["yang_deficiency", "phlegm_damp"],
        "effects": ["清热润燥", "生津解毒"],
        "recipes": ["麻婆豆腐", "豆腐汤"]
    },

    # 痰湿质推荐食物
    {
        "name": "白萝卜",
        "name_en": "White Radish",
        "nature": "凉",
        "flavor": "辛、甘",
        "meridians": ["肺", "胃"],
        "suitable_constitutions": ["phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["qi_deficiency", "yang_deficiency"],
        "effects": ["下气消食", "化痰止咳"],
        "recipes": ["萝卜排骨汤", "萝卜炖牛腩"]
    },
    {
        "name": "赤小豆",
        "name_en": "Red Bean",
        "nature": "平",
        "flavor": "甘、酸",
        "meridians": ["心", "小肠"],
        "suitable_constitutions": ["phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["qi_deficiency"],
        "effects": ["利水消肿", "解毒排脓"],
        "recipes": ["红豆汤", "红豆薏米粥"]
    },
    {
        "name": "薏米",
        "name_en": "Coix Seed",
        "nature": "凉",
        "flavor": "甘、淡",
        "meridians": ["脾", "胃", "肺"],
        "suitable_constitutions": ["phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["yang_deficiency", "qi_deficiency"],
        "effects": ["利水渗湿", "健脾止泻"],
        "recipes": ["薏米红豆粥", "薏米茶"]
    },
    {
        "name": "荷叶",
        "name_en": "Lotus Leaf",
        "nature": "平",
        "flavor": "苦、涩",
        "meridians": ["肝", "脾", "胃"],
        "suitable_constitutions": ["phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["qi_deficiency", "yang_deficiency"],
        "effects": ["清热解暑", "升发清阳", "凉血止血"],
        "recipes": ["荷叶茶", "荷叶粥"]
    },
    {
        "name": "海带",
        "name_en": "Kelp",
        "nature": "寒",
        "flavor": "咸",
        "meridians": ["肝", "胃", "肾"],
        "suitable_constitutions": ["phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["yang_deficiency", "qi_deficiency"],
        "effects": ["消痰软坚", "利水消肿"],
        "recipes": ["海带排骨汤", "凉拌海带"]
    },
    {
        "name": "冬瓜",
        "name_en": "Winter Melon",
        "nature": "凉",
        "flavor": "甘、淡",
        "meridians": ["肺", "大肠", "膀胱"],
        "suitable_constitutions": ["phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["清热利水", "消肿解毒"],
        "recipes": ["冬瓜汤", "冬瓜炒肉"]
    },
    {
        "name": "黄瓜",
        "name_en": "Cucumber",
        "nature": "凉",
        "flavor": "甘",
        "meridians": ["胃", "大肠"],
        "suitable_constitutions": ["damp_heat", "phlegm_damp"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["清热利水", "解毒消肿"],
        "recipes": ["凉拌黄瓜", "黄瓜炒蛋"]
    },
    {
        "name": "玉米",
        "name_en": "Corn",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["胃", "大肠"],
        "suitable_constitutions": ["phlegm_damp", "peace"],
        "avoid_constitutions": [],
        "effects": ["健脾开胃", "利水消肿"],
        "recipes": ["玉米粥", "玉米排骨汤"]
    },
    {
        "name": "山楂",
        "name_en": "Hawthorn",
        "nature": "微温",
        "flavor": "酸、甘",
        "meridians": ["脾", "胃", "肝"],
        "suitable_constitutions": ["phlegm_damp", "blood_stasis"],
        "avoid_constitutions": ["qi_deficiency", "yang_deficiency"],
        "effects": ["消食健胃", "行气散瘀"],
        "recipes": ["山楂茶", "山楂糕"]
    },
    {
        "name": "橙子",
        "name_en": "Orange",
        "nature": "凉",
        "flavor": "酸、甘",
        "meridians": ["肺", "脾"],
        "suitable_constitutions": ["phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["生津止渴", "开胃下气"],
        "recipes": ["鲜榨橙汁", "橙子茶"]
    },

    # 湿热质推荐食物
    {
        "name": "苦瓜",
        "name_en": "Bitter Melon",
        "nature": "寒",
        "flavor": "苦",
        "meridians": ["心", "脾", "胃"],
        "suitable_constitutions": ["damp_heat"],
        "avoid_constitutions": ["yang_deficiency", "qi_deficiency"],
        "effects": ["清热祛暑", "明目解毒"],
        "recipes": ["苦瓜炒蛋", "凉拌苦瓜"]
    },
    {
        "name": "芹菜",
        "name_en": "Celery",
        "nature": "凉",
        "flavor": "甘、苦",
        "meridians": ["肝", "胃"],
        "suitable_constitutions": ["damp_heat", "blood_stasis"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["清热平肝", "祛风利湿"],
        "recipes": ["芹菜炒香干", "芹菜炒肉"]
    },
    {
        "name": "黄瓜",
        "name_en": "Cucumber",
        "nature": "凉",
        "flavor": "甘",
        "meridians": ["胃", "大肠"],
        "suitable_constitutions": ["damp_heat", "phlegm_damp"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["清热利水", "解毒消肿"],
        "recipes": ["凉拌黄瓜", "黄瓜炒蛋"]
    },
    {
        "name": "莲藕",
        "name_en": "Lotus Root",
        "nature": "寒",
        "flavor": "甘",
        "meridians": ["肝", "肺", "胃"],
        "suitable_constitutions": ["damp_heat", "blood_stasis"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["清热生津", "凉血散瘀"],
        "recipes": ["藕片汤", "凉拌藕片"]
    },
    {
        "name": "绿茶",
        "name_en": "Green Tea",
        "nature": "凉",
        "flavor": "苦、甘",
        "meridians": ["心", "胃", "肺"],
        "suitable_constitutions": ["damp_heat"],
        "avoid_constitutions": ["yang_deficiency", "qi_deficiency"],
        "effects": ["清热解毒", "清心除烦"],
        "recipes": ["绿茶", "柠檬绿茶"]
    },
    {
        "name": "西瓜",
        "name_en": "Watermelon",
        "nature": "寒",
        "flavor": "甘",
        "meridians": ["心", "胃", "膀胱"],
        "suitable_constitutions": ["damp_heat", "yin_deficiency"],
        "avoid_constitutions": ["yang_deficiency", "phlegm_damp"],
        "effects": ["清热解暑", "除烦止渴", "利尿"],
        "recipes": ["西瓜汁", "西瓜沙拉"]
    },
    {
        "name": "薏米",
        "name_en": "Coix Seed",
        "nature": "凉",
        "flavor": "甘、淡",
        "meridians": ["脾", "胃", "肺"],
        "suitable_constitutions": ["damp_heat", "phlegm_damp"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["利水渗湿", "清热排脓"],
        "recipes": ["薏米红豆粥", "薏米茶"]
    },
    {
        "name": "菊花",
        "name_en": "Chrysanthemum",
        "nature": "微寒",
        "flavor": "辛、甘、苦",
        "meridians": ["肝", "肺"],
        "suitable_constitutions": ["damp_heat"],
        "avoid_constitutions": ["yang_deficiency", "qi_deficiency"],
        "effects": ["清热解毒", "清肝明目"],
        "recipes": ["菊花茶", "枸杞菊花茶"]
    },
    {
        "name": "芦荟",
        "name_en": "Aloe Vera",
        "nature": "寒",
        "flavor": "苦",
        "meridians": ["肝", "胃", "大肠"],
        "suitable_constitutions": ["damp_heat"],
        "avoid_constitutions": ["yang_deficiency", "qi_deficiency"],
        "effects": ["清热解毒", "润肠通便"],
        "recipes": ["芦荟茶", "芦荟酸奶"]
    },
    {
        "name": "荸荠",
        "name_en": "Water Chestnut",
        "nature": "寒",
        "flavor": "甘",
        "meridians": ["肺", "胃"],
        "suitable_constitutions": ["damp_heat", "yin_deficiency"],
        "avoid_constitutions": ["yang_deficiency", "phlegm_damp"],
        "effects": ["清热生津", "化痰明目"],
        "recipes": ["荸荠汁", "荸荠炒肉片"]
    },

    # 血瘀质推荐食物
    {
        "name": "黑豆",
        "name_en": "Black Bean",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["脾", "肾"],
        "suitable_constitutions": ["blood_stasis", "qi_deficiency"],
        "avoid_constitutions": ["phlegm_damp"],
        "effects": ["活血利水", "祛风解毒"],
        "recipes": ["黑豆汤", "黑豆粥"]
    },
    {
        "name": "山楂",
        "name_en": "Hawthorn",
        "nature": "微温",
        "flavor": "酸、甘",
        "meridians": ["脾", "胃", "肝"],
        "suitable_constitutions": ["blood_stasis", "phlegm_damp"],
        "avoid_constitutions": ["qi_deficiency", "yang_deficiency"],
        "effects": ["消食健胃", "行气散瘀"],
        "recipes": ["山楂茶", "山楂糕"]
    },
    {
        "name": "玫瑰花",
        "name_en": "Rose",
        "nature": "微温",
        "flavor": "甘、微苦",
        "meridians": ["肝", "脾"],
        "suitable_constitutions": ["blood_stasis", "qi_depression"],
        "avoid_constitutions": [],
        "effects": ["行气解郁", "和血止痛"],
        "recipes": ["玫瑰花茶", "玫瑰糕"]
    },
    {
        "name": "当归",
        "name_en": "Angelica",
        "nature": "温",
        "flavor": "甘、辛",
        "meridians": ["肝", "心", "脾"],
        "suitable_constitutions": ["blood_stasis", "yang_deficiency", "qi_deficiency"],
        "avoid_constitutions": ["damp_heat", "phlegm_damp"],
        "effects": ["补血活血", "调经止痛"],
        "recipes": ["当归生姜羊肉汤", "当归煮蛋"]
    },
    {
        "name": "黑木耳",
        "name_en": "Black Fungus",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["肺", "胃", "大肠"],
        "suitable_constitutions": ["blood_stasis", "peace"],
        "avoid_constitutions": ["phlegm_damp"],
        "effects": ["益气强身", "活血止血"],
        "recipes": ["凉拌黑木耳", "黑木耳炒肉"]
    },
    {
        "name": "红花",
        "name_en": "Safflower",
        "nature": "温",
        "flavor": "辛",
        "meridians": ["心", "肝"],
        "suitable_constitutions": ["blood_stasis"],
        "avoid_constitutions": [],
        "effects": ["活血通经", "祛瘀止痛"],
        "recipes": ["红花茶"]
    },
    {
        "name": "桃仁",
        "name_en": "Peach Kernel",
        "nature": "平",
        "flavor": "苦、甘",
        "meridians": ["心", "肝", "大肠"],
        "suitable_constitutions": ["blood_stasis"],
        "avoid_constitutions": [],
        "effects": ["活血祛瘀", "润肠通便"],
        "recipes": ["桃仁粥"]
    },
    {
        "name": "川芎",
        "name_en": "Szechuan Lovage",
        "nature": "温",
        "flavor": "辛",
        "meridians": ["肝", "胆", "心包"],
        "suitable_constitutions": ["blood_stasis"],
        "avoid_constitutions": ["damp_heat"],
        "effects": ["活血行气", "祛风止痛"],
        "recipes": ["川芎茶"]
    },
    {
        "name": "丹参",
        "name_en": "Salvia",
        "nature": "微寒",
        "flavor": "苦",
        "meridians": ["心", "心包", "肝"],
        "suitable_constitutions": ["blood_stasis"],
        "avoid_constitutions": [],
        "effects": ["活血祛瘀", "通经止痛", "清心除烦"],
        "recipes": ["丹参茶"]
    },
    {
        "name": "益母草",
        "name_en": "Motherwort",
        "nature": "微寒",
        "flavor": "苦、辛",
        "meridians": ["肝", "心包"],
        "suitable_constitutions": ["blood_stasis"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["活血调经", "利水消肿"],
        "recipes": ["益母草茶"]
    },

    # 气郁质推荐食物
    {
        "name": "陈皮",
        "name_en": "Dried Tangerine Peel",
        "nature": "温",
        "flavor": "辛、苦",
        "meridians": ["脾", "肺"],
        "suitable_constitutions": ["qi_depression", "phlegm_damp"],
        "avoid_constitutions": ["yin_deficiency", "damp_heat"],
        "effects": ["理气健脾", "燥湿化痰"],
        "recipes": ["陈皮茶", "陈皮粥"]
    },
    {
        "name": "玫瑰花",
        "name_en": "Rose",
        "nature": "微温",
        "flavor": "甘、微苦",
        "meridians": ["肝", "脾"],
        "suitable_constitutions": ["qi_depression", "blood_stasis"],
        "avoid_constitutions": [],
        "effects": ["行气解郁", "和血止痛"],
        "recipes": ["玫瑰花茶", "玫瑰糕"]
    },
    {
        "name": "佛手",
        "name_en": "Fingered Citron",
        "nature": "温",
        "flavor": "辛、苦、酸",
        "meridians": ["肝", "脾", "胃", "肺"],
        "suitable_constitutions": ["qi_depression"],
        "avoid_constitutions": [],
        "effects": ["疏肝解郁", "理气和胃"],
        "recipes": ["佛手茶", "佛手粥"]
    },
    {
        "name": "香附",
        "name_en": "Cyperus",
        "nature": "平",
        "flavor": "辛、微苦",
        "meridians": ["肝", "脾", "三焦"],
        "suitable_constitutions": ["qi_depression"],
        "avoid_constitutions": [],
        "effects": ["疏肝解郁", "理气宽中", "调经止痛"],
        "recipes": ["香附茶"]
    },
    {
        "name": "柑橘",
        "name_en": "Citrus",
        "nature": "凉",
        "flavor": "酸、甘",
        "meridians": ["肺", "胃"],
        "suitable_constitutions": ["qi_depression", "phlegm_damp"],
        "avoid_constitutions": [],
        "effects": ["生津止渴", "开胃下气"],
        "recipes": ["鲜榨橘汁", "柑橘茶"]
    },
    {
        "name": "柚子",
        "name_en": "Pomelo",
        "nature": "寒",
        "flavor": "酸、甘",
        "meridians": ["肺", "脾"],
        "suitable_constitutions": ["qi_depression", "phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["消食化痰", "醒酒"],
        "recipes": ["柚子茶", "蜂蜜柚子茶"]
    },
    {
        "name": "金桔",
        "name_en": "Kumquat",
        "nature": "温",
        "flavor": "辛、甘、酸",
        "meridians": ["肺", "胃"],
        "suitable_constitutions": ["qi_depression", "phlegm_damp"],
        "avoid_constitutions": [],
        "effects": ["理气解郁", "化痰醒酒"],
        "recipes": ["金桔茶", "糖渍金桔"]
    },
    {
        "name": "薄荷",
        "name_en": "Mint",
        "nature": "凉",
        "flavor": "辛",
        "meridians": ["肺", "肝"],
        "suitable_constitutions": ["qi_depression", "damp_heat"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["疏散风热", "清利头目", "疏肝行气"],
        "recipes": ["薄荷茶", "薄荷粥"]
    },
    {
        "name": "合欢花",
        "name_en": "Silk Tree Flower",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["心", "肝"],
        "suitable_constitutions": ["qi_depression"],
        "avoid_constitutions": [],
        "effects": ["解郁安神"],
        "recipes": ["合欢花茶"]
    },
    {
        "name": "薰衣草",
        "name_en": "Lavender",
        "nature": "凉",
        "flavor": "辛",
        "meridians": ["心", "肝"],
        "suitable_constitutions": ["qi_depression"],
        "avoid_constitutions": [],
        "effects": ["疏肝解郁", "安神定志"],
        "recipes": ["薰衣草茶"]
    },

    # 特禀质推荐食物
    {
        "name": "蜂蜜",
        "name_en": "Honey",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["肺", "脾", "大肠"],
        "suitable_constitutions": ["special", "peace", "qi_deficiency"],
        "avoid_constitutions": ["damp_heat", "phlegm_damp"],
        "effects": ["补中润燥", "止痛解毒"],
        "recipes": ["蜂蜜水", "蜂蜜柚子茶"]
    },
    {
        "name": "大枣",
        "name_en": "Jujube",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["脾", "胃", "心"],
        "suitable_constitutions": ["special", "qi_deficiency", "yang_deficiency"],
        "avoid_constitutions": ["damp_heat", "phlegm_damp"],
        "effects": ["补中益气", "养血安神"],
        "recipes": ["红枣茶", "红枣桂圆粥"]
    },
    {
        "name": "胡萝卜",
        "name_en": "Carrot",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["肺", "脾"],
        "suitable_constitutions": ["special", "peace", "qi_deficiency"],
        "avoid_constitutions": [],
        "effects": ["健脾化滞", "补肝明目"],
        "recipes": ["胡萝卜汤", "胡萝卜炒蛋"]
    },
    {
        "name": "南瓜",
        "name_en": "Pumpkin",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["脾", "胃"],
        "suitable_constitutions": ["special", "qi_deficiency", "yang_deficiency"],
        "avoid_constitutions": ["damp_heat"],
        "effects": ["补中益气", "消炎止痛"],
        "recipes": ["南瓜粥", "南瓜饼"]
    },
    {
        "name": "苹果",
        "name_en": "Apple",
        "nature": "凉",
        "flavor": "甘、酸",
        "meridians": ["脾", "肺"],
        "suitable_constitutions": ["special", "peace"],
        "avoid_constitutions": ["yang_deficiency", "phlegm_damp"],
        "effects": ["生津润肺", "除烦解暑"],
        "recipes": ["苹果汁", "苹果粥"]
    },
    {
        "name": "菠菜",
        "name_en": "Spinach",
        "nature": "凉",
        "flavor": "甘",
        "meridians": ["肝", "胃", "大肠"],
        "suitable_constitutions": ["special", "damp_heat", "peace"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["养血止血", "滋阴润燥"],
        "recipes": ["菠菜汤", "凉拌菠菜"]
    },
    {
        "name": "西蓝花",
        "name_en": "Broccoli",
        "nature": "凉",
        "flavor": "甘",
        "meridians": ["肾", "脾", "胃"],
        "suitable_constitutions": ["special", "damp_heat", "peace"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["补肾填精", "健脑壮骨"],
        "recipes": ["蒜蓉西蓝花", "西蓝花汤"]
    },
    {
        "name": "小米",
        "name_en": "Millet",
        "nature": "凉",
        "flavor": "甘、咸",
        "meridians": ["脾", "胃", "肾"],
        "suitable_constitutions": ["special", "peace", "qi_deficiency"],
        "avoid_constitutions": [],
        "effects": ["健脾益胃", "养心安神"],
        "recipes": ["小米粥", "小米红枣粥"]
    },
    {
        "name": "山药",
        "name_en": "Chinese Yam",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["脾", "肺", "肾"],
        "suitable_constitutions": ["special", "qi_deficiency", "peace"],
        "avoid_constitutions": ["phlegm_damp"],
        "effects": ["补脾养胃", "生津益肺", "补肾涩精"],
        "recipes": ["山药粥", "山药炖排骨"]
    },
    {
        "name": "莲藕",
        "name_en": "Lotus Root",
        "nature": "寒",
        "flavor": "甘",
        "meridians": ["肝", "肺", "胃"],
        "suitable_constitutions": ["special", "damp_heat", "blood_stasis"],
        "avoid_constitutions": ["yang_deficiency"],
        "effects": ["清热生津", "凉血散瘀"],
        "recipes": ["藕片汤", "凉拌藕片"]
    }
]
