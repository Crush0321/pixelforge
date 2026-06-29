# PixelForge 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个基于 Flask 的 AI 图片生成网页工具，支持硅基流动平台的多个模型，提供极简科技风的用户界面。

**Architecture:** 使用 Flask + Jinja2 服务端渲染，Tailwind CSS 构建深色科技风界面，原生 JavaScript 处理异步交互，JSON 文件存储历史记录。后端调用硅基流动 API 生成图片。

**Tech Stack:** Python 3.x, Flask, Jinja2, Tailwind CSS (CDN), JavaScript (Fetch API), JSON storage

---

## 文件结构

```
pixelforge/
├── app.py                      # Flask 主应用，路由处理
├── config.py                   # 配置管理，环境变量读取
├── image_generator.py          # 图片生成核心逻辑
├── requirements.txt            # Python 依赖
├── .env.example                # 环境变量示例
├── data/
│   ├── history.json            # 历史记录
│   └── config.json             # 用户配置
├── static/
│   ├── css/
│   │   └── style.css           # 自定义样式
│   └── js/
│       └── main.js             # 前端 JavaScript
├── templates/
│   ├── base.html               # 基础模板
│   ├── index.html              # 主页面
│   └── components/
│       ├── header.html         # 头部导航
│       ├── generator.html      # 生成器表单
│       ├── result.html         # 结果展示
│       └── history.html        # 历史记录
└── tests/
    ├── test_app.py             # API 测试
    ├── test_generator.py       # 生成器测试
    └── conftest.py             # 测试配置
```

---

## Task 1: 项目初始化与依赖配置

**Files:**
- Create: `pixelforge/requirements.txt`
- Create: `pixelforge/.env.example`
- Create: `pixelforge/config.py`

- [ ] **Step 1: 创建项目目录结构**

```bash
mkdir -p pixelforge/{data,static/{css,js,images/generated},templates/components,tests}
```

- [ ] **Step 2: 创建 requirements.txt**

```txt
# pixelforge/requirements.txt
flask>=3.0.0
requests>=2.31.0
python-dotenv>=1.0.0
pytest>=8.0.0
```

- [ ] **Step 3: 创建 .env.example**

```bash
# pixelforge/.env.example
# SiliconFlow API 密钥（必填）
SILICONFLOW_API_KEY=sk-your-api-key-here

# 可选配置
FLASK_PORT=5000
FLASK_DEBUG=true
```

- [ ] **Step 4: 创建 config.py**

```python
# pixelforge/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """应用配置"""
    # API 配置
    SILICONFLOW_API_KEY = os.getenv('SILICONFLOW_API_KEY', '')
    SILICONFLOW_API_URL = 'https://api.siliconflow.cn/v1/images/generations'

    # Flask 配置
    PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    # 数据存储
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    HISTORY_FILE = os.path.join(DATA_DIR, 'history.json')
    CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

    # 图片存储
    IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images', 'generated')

    # 历史记录限制
    MAX_HISTORY = 20

    # 可用模型列表
    MODELS = [
        {
            'id': 'Tongyi-MAI/Z-Image-Turbo',
            'name': 'Z-Image Turbo',
            'provider': '通义',
            'description': '快速生成，性价比高'
        },
        {
            'id': 'Tongyi-MAI/Z-Image',
            'name': 'Z-Image',
            'provider': '通义',
            'description': '标准版，效果稳定'
        },
        {
            'id': 'baidu/ERNIE-Image-Turbo',
            'name': 'ERNIE Image Turbo',
            'provider': '百度',
            'description': '快速生成'
        },
        {
            'id': 'Qwen/Qwen-Image-Edit-2509',
            'name': 'Qwen Image Edit 2509',
            'provider': '通义千问',
            'description': '图片编辑（新版）'
        },
        {
            'id': 'Qwen/Qwen-Image-Edit',
            'name': 'Qwen Image Edit',
            'provider': '通义千问',
            'description': '图片编辑'
        },
        {
            'id': 'Qwen/Qwen-Image',
            'name': 'Qwen Image',
            'provider': '通义千问',
            'description': '图片生成'
        },
        {
            'id': 'Kwai-Kolors/Kolors',
            'name': 'Kolors',
            'provider': '快手',
            'description': '中文理解强，公众号封面推荐'
        }
    ]

    # 图片尺寸选项
    SIZES = [
        {'id': '1024x576', 'name': '16:9 横版', 'width': 1024, 'height': 576},
        {'id': '1024x1024', 'name': '1:1 正方形', 'width': 1024, 'height': 1024},
        {'id': '576x1024', 'name': '9:16 竖版', 'width': 576, 'height': 1024},
        {'id': '768x1024', 'name': '3:4 竖版', 'width': 768, 'height': 1024},
        {'id': '1024x768', 'name': '4:3 横版', 'width': 1024, 'height': 768},
    ]

    @classmethod
    def init_data_dir(cls):
        """初始化数据目录和文件"""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.IMAGE_DIR, exist_ok=True)

        # 初始化历史记录文件
        if not os.path.exists(cls.HISTORY_FILE):
            cls._save_json(cls.HISTORY_FILE, {'records': [], 'total': 0})

        # 初始化配置文件
        if not os.path.exists(cls.CONFIG_FILE):
            cls._save_json(cls.CONFIG_FILE, {
                'default_model': 'Kwai-Kolors/Kolors',
                'default_size': '1024x576',
                'default_steps': 25
            })

    @staticmethod
    def _save_json(filepath, data):
        """保存 JSON 文件"""
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_json(filepath):
        """加载 JSON 文件"""
        import json
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
```

