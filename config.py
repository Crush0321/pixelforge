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
    PORT = int(os.getenv('FLASK_PORT', 5001))
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
