# PixelForge

AI 图片生成 Web 应用，基于 Flask + SiliconFlow API。

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API 密钥
cp .env.example .env
# 编辑 .env，填入 SILICONFLOW_API_KEY

# 3. 启动
python app.py
```

访问 http://localhost:5000

## 功能

- 多模型支持（Kolors、通义、百度等）
- 自定义图片尺寸和推理步数
- 生成历史记录
- 响应式 Web 界面

## 项目结构

```
├── app.py                # Flask 应用入口
├── config.py             # 配置管理
├── image_generator.py    # 图片生成器核心
├── requirements.txt      # Python 依赖
├── templates/            # HTML 模板
├── static/               # 静态资源
├── data/                 # 运行时数据（JSON）
├── tests/                # 测试
└── generated_images/     # 生成的图片
```
