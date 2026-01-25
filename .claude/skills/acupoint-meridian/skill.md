# id: acupoint-meridian
# name: 穴位与经络查询系统
# description: 提供272个标准穴位数据、症状→穴位映射、12经络分类与GIF资源管理的专业能力
# version: 1.0.0
# author: Claude Code
# tags: [tcm, acupoint, meridian, chinese-medicine]

---

## 穴位与经络查询系统 Skill

### 核心数据结构

#### Acupoint 模型 (backend/api/models/__init__.py)
```python
class Acupoint(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    code = Column(String(50), unique=True, index=True)  # 拼音代码，如 "baihui"
    pinyin = Column(String(100))
    meridian = Column(String(50), nullable=False, index=True)  # 所属经络
    location = Column(Text)  # 定位描述
    functions = Column(Text)  # 功效
    indications = Column(Text)  # 主治
    methods = Column(Text)  # 操作方法
    image_url = Column(String(500))  # 穴位图片URL
    aliases = Column(JSON, nullable=False, default=list)  # 别名数组
```

#### SymptomAcupoint 模型（症状→穴位关联）
```python
class SymptomAcupoint(Base):
    id = Column(Integer, primary_key=True)
    symptom = Column(String(200), nullable=False, index=True)
    acupoint_id = Column(Integer, ForeignKey("acupoints.id"), nullable=False)
    priority = Column(Integer, default=0)  # 优先级，排序用
```

---

### 12 经络标准分类

| 中文名称 | 英文代码 | GIF 文件名 |
|---------|---------|-----------|
| 手太阴肺经 | lung_lung | 手太阴肺经.gif |
| 手阳明大肠经 | large_intestine | 手阳明大肠经.gif |
| 足阳明胃经 | stomach | 足阳明胃经.gif |
| 足太阴脾经 | spleen | 足太阴脾经.gif |
| 手少阴心经 | heart | 手少阴心经.gif |
| 手太阳小肠经 | small_intestine | 手太阳小肠经.gif |
| 足太阳膀胱经 | bladder | 足太阳膀胱经.gif |
| 足少阴肾经 | kidney | 足少阴肾经.gif |
| 手厥阴心包经 | pericardium | 手厥阴心包经.gif |
| 手少阳三焦经 | sanjiao | 手少阳三焦经.gif |
| 足少阳胆经 | gallbladder | 足少阳胆经.gif |
| 足厥阴肝经 | liver | 足厥阴肝经.gif |

**GIF 资源路径**: `frontend/src/static/acupoints/meridians/{经络名称}.gif`

---

### 穴位图片命名规范

#### 单穴位图片
- **格式**: `{穴位名称}.jpg`
- **路径**: `backend/static/acupoints/{穴位名称}.jpg`
- **示例**: `百会.jpg`, `合谷.jpg`, `足三里.jpg`
- **数量**: 214 个单穴位图片

#### 图片映射文件
- **路径**: `backend/static/acupoints/acupoint_images.json`
- **格式**:
```json
{
  "百会": {
    "image": "/static/acupoints/百会.jpg",
    "single": true
  }
}
```

---

### 服务层模式

#### AcupointService 核心方法

```python
class AcupointService:
    def get_acupoint_by_id(self, acupoint_id: int, db: Session) -> Optional[Acupoint]:
        """根据ID获取穴位"""

    def get_acupoint_by_name(self, name: str, db: Session) -> Optional[Acupoint]:
        """根据名称或别名获取穴位"""

    def search_acupoints(
        self,
        keyword: str,
        db: Session,
        skip: int = 0,
        limit: int = 20
    ) -> List[Acupoint]:
        """关键词搜索（名称、拼音、别名）"""

    def get_acupoints_by_meridian(
        self,
        meridian: str,
        db: Session
    ) -> List[Acupoint]:
        """获取某经络的所有穴位"""

    def get_acupoints_by_symptom(
        self,
        symptom: str,
        db: Session
    ) -> List[Dict[str, Any]]:
        """根据症状查找穴位（按 priority 排序）"""

    def get_acupoints_by_body_part(
        self,
        part: str,
        db: Session
    ) -> List[Dict[str, Any]]:
        """根据部位查找穴位"""
```

---

