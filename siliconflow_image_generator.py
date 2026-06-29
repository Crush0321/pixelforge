#!/usr/bin/env python3
"""
硅基流动 (SiliconFlow) FLUX.1-schnell 图片生成工具

使用 SiliconFlow API 调用 black-forest-labs/FLUX.1-schnell 模型生成图片。

使用方法:
    python siliconflow_image_generator.py "一只可爱的猫咪" --size 1024x1024

环境变量:
    SILICONFLOW_API_KEY: 你的 SiliconFlow API 密钥

作者: Claude
日期: 2026-06-29
"""

import os
import sys
import json
import base64
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any


# 默认配置
DEFAULT_API_URL = "https://api.siliconflow.cn/v1/images/generations"
DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"
DEFAULT_IMAGE_SIZE = "1024x1024"
DEFAULT_NUM_INFERENCE_STEPS = 20
DEFAULT_BATCH_SIZE = 1
DEFAULT_OUTPUT_DIR = "./generated_images"


class SiliconFlowImageGenerator:
    """SiliconFlow 图片生成器"""

    def __init__(self, api_key: str, api_url: str = DEFAULT_API_URL):
        """
        初始化图片生成器

        Args:
            api_key: SiliconFlow API 密钥
            api_url: API 端点 URL
        """
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        image_size: str = DEFAULT_IMAGE_SIZE,
        num_inference_steps: int = DEFAULT_NUM_INFERENCE_STEPS,
        batch_size: int = DEFAULT_BATCH_SIZE,
        seed: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成图片

        Args:
            prompt: 图片描述文本
            model: 模型名称
            image_size: 图片尺寸 (如 "1024x1024", "768x1024")
            num_inference_steps: 推理步数
            batch_size: 批次大小（一次生成的图片数量）
            seed: 随机种子（可选，用于可复现生成）
            **kwargs: 其他可选参数

        Returns:
            API 响应数据

        Raises:
            requests.exceptions.RequestException: 请求失败
            ValueError: 参数错误
        """
        # 构建请求体
        payload = {
            "model": model,
            "prompt": prompt,
            "image_size": image_size,
            "num_inference_steps": num_inference_steps,
            "batch_size": batch_size
        }

        # 添加可选参数
        if seed is not None:
            payload["seed"] = seed

        # 添加其他自定义参数
        payload.update(kwargs)

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=120  # 2分钟超时
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API 请求失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"错误详情: {e.response.text}")
            raise

    def save_images(
        self,
        response_data: Dict[str, Any],
        output_dir: str = DEFAULT_OUTPUT_DIR,
        filename_prefix: str = "generated"
    ) -> List[str]:
        """
        保存生成的图片到本地

        Args:
            response_data: API 响应数据
            output_dir: 输出目录
            filename_prefix: 文件名前缀

        Returns:
            保存的文件路径列表
        """
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 获取图片数据
        images = response_data.get("images", response_data.get("data", []))

        if not images:
            print("警告: 响应中没有找到图片数据")
            print(f"响应内容: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            return saved_files

        for i, image_data in enumerate(images):
            # 生成文件名
            if len(images) == 1:
                filename = f"{filename_prefix}_{timestamp}.png"
            else:
                filename = f"{filename_prefix}_{timestamp}_{i+1}.png"

            filepath = output_path / filename

            # 获取图片数据（可能是 URL 或 base64）
            if isinstance(image_data, dict):
                if "url" in image_data:
                    # 下载图片
                    img_response = requests.get(image_data["url"], timeout=60)
                    img_response.raise_for_status()
                    with open(filepath, "wb") as f:
                        f.write(img_response.content)
                elif "b64_json" in image_data:
                    # 解码 base64
                    img_bytes = base64.b64decode(image_data["b64_json"])
                    with open(filepath, "wb") as f:
                        f.write(img_bytes)
                else:
                    print(f"警告: 未知的图片数据格式: {image_data.keys()}")
                    continue
            elif isinstance(image_data, str):
                # 可能是 URL 或 base64 字符串
                if image_data.startswith(("http://", "https://")):
                    img_response = requests.get(image_data, timeout=60)
                    img_response.raise_for_status()
                    with open(filepath, "wb") as f:
                        f.write(img_response.content)
                else:
                    # 尝试作为 base64 解码
                    try:
                        img_bytes = base64.b64decode(image_data)
                        with open(filepath, "wb") as f:
                            f.write(img_bytes)
                    except Exception:
                        print(f"警告: 无法解码图片数据")
                        continue
            else:
                print(f"警告: 未知的图片数据类型: {type(image_data)}")
                continue

            saved_files.append(str(filepath))
            print(f"✓ 图片已保存: {filepath}")

        return saved_files


def get_api_key() -> str:
    """
    获取 API 密钥

    优先从环境变量获取，如果没有则提示用户输入

    Returns:
        API 密钥
    """
    api_key = os.environ.get("SILICONFLOW_API_KEY")

    if not api_key:
        api_key = input("请输入你的 SiliconFlow API 密钥: ").strip()

    if not api_key:
        print("错误: 必须提供 API 密钥")
        sys.exit(1)

    return api_key


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="使用 SiliconFlow FLUX.1-schnell 模型生成图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "一只可爱的猫咪坐在花园里"
  %(prog)s "A beautiful sunset" --size 1024x1024 --steps 30
  %(prog)s "科幻城市" --batch 4 --output ./my_images
  %(prog)s "风景画" --seed 42  # 使用固定种子可复现
        """
    )

    parser.add_argument(
        "prompt",
        help="图片描述文本（支持中文和英文）"
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"模型名称 (默认: {DEFAULT_MODEL})"
    )

    parser.add_argument(
        "--size", "--image-size",
        default=DEFAULT_IMAGE_SIZE,
        help=f"图片尺寸，如 1024x1024, 768x1024 (默认: {DEFAULT_IMAGE_SIZE})"
    )

    parser.add_argument(
        "--steps", "--num-inference-steps",
        type=int,
        default=DEFAULT_NUM_INFERENCE_STEPS,
        help=f"推理步数，步数越多质量越高但速度越慢 (默认: {DEFAULT_NUM_INFERENCE_STEPS})"
    )

    parser.add_argument(
        "--batch", "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"一次生成的图片数量 (默认: {DEFAULT_BATCH_SIZE})"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="随机种子（可选，用于可复现生成）"
    )

    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT_DIR,
        help=f"输出目录 (默认: {DEFAULT_OUTPUT_DIR})"
    )

    parser.add_argument(
        "--prefix",
        default="flux",
        help="输出文件名前缀 (默认: flux)"
    )

    parser.add_argument(
        "--api-key",
        help="SiliconFlow API 密钥（也可通过环境变量 SILICONFLOW_API_KEY 设置）"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细信息"
    )

    args = parser.parse_args()

    # 获取 API 密钥
    api_key = args.api_key or os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        print("错误: 请通过 --api-key 参数或 SILICONFLOW_API_KEY 环境变量提供 API 密钥")
        print("获取 API 密钥: https://cloud.siliconflow.cn")
        sys.exit(1)

    # 创建生成器
    generator = SiliconFlowImageGenerator(api_key)

    # 显示配置
    if args.verbose:
        print("\n" + "="*50)
        print("配置信息")
        print("="*50)
        print(f"模型: {args.model}")
        print(f"提示词: {args.prompt}")
        print(f"图片尺寸: {args.size}")
        print(f"推理步数: {args.steps}")
        print(f"批次大小: {args.batch}")
        if args.seed is not None:
            print(f"随机种子: {args.seed}")
        print(f"输出目录: {args.output}")
        print("="*50 + "\n")

    # 生成图片
    print(f"正在生成图片...")
    print(f"提示词: {args.prompt}")

    try:
        response_data = generator.generate_image(
            prompt=args.prompt,
            model=args.model,
            image_size=args.size,
            num_inference_steps=args.steps,
            batch_size=args.batch,
            seed=args.seed
        )

        if args.verbose:
            print("\nAPI 响应:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))

        # 保存图片
        saved_files = generator.save_images(
            response_data,
            output_dir=args.output,
            filename_prefix=args.prefix
        )

        if saved_files:
            print(f"\n✓ 成功生成 {len(saved_files)} 张图片!")
        else:
            print("\n✗ 未能保存任何图片")
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"\n✗ 请求失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