- [ ] **Step 5: 安装依赖并验证**

```bash
cd pixelforge
pip install -r requirements.txt
python -c "from config import Config; Config.init_data_dir(); print('Config OK')"
```

Expected: 输出 "Config OK"，data 目录创建成功

- [ ] **Step 6: 初始化 Git 并提交**

```bash
cd pixelforge
git init
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "data/*.json" >> .gitignore
echo "static/images/generated/" >> .gitignore
git add .
git commit -m "feat: initialize project structure with config"
```

---

## Task 2: 实现图片生成核心模块

**Files:**
- Create: `pixelforge/image_generator.py`
- Create: `pixelforge/tests/test_generator.py`

- [ ] **Step 1: 创建测试文件**

```python
# pixelforge/tests/test_generator.py
import pytest
from image_generator import ImageGenerator

def test_init_with_api_key():
    """测试初始化带 API key"""
    generator = ImageGenerator(api_key='sk-test-key')
    assert generator.api_key == 'sk-test-key'
    assert generator.api_url == 'https://api.siliconflow.cn/v1/images/generations'

def test_build_payload():
    """测试构建请求体"""
    generator = ImageGenerator(api_key='sk-test-key')
    payload = generator.build_payload(
        prompt='一只猫',
        model='Kwai-Kolors/Kolors',
        size='1024x576',
        steps=25
    )
    assert payload['model'] == 'Kwai-Kolors/Kolors'
    assert payload['prompt'] == '一只猫'
    assert payload['image_size'] == '1024x576'
    assert payload['num_inference_steps'] == 25
    assert payload['batch_size'] == 1

def test_build_payload_with_seed():
    """测试带随机种子的请求体"""
    generator = ImageGenerator(api_key='sk-test-key')
    payload = generator.build_payload(
        prompt='一只猫',
        model='Kwai-Kolors/Kolors',
        size='1024x576',
        steps=25,
        seed=42
    )
    assert payload['seed'] == 42
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd pixelforge
pytest tests/test_generator.py -v
```

Expected: FAIL - ModuleNotFoundError: No module named 'image_generator'

- [ ] **Step 3: 实现 ImageGenerator 类**

```python
# pixelforge/image_generator.py
import os
import uuid
import requests
from datetime import datetime
from typing import Optional, Dict, Any, List

class ImageGenerator:
    """硅基流动图片生成器"""

    def __init__(self, api_key: str, api_url: str = 'https://api.siliconflow.cn/v1/images/generations'):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def build_payload(
        self,
        prompt: str,
        model: str,
        size: str,
        steps: int,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """构建 API 请求体"""
        payload = {
            'model': model,
            'prompt': prompt,
            'image_size': size,
            'num_inference_steps': steps,
            'batch_size': 1
        }
        if seed is not None:
            payload['seed'] = seed
        return payload

    def generate(
        self,
        prompt: str,
        model: str,
        size: str,
        steps: int,
        seed: Optional[int] = None,
        timeout: int = 60
    ) -> Dict[str, Any]:
        """
        生成图片

        Returns:
            {
                'success': True/False,
                'image_url': '图片URL',
                'filename': '文件名',
                'generation_time': 耗时秒数,
                'seed': 种子值,
                'error': '错误信息' (仅失败时)
            }
        """
        import time

        payload = self.build_payload(prompt, model, size, steps, seed)
        start_time = time.time()

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()

            # 提取图片 URL
            images = result.get('images', result.get('data', []))
            if not images:
                return {
                    'success': False,
                    'error': '未返回图片数据'
                }

            image_url = images[0].get('url', '') if isinstance(images[0], dict) else images[0]
            generation_time = round(time.time() - start_time, 2)
            used_seed = result.get('seed', seed)

            return {
                'success': True,
                'image_url': image_url,
                'generation_time': generation_time,
                'seed': used_seed
            }

        except requests.exceptions.Timeout:
            return {'success': False, 'error': '请求超时，请重试'}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'请求失败: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': f'生成失败: {str(e)}'}

    def download_image(self, url: str, save_dir: str) -> Optional[str]:
        """
        下载图片到本地

        Returns:
            文件名（成功）或 None（失败）
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # 生成唯一文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            filename = f'generated_{timestamp}_{unique_id}.png'

            filepath = os.path.join(save_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)

            return filename

        except Exception as e:
            print(f'下载图片失败: {e}')
            return None
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd pixelforge
pytest tests/test_generator.py -v
```

Expected: 3 passed

- [ ] **Step 5: 提交代码**

```bash
git add image_generator.py tests/test_generator.py
git commit -m "feat: implement image generator core module"
```

---

## Task 3: 实现历史记录管理

**Files:**
- Create: `pixelforge/tests/test_history.py`
- Modify: `pixelforge/config.py`

- [ ] **Step 1: 创建历史记录测试**

