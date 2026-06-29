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
