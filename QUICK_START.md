# 快速开始指南

## 3 分钟快速上手

### 第 1 步：获取 API 密钥

1. 访问 https://cloud.siliconflow.cn
2. 注册账号（新用户有免费额度）
3. 登录后进入「API Keys」页面
4. 点击「创建 API Key」
5. 复制生成的密钥（格式：`sk-xxxxxxxxxxxxx`）

### 第 2 步：设置环境变量

在终端中执行：

```bash
export SILICONFLOW_API_KEY="你的API密钥"
```

或者创建 `.env` 文件：

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥
```

### 第 3 步：运行程序

**最简单的方式：**

```bash
# 给脚本添加执行权限（首次运行）
chmod +x run.sh

# 运行
./run.sh "一只可爱的猫咪"
```

**或者使用 Python：**

```bash
# 创建虚拟环境（首次运行）
python3 -m venv venv
source venv/bin/activate

# 安装依赖（首次运行）
pip install requests

# 运行
python3 siliconflow_image_generator.py "一只可爱的猫咪"
```

## 常用命令

### 基础用法

```bash
# 生成一张图片
python3 siliconflow_image_generator.py "可爱的狗狗"

# 指定输出目录
python3 siliconflow_image_generator.py "风景画" -o ./my_images

# 生成多张图片
python3 siliconflow_image_generator.py "科幻城市" --batch 4
```

### 高级用法

```bash
# 指定图片尺寸
python3 siliconflow_image_generator.py "肖像画" --size 768x1024

# 增加推理步数（提高质量）
python3 siliconflow_image_generator.py "精细插画" --steps 30

# 使用固定种子（可复现）
python3 siliconflow_image_generator.py "测试图片" --seed 42

# 显示详细信息
python3 siliconflow_image_generator.py "调试模式" -v
```

## Python 代码示例

```python
from siliconflow_image_generator import SiliconFlowImageGenerator

# 初始化
generator = SiliconFlowImageGenerator(api_key="sk-your-api-key")

# 生成图片
response = generator.generate_image(
    prompt="一只可爱的橘猫",
    image_size="1024x1024",
    num_inference_steps=20
)

# 保存图片
saved_files = generator.save_images(response, output_dir="./output")
print(f"生成了 {len(saved_files)} 张图片")
```

## 提示词示例

### 中文

```
一只可爱的橘猫坐在阳光明媚的窗台上，背景是绿植
```

```
未来科技城市的夜景，霓虹灯闪烁，赛博朋克风格
```

```
高山流水，中国水墨画风格，留白构图
```

### 英文

```
A cozy coffee shop with warm lighting, photorealistic
```

```
Cute robot character, Pixar style, 3D render
```

## 常见问题

**Q: 提示"未检测到 API 密钥"怎么办？**

A: 请确保已设置环境变量：
```bash
export SILICONFLOW_API_KEY="sk-your-api-key"
```

**Q: 生成失败怎么办？**

A: 
1. 检查 API 密钥是否正确
2. 检查账户余额是否充足
3. 检查网络连接
4. 使用 `-v` 参数查看详细错误信息

**Q: 图片保存在哪里？**

A: 默认保存在 `./generated_images/` 目录，可通过 `-o` 参数修改。

**Q: 如何提高图片质量？**

A:
1. 增加推理步数：`--steps 30`
2. 使用更详细的提示词
3. 指定艺术风格

## 获取帮助

查看完整文档：
```bash
cat README_SiliconFlow.md
```

查看所有参数：
```bash
python3 siliconflow_image_generator.py --help
```

运行示例：
```bash
python3 siliconflow_example.py
```

运行测试：
```bash
python3 -m unittest test_siliconflow -v
```

## 文件说明

```
zxc/
├── run.sh                      # 快速启动脚本（推荐）
├── quick_demo.py               # 最简单的示例
├── siliconflow_image_generator.py  # 主工具
├── siliconflow_example.py      # 完整示例
├── test_siliconflow.py         # 测试脚本
├── README_SiliconFlow.md       # 完整文档
├── QUICK_START.md              # 本文件
├── PROJECT_SUMMARY.md          # 项目总结
├── .env.example                # 配置示例
└── requirements.txt            # 依赖列表
```

## 下一步

1. 阅读 `README_SiliconFlow.md` 了解所有功能
2. 运行 `python3 siliconflow_example.py` 查看完整示例
3. 尝试不同的提示词和参数
4. 集成到你的项目中

祝你使用愉快！🎨