```python
# pixelforge/tests/test_history.py
import pytest
import os
import json
import tempfile
from config import Config

@pytest.fixture
def temp_config():
    """创建临时配置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        Config.DATA_DIR = tmpdir
        Config.HISTORY_FILE = os.path.join(tmpdir, 'history.json')
        Config.CONFIG_FILE = os.path.join(tmpdir, 'config.json')
        Config.init_data_dir()
        yield Config

def test_init_history(temp_config):
    """测试初始化历史记录"""
    history = temp_config.load_json(temp_config.HISTORY_FILE)
    assert 'records' in history
    assert history['records'] == []
    assert history['total'] == 0

def test_add_history_record(temp_config):
    """测试添加历史记录"""
    # 加载历史
    history = temp_config.load_json(temp_config.HISTORY_FILE)

    # 添加记录
    record = {
        'id': 'test-uuid-123',
        'prompt': '一只猫',
        'model': 'Kwai-Kolors/Kolors',
        'size': '1024x576',
        'steps': 25,
        'seed': 42,
        'image_filename': 'test.png',
        'generation_time': 3.5,
        'created_at': '2026-06-29T12:00:00'
    }
    history['records'].append(record)
    history['total'] = 1

    # 保存
    temp_config._save_json(temp_config.HISTORY_FILE, history)

    # 验证
    loaded = temp_config.load_json(temp_config.HISTORY_FILE)
    assert len(loaded['records']) == 1
    assert loaded['records'][0]['prompt'] == '一只猫'

def test_history_limit(temp_config):
    """测试历史记录限制"""
    history = temp_config.load_json(temp_config.HISTORY_FILE)

    # 添加 25 条记录
    for i in range(25):
        record = {
            'id': f'uuid-{i}',
            'prompt': f'测试 {i}',
            'model': 'Kwai-Kolors/Kolors',
            'image_filename': f'test_{i}.png',
            'generation_time': 3.0,
            'created_at': f'2026-06-29T12:{i:02d}:00'
        }
        history['records'].append(record)

    history['total'] = 25
    temp_config._save_json(temp_config.HISTORY_FILE, history)

    # 验证可以加载 25 条
    loaded = temp_config.load_json(temp_config.HISTORY_FILE)
    assert len(loaded['records']) == 25
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd pixelforge
pytest tests/test_history.py -v
```

Expected: FAIL - 依赖 Config 类的正确实现

- [ ] **Step 3: 运行测试验证通过**

```bash
cd pixelforge
pytest tests/test_history.py -v
```

Expected: 3 passed (Config 类已在 Task 1 实现)

- [ ] **Step 4: 提交代码**

```bash
git add tests/test_history.py
git commit -m "test: add history management tests"
```

---

## Task 4: 实现 Flask API 接口

**Files:**
- Create: `pixelforge/app.py`
- Create: `pixelforge/tests/test_app.py`

- [ ] **Step 1: 创建 API 测试**

```python
# pixelforge/tests/test_app.py
import pytest
import os
import tempfile
from app import app

@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """测试主页加载"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'PixelForge' in response.data

def test_get_models(client):
    """测试获取模型列表"""
    response = client.get('/api/models')
    assert response.status_code == 200
    data = response.get_json()
    assert 'models' in data
    assert len(data['models']) == 7
    assert data['models'][0]['id'] == 'Tongyi-MAI/Z-Image-Turbo'

def test_get_history(client):
    """测试获取历史记录"""
    response = client.get('/api/history')
    assert response.status_code == 200
    data = response.get_json()
    assert 'records' in data
    assert 'total' in data

def test_generate_missing_prompt(client):
    """测试缺少提示词"""
    response = client.post('/api/generate', json={
        'model': 'Kwai-Kolors/Kolors',
        'size': '1024x576',
        'steps': 25
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] == False
    assert '提示词' in data['error']
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd pixelforge
pytest tests/test_app.py -v
```

Expected: FAIL - ModuleNotFoundError: No module named 'app'

- [ ] **Step 3: 实现 Flask 应用**

