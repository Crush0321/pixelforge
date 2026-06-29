# SiliconFlow 图片生成工具 - 项目总结

## 项目概述

本项目提供了一个完整的 Python 工具，用于调用 SiliconFlow API 使用 FLUX.1-schnell 模型生成高质量图片。

## 文件清单

### 核心文件

| 文件 | 说明 | 用途 |
|------|------|------|
| `siliconflow_image_generator.py` | 主工具脚本 | 核心功能，包含 `SiliconFlowImageGenerator` 类和命令行接口 |
| `siliconflow_example.py` | 使用示例 | 展示各种使用场景的完整示例 |
| `quick_demo.py` | 快速演示 | 最简单的使用示例，适合快速上手 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `.env.example` | 环境变量配置示例 |
| `requirements.txt` | Python 依赖列表 |
| `run.sh` | 快速启动脚本（自动创建虚拟环境） |

### 文档文件

| 文件 | 说明 |
|------|------|
| `README_SiliconFlow.md` | 完整的使用文档 |
| `PROJECT_SUMMARY.md` | 本文件，项目总结 |

### 测试文件

| 文件 | 说明 |
|------|------|
| `test_siliconflow.py` | 单元测试脚本 |

## 快速开始

### 1. 获取 API 密钥

访问 [SiliconFlow 官网](https://cloud.siliconflow.cn) 注册并获取 API 密钥。

### 2. 设置环境变量

```bash
export SILICONFLOW_API_KEY="sk-your-api-key-here"
```

### 3. 运行演示

**方法一：使用快速启动脚本（推荐）**

```bash
./run.sh "一只可爱的猫咪"
```

**方法二：手动运行**

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install requests

# 运行
python3 siliconflow_image_generator.py "一只可爱的猫咪"
```

**方法三：Python 代码调用**

```python
from siliconflow_image_generator import SiliconFlowImageGenerator

generator = SiliconFlowImageGenerator(api_key="sk-your-api-key")
response = generator.generate_image(prompt="一只可爱的猫咪")
saved_files = generator.save_images(response)
```

## 功能特性

✅ **中英文支持** - 支持中文和英文提示词

✅ **自定义尺寸** - 支持多种图片尺寸（1024x1024, 768x1024 等）

✅ **批量生成** - 一次可生成多张图片

✅ **固定种子** - 使用随机种子可复现生成结果

✅ **自动保存** - 自动保存生成的图片到本地

✅ **错误处理** - 完善的错误处理和提示

✅ **命令行接口** - 支持命令行参数配置

✅ **Python API** - 提供完整的 Python 类接口

## 支持的图片尺寸

- `512x512` - 小尺寸
- `768x768` - 中等尺寸
- `1024x1024` - 标准尺寸（默认）
- `768x1024` - 竖版
- `1024x768` - 横版

## 推理步数建议

| 步数 | 效果 | 速度 | 推荐场景 |
|------|------|------|----------|
| 10-15 | 基础 | 快 | 快速预览 |
| 20-25 | 良好 | 中 | 日常使用（默认） |
| 30-40 | 优秀 | 慢 | 高质量需求 |

## 提示词技巧

### 中文提示词

```
一只可爱的橘猫坐在阳光明媚的窗台上，背景是绿植，温馨的氛围
```

```
未来科技城市的夜景，霓虹灯闪烁，飞行汽车穿梭，赛博朋克风格
```

### 英文提示词

```
A cozy coffee shop interior with warm lighting, autumn vibes, photorealistic
```

```
Cute robot character, Pixar style, friendly expression, 3D render
```

## API 配额说明

- 新用户有**免费额度**可供试用
- 具体额度请查看 [SiliconFlow 控制台](https://cloud.siliconflow.cn)
- 额度用完后需要充值

## 常见问题

### Q: 如何获取 API 密钥？

A: 访问 https://cloud.siliconflow.cn 注册账号，在 API Keys 页面创建密钥。

### Q: 为什么生成失败？

A: 常见原因：
1. API 密钥错误或过期
2. 账户余额不足
3. 网络连接问题
4. 参数格式错误

### Q: 如何提高图片质量？

A: 
1. 增加推理步数（`--steps 30`）
2. 使用更详细的提示词
3. 指定艺术风格

### Q: 图片保存在哪里？

A: 默认保存在 `./generated_images/` 目录，可通过 `--output` 参数自定义。

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户界面层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ 命令行接口  │  │ Python API  │  │ 示例脚本    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │            │
│         └────────────────┼────────────────┘            │
│                          │                             │
│                          ▼                             │
│  ┌─────────────────────────────────────────────────┐  │
│  │          SiliconFlowImageGenerator              │  │
│  │  - generate_image()  生成图片                   │  │
│  │  - save_images()     保存图片                   │  │
│  └─────────────────────────────────────────────────┘  │
│                          │                             │
│                          ▼                             │
│  ┌─────────────────────────────────────────────────┐  │
│  │           SiliconFlow API                       │  │
│  │  FLUX.1-schnell 模型                            │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 依赖说明

- Python 3.7+
- requests 库

## 许可证

MIT License

## 相关资源

- [SiliconFlow 官网](https://cloud.siliconflow.cn)
- [SiliconFlow 文档](https://docs.siliconflow.cn)
- [FLUX.1 模型介绍](https://blackforestlabs.ai)

## 更新日志

### 2026-06-29
- 初始版本发布
- 实现基本图片生成功能
- 添加命令行接口
- 添加 Python API
- 添加使用示例
- 添加单元测试
- 添加完整文档
