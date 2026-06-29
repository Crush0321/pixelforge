# SiliconFlow FLUX.1-schnell 图片生成工具

使用 SiliconFlow API 调用 Black Forest Labs 的 FLUX.1-schnell 模型生成高质量图片。

## 功能特性

- 🎨 支持中英文提示词
- 📐 自定义图片尺寸
- 🔄 批量生成图片
- 🎯 固定种子可复现生成
- 💾 自动保存到本地
- 🛡️ 完善的错误处理

## 快速开始

### 1. 获取 API 密钥

1. 访问 [SiliconFlow 官网](https://cloud.siliconflow.cn)
2. 注册并登录账号
3. 在 API Keys 页面创建新的密钥
4. 新用户有免费额度可供试用

### 2. 安装依赖

**方法一：使用虚拟环境（推荐）**

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install requests
```

**方法二：直接安装**

```bash
pip install requests
```

### 3. 配置 API 密钥

**方法一：环境变量（推荐）**

```bash
# Linux/macOS
export SILICONFLOW_API_KEY="sk-your-api-key-here"

# Windows
set SILICONFLOW_API_KEY=sk-your-api-key-here
```

**方法二：命令行参数**

```bash
python siliconflow_image_generator.py "你的提示词" --api-key sk-your-api-key-here
```

### 4. 生成图片

#### 命令行使用

```bash
# 基础用法
python siliconflow_image_generator.py "一只可爱的猫咪"

# 指定参数
python siliconflow_image_generator.py "A beautiful sunset" \
    --size 1024x1024 \
    --steps 30 \
    --output ./my_images

# 批量生成
python siliconflow_image_generator.py "科幻城市" --batch 4

# 使用固定种子（可复现）
python siliconflow_image_generator.py "风景画" --seed 42

# 显示详细信息
python siliconflow_image_generator.py "可爱的狗狗" -v
```

#### Python 代码调用

```python
from siliconflow_image_generator import SiliconFlowImageGenerator

# 初始化生成器
generator = SiliconFlowImageGenerator(api_key="sk-your-api-key-here")

# 生成图片
response = generator.generate_image(
    prompt="一只可爱的橘猫坐在窗台上",
    image_size="1024x1024",
    num_inference_steps=20
)

# 保存图片
saved_files = generator.save_images(response, output_dir="./output")
print(f"生成了 {len(saved_files)} 张图片")
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `prompt` | 图片描述文本（必填） | - |
| `--model` | 模型名称 | `black-forest-labs/FLUX.1-schnell` |
| `--size` | 图片尺寸 | `1024x1024` |
| `--steps` | 推理步数（越大质量越高） | `20` |
| `--batch` | 一次生成的图片数量 | `1` |
| `--seed` | 随机种子 | 随机 |
| `--output` | 输出目录 | `./generated_images` |
| `--prefix` | 文件名前缀 | `flux` |
| `--api-key` | API 密钥 | 环境变量 |
| `--verbose` | 显示详细信息 | `False` |

## 支持的图片尺寸

- `512x512`
- `768x768`
- `1024x1024`
- `768x1024`（竖版）
- `1024x768`（横版）
- 其他尺寸请参考 SiliconFlow 文档

## 提示词技巧

### 中文提示词示例

```
一只可爱的橘猫坐在阳光明媚的窗台上，背景是绿植，温馨的氛围
```

```
未来科技城市的夜景，霓虹灯闪烁，飞行汽车穿梭，赛博朋克风格
```

```
高山流水，中国水墨画风格，留白构图
```

### 英文提示词示例

```
A cozy coffee shop interior with warm lighting, autumn vibes, photorealistic
```

```
Abstract digital art with vibrant neon colors, geometric shapes
```

```
Cute robot character, Pixar style, friendly expression, 3D render
```

### 提示词建议

1. **具体描述**：越详细的描述，生成的图片越符合预期
2. **风格指定**：可以指定艺术风格（如"水彩画"、"油画"、"赛博朋克"）
3. **光影描述**：添加光线描述（如"暖色调"、"逆光"、"黄金时刻"）
4. **构图提示**：可以描述构图方式（如"特写"、"全景"、"俯视"）

## 运行示例

运行示例脚本来查看各种用法：

```bash
python siliconflow_example.py
```

示例脚本包含：
1. 基础图片生成
2. 批量生成图片
3. 自定义图片尺寸
4. 使用固定种子
5. 英文提示词

## 错误处理

### 常见错误及解决方案

**1. API 密钥错误**
```
错误: 请通过 --api-key 参数或 SILICONFLOW_API_KEY 环境变量提供 API 密钥
```
→ 请确保正确设置了 API 密钥

**2. 请求超时**
```
API 请求失败: Connection timeout
```
→ 检查网络连接，或稍后重试

**3. 余额不足**
```
错误详情: {"code":"20012","message":"Insufficient balance"}
```
→ 请充值或等待免费额度重置

**4. 参数错误**
```
错误详情: {"code":"400","message":"Invalid parameter"}
```
→ 检查参数格式，参考本文档的参数说明

## 文件结构

```
zxc/
├── siliconflow_image_generator.py  # 主工具脚本
├── siliconflow_example.py          # 使用示例
├── README_SiliconFlow.md          # 本文档
└── generated_images/              # 默认输出目录（自动创建）
```

## API 参考

### 生成图片

**请求**
```
POST https://api.siliconflow.cn/v1/images/generations
```

**请求头**
```
Authorization: Bearer {api_key}
Content-Type: application/json
```

**请求体**
```json
{
  "model": "black-forest-labs/FLUX.1-schnell",
  "prompt": "图片描述",
  "image_size": "1024x1024",
  "num_inference_steps": 20,
  "batch_size": 1
}
```

**响应**
```json
{
  "images": [
    {
      "url": "https://..."
    }
  ],
  "timings": {
    "inference": 1.23
  }
}
```

## 许可证

MIT License

## 相关链接

- [SiliconFlow 官网](https://cloud.siliconflow.cn)
- [SiliconFlow 文档](https://docs.siliconflow.cn)
- [FLUX.1 模型介绍](https://blackforestlabs.ai)

## 问题反馈

如遇到问题，请检查：
1. API 密钥是否正确
2. 网络连接是否正常
3. 账户余额是否充足
4. 参数格式是否正确

如仍有问题，请访问 [SiliconFlow 官方文档](https://docs.siliconflow.cn) 获取帮助。
