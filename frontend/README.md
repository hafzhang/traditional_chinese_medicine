# Constitution Recognition Frontend

中医体质识别小程序前端

## 技术栈

- **uni-app** - 跨平台开发框架
- **Vue 3** - 前端框架
- **Pinia** - 状态管理
- **SCSS** - CSS 预处理器

## 项目结构

```
frontend/
├── package.json           # 项目依赖
├── vite.config.js         # Vite 配置
├── src/
│   ├── main.js            # 应用入口
│   ├── App.vue            # 根组件
│   ├── pages.json         # 页面配置
│   ├── manifest.json      # 应用配置
│   ├── pages/             # 页面
│   │   ├── index/         # 首页
│   │   ├── test/          # 测试页
│   │   ├── result/        # 结果页
│   │   ├── detail/        # 详情页
│   │   └── food/          # 饮食推荐页
│   ├── api/               # API 接口
│   ├── utils/             # 工具函数
│   ├── styles/            # 全局样式
│   └── static/            # 静态资源
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 开发运行

```bash
# 微信小程序
npm run dev:mp-weixin

# H5
npm run dev:h5

# 抖音小程序
npm run dev:mp-toutiao
```

### 3. 构建发布

```bash
# 微信小程序
npm run build:mp-weixin

# H5
npm run build:h5
```

## 页面说明

### 首页 (index)
- 展示九种体质类型
- 功能特点介绍
- 快速开始测试入口

### 测试页 (test)
- 30题问卷答题
- 进度条显示
- 快速跳转导航
- 本地答案缓存

### 结果页 (result)
- 体质判定结果
- 分数可视化展示
- 主要/次要体质显示
- 跳转详情和饮食推荐

### 详情页 (detail)
- 体质特征详细描述
- 调理原则（饮食、运动、起居、情志）
- 免责声明

### 饮食推荐页 (food)
- 宜吃食物列表
- 不宜食物列表
- 推荐食谱
- 饮食原则建议

## API 接口

所有 API 请求通过 `src/api/constitution.js` 封装：

```javascript
import { getQuestions, submitTest, getResult, getFoodRecommendations } from '@/api/constitution.js'

// 获取问题列表
await getQuestions()

// 提交测试
await submitTest(answers)

// 获取结果
await getResult(resultId)

// 获取饮食推荐
await getFoodRecommendations(constitution)
```

## 样式规范

全局样式定义在 `src/styles/global.scss`：

- 颜色变量
- 组件样式
- 工具类
- 体质颜色映射

## 注意事项

1. **图片资源**: tabBar 图标和 logo 需要自行添加到 `src/static/` 目录

2. **API 配置**: 开发环境代理配置在 `vite.config.js`

3. **平台差异**: 注意不同小程序平台的 API 差异

4. **状态管理**: 使用 uni.setStorageSync/getStorageSync 进行本地数据持久化

## 开发建议

1. 使用 Chrome DevTools 调试 H5 版本
2. 使用微信开发者工具调试小程序版本
3. 注意 uni-app 各端 API 兼容性
4. 使用条件编译处理平台差异代码

## License

MIT
