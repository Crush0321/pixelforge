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

def test_full_page_render(client):
    """测试完整页面渲染"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode()
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
