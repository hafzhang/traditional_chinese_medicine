#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基于中医理论和权威典籍的食材数据库
来源：《中国药典》、《本草纲目》、《中医食疗学》教材
"""

# 常见食材性味归经数据库
# 基于：《中国药典》2020版、《本草纲目》、《中医食疗学》统编教材
INGREDIENT_TCM_DATABASE = {
    # ========== 谷物薯类 ==========
    "大米": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "胃"],
        "efficacy": ["补中益气", "健脾养胃"],
        "suitable": ["peace", "qi_deficiency", "yang_deficiency"],
        "avoid": [], "source": "《本草纲目》"
    },
    "小米": {
        "nature": "凉", "flavor": "甘", "meridian": ["脾", "胃"],
        "efficacy": ["健脾和胃", "补虚损"],
        "suitable": ["qi_deficiency", "yin_deficiency", "peace"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },
    "糯米": {
        "nature": "温", "flavor": "甘", "meridian": ["脾", "胃", "肺"],
        "efficacy": ["补中益气", "健脾止泻"],
        "suitable": ["qi_deficiency", "yang_deficiency"],
        "avoid": ["damp_heat", "phlegm_damp"], "source": "《中药大辞典》"
    },
    "玉米": {
        "nature": "平", "flavor": "甘", "meridian": ["胃", "大肠"],
        "efficacy": ["调中开胃", "利尿消肿"],
        "suitable": ["peace"], "avoid": [], "source": "《本草纲目》"
    },
    "红薯": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "肾"],
        "efficacy": ["补脾益胃", "通便", "生津"],
        "suitable": ["peace", "qi_deficiency"],
        "avoid": ["damp_heat"], "source": "《本草纲目拾遗》"
    },
    "山药": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "肺", "肾"],
        "efficacy": ["健脾补肺", "固肾益精"],
        "suitable": ["qi_deficiency", "yin_deficiency", "peace"],
        "avoid": ["damp_heat"], "source": "《中国药典》"
    },
    "薏米": {
        "nature": "凉", "flavor": "甘", "meridian": ["脾", "肺", "肾"],
        "efficacy": ["健脾渗湿", "清热排脓"],
        "suitable": ["phlegm_damp", "damp_heat", "qi_deficiency"],
        "avoid": ["yang_deficiency"], "source": "《中国药典》"
    },

    # ========== 蔬菜类 ==========
    "白菜": {
        "nature": "平", "flavor": "甘", "meridian": ["胃", "大肠"],
        "efficacy": ["清热除烦", "通利肠胃"],
        "suitable": ["peace", "damp_heat"], "avoid": [], "source": "《本草纲目》"
    },
    "菠菜": {
        "nature": "凉", "flavor": "甘", "meridian": ["胃", "大肠"],
        "efficacy": ["养血止血", "滋阴润燥"],
        "suitable": ["yin_deficiency", "blood_stasis", "peace"],
        "avoid": ["yang_deficiency"], "source": "《本草求真》"
    },
    "韭菜": {
        "nature": "温", "flavor": "辛", "meridian": ["肝", "胃", "肾"],
        "efficacy": ["温补肾阳", "行气活血"],
        "suitable": ["yang_deficiency", "blood_stasis"],
        "avoid": ["yin_deficiency", "damp_heat"], "source": "《本草拾遗》"
    },
    "芹菜": {
        "nature": "凉", "flavor": "甘", "meridian": ["肝", "胃"],
        "efficacy": ["清热平肝", "利尿消肿"],
        "suitable": ["damp_heat", "qi_depression", "yin_deficiency"],
        "avoid": ["yang_deficiency"], "source": "《本草推陈》"
    },
    "冬瓜": {
        "nature": "凉", "flavor": "甘", "meridian": ["肺", "大肠", "膀胱"],
        "efficacy": ["清热利水", "消肿解毒"],
        "suitable": ["phlegm_damp", "damp_heat", "yin_deficiency"],
        "avoid": ["yang_deficiency"], "source": "《名医别录》"
    },
    "黄瓜": {
        "nature": "凉", "flavor": "甘", "meridian": ["胃", "大肠"],
        "efficacy": ["清热利水", "解毒消肿"],
        "suitable": ["damp_heat", "yin_deficiency"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },
    "苦瓜": {
        "nature": "寒", "flavor": "苦", "meridian": ["心", "脾", "胃"],
        "efficacy": ["清热祛暑", "明目解毒"],
        "suitable": ["damp_heat", "yin_deficiency"],
        "avoid": ["yang_deficiency", "qi_deficiency"], "source": "《本草纲目》"
    },
    "西红柿": {
        "nature": "微寒", "flavor": "甘", "meridian": ["肝", "胃", "肺"],
        "efficacy": ["生津止渴", "健胃消食"],
        "suitable": ["yin_deficiency", "peace"],
        "avoid": ["yang_deficiency"], "source": "《陆川本草》"
    },
    "茄子": {
        "nature": "凉", "flavor": "甘", "meridian": ["脾", "胃", "大肠"],
        "efficacy": ["清热活血", "消肿止痛"],
        "suitable": ["blood_stasis", "damp_heat"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },
    "胡萝卜": {
        "nature": "平", "flavor": "甘", "meridian": ["肺", "脾"],
        "efficacy": ["健脾消食", "补肝明目"],
        "suitable": ["peace", "qi_deficiency"],
        "avoid": [], "source": "《本草求真》"
    },
    "白萝卜": {
        "nature": "凉", "flavor": "辛", "meridian": ["肺", "胃"],
        "efficacy": ["清热生津", "下气消食"],
        "suitable": ["damp_heat", "qi_depression", "peace"],
        "avoid": ["yang_deficiency", "qi_deficiency"], "source": "《本草纲目》"
    },
    "莲藕": {
        "nature": "寒", "flavor": "甘", "meridian": ["心", "脾", "胃"],
        "efficacy": ["清热生津", "凉血止血"],
        "suitable": ["yin_deficiency", "damp_heat", "blood_stasis"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },
    "百合": {
        "nature": "微寒", "flavor": "甘", "meridian": ["心", "肺"],
        "efficacy": ["养阴润肺", "清心安神"],
        "suitable": ["yin_deficiency", "qi_depression"],
        "avoid": ["yang_deficiency", "phlegm_damp"], "source": "《中国药典》"
    },
    "芋头": {
        "nature": "平", "flavor": "甘", "meridian": ["肠", "胃"],
        "efficacy": ["健脾补虚", "散结"],
        "suitable": ["qi_deficiency", "peace"],
        "avoid": ["damp_heat"], "source": "《本草纲目》"
    },
    "竹笋": {
        "nature": "寒", "flavor": "甘", "meridian": ["胃", "大肠"],
        "efficacy": ["清热化痰", "利水消肿"],
        "suitable": ["phlegm_damp", "damp_heat"],
        "avoid": ["yang_deficiency", "qi_deficiency"], "source": "《本草纲目拾遗》"
    },

    # ========== 豆类 ==========
    "黄豆": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "胃"],
        "efficacy": ["健脾利湿", "补虚"],
        "suitable": ["peace", "qi_deficiency", "phlegm_damp"],
        "avoid": [], "source": "《日用本草》"
    },
    "黑豆": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "肾"],
        "efficacy": ["补肾益阴", "健脾利湿"],
        "suitable": ["yin_deficiency", "qi_deficiency", "peace"],
        "avoid": [], "source": "《本草纲目》"
    },
    "红豆": {
        "nature": "平", "flavor": "甘", "meridian": ["心", "小肠"],
        "efficacy": ["利水消肿", "解毒排脓"],
        "suitable": ["phlegm_damp", "damp_heat"],
        "avoid": [], "source": "《本草纲目》"
    },
    "绿豆": {
        "nature": "寒", "flavor": "甘", "meridian": ["心", "胃"],
        "efficacy": ["清热解毒", "消暑利水"],
        "suitable": ["damp_heat", "yin_deficiency"],
        "avoid": ["yang_deficiency", "qi_deficiency"], "source": "《本草纲目》"
    },
    "豆腐": {
        "nature": "凉", "flavor": "甘", "meridian": ["脾", "胃", "大肠"],
        "efficacy": ["益气和中", "生津润燥"],
        "suitable": ["peace", "yin_deficiency", "qi_deficiency"],
        "avoid": ["yang_deficiency", "phlegm_damp"], "source": "《本草纲目》"
    },

    # ========== 水果类 ==========
    "苹果": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "肺"],
        "efficacy": ["健脾开胃", "生津止渴"],
        "suitable": ["peace"], "avoid": [], "source": "《千金·食治》"
    },
    "梨": {
        "nature": "凉", "flavor": "甘", "meridian": ["肺", "胃"],
        "efficacy": ["清热生津", "润肺化痰"],
        "suitable": ["yin_deficiency", "damp_heat", "phlegm_damp"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },
    "香蕉": {
        "nature": "寒", "flavor": "甘", "meridian": ["肺", "大肠"],
        "efficacy": ["清热润肠"],
        "suitable": ["yin_deficiency", "damp_heat"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目拾遗》"
    },
    "西瓜": {
        "nature": "寒", "flavor": "甘", "meridian": ["心", "胃", "膀胱"],
        "efficacy": ["清热解暑", "除烦止渴", "利小便"],
        "suitable": ["damp_heat", "yin_deficiency"],
        "avoid": ["yang_deficiency", "qi_deficiency"], "source": "《本草纲目》"
    },
    "桃": {
        "nature": "温", "flavor": "甘", "meridian": ["胃", "大肠"],
        "efficacy": ["生津润肠", "活血消积"],
        "suitable": ["yang_deficiency", "blood_stasis"],
        "avoid": [], "source": "《本草纲目》"
    },
    "柿子": {
        "nature": "寒", "flavor": "甘", "meridian": ["肺", "胃"],
        "efficacy": ["清热润肺", "生津止渴"],
        "suitable": ["yin_deficiency", "damp_heat"],
        "avoid": ["yang_deficiency", "phlegm_damp"], "source": "《本草纲目》"
    },
    "橘子": {
        "nature": "温", "flavor": "甘", "meridian": ["肺", "胃"],
        "efficacy": ["开胃理气", "止咳润肺"],
        "suitable": ["yang_deficiency", "phlegm_damp"],
        "avoid": ["yin_deficiency"], "source": "《本草纲目》"
    },
    "橙子": {
        "nature": "凉", "flavor": "酸", "meridian": ["肺", "胃"],
        "efficacy": ["生津止渴", "开胃下气"],
        "suitable": ["yin_deficiency", "qi_depression"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },
    "红枣": {
        "nature": "温", "flavor": "甘", "meridian": ["脾", "胃"],
        "efficacy": ["补中益气", "养血安神"],
        "suitable": ["qi_deficiency", "yang_deficiency", "blood_stasis"],
        "avoid": ["damp_heat", "phlegm_damp"], "source": "《中国药典》"
    },
    "桂圆": {
        "nature": "温", "flavor": "甘", "meridian": ["心", "脾"],
        "efficacy": ["补益心脾", "养血安神"],
        "suitable": ["qi_deficiency", "yang_deficiency", "blood_stasis"],
        "avoid": ["damp_heat", "yin_deficiency"], "source": "《本草纲目》"
    },
    "山楂": {
        "nature": "微温", "flavor": "酸", "meridian": ["脾", "胃", "肝"],
        "efficacy": ["消食化积", "行气散瘀"],
        "suitable": ["qi_depression", "blood_stasis", "phlegm_damp"],
        "avoid": ["qi_deficiency", "yang_deficiency"], "source": "《中国药典》"
    },
    "荔枝": {
        "nature": "温", "flavor": "甘", "meridian": ["脾", "肝"],
        "efficacy": ["补脾益肝", "理气补血"],
        "suitable": ["yang_deficiency", "qi_deficiency", "blood_stasis"],
        "avoid": ["damp_heat", "yin_deficiency"], "source": "《本草纲目》"
    },
    "葡萄": {
        "nature": "平", "flavor": "甘", "meridian": ["肺", "脾", "肾"],
        "efficacy": ["补气血", "强筋骨"],
        "suitable": ["peace", "qi_deficiency", "blood_stasis"],
        "avoid": [], "source": "《本草纲目》"
    },

    # ========== 肉类 ==========
    "猪肉": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "胃", "肾"],
        "efficacy": ["滋阴润燥", "补肾养血"],
        "suitable": ["peace", "yin_deficiency", "qi_deficiency"],
        "avoid": ["phlegm_damp"], "source": "《本草纲目》"
    },
    "牛肉": {
        "nature": "温", "flavor": "甘", "meridian": ["脾", "胃"],
        "efficacy": ["补脾胃", "益气血", "强筋骨"],
        "suitable": ["qi_deficiency", "yang_deficiency"],
        "avoid": [], "source": "《本草纲目》"
    },
    "羊肉": {
        "nature": "温", "flavor": "甘", "meridian": ["脾", "肾"],
        "efficacy": ["温中补虚", "补肾助阳"],
        "suitable": ["yang_deficiency", "qi_deficiency"],
        "avoid": ["yin_deficiency", "damp_heat"], "source": "《本草纲目》"
    },
    "鸡肉": {
        "nature": "温", "flavor": "甘", "meridian": ["脾", "胃"],
        "efficacy": ["温中益气", "补精填髓"],
        "suitable": ["qi_deficiency", "yang_deficiency"],
        "avoid": [], "source": "《本草纲目》"
    },
    "鸭肉": {
        "nature": "凉", "flavor": "甘", "meridian": ["脾", "胃", "肺", "肾"],
        "efficacy": ["滋阴养胃", "利水消肿"],
        "suitable": ["yin_deficiency", "damp_heat", "phlegm_damp"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },
    "鸡蛋": {
        "nature": "平", "flavor": "甘", "meridian": ["肺", "脾", "胃"],
        "efficacy": ["补肺养血", "滋阴润燥"],
        "suitable": ["peace", "qi_deficiency", "yin_deficiency"],
        "avoid": [], "source": "《本草纲目》"
    },

    # ========== 海鲜类 ==========
    "鱼": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "胃", "肾"],
        "efficacy": ["健脾利水", "补肝益肾"],
        "suitable": ["peace", "qi_deficiency"], "avoid": [], "source": "《本草纲目》"
    },
    "鲫鱼": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "胃", "大肠"],
        "efficacy": ["健脾利湿", "补虚"],
        "suitable": ["qi_deficiency", "phlegm_damp", "peace"],
        "avoid": [], "source": "《本草经疏》"
    },
    "鲤鱼": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "肾"],
        "efficacy": ["健脾利水", "下气通乳"],
        "suitable": ["peace", "qi_deficiency", "phlegm_damp"],
        "avoid": [], "source": "《本草纲目》"
    },
    "虾": {
        "nature": "温", "flavor": "甘", "meridian": ["肝", "肾"],
        "efficacy": ["补肾壮阳", "通乳"],
        "suitable": ["yang_deficiency", "qi_deficiency"],
        "avoid": ["yin_deficiency", "damp_heat"], "source": "《本草纲目》"
    },
    "螃蟹": {
        "nature": "寒", "flavor": "咸", "meridian": ["肝", "胃"],
        "efficacy": ["清热解毒", "散瘀消肿"],
        "suitable": ["damp_heat", "blood_stasis", "yin_deficiency"],
        "avoid": ["yang_deficiency", "qi_deficiency"], "source": "《本草纲目》"
    },

    # ========== 调味品类 ==========
    "生姜": {
        "nature": "温", "flavor": "辛", "meridian": ["肺", "胃", "脾"],
        "efficacy": ["发汗解表", "温中止呕", "温肺止咳"],
        "suitable": ["yang_deficiency", "phlegm_damp"],
        "avoid": ["yin_deficiency", "damp_heat"], "source": "《中国药典》"
    },
    "大蒜": {
        "nature": "温", "flavor": "辛", "meridian": ["脾", "胃", "肺"],
        "efficacy": ["温中消食", "解毒杀虫"],
        "suitable": ["yang_deficiency", "phlegm_damp"],
        "avoid": ["yin_deficiency", "damp_heat"], "source": "《本草纲目》"
    },
    "葱": {
        "nature": "温", "flavor": "辛", "meridian": ["肺", "胃"],
        "efficacy": ["发汗解表", "通阳止痛"],
        "suitable": ["yang_deficiency"], "avoid": ["yin_deficiency"], "source": "《本草纲目》"
    },
    "辣椒": {
        "nature": "热", "flavor": "辛", "meridian": ["心", "脾"],
        "efficacy": ["温中散寒", "开胃消食"],
        "suitable": ["yang_deficiency"],
        "avoid": ["yin_deficiency", "damp_heat", "phlegm_damp"], "source": "《本草纲目拾遗》"
    },
    "花椒": {
        "nature": "温", "flavor": "辛", "meridian": ["脾", "胃", "肾"],
        "efficacy": ["温中止痛", "杀虫止痒"],
        "suitable": ["yang_deficiency", "phlegm_damp"],
        "avoid": ["yin_deficiency", "damp_heat"], "source": "《中国药典》"
    },
    "胡椒": {
        "nature": "热", "flavor": "辛", "meridian": ["胃", "大肠"],
        "efficacy": ["温中散寒", "下气止痛"],
        "suitable": ["yang_deficiency"],
        "avoid": ["yin_deficiency", "damp_heat", "phlegm_damp"], "source": "《本草纲目》"
    },
    "盐": {
        "nature": "寒", "flavor": "咸", "meridian": ["胃", "肾", "大肠", "小肠"],
        "efficacy": ["清热解毒", "凉血"],
        "suitable": ["yin_deficiency", "damp_heat"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },
    "醋": {
        "nature": "温", "flavor": "酸", "meridian": ["肝", "胃"],
        "efficacy": ["活血散瘀", "消食化积"],
        "suitable": ["blood_stasis", "qi_depression"],
        "avoid": ["qi_deficiency"], "source": "《本草纲目》"
    },
    "白糖": {
        "nature": "平", "flavor": "甘", "meridian": ["肺", "脾"],
        "efficacy": ["润肺生津", "补中缓急"],
        "suitable": ["peace", "qi_deficiency"],
        "avoid": ["damp_heat"], "source": "《本草纲目》"
    },
    "蜂蜜": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "肺", "大肠"],
        "efficacy": ["补中润燥", "止痛解毒"],
        "suitable": ["peace", "qi_deficiency", "yin_deficiency"],
        "avoid": ["damp_heat", "phlegm_damp"], "source": "《中国药典》"
    },

    # ========== 菌藻类 ==========
    "香菇": {
        "nature": "平", "flavor": "甘", "meridian": ["肝", "胃"],
        "efficacy": ["扶正补虚", "健脾开胃"],
        "suitable": ["peace", "qi_deficiency"],
        "avoid": [], "source": "《本草求真》"
    },
    "木耳": {
        "nature": "平", "flavor": "甘", "meridian": ["胃", "大肠"],
        "efficacy": ["益气润肺", "凉血止血"],
        "suitable": ["peace", "yin_deficiency", "blood_stasis"],
        "avoid": [], "source": "《本草纲目》"
    },
    "海带": {
        "nature": "寒", "flavor": "咸", "meridian": ["肝", "胃", "肾"],
        "efficacy": ["消痰软坚", "利水消肿"],
        "suitable": ["phlegm_damp", "yin_deficiency"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },
    "紫菜": {
        "nature": "寒", "flavor": "甘", "meridian": ["肺"],
        "efficacy": ["化痰软坚", "清热利尿"],
        "suitable": ["phlegm_damp", "damp_heat"],
        "avoid": ["yang_deficiency"], "source": "《本草纲目》"
    },

    # ========== 坚果种子类 ==========
    "花生": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "肺"],
        "efficacy": ["健脾养胃", "润肺化痰"],
        "suitable": ["peace", "qi_deficiency", "yin_deficiency"],
        "avoid": ["phlegm_damp"], "source": "《本草纲目拾遗》"
    },
    "核桃": {
        "nature": "温", "flavor": "甘", "meridian": ["肾", "肺", "大肠"],
        "efficacy": ["补肾温肺", "润肠通便"],
        "suitable": ["yang_deficiency", "qi_deficiency", "yin_deficiency"],
        "avoid": ["damp_heat", "phlegm_damp"], "source": "《本草纲目》"
    },
    "莲子": {
        "nature": "平", "flavor": "甘", "meridian": ["脾", "肾", "心"],
        "efficacy": ["补脾止泻", "益肾固精", "养心安神"],
        "suitable": ["qi_deficiency", "peace", "yin_deficiency"],
        "avoid": ["damp_heat", "phlegm_damp"], "source": "《中国药典》"
    },
    "芝麻": {
        "nature": "平", "flavor": "甘", "meridian": ["肝", "肾", "大肠"],
        "efficacy": ["补肝肾", "润肠燥"],
        "suitable": ["peace", "yin_deficiency", "blood_stasis"],
        "avoid": [], "source": "《本草纲目》"
    },

    # ========== 药食同源类 ==========
    "人参": {
        "nature": "微温", "flavor": "甘", "meridian": ["脾", "肺", "心"],
        "efficacy": ["大补元气", "补脾益肺", "生津安神"],
        "suitable": ["qi_deficiency", "yang_deficiency"],
        "avoid": ["damp_heat", "yin_deficiency"], "source": "《中国药典》"
    },
    "黄芪": {
        "nature": "微温", "flavor": "甘", "meridian": ["脾", "肺"],
        "efficacy": ["补气升阳", "固表止汗", "利水消肿"],
        "suitable": ["qi_deficiency", "yang_deficiency"],
        "avoid": ["yin_deficiency", "damp_heat"], "source": "《中国药典》"
    },
    "当归": {
        "nature": "温", "flavor": "甘", "meridian": ["肝", "心", "脾"],
        "efficacy": ["补血活血", "调经止痛"],
        "suitable": ["blood_stasis", "qi_deficiency", "yang_deficiency"],
        "avoid": ["damp_heat", "phlegm_damp"], "source": "《中国药典》"
    },
    "枸杞": {
        "nature": "平", "flavor": "甘", "meridian": ["肝", "肾", "肺"],
        "efficacy": ["滋补肝肾", "益精明目"],
        "suitable": ["peace", "yin_deficiency", "blood_stasis"],
        "avoid": [], "source": "《中国药典》"
    },
    "银耳": {
        "nature": "平", "flavor": "甘", "meridian": ["肺", "胃", "肾"],
        "efficacy": ["滋阴润肺", "养胃生津"],
        "suitable": ["yin_deficiency", "peace"],
        "avoid": ["damp_heat", "phlegm_damp"], "source": "《本草纲目》"
    },
}

# 节气与推荐食材映射
SOLAR_TERM_INGREDIENTS = {
    "立春": ["韭菜", "菠菜", "葱", "萝卜"],
    "雨水": ["山药", "红枣", "莲子"],
    "惊蛰": ["梨", "银耳", "百合"],
    "春分": ["菠菜", "荠菜", "春笋"],
    "清明": ["菠菜", "芹菜", "韭菜"],
    "谷雨": ["香椿", "菠菜", "韭菜"],

    "立夏": ["黄瓜", "西红柿", "苦瓜"],
    "小满": ["黄瓜", "冬瓜", "苦瓜"],
    "芒种": ["绿豆", "西瓜", "苦瓜"],
    "夏至": ["绿豆", "西瓜", "黄瓜"],
    "小暑": ["绿豆", "西瓜", "苦瓜"],
    "大暑": ["绿豆", "西瓜", "冬瓜"],

    "立秋": ["梨", "银耳", "百合"],
    "处暑": ["梨", "银耳", "百合"],
    "白露": ["梨", "银耳", "百合"],
    "秋分": ["梨", "百合", "银耳"],
    "寒露": ["梨", "百合", "柿子"],
    "霜降": ["梨", "柿子", "百合"],

    "立冬": ["萝卜", "白菜", "羊肉"],
    "小雪": ["萝卜", "白菜", "羊肉"],
    "大雪": ["羊肉", "萝卜", "白菜"],
    "冬至": ["羊肉", "萝卜", "韭菜"],
    "小寒": ["羊肉", "韭菜", "生姜"],
    "大寒": ["羊肉", "韭菜", "生姜"],
}

# 体质与推荐食材映射
CONSTITUTION_INGREDIENTS = {
    "peace": list(INGREDIENT_TCM_DATABASE.keys()),  # 平和质适合大部分食物

    "qi_deficiency": [
        "山药", "红枣", "小米", "鸡肉", "牛肉", "鲫鱼",
        "香菇", "莲子", "黄芪", "人参", "糯米"
    ],

    "yang_deficiency": [
        "羊肉", "韭菜", "生姜", "大蒜", "辣椒", "花椒",
        "胡椒", "桂圆", "荔枝", "鸡肉", "核桃"
    ],

    "yin_deficiency": [
        "梨", "银耳", "百合", "绿豆", "黄瓜", "西红柿",
        "鸭肉", "鸡蛋", "菠菜", "冬瓜", "莲藕"
    ],

    "phlegm_damp": [
        "冬瓜", "薏米", "红豆", "陈皮", "生姜", "大蒜",
        "鲤鱼", "海带", "紫菜", "白萝卜", "山楂"
    ],

    "damp_heat": [
        "绿豆", "苦瓜", "黄瓜", "冬瓜", "芹菜", "西红柿",
        "莲藕", "薏米", "鸭肉", "鲤鱼", "海带"
    ],

    "blood_stasis": [
        "当归", "红花", "山楂", "醋", "黑木耳", "洋葱",
        "生姜", "大蒜", "韭菜", "螃蟹", "葡萄"
    ],

    "qi_depression": [
        "陈皮", "佛手", "玫瑰", "芹菜", "菠菜", "萝卜",
        "山楂", "醋", "洋葱", "大蒜", "韭菜"
    ],

    "special": [
        "小米", "大米", "苹果", "胡萝卜", "土豆", "山药",
        "鸡肉", "牛肉", "鲤鱼"  # 温和、不易过敏的食物
    ],
}
