# PixelForge

AI 图片生成 Web 应用，基于 Flask + SiliconFlow API，支持多种模型和图片尺寸。

## 功能特性

- 🎨 **多模型支持** — Kolors、通义 Z-Image、百度 ERNIE、通义千问等 7 个模型
- 📐 **自定义尺寸** — 16:9 横版、1:1 正方形、9:16 竖版等 5 种比例
- 🎛️ **推理步数调节** — 15-35 步，平衡速度与质量
- 🎯 **随机种子** — 固定种子可复现生成结果
- 📜 **历史记录** — 自动保存最近 20 条生成记录
- 📥 **一键下载** — 生成后直接下载图片
- 🌙 **暗色主题** — Tailwind CSS 深色 UI

## 快速开始

### 1. 安装依赖

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置 API 密钥

```bash
cp .env.example .env
```

编辑 `.env`，填入你的 SiliconFlow API 密钥：

```
SILICONFLOW_API_KEY=sk-your-api-key-here
```

> 获取密钥：https://cloud.siliconflow.cn （新用户有免费额度）

### 3. 启动

```bash
python app.py
```

访问 http://localhost:5001

> macOS 默认 5000 端口被 AirPlay 占用，项目默认使用 5001。可在 `.env` 中修改 `FLASK_PORT`。

## 使用方式

### Web 界面

1. 输入提示词（支持中英文）
2. 选择模型、尺寸、推理步数
3. 点击「开始生成」
4. 查看结果，可下载或重新生成

快捷键：`Ctrl + Enter` 快速生成

### API 调用

```bash
# 获取可用模型
curl http://localhost:5001/api/models

# 生成图片
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "一只可爱的猫咪", "model": "Kwai-Kolors/Kolors", "size": "1024x576", "steps": 25}'

# 获取历史记录
curl http://localhost:5001/api/history

# 清空历史
curl -X DELETE http://localhost:5001/api/history
```

## 支持的模型

| 模型 | 提供商 | 说明 |
|------|--------|------|
| Kwai-Kolors/Kolors | 快手 | 中文理解强，公众号封面推荐 |
| Tongyi-MAI/Z-Image-Turbo | 通义 | 快速生成，性价比高 |
| Tongyi-MAI/Z-Image | 通义 | 标准版，效果稳定 |
| baidu/ERNIE-Image-Turbo | 百度 | 快速生成 |
| Qwen/Qwen-Image | 通义千问 | 图片生成 |
| Qwen/Qwen-Image-Edit | 通义千问 | 图片编辑 |
| Qwen/Qwen-Image-Edit-2509 | 通义千问 | 图片编辑（新版） |

## 支持的尺寸

| 尺寸 | 比例 |
|------|------|
| 1024x576 | 16:9 横版 |
| 1024x1024 | 1:1 正方形 |
| 576x1024 | 9:16 竖版 |
| 768x1024 | 3:4 竖版 |
| 1024x768 | 4:3 横版 |

## 项目结构

```
pixelforge/
├── app.py                # Flask 应用入口
├── config.py             # 配置管理（模型、尺寸、路径）
├── image_generator.py    # SiliconFlow API 图片生成器
├── requirements.txt      # Python 依赖
├── .env.example          # 环境变量模板
├── .env                  # 环境变量（不提交）
├── templates/
│   ├── base.html         # 基础模板（Tailwind CSS）
│   ├── index.html        # 主页
│   └── components/
│       ├── header.html   # 顶部导航
│       ├── generator.html # 生成表单
│       ├── result.html   # 结果展示
│       └── history.html  # 历史记录
├── static/
│   ├── css/style.css     # 自定义样式
│   └── js/main.js        # 前端交互逻辑
├── tests/
│   ├── test_app.py       # API 路由测试
│   ├── test_generator.py # 图片生成器测试
│   └── test_history.py   # 历史记录测试
├── data/                 # 运行时数据（自动创建）
│   ├── config.json       # 用户配置
│   └── history.json      # 历史记录
└── generated_images/     # 生成的图片
```

## 测试

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

19 个测试覆盖：
- 页面渲染与 API 路由
- 图片生成器（成功/超时/异常/空结果）
- 下载图片（成功/失败）
- 历史记录（初始化/添加/数量限制）

## 配置项

在 `.env` 中可配置：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SILICONFLOW_API_KEY` | — | SiliconFlow API 密钥（必填） |
| `FLASK_PORT` | 5001 | 服务端口 |
| `FLASK_DEBUG` | false | 调试模式 |

## 提示词技巧

**中文示例：**
```
一只可爱的橘猫坐在阳光明媚的窗台上，背景是绿植，温馨的氛围
未来科技城市的夜景，霓虹灯闪烁，飞行汽车穿梭，赛博朋克风格
```

**英文示例：**
```
A cozy coffee shop interior with warm lighting, autumn vibes, photorealistic
Cute robot character, Pixar style, friendly expression, 3D render
```

**建议：** 越具体的描述 → 越符合预期的结果。可指定风格（水彩、油画）、光影（暖色调、逆光）、构图（特写、全景）。

## License

MIT
