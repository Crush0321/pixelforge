import pytest
from unittest.mock import patch, MagicMock
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


@patch('image_generator.requests.post')
def test_generate_success(mock_post):
    """测试生成图片成功"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': [{'url': 'https://example.com/image.png'}],
        'seed': 12345
    }
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    generator = ImageGenerator(api_key='sk-test-key')
    result = generator.generate(
        prompt='一只猫',
        model='Kwai-Kolors/Kolors',
        size='1024x576',
        steps=25,
        seed=42
    )

    assert result['success'] is True
    assert result['image_url'] == 'https://example.com/image.png'
    assert result['generation_time'] >= 0
    assert result['seed'] == 12345
    assert result['error'] is None


@patch('image_generator.requests.post')
def test_generate_timeout(mock_post):
    """测试生成图片超时"""
    import requests
    mock_post.side_effect = requests.exceptions.Timeout()

    generator = ImageGenerator(api_key='sk-test-key')
    result = generator.generate(
        prompt='一只猫',
        model='Kwai-Kolors/Kolors',
        size='1024x576',
        steps=25,
        timeout=1
    )

    assert result['success'] is False
    assert result['image_url'] is None
    assert result['generation_time'] == 0
    assert result['seed'] is None
    assert '超时' in result['error']


@patch('image_generator.requests.get')
def test_download_image_success(mock_get, tmp_path):
    """测试下载图片成功"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'\x89PNG\r\n\x1a\n'  # PNG header bytes
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    generator = ImageGenerator(api_key='sk-test-key')
    filename = generator.download_image(
        url='https://example.com/image.png',
        save_dir=str(tmp_path)
    )

    assert filename is not None
    assert filename.endswith('.png')


def test_build_payload_seed_absent():
    """测试 seed=None 时 payload 中不含 seed 键"""
    generator = ImageGenerator(api_key='sk-test-key')
    payload = generator.build_payload(
        prompt='一只猫',
        model='Kwai-Kolors/Kolors',
        size='1024x576',
        steps=25,
        seed=None
    )
    assert 'seed' not in payload


@patch('image_generator.requests.post')
def test_generate_request_exception(mock_post):
    """测试请求异常时返回 success=False 及全部 5 个键"""
    import requests
    mock_post.side_effect = requests.exceptions.RequestException('Connection error')

    generator = ImageGenerator(api_key='sk-test-key')
    result = generator.generate(
        prompt='一只猫',
        model='Kwai-Kolors/Kolors',
        size='1024x576',
        steps=25
    )

    assert result['success'] is False
    assert result['image_url'] is None
    assert result['generation_time'] == 0
    assert result['seed'] is None
    assert result['error'] is not None


@patch('image_generator.requests.post')
def test_generate_no_images_returned(mock_post):
    """测试 API 返回空图片列表时 success=False"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': [],
        'seed': 12345
    }
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    generator = ImageGenerator(api_key='sk-test-key')
    result = generator.generate(
        prompt='一只猫',
        model='Kwai-Kolors/Kolors',
        size='1024x576',
        steps=25
    )

    assert result['success'] is False


@patch('image_generator.requests.get')
def test_download_image_failure(mock_get, tmp_path):
    """测试下载图片失败时返回 None"""
    import requests
    mock_get.side_effect = requests.exceptions.RequestException('Network error')

    generator = ImageGenerator(api_key='sk-test-key')
    filename = generator.download_image(
        url='https://example.com/image.png',
        save_dir=str(tmp_path)
    )

    assert filename is None