```python
# pixelforge/app.py
import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from config import Config
from image_generator import ImageGenerator

# 初始化配置
Config.init_data_dir()

# 创建 Flask 应用
app = Flask(__name__)
app.config.from_object(Config)

# 图片生成器（延迟初始化）
generator = None

def get_generator():
    """获取或创建图片生成器实例"""
    global generator
    if generator is None:
        if not Config.SILICONFLOW_API_KEY:
            raise ValueError('请配置 SILICONFLOW_API_KEY')
        generator = ImageGenerator(Config.SILICONFLOW_API_KEY)
    return generator


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html',
                         models=Config.MODELS,
                         sizes=Config.SIZES)


# ==================== API 路由 ====================

@app.route('/api/models')
def get_models():
    """获取可用模型列表"""
    return jsonify({'models': Config.MODELS})


@app.route('/api/history')
def get_history():
    """获取历史记录"""
    try:
        history = Config.load_json(Config.HISTORY_FILE)
        return jsonify(history)
    except Exception as e:
        return jsonify({'records': [], 'total': 0})


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """清空历史记录"""
    try:
        Config._save_json(Config.HISTORY_FILE, {'records': [], 'total': 0})

        # 删除图片文件
        for filename in os.listdir(Config.IMAGE_DIR):
            filepath = os.path.join(Config.IMAGE_DIR, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)

        return jsonify({'success': True, 'message': '历史记录已清空'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/generate', methods=['POST'])
def generate_image():
    """生成图片"""
    data = request.get_json()

    # 验证参数
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({'success': False, 'error': '请输入提示词'}), 400

    model = data.get('model', 'Kwai-Kolors/Kolors')
    size = data.get('size', '1024x576')
    steps = data.get('steps', 25)
    seed = data.get('seed')

    # 验证模型
    valid_models = [m['id'] for m in Config.MODELS]
    if model not in valid_models:
        return jsonify({'success': False, 'error': '无效的模型选择'}), 400

    # 验证步数
    if not isinstance(steps, int) or steps < 1 or steps > 50:
        return jsonify({'success': False, 'error': '步数应在 1-50 之间'}), 400

    try:
        # 调用生成器
        gen = get_generator()
        result = gen.generate(
            prompt=prompt,
            model=model,
            size=size,
            steps=steps,
            seed=seed
        )

        if not result['success']:
            return jsonify(result), 500

        # 下载图片
        filename = gen.download_image(result['image_url'], Config.IMAGE_DIR)
        if not filename:
            return jsonify({'success': False, 'error': '图片下载失败'}), 500

        # 保存历史记录
        record = {
            'id': str(uuid.uuid4()),
            'prompt': prompt,
            'model': model,
            'size': size,
            'steps': steps,
            'seed': result.get('seed'),
            'image_filename': filename,
            'generation_time': result['generation_time'],
            'created_at': datetime.now().isoformat()
        }

        history = Config.load_json(Config.HISTORY_FILE)
        history['records'].insert(0, record)

        # 限制历史记录数量
        if len(history['records']) > Config.MAX_HISTORY:
            # 删除旧图片
            for old_record in history['records'][Config.MAX_HISTORY:]:
                old_path = os.path.join(Config.IMAGE_DIR, old_record['image_filename'])
                if os.path.exists(old_path):
                    os.remove(old_path)
            history['records'] = history['records'][:Config.MAX_HISTORY]

        history['total'] = len(history['records'])
        Config._save_json(Config.HISTORY_FILE, history)

        # 返回结果
        return jsonify({
            'success': True,
            'data': {
                'image_url': f'/static/images/generated/{filename}',
                'filename': filename,
                'model': model,
                'prompt': prompt,
                'size': size,
                'steps': steps,
                'seed': result.get('seed'),
                'generation_time': result['generation_time']
            }
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'生成失败: {str(e)}'}), 500


# ==================== 静态文件 ====================

@app.route('/static/images/generated/<filename>')
def serve_generated_image(filename):
    """提供生成的图片"""
    return send_from_directory(Config.IMAGE_DIR, filename)


# ==================== 启动 ====================

if __name__ == '__main__':
    print(f'PixelForge 启动中...')
    print(f'访问地址: http://localhost:{Config.PORT}')
    print(f'API 密钥: {"已配置" if Config.SILICONFLOW_API_KEY else "未配置"}')
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd pixelforge
pytest tests/test_app.py -v
```

Expected: 4 passed

- [ ] **Step 5: 提交代码**

```bash
git add app.py tests/test_app.py
git commit -m "feat: implement Flask API endpoints"
```

---

## Task 5: 实现基础 HTML 模板

**Files:**
- Create: `pixelforge/templates/base.html`
- Create: `pixelforge/templates/index.html`
- Create: `pixelforge/templates/components/header.html`

- [ ] **Step 1: 创建 base.html**

```html
<!-- pixelforge/templates/base.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}PixelForge{% endblock %}</title>

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- 自定义配置 -->
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        'dark': {
                            '900': '#0B0C10',
                            '800': '#1F2937',
                            '700': '#374151',
                        },
                        'neon': {
                            'blue': '#3B82F6',
                            'purple': '#8B5CF6',
                            'cyan': '#06B6D4',
                        }
                    }
                }
            }
        }
    </script>

    <!-- 自定义样式 -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

    {% block extra_css %}{% endblock %}
</head>
<body class="bg-dark-900 text-gray-100 min-h-screen">
    {% block content %}{% endblock %}

    <!-- 主脚本 -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

- [ ] **Step 2: 创建 header.html**

```html
<!-- pixelforge/templates/components/header.html -->
<header class="border-b border-gray-800 bg-dark-900/80 backdrop-blur-sm sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-blue to-neon-purple flex items-center justify-center">
                <span class="text-xl">🔥</span>
            </div>
            <h1 class="text-xl font-bold bg-gradient-to-r from-neon-blue to-neon-purple bg-clip-text text-transparent">
                PixelForge
            </h1>
        </div>

        <!-- 右侧按钮 -->
        <div class="flex items-center space-x-4">
            <button
                id="historyToggle"
                class="px-4 py-2 rounded-lg bg-dark-800 hover:bg-dark-700 transition-colors text-sm"
            >
                📜 历史记录
            </button>
        </div>
    </div>
</header>
```

- [ ] **Step 3: 创建 index.html**

```html
<!-- pixelforge/templates/index.html -->
{% extends "base.html" %}

{% block title %}PixelForge - AI 图片生成{% endblock %}

{% block content %}
<div class="min-h-screen">
    <!-- 头部 -->
    {% include "components/header.html" %}

    <!-- 主内容区 -->
    <main class="max-w-6xl mx-auto px-4 py-8">
        <!-- 生成器区域 -->
        <section id="generatorSection" class="mb-12">
            {% include "components/generator.html" %}
        </section>

        <!-- 结果展示区域 -->
        <section id="resultSection" class="mb-12 hidden">
            {% include "components/result.html" %}
        </section>

        <!-- 历史记录区域 -->
        <section id="historySection" class="hidden">
            {% include "components/history.html" %}
        </section>
    </main>

    <!-- Toast 提示 -->
    <div id="toast" class="fixed bottom-8 right-8 z-50 hidden">
        <div class="bg-dark-800 border border-gray-700 rounded-lg px-6 py-4 shadow-xl">
            <span id="toastMessage"></span>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 4: 验证模板渲染**

```bash
cd pixelforge
python app.py &
sleep 2
curl -s http://localhost:5000 | head -20
kill %1
```

