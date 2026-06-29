#!/usr/bin/env python3
"""
SiliconFlow 图片生成工具 - 测试脚本

用于测试工具的基本功能，不执行实际的 API 调用
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from siliconflow_image_generator import SiliconFlowImageGenerator


class TestSiliconFlowImageGenerator(unittest.TestCase):
    """测试 SiliconFlowImageGenerator 类"""

    def setUp(self):
        """测试前准备"""
        self.api_key = "sk-test-key-123"
        self.generator = SiliconFlowImageGenerator(self.api_key)

    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.generator.api_key, self.api_key)
        self.assertIn("Bearer", self.generator.headers["Authorization"])
        self.assertIn(self.api_key, self.generator.headers["Authorization"])

    def test_headers(self):
        """测试请求头"""
        self.assertEqual(self.generator.headers["Content-Type"], "application/json")
        self.assertEqual(
            self.generator.headers["Authorization"],
            f"Bearer {self.api_key}"
        )

    @patch('requests.post')
    def test_generate_image_success(self, mock_post):
        """测试成功生成图片"""
        # 模拟成功的 API 响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "images": [
                {"url": "https://example.com/image1.png"},
                {"url": "https://example.com/image2.png"}
            ],
            "timings": {"inference": 1.5}
        }
        mock_post.return_value = mock_response

        # 调用生成方法
        result = self.generator.generate_image(
            prompt="测试图片",
            image_size="1024x1024",
            num_inference_steps=20,
            batch_size=2
        )

        # 验证结果
        self.assertIn("images", result)
        self.assertEqual(len(result["images"]), 2)

        # 验证请求参数
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        self.assertEqual(payload["prompt"], "测试图片")
        self.assertEqual(payload["image_size"], "1024x1024")
        self.assertEqual(payload["batch_size"], 2)

    @patch('requests.post')
    def test_generate_image_with_seed(self, mock_post):
        """测试使用固定种子生成图片"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "images": [{"url": "https://example.com/image.png"}]
        }
        mock_post.return_value = mock_response

        # 使用种子
        self.generator.generate_image(
            prompt="测试",
            seed=42
        )

        # 验证种子参数
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        self.assertEqual(payload["seed"], 42)

    @patch('requests.post')
    def test_generate_image_failure(self, mock_post):
        """测试生成失败的情况"""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("API Error")

        with self.assertRaises(requests.exceptions.RequestException):
            self.generator.generate_image(prompt="测试")

    @patch('requests.get')
    @patch('builtins.open', unittest.mock.mock_open())
    def test_save_images_from_url(self, mock_get):
        """测试从 URL 保存图片"""
        # 模拟图片下载
        mock_response = MagicMock()
        mock_response.content = b"fake image content"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # 模拟 API 响应
        response_data = {
            "images": [
                {"url": "https://example.com/image.png"}
            ]
        }

        # 保存图片
        saved_files = self.generator.save_images(
            response_data,
            output_dir="./test_output",
            filename_prefix="test"
        )

        # 验证
        self.assertEqual(len(saved_files), 1)
        mock_get.assert_called_once()

    def test_save_images_empty(self):
        """测试保存空图片列表"""
        response_data = {"images": []}

        saved_files = self.generator.save_images(response_data)
        self.assertEqual(len(saved_files), 0)

    def test_save_images_no_data(self):
        """测试响应中没有图片数据"""
        response_data = {"other_key": "value"}

        saved_files = self.generator.save_images(response_data)
        self.assertEqual(len(saved_files), 0)


def run_tests():
    """运行测试"""
    print("\n" + "="*60)
    print("SiliconFlow 图片生成工具 - 单元测试")
    print("="*60 + "\n")

    # 运行测试
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()
