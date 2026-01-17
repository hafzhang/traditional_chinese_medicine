-- 中医体质养生助手 - 数据库初始化脚本
-- 适用于 PostgreSQL

-- 创建数据库
-- CREATE DATABASE tcm_db;

-- 连接到数据库
-- \c tcm_db;

-- ============================================
-- 用户表
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- 抖音/微信 openid
    douyin_openid VARCHAR(128) UNIQUE,
    wechat_openid VARCHAR(128) UNIQUE,
    unionid VARCHAR(128),

    -- 基础信息
    nickname VARCHAR(100),
    avatar_url VARCHAR(500),
    gender INT CHECK (gender IN (0, 1, 2)),  -- 0:未知 1:男 2:女
    age INT,
    region VARCHAR(100),
    phone VARCHAR(20),

    -- 会员信息
    member_level VARCHAR(20) DEFAULT 'free', -- free, silver, gold, diamond
    member_expire_at TIMESTAMP,

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 体质结果表
-- ============================================
CREATE TABLE IF NOT EXISTS constitution_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,

    -- 体质类型
    primary_constitution VARCHAR(50) NOT NULL,
    secondary_constitutions JSONB,

    -- 各维度得分
    scores JSONB NOT NULL,

    -- 测试详情
    answers JSONB,  -- 用户答案
    duration INT,   -- 完成时长(秒)

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 食物库
-- ============================================
CREATE TABLE IF NOT EXISTS foods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,

    -- 中医属性
    nature VARCHAR(20), -- 寒、凉、平、温、热
    flavor VARCHAR(50), -- 酸、苦、甘、辛、咸、涩
    meridians TEXT[],  -- 归经

    -- 体质适配
    suitable_constitutions TEXT[],
    avoid_constitutions TEXT[],

    -- 营养信息
    nutrition_info JSONB,

    -- 图片
    images TEXT[],

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 推荐食谱表
-- ============================================
CREATE TABLE IF NOT EXISTS recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,

    -- 适用体质
    suitable_constitutions TEXT[],

    -- 食材和步骤
    ingredients JSONB,
    steps JSONB,

    -- 图片
    images TEXT[],

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 运动方案表
-- ============================================
CREATE TABLE IF NOT EXISTS exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,

    -- 适用体质
    suitable_constitutions TEXT[],

    -- 运动类型
    exercise_type VARCHAR(50), -- aerobic, strength, flexibility, balance

    -- 时长和强度
    duration_min INT,
    intensity VARCHAR(20), -- low, medium, high

    -- 图片/视频
    images TEXT[],
    video_url VARCHAR(500),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 创建索引
-- ============================================

-- 用户表索引
CREATE INDEX IF NOT EXISTS idx_users_douyin_openid ON users(douyin_openid);
CREATE INDEX IF NOT EXISTS idx_users_wechat_openid ON users(wechat_openid);

-- 体质结果表索引
CREATE INDEX IF NOT EXISTS idx_results_user ON constitution_results(user_id);
CREATE INDEX IF NOT EXISTS idx_results_created ON constitution_results(created_at DESC);

-- 食物库索引
CREATE INDEX IF NOT EXISTS idx_foods_suitable ON foods USING GIN(suitable_constitutions);
CREATE INDEX IF NOT EXISTS idx_foods_avoid ON foods USING GIN(avoid_constitutions);

-- 食谱表索引
CREATE INDEX IF NOT EXISTS idx_recipes_suitable ON recipes USING GIN(suitable_constitutions);

-- ============================================
-- 插入示例数据
-- ============================================