Expected: HTML 输出包含 PixelForge 和 Tailwind CSS

- [ ] **Step 5: 提交代码**

```bash
git add templates/
git commit -m "feat: add base HTML templates with dark theme"
```

---

## Task 6: 实现生成器表单组件

**Files:**
- Create: `pixelforge/templates/components/generator.html`

- [ ] **Step 1: 创建 generator.html**

```html
<!-- pixelforge/templates/components/generator.html -->
<div class="bg-dark-800 rounded-2xl p-8 border border-gray-800">
    <h2 class="text-2xl font-bold mb-6">✨ AI 图片生成</h2>

    <!-- 提示词输入 -->
    <div class="mb-6">
        <label class="block text-sm font-medium text-gray-400 mb-2">
            提示词（支持中英文）
        </label>
        <textarea
            id="promptInput"
            rows="4"
            class="w-full bg-dark-900 border border-gray-700 rounded-xl px-4 py-3 focus:border-neon-blue focus:ring-1 focus:ring-neon-blue outline-none transition-colors resize-none"
            placeholder="描述你想要生成的图片，例如：一只可爱的猫咪坐在阳光明媚的窗台上..."
        ></textarea>
    </div>

    <!-- 参数配置行 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <!-- 模型选择 -->
        <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">
                选择模型
            </label>
            <select
                id="modelSelect"
                class="w-full bg-dark-900 border border-gray-700 rounded-xl px-4 py-3 focus:border-neon-blue outline-none transition-colors appearance-none cursor-pointer"
            >
                {% for model in models %}
                <option value="{{ model.id }}" {% if model.id == 'Kwai-Kolors/Kolors' %}selected{% endif %}>
                    {{ model.name }} ({{ model.provider }})
                </option>
                {% endfor %}
            </select>
        </div>

        <!-- 图片尺寸 -->
        <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">
                图片尺寸
            </label>
            <select
                id="sizeSelect"
                class="w-full bg-dark-900 border border-gray-700 rounded-xl px-4 py-3 focus:border-neon-blue outline-none transition-colors appearance-none cursor-pointer"
            >
                {% for size in sizes %}
                <option value="{{ size.id }}" {% if size.id == '1024x576' %}selected{% endif %}>
                    {{ size.name }} ({{ size.id }})
                </option>
                {% endfor %}
            </select>
        </div>

        <!-- 推理步数 -->
        <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">
                推理步数: <span id="stepsValue">25</span>
            </label>
            <input
                type="range"
                id="stepsRange"
                min="15"
                max="35"
                value="25"
                class="w-full h-2 bg-dark-900 rounded-lg appearance-none cursor-pointer slider"
            >
            <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>15 (快速)</span>
                <span>35 (精细)</span>
            </div>
        </div>
    </div>

    <!-- 随机种子（可选） -->
    <div class="mb-6">
        <label class="block text-sm font-medium text-gray-400 mb-2">
            随机种子（可选，留空则随机）
        </label>
        <input
            type="number"
            id="seedInput"
            class="w-full md:w-48 bg-dark-900 border border-gray-700 rounded-xl px-4 py-3 focus:border-neon-blue outline-none transition-colors"
            placeholder="例如: 42"
        >
    </div>

    <!-- 生成按钮 -->
    <button
        id="generateBtn"
        class="w-full py-4 rounded-xl bg-gradient-to-r from-neon-blue to-neon-purple text-white font-bold text-lg hover:shadow-lg hover:shadow-neon-blue/30 transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98]"
    >
        ✨ 开始生成
    </button>
</div>
```

- [ ] **Step 2: 提交代码**

```bash
git add templates/components/generator.html
git commit -m "feat: add generator form component"
```

---

## Task 7: 实现结果展示组件

**Files:**
- Create: `pixelforge/templates/components/result.html`

- [ ] **Step 1: 创建 result.html**

```html
<!-- pixelforge/templates/components/result.html -->
<div class="bg-dark-800 rounded-2xl p-8 border border-gray-800">
    <h2 class="text-2xl font-bold mb-6">🖼️ 生成结果</h2>

    <!-- 加载状态 -->
    <div id="loadingState" class="hidden text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-neon-blue mb-4"></div>
        <p class="text-gray-400">正在生成中...</p>
        <p class="text-sm text-gray-500 mt-2">预计需要 3-5 秒</p>
    </div>

    <!-- 图片展示 -->
    <div id="imageDisplay" class="hidden">
        <!-- 图片 -->
        <div class="relative group rounded-xl overflow-hidden bg-dark-900">
            <img
                id="generatedImage"
                src=""
                alt="Generated Image"
                class="w-full h-auto"
            >
            <!-- 悬停遮罩 -->
            <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <span class="text-white">点击查看大图</span>
            </div>
        </div>

        <!-- 生成信息 -->
        <div class="mt-4 flex flex-wrap gap-4 text-sm text-gray-400">
            <span>⏱️ 耗时: <span id="generationTime">-</span>s</span>
            <span>🎯 模型: <span id="usedModel">-</span></span>
            <span>🌱 种子: <span id="usedSeed">-</span></span>
        </div>

        <!-- 操作按钮 -->
        <div class="mt-6 flex flex-wrap gap-3">
            <button
                id="downloadBtn"
                class="px-6 py-3 rounded-xl bg-neon-blue hover:bg-blue-600 transition-colors font-medium"
            >
                📥 下载图片
            </button>
            <button
                id="regenerateBtn"
                class="px-6 py-3 rounded-xl bg-dark-700 hover:bg-dark-600 transition-colors font-medium"
            >
                🔄 重新生成
            </button>
            <button
                id="refineBtn"
                class="px-6 py-3 rounded-xl bg-dark-700 hover:bg-dark-600 transition-colors font-medium"
            >
                ✏️ 微调提示词
            </button>
        </div>
    </div>

    <!-- 错误状态 -->
    <div id="errorState" class="hidden text-center py-12">
        <div class="text-red-400 text-5xl mb-4">❌</div>
        <p class="text-red-400" id="errorMessage">生成失败</p>
        <button
            id="retryBtn"
            class="mt-4 px-6 py-3 rounded-xl bg-dark-700 hover:bg-dark-600 transition-colors"
        >
            重试
        </button>
    </div>
</div>
```