### API 端点规范

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/acupoints` | GET | 获取穴位列表（分页） |
| `/api/acupoints/{id}` | GET | 获取穴位详情 |
| `/api/acupoints/search` | GET | 关键词搜索 |
| `/api/acupoints/by-meridian` | GET | 按经络查询 |
| `/api/acupoints/by-symptom` | GET | 按症状查询 |
| `/api/acupoints/by-part` | GET | 按部位查询 |
| `/api/acupoints/meridians` | GET | 获取经络列表 |
| `/api/acupoints/body-parts` | GET | 获取部位列表 |

---

### 前端页面结构

#### 穴位列表页 (pages/acupoints/list.vue)

**页面布局**：
```
┌─────────────────────────────────────┐
│  [搜索框]           🔍              │
├─────────────────────────────────────┤
│  [按经络] [按部位]  ← Tab 切换      │
├─────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐           │
│  │  百会   │ │  合谷   │           │
│  │ Baihui  │ │ Hegu    │           │
│  └─────────┘ └─────────┘           │
│  ┌─────────┐ ┌─────────┐           │
│  │ 足三里  │ │  内关   │           │
│  │ Zusanli │ │ Neiguan │           │
│  └─────────┘ └─────────┘           │
│                                     │
│        [加载更多 / 分页]            │
└─────────────────────────────────────┘
```

**功能规范**：
```vue
<template>
  <view class="acupoint-list">
    <!-- 搜索框 -->
    <view class="search-bar">
      <input v-model="keyword" placeholder="搜索穴位名称/拼音" />
    </view>

    <!-- Tab 切换 -->
    <view class="tabs">
      <view
        :class="['tab', { active: activeTab === 'meridian' }]"
        @click="switchTab('meridian')"
      >按经络</view>
      <view
        :class="['tab', { active: activeTab === 'part' }]"
        @click="switchTab('part')"
      >按部位</view>
    </view>

    <!-- 经络列表（按经络 Tab） -->
    <view v-if="activeTab === 'meridian'" class="meridian-list">
      <view
        v-for="meridian in meridians"
        :key="meridian.code"
        class="meridian-section"
      >
        <view class="meridian-title">{{ meridian.name }}</view>
        <view class="acupoint-grid">
          <view
            v-for="point in meridian.acupoints"
            :key="point.id"
            class="acupoint-card"
            @click="goDetail(point.id)"
          >
            <text class="name">{{ point.name }}</text>
            <text class="pinyin">{{ point.pinyin }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 部位列表（按部位 Tab） -->
    <view v-if="activeTab === 'part'" class="part-list">
      <view
        v-for="part in bodyParts"
        :key="part.code"
        class="part-section"
      >
        <view class="part-title">{{ part.name }}</view>
        <view class="acupoint-grid">
          <view
            v-for="point in part.acupoints"
            :key="point.id"
            class="acupoint-card"
            @click="goDetail(point.id)"
          >
            <text class="name">{{ point.name }}</text>
            <text class="pinyin">{{ point.pinyin }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>
```

**样式规范**：
```scss
.acupoint-list {
  background: #f5f5f5;
  min-height: 100vh;

  .search-bar {
    padding: 20rpx;
    background: #fff;

    input {
      height: 70rpx;
      background: #f5f5f5;
      border-radius: 35rpx;
      padding: 0 30rpx;
    }
  }

  .tabs {
    display: flex;
    background: #fff;
    border-bottom: 1rpx solid #eee;

    .tab {
      flex: 1;
      text-align: center;
      padding: 30rpx 0;
      font-size: 32rpx;
      color: #666;

      &.active {
        color: #1acc76;
        border-bottom: 4rpx solid #1acc76;
      }
    }
  }

  .acupoint-card {
    background: #fff;
    border-radius: 16rpx;
    padding: 30rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.08);

    .name {
      display: block;
      font-size: 36rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 10rpx;
    }

    .pinyin {
      display: block;
      font-size: 24rpx;
      color: #999;
    }
  }
}
```

---

#### 穴位详情页 (pages/acupoints/detail.vue)

**页面布局**：
```
┌─────────────────────────────────────┐
│  ← 返回              穴位详情        │
├─────────────────────────────────────┤
│                                     │
│        ┌─────────────────┐          │
│        │                 │          │
│        │   穴位图片      │          │
│        │                 │          │
│        └─────────────────┘          │
│                                     │
│           百会 (GV20)               │
│        手太阴肺经 · 督脉            │
│                                     │
├─────────────────────────────────────┤
│  【定位】                           │
│  头顶部正中线与两耳尖连线的交点...  │
│                                     │
│  【功效】                           │
│  升阳举陷、益气固脱...              │
│                                     │
│  【主治】                           │
│  头痛、眩晕、失眠、健忘...          │
│                                     │
│  【操作方法】                       │
│  平刺0.5-0.8寸，可灸...             │
├─────────────────────────────────────┤
│  【经络循行】                       │
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │     手太阴肺经 GIF          │   │
│  │     (自动循环播放)          │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
│  起于中焦，下络大肠，还循胃口...    │
└─────────────────────────────────────┘
```

**功能规范**：
```vue
<template>
  <view class="acupoint-detail">
    <!-- 导航栏 -->
    <view class="navbar">
      <view class="back" @click="goBack">←</view>
      <text class="title">穴位详情</text>
    </view>

    <!-- 穴位图片 -->
    <view class="image-section">
      <image
        :src="acupoint.image_url"
        mode="aspectFit"
        class="acupoint-image"
      />
    </view>

    <!-- 基本信息 -->
    <view class="info-section">
      <view class="name-row">
        <text class="name">{{ acupoint.name }}</text>
        <text class="code">({{ acupoint.code }})</text>
      </view>
      <view class="meridian">{{ acupoint.meridian_name }}</view>
    </view>

    <!-- 详细信息 -->
    <view class="detail-section">
      <view class="detail-item">
        <view class="label">【定位】</view>
        <view class="content">{{ acupoint.location }}</view>
      </view>

      <view class="detail-item">
        <view class="label">【功效】</view>
        <view class="content">{{ acupoint.functions }}</view>
      </view>

      <view class="detail-item">
        <view class="label">【主治】</view>
        <view class="content">{{ acupoint.indications }}</view>
      </view>

      <view class="detail-item">
        <view class="label">【操作方法】</view>
        <view class="content">{{ acupoint.methods }}</view>
      </view>
    </view>

    <!-- 经络 GIF 动画 -->
    <view class="meridian-section">
      <view class="section-title">【经络循行】</view>
      <image
        :src="`/static/acupoints/meridians/${acupoint.meridian_name}.gif`"
        mode="aspectFit"
        class="meridian-gif"
      />
      <view class="meridian-desc">{{ meridianDescription }}</view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      acupoint: {},
      meridianDescription: ''
    }
  },
  onLoad(options) {
    this.loadAcupoint(options.id)
  },
  methods: {
    async loadAcupoint(id) {
      const res = await uni.request({
        url: `/api/acupoints/${id}`
      })
      this.acupoint = res.data.data
      this.meridianDescription = this.getMeridianDescription(this.acupoint.meridian)
    },
    getMeridianDescription(meridian) {
      const descriptions = {
        'lung_lung': '起于中焦，下络大肠，还循胃口，上膈属肺...',
        'large_intestine': '起于食指桡侧端，沿食指内间...（大肠经）',
        // ... 其他经络描述
      }
      return descriptions[meridian] || ''
    }
  }
}
</script>
```

**样式规范**：
```scss
.acupoint-detail {
  background: #f5f5f5;
  min-height: 100vh;

  .navbar {
    height: 88rpx;
    background: #fff;
    display: flex;
    align-items: center;
    padding: 0 30rpx;
    border-bottom: 1rpx solid #eee;

    .back { font-size: 40rpx; }
    .title {
      flex: 1;
      text-align: center;
      font-size: 36rpx;
      font-weight: bold;
    }
  }

  .image-section {
    background: #fff;
    padding: 40rpx;
    text-align: center;

    .acupoint-image {
      width: 400rpx;
      height: 400rpx;
    }
  }

  .info-section {
    background: #fff;
    padding: 30rpx;
    text-align: center;
    margin-bottom: 20rpx;

    .name {
      font-size: 48rpx;
      font-weight: bold;
      color: #333;
    }
    .code {
      font-size: 28rpx;
      color: #999;
      margin-left: 10rpx;
    }
    .meridian {
      font-size: 28rpx;
      color: #1acc76;
      margin-top: 10rpx;
    }
  }

  .detail-section {
    background: #fff;
    padding: 30rpx;
    margin-bottom: 20rpx;

    .detail-item {
      margin-bottom: 30rpx;

      &:last-child { margin-bottom: 0; }

      .label {
        font-size: 32rpx;
        font-weight: bold;
        color: #333;
        margin-bottom: 15rpx;
      }
      .content {
        font-size: 28rpx;
        color: #666;
        line-height: 1.8;
      }
    }
  }

  .meridian-section {
    background: #fff;
    padding: 30rpx;

    .section-title {
      font-size: 32rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 20rpx;
    }

    .meridian-gif {
      width: 100%;
      height: 300rpx;
      background: #f5f5f5;
      border-radius: 16rpx;
      margin-bottom: 20rpx;
    }

    .meridian-desc {
      font-size: 28rpx;
      color: #666;
      line-height: 1.8;
    }
  }
}
```

---

### 部位分类标准

| 代码 | 中文名称 | 说明 |
|------|---------|------|
| head | 头部 | 头面穴位 |
| neck | 颈部 | 颈项穴位 |
| shoulder | 肩部 | 肩膀穴位 |
| arm_upper | 上臂 | 上臂内侧/外侧 |
| arm_lower | 前臂 | 前臂内侧/外侧 |
| hand | 手部 | 手掌、手背 |
| chest | 胸部 | 胸膺穴位 |
| abdomen | 腹部 | 上腹、下腹 |
| back | 背部 | 背腰、骶部 |
| thigh_upper | 大腿 | 大腿前/内/外侧 |
| thigh_lower | 小腿 | 小腿前/后侧 |
| foot | 足部 | 足背、足底 |

---

### 开发检查清单

添加新穴位时：
- [ ] 检查是否已有图片（命名规范：`{穴位名}.jpg`）
- [ ] 如无图片，从 `272_pages_acupunture_point_chart/` 复制
- [ ] 更新 `acupoint_images.json` 映射
- [ ] 确认 `meridian` 使用标准英文代码
- [ ] 添加 `aliases` 数组（常用别名）
- [ ] 如需症状关联，更新 `SymptomAcupoint` 表

添加新经络 GIF 时：
- [ ] 放入 `frontend/src/static/acupoints/meridians/`
- [ ] 文件名使用中文：`{经络中文名}.gif`
- [ ] 更新上方"12经络标准分类"表