-- 插入食物示例数据
INSERT INTO foods (name, nature, flavor, meridians, suitable_constitutions, avoid_constitutions) VALUES
('山药', '平', '甘', ARRAY['脾', '肺', '肾'], ARRAY['qi_deficiency', 'yin_deficiency'], ARRAY['phlegm_damp']),
('大枣', '温', '甘', ARRAY['脾', '胃'], ARRAY['qi_deficiency', 'yang_deficiency'], ARRAY['damp_heat']),
('生姜', '温', '辛', ARRAY['肺', '脾'], ARRAY['yang_deficiency', 'phlegm_damp'], ARRAY['yin_deficiency']),
('绿豆', '寒', '甘', ARRAY['心', '胃'], ARRAY['damp_heat', 'yin_deficiency'], ARRAY['yang_deficiency']),
('羊肉', '温', '甘', ARRAY['脾', '肾'], ARRAY['yang_deficiency', 'qi_deficiency'], ARRAY['yin_deficiency', 'damp_heat']),
('鸭肉', '寒', '甘', ARRAY['脾', '肺'], ARRAY['yin_deficiency', 'damp_heat'], ARRAY['yang_deficiency']),
('山楂', '微温', '酸、甘', ARRAY['脾', '胃', '肝'], ARRAY['phlegm_damp', 'blood_stasis'], ARRAY['qi_deficiency', 'special']),
('银耳', '平', '甘', ARRAY['肺', '胃'], ARRAY['yin_deficiency', 'peace'], ARRAY['phlegm_damp']),
('百合', '微寒', '甘', ARRAY['心', '肺'], ARRAY['yin_deficiency', 'peace'], ARRAY['yang_deficiency']),
('薏米', '微寒', '甘', ARRAY['脾', '肺'], ARRAY['phlegm_damp', 'damp_heat'], ARRAY['yang_deficiency'])
ON CONFLICT DO NOTHING;

-- 插入食谱示例数据
INSERT INTO recipes (name, description, suitable_constitutions, ingredients, steps) VALUES
('黄芪炖鸡', '补气健脾，增强体质', ARRAY['qi_deficiency'],
 '{"main": ["鸡肉500g", "黄芪30g", "大枣10枚"], "seasoning": ["生姜", "盐"]}'::jsonb,
 '["鸡肉切块焯水", "加入黄芪、大枣、生姜", "小火炖煮1小时", "加盐调味即可"]'::jsonb),
('山药粥', '健脾养胃，补气养血', ARRAY['qi_deficiency', 'peace'],
 '{"main": ["山药100g", "大米50g", "小米30g"], "seasoning": ["红枣", "枸杞"]}'::jsonb,
 '["山药去皮切丁", "大米小米洗净", "所有材料煮粥", "煮至软烂即可"]'::jsonb),
('姜枣茶', '温中散寒，补气养血', ARRAY['yang_deficiency', 'qi_deficiency'],
 '{"main": ["生姜3片", "大枣5枚", "红糖适量"]}'::jsonb,
 '["生姜切片", "大枣去核", "煮水15分钟", "加入红糖调味即可"]'::jsonb),
('百合银耳汤', '滋阴润燥，养颜美容', ARRAY['yin_deficiency', 'peace'],
 '{"main": ["百合20g", "银耳10g", "冰糖适量"]}'::jsonb,
 '["银耳泡发撕小朵", "百合洗净", "加冰糖煮30分钟", "煮至粘稠即可"]'::jsonb),
('冬瓜薏米汤', '健脾利湿，清热排毒', ARRAY['phlegm_damp', 'damp_heat'],
 '{"main": ["冬瓜200g", "薏米50g"], "seasoning": ["盐"]}'::jsonb,
 '["薏米提前浸泡", "冬瓜带皮切块", "煮汤40分钟", "加盐调味即可"]'::jsonb)
ON CONFLICT DO NOTHING;

-- ============================================
-- 创建视图
-- ============================================

-- 用户体质统计视图
CREATE OR REPLACE VIEW user_constitution_stats AS
SELECT
    u.id as user_id,
    u.nickname,
    cr.primary_constitution,
    cr.scores,
    cr.created_at as last_test_at
FROM users u
LEFT JOIN LATERAL (
    SELECT *
    FROM constitution_results
    WHERE user_id = u.id
    ORDER BY created_at DESC
    LIMIT 1
) cr ON true;

-- ============================================
-- 授权（根据实际情况修改）
-- ============================================
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tcm_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tcm_user;

COMMENT ON DATABASE tcm_db IS '中医体质养生助手数据库';
COMMENT ON TABLE users IS '用户表';
COMMENT ON TABLE constitution_results IS '体质测试结果表';
COMMENT ON TABLE foods IS '食物库';
COMMENT ON TABLE recipes IS '食谱表';