- [ ] **Step 2: 提交代码**

```bash
git add templates/components/result.html
git commit -m "feat: add result display component"
```

---

## Task 8: 实现历史记录组件

**Files:**
- Create: `pixelforge/templates/components/history.html`

- [ ] **Step 1: 创建 history.html**

```html
<!-- pixelforge/templates/components/history.html -->
<div class="bg-dark-800 rounded-2xl p-8 border border-gray-800">
    <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold">📜 最近生成</h2>
        <button
            id="clearHistoryBtn"
            class="px-4 py-2 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-colors text-sm"
        >
            清空历史
        </button>
    </div>

    <!-- 历史记录网格 -->
    <div id="historyGrid" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
        <!-- 动态填充 -->
    </div>

    <!-- 空状态 -->
    <div id="historyEmpty" class="hidden text-center py-12 text-gray-500">
        <p class="text-4xl mb-4">📭</p>
        <p>暂无历史记录</p>
        <p class="text-sm mt-2">生成的图片将显示在这里</p>
    </div>
</div>

<!-- 历史记录项模板 -->
<template id="historyItemTemplate">
    <div class="history-item relative group cursor-pointer rounded-xl overflow-hidden bg-dark-900 aspect-square">
        <img src="" alt="" class="w-full h-full object-cover">
        <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity p-3 flex flex-col justify-end">
            <p class="text-white text-xs line-clamp-2"></p>
            <p class="text-gray-400 text-xs mt-1"></p>
        </div>
    </div>
</template>
```

- [ ] **Step 2: 提交代码**

```bash
git add templates/components/history.html
git commit -m "feat: add history records component"
```

---

## Task 9: 实现前端 JavaScript 交互

**Files:**
- Create: `pixelforge/static/js/main.js`

- [ ] **Step 1: 创建 main.js**

