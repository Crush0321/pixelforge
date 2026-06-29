import os
import uuid
import requests
from datetime import datetime
from typing import Optional, Dict, Any


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
                    'image_url': None,
                    'generation_time': 0,
                    'seed': None,
                    'error': '未返回图片数据'
                }

            image_url = images[0].get('url', '') if isinstance(images[0], dict) else images[0]
            generation_time = round(time.time() - start_time, 2)
            used_seed = result.get('seed', seed)

            return {
                'success': True,
                'image_url': image_url,
                'generation_time': generation_time,
                'seed': used_seed,
                'error': None
            }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'image_url': None,
                'generation_time': 0,
                'seed': None,
                'error': '请求超时，请重试'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'image_url': None,
                'generation_time': 0,
                'seed': None,
                'error': f'请求失败: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'image_url': None,
                'generation_time': 0,
                'seed': None,
                'error': f'生成失败: {str(e)}'
            }

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
