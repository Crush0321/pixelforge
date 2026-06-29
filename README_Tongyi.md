# 通义万相 (Tongyi Wanxiang) 图片生成工具

使用阿里云 DashScope API 调用通义万相模型生成高质量图片。

## 功能特性

- 🎨 支持中英文提示词
- 📐 多种图片尺寸可选
- 🎭 多种艺术风格
- 🔄 批量生成图片
- 🎯 固定种子可复现生成
- 💾 自动保存到本地
- ⏱️ 异步任务支持
- 🛡️ 完善的错误处理

## 快速开始

### 1. 获取 API 密钥

1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 开通"通义万相"模型服务
3. 创建 API Key
4. 新用户通常有免费额度（约 500 张图片）

### 2. 配置 API 密钥

**方法一：环境变量（推荐）**

```bash
# Linux/macOS
export DASHSCOPE_API_KEY="sk-your-api-key-here"

# Windows
set DASHSCOPE_API_KEY=sk-your-api-key-here
```

**方法二：命令行参数**

```bash
python tongyi_image_generator.py "你的提示词" --api-key sk-your-api-key-here
```

### 3. 生成图片

```bash
# 基础用法
python tongyi_image_generator.py "一只可爱的猫咪"

# 指定风格和尺寸
python tongyi_image_generator.py "动漫风格的少女" --style "<anime>" --size 1024*1024

# 批量生成
python tongyi_image_generator.py "科幻城市" --num 4

# 使用固定种子
python tongyi_image_generator.py "风景画" --seed 42
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `prompt` | 图片描述文本（必填） | - |
| `--model` | 模型名称 | `wanx-v1` |
| `--size` | 图片尺寸 | `1024*1024` |
| `--num` | 生成图片数量 | `1` |
| `--style` | 图片风格 | `<auto>` |
| `--seed` | 随机种子 | 随机 |
| `--output` | 输出目录 | `./generated_images` |
| `--prefix` | 文件名前缀 | `tongyi` |
| `--api-key` | API 密钥 | 环境变量 |
| `--timeout` | 最大等待时间（秒） | `300` |
| `--verbose` | 显示详细信息 | `False` |

## 支持的图片尺寸

| 尺寸 | 说明 |
|------|------|
| `512*512` | 小尺寸 |
| `768*768` | 中等尺寸 |
| `1024*1024` | 标准尺寸（默认） |
| `768*1024` | 竖版 |
| `1024*768` | 横版 |

## 支持的艺术风格

| 风格 | 说明 |
|------|------|
| `<auto>` | 自动（默认） |
| `<3d cartoon>` | 3D 卡通 |
| `<anime>` | 动漫 |
| `<oil painting>` | 油画 |
| `<watercolor>` | 水彩 |
| `<sketch>` | 素描 |
| `<chinese painting>` | 中国画 |
| `<flat illustration>` | 扁平插画 |

## 提示词技巧

### 中文提示词

```
一只可爱的橘猫坐在阳光明媚的窗台上，背景是绿植
```

```
未来科技城市的夜景，霓虹灯闪烁，赛博朋克风格
```

```
高山流水，中国水墨画风格，留白构图
```

### 英文提示词

```
A cozy coffee shop with warm lighting, photorealistic
```

```
Cute robot character, Pixar style, 3D render
```

### 风格化提示词

```
# 动漫风格
可爱的魔法少女，大眼睛，樱花背景 --style "<anime>"

# 油画风格
向日葵花田，莫奈风格 --style "<oil painting>"

# 中国画风格
山水画，留白构图 --style "<chinese painting>"

# 3D 卡通
可爱的熊猫宝宝 --style "<3d cartoon>"
```

## Python 代码示例

```python
from tongyi_image_generator import TongyiImageGenerator

# 初始化生成器
generator = TongyiImageGenerator(api_key="sk-your-api-key")

# 生成图片
response = generator.generate_image(
    prompt="一只可爱的橘猫",
    image_size="1024*1024",
    num_images=1,
    style="<auto>"
)

# 保存图片
saved_files = generator.save_images(response, output_dir="./output")
print(f"生成了 {len(saved_files)} 张图片")
```

## 异步任务说明

通义万相使用异步任务模式：

1. **提交任务** - 返回任务 ID
2. **轮询状态** - 定期查询任务状态
3. **获取结果** - 任务完成后获取图片 URL
4. **下载保存** - 下载图片到本地

默认最大等待时间为 300 秒（5 分钟），可通过 `--timeout` 参数调整。

## 常见问题

**Q: 如何获取 API 密钥？**

A: 访问 https://dashscope.console.aliyun.com/ 开通服务并创建 API Key。

**Q: 生成失败怎么办？**

A:
1. 检查 API 密钥是否正确
2. 检查账户余额/免费额度
3. 检查网络连接
4. 使用 `-v` 参数查看详细信息

**Q: 图片保存在哪里？**

A: 默认保存在 `./generated_images/` 目录，可通过 `-o` 参数修改。

**Q: 如何提高图片质量？**

A:
1. 使用更详细的提示词
2. 指定合适的艺术风格
3. 尝试不同的模型版本

**Q: 生成需要多长时间？**

A: 通常需要 10-60 秒，取决于图片复杂度和服务器负载。

## 与其他工具的对比

| 特性 | 通义万相 | SiliconFlow |
|------|----------|-------------|
| 提供商 | 阿里云 | SiliconFlow |
| 模型 | wanx-v1, wanx2.1 | FLUX.1, Kolors |
| 风格支持 | 丰富 | 较少 |
| 免费额度 | 500 张 | 有 |
| 调用方式 | 异步 | 同步/异步 |

## 许可证

MIT License

## 相关链接

- [阿里云 DashScope](https://dashscope.console.aliyun.com/)
- [通义万相文档](https://help.aliyun.com/zh/dashscope/)
- [API 参考](https://help.aliyun.com/zh/dashscope/developer-reference/api-details-11)