```javascript
// pixelforge/static/js/main.js

// ==================== 全局状态 ====================

const PixelForge = {
    isGenerating: false,
    currentImageUrl: null,

    // DOM 元素缓存
    elements: {}
};

// ==================== 初始化 ====================

document.addEventListener('DOMContentLoaded', () => {
    PixelForge.init();
});

PixelForge.init = function() {
    // 缓存 DOM 元素
    this.elements = {
        promptInput: document.getElementById('promptInput'),
        modelSelect: document.getElementById('modelSelect'),
        sizeSelect: document.getElementById('sizeSelect'),
        stepsRange: document.getElementById('stepsRange'),
        stepsValue: document.getElementById('stepsValue'),
        seedInput: document.getElementById('seedInput'),
        generateBtn: document.getElementById('generateBtn'),

        resultSection: document.getElementById('resultSection'),
        loadingState: document.getElementById('loadingState'),
        imageDisplay: document.getElementById('imageDisplay'),
        errorState: document.getElementById('errorState'),
        generatedImage: document.getElementById('generatedImage'),
        generationTime: document.getElementById('generationTime'),
        usedModel: document.getElementById('usedModel'),
        usedSeed: document.getElementById('usedSeed'),
        errorMessage: document.getElementById('errorMessage'),

        downloadBtn: document.getElementById('downloadBtn'),
        regenerateBtn: document.getElementById('regenerateBtn'),
        refineBtn: document.getElementById('refineBtn'),
        retryBtn: document.getElementById('retryBtn'),

        historyToggle: document.getElementById('historyToggle'),
        historySection: document.getElementById('historySection'),
        historyGrid: document.getElementById('historyGrid'),
        historyEmpty: document.getElementById('historyEmpty'),
        clearHistoryBtn: document.getElementById('clearHistoryBtn'),

        toast: document.getElementById('toast'),
        toastMessage: document.getElementById('toastMessage')
    };

    // 绑定事件
    this.bindEvents();

    // 加载历史记录
    this.loadHistory();

    console.log('PixelForge 初始化完成');
};

// ==================== 事件绑定 ====================

PixelForge.bindEvents = function() {
    const { elements: el } = this;

    // 步数滑块更新
    el.stepsRange.addEventListener('input', (e) => {
        el.stepsValue.textContent = e.target.value;
    });

    // 生成按钮
    el.generateBtn.addEventListener('click', () => this.generate());

    // 重新生成
    el.regenerateBtn.addEventListener('click', () => this.generate());
    el.retryBtn.addEventListener('click', () => this.generate());

    // 下载图片
    el.downloadBtn.addEventListener('click', () => this.downloadImage());

    // 微调提示词
    el.refineBtn.addEventListener('click', () => {
        el.promptInput.focus();
        this.showToast('info', '请修改提示词后重新生成');
    });

    // 历史记录切换
    el.historyToggle.addEventListener('click', () => {
        el.historySection.classList.toggle('hidden');
    });

    // 清空历史
    el.clearHistoryBtn.addEventListener('click', () => this.clearHistory());

    // Ctrl+Enter 快捷键生成
    el.promptInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            this.generate();
        }
    });
};

// ==================== 图片生成 ====================

PixelForge.generate = async function() {
    if (this.isGenerating) return;

    const { elements: el } = this;
    const prompt = el.promptInput.value.trim();

    // 验证提示词
    if (!prompt) {
        this.showToast('error', '请输入提示词');
        el.promptInput.focus();
        return;
    }

    // 准备请求数据
    const requestData = {
        prompt: prompt,
        model: el.modelSelect.value,
        size: el.sizeSelect.value,
        steps: parseInt(el.stepsRange.value)
    };

    // 添加随机种子（如果有）
    const seed = el.seedInput.value.trim();
    if (seed) {
        requestData.seed = parseInt(seed);
    }

    // 更新 UI 状态
    this.setGenerating(true);
    el.resultSection.classList.remove('hidden');
    el.loadingState.classList.remove('hidden');
    el.imageDisplay.classList.add('hidden');
    el.errorState.classList.add('hidden');

    // 滚动到结果区
    el.resultSection.scrollIntoView({ behavior: 'smooth' });

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();

        if (result.success) {
            // 显示生成结果
            this.showResult(result.data);
            // 刷新历史记录
            this.loadHistory();
            this.showToast('success', '图片生成成功！');
        } else {
            this.showError(result.error || '生成失败');
        }

    } catch (error) {
        console.error('生成请求失败:', error);
        this.showError('网络请求失败，请检查网络连接');
    } finally {
        this.setGenerating(false);
    }
};

// ==================== UI 更新 ====================

PixelForge.setGenerating = function(isGenerating) {
    this.isGenerating = isGenerating;
    const { elements: el } = this;

    el.generateBtn.disabled = isGenerating;
    el.generateBtn.textContent = isGenerating ? '⏳ 生成中...' : '✨ 开始生成';
    el.generateBtn.classList.toggle('opacity-50', isGenerating);
    el.generateBtn.classList.toggle('cursor-not-allowed', isGenerating);
};

PixelForge.showResult = function(data) {
    const { elements: el } = this;

    this.currentImageUrl = data.image_url;

    el.generatedImage.src = data.image_url;
    el.generationTime.textContent = data.generation_time;
    el.usedModel.textContent = data.model;
    el.usedSeed.textContent = data.seed || '随机';

    el.loadingState.classList.add('hidden');
    el.imageDisplay.classList.remove('hidden');
    el.errorState.classList.add('hidden');
};

PixelForge.showError = function(message) {
    const { elements: el } = this;

    el.errorMessage.textContent = message;
    el.loadingState.classList.add('hidden');
    el.imageDisplay.classList.add('hidden');
    el.errorState.classList.remove('hidden');
};

// ==================== 下载功能 ====================

PixelForge.downloadImage = function() {
    if (!this.currentImageUrl) return;

    const link = document.createElement('a');
    link.href = this.currentImageUrl;
    link.download = `pixelforge_${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    this.showToast('success', '图片下载已开始');
};

// ==================== 历史记录 ====================

PixelForge.loadHistory = async function() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();

        this.renderHistory(data.records || []);

    } catch (error) {
        console.error('加载历史记录失败:', error);
    }
};

PixelForge.renderHistory = function(records) {
    const { elements: el } = this;

    if (records.length === 0) {
        el.historyGrid.classList.add('hidden');
        el.historyEmpty.classList.remove('hidden');
        return;
    }

    el.historyGrid.classList.remove('hidden');
    el.historyEmpty.classList.add('hidden');
    el.historyGrid.innerHTML = '';

    records.forEach(record => {
        const item = document.createElement('div');
        item.className = 'history-item relative group cursor-pointer rounded-xl overflow-hidden bg-dark-900 aspect-square';
        item.innerHTML = `
            <img src="/static/images/generated/${record.image_filename}" alt="${record.prompt}" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity p-3 flex flex-col justify-end">
                <p class="text-white text-xs line-clamp-2">${this.escapeHtml(record.prompt)}</p>
                <p class="text-gray-400 text-xs mt-1">${record.model.split('/')[1]}</p>
            </div>
        `;

        // 点击加载到生成区
        item.addEventListener('click', () => {
            this.elements.promptInput.value = record.prompt;
            this.showResult({
                image_url: `/static/images/generated/${record.image_filename}`,
                generation_time: record.generation_time,
                model: record.model,
                seed: record.seed
            });
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        el.historyGrid.appendChild(item);
    });
};

PixelForge.clearHistory = async function() {
    if (!confirm('确定要清空所有历史记录吗？此操作不可恢复。')) return;

    try {
        const response = await fetch('/api/history', { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            this.showToast('success', '历史记录已清空');
            this.loadHistory();
        } else {
            this.showToast('error', result.error || '清空失败');
        }
    } catch (error) {
        this.showToast('error', '操作失败');
    }
};

// ==================== 工具函数 ====================

PixelForge.showToast = function(type, message) {
    const { elements: el } = this;

    const colors = {
        success: 'border-green-500',
        error: 'border-red-500',
        info: 'border-blue-500',
        warning: 'border-yellow-500'
    };

    el.toast.className = `fixed bottom-8 right-8 z-50 bg-dark-800 ${colors[type] || colors.info} border-l-4 rounded-lg px-6 py-4 shadow-xl`;
    el.toastMessage.textContent = message;

    // 显示动画
    el.toast.classList.remove('hidden');
    el.toast.style.opacity = '0';
    el.toast.style.transform = 'translateY(20px)';

    requestAnimationFrame(() => {
        el.toast.style.transition = 'all 0.3s ease';
        el.toast.style.opacity = '1';
        el.toast.style.transform = 'translateY(0)';
    });

    // 自动隐藏
    setTimeout(() => {
        el.toast.style.opacity = '0';
        el.toast.style.transform = 'translateY(20px)';
        setTimeout(() => el.toast.classList.add('hidden'), 300);
    }, 3000);
};

PixelForge.escapeHtml = function(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
};
```

- [ ] **Step 2: 提交代码**

```bash
git add static/js/main.js
git commit -m "feat: implement frontend JavaScript interactions"
```

---

## Task 10: 实现自定义样式

**Files:**
- Create: `pixelforge/static/css/style.css`

- [ ] **Step 1: 创建 style.css**

```css
/* pixelforge/static/css/style.css */

/* ==================== 全局样式 ==================== */

* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

/* ==================== 滚动条样式 ==================== */

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #1F2937;
}

::-webkit-scrollbar-thumb {
    background: #4B5563;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #6B7280;
}

/* ==================== 滑块样式 ==================== */

.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    cursor: pointer;
    border: 2px solid #1F2937;
    box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

.slider::-webkit-slider-thumb:hover {
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.7);
}

.slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    cursor: pointer;
    border: 2px solid #1F2937;
}

/* ==================== 霓虹发光效果 ==================== */

.neon-glow {
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.3),
                0 0 30px rgba(59, 130, 246, 0.1);
}

.neon-glow:hover {
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.5),
                0 0 40px rgba(59, 130, 246, 0.2);
}

/* ==================== 渐变文字 ==================== */

.gradient-text {
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ==================== 卡片悬停效果 ==================== */

.card-hover {
    transition: all 0.3s ease;
}

.card-hover:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

/* ==================== 加载动画 ==================== */

@keyframes pulse-glow {
    0%, 100% {
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
    }
    50% {
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.6);
    }
}

.animate-pulse-glow {
    animation: pulse-glow 2s ease-in-out infinite;
}

/* ==================== 历史记录项 ==================== */

.history-item {
    transition: all 0.3s ease;
}

.history-item:hover {
    transform: scale(1.05);
    z-index: 10;
}

/* ==================== 响应式调整 ==================== */

@media (max-width: 768px) {
    .grid-cols-3 {
        grid-template-columns: 1fr;
    }
}

/* ==================== Toast 动画 ==================== */

#toast {
    transition: all 0.3s ease;
}

/* ==================== 按钮点击效果 ==================== */

button:active {
    transform: scale(0.98);
}

/* ==================== 代码字体 ==================== */

code, pre {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
}
```

- [ ] **Step 2: 提交代码**

```bash
git add static/css/style.css
git commit -m "feat: add custom styles with neon effects"
```

---

## Task 11: 集成测试与最终验证

**Files:**
- Modify: `pixelforge/tests/test_app.py`

- [ ] **Step 1: 添加集成测试**

```python
# pixelforge/tests/test_app.py (追加)

def test_full_page_render(client):
    """测试完整页面渲染"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode()

    # 检查关键元素
    assert 'PixelForge' in html
    assert 'promptInput' in html
    assert 'modelSelect' in html
    assert 'generateBtn' in html
    assert 'historySection' in html

def test_models_content(client):
    """测试模型列表内容"""
    response = client.get('/api/models')
    data = response.get_json()

    model_ids = [m['id'] for m in data['models']]
    assert 'Kwai-Kolors/Kolors' in model_ids
    assert 'Tongyi-MAI/Z-Image-Turbo' in model_ids
    assert 'Qwen/Qwen-Image' in model_ids
```

- [ ] **Step 2: 运行所有测试**

```bash
cd pixelforge
pytest tests/ -v
```

Expected: All tests passed

- [ ] **Step 3: 手动启动测试**

```bash
cd pixelforge

# 确保 .env 文件存在
cp .env.example .env
# 编辑 .env 填入 API 密钥

# 启动应用
python app.py
```

Expected:
- 输出启动信息
- 访问 http://localhost:5000 可以看到界面
- 下拉框显示 7 个模型
- 历史记录区域正常显示

- [ ] **Step 4: 最终提交**

```bash
git add .
git commit -m "feat: complete PixelForge v1.0 implementation"
```

---

## 实现完成检查清单

- [ ] 所有测试通过
- [ ] 应用可以正常启动
- [ ] 界面正常显示（深色主题）
- [ ] 模型下拉框显示 7 个选项
- [ ] 可以输入提示词并生成图片
- [ ] 生成结果正确显示
- [ ] 历史记录正常工作
- [ ] 下载图片功能正常
- [ ] 错误处理正常（无 API 密钥时提示）
- [ ] 响应式布局正常

---

## 常见问题

### Q: API 密钥在哪里配置？

A: 在 `pixelforge/.env` 文件中设置 `SILICONFLOW_API_KEY`

### Q: 如何添加更多模型？

A: 修改 `config.py` 中的 `MODELS` 列表

### Q: 图片保存在哪里？

A: `pixelforge/static/images/generated/` 目录

### Q: 如何修改历史记录数量？

A: 修改 `config.py` 中的 `MAX_HISTORY` 值
