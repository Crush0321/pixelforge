#!/usr/bin/env python3
"""
通义万相 (Tongyi Wanxiang) 图片生成工具

使用阿里云 DashScope API 调用通义万相模型生成高质量图片。

使用方法:
    python tongyi_image_generator.py "一只可爱的猫咪" --size 1024x1024

环境变量:
    DASHSCOPE_API_KEY: 你的 DashScope API 密钥

作者: Claude
日期: 2026-06-29
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any


# 默认配置
DEFAULT_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
DEFAULT_TASK_URL = "https://dashscope.aliyuncs.com/api/v1/tasks"
DEFAULT_MODEL = "wanx-v1"
DEFAULT_IMAGE_SIZE = "1024*1024"
DEFAULT_NUM_IMAGES = 1
DEFAULT_OUTPUT_DIR = "./generated_images"

# 支持的图片尺寸
SUPPORTED_SIZES = [
    "512*512",
    "768*768",
    "1024*1024",
    "768*1024",
    "1024*768"
]

# 支持的风格
SUPPORTED_STYLES = [
    "<auto>",           # 自动
    "<3d cartoon>",     # 3D卡通
    "<anime>",          # 动漫
    "<oil painting>",   # 油画
    "<watercolor>",     # 水彩
    "<sketch>",         # 素描
    "<chinese painting>", # 中国画
    "<flat illustration>", # 扁平插画"
]


class TongyiImageGenerator:
    """通义万相图片生成器"""

    def __init__(self, api_key: str, api_url: str = DEFAULT_API_URL):
        """
        初始化图片生成器

        Args:
            api_key: DashScope API 密钥
            api_url: API 端点 URL
        """
        self.api_key = api_key
        self.api_url = api_url
        self.task_url = DEFAULT_TASK_URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"  # 使用异步模式
        }

    def submit_task(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        image_size: str = DEFAULT_IMAGE_SIZE,
        num_images: int = DEFAULT_NUM_IMAGES,
        style: str = "<auto>",
        seed: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        提交图片生成任务

        Args:
            prompt: 图片描述文本
            model: 模型名称
            image_size: 图片尺寸 (如 "1024*1024")
            num_images: 生成图片数量
            style: 图片风格
            seed: 随机种子（可选）
            **kwargs: 其他可选参数

        Returns:
            任务 ID

        Raises:
            requests.exceptions.RequestException: 请求失败
            ValueError: 参数错误
        """
        # 构建请求体
        payload = {
            "model": model,
            "input": {
                "prompt": prompt
            },
            "parameters": {
                "n": num_images,
                "size": image_size,
                "style": style
            }
        }

        # 添加可选参数
        if seed is not None:
            payload["parameters"]["seed"] = seed

        # 添加其他自定义参数
        if kwargs:
            payload["parameters"].update(kwargs)

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            # 检查响应
            if "output" in result and "task_id" in result["output"]:
                return result["output"]["task_id"]
            else:
                raise ValueError(f"无效的响应格式: {result}")

        except requests.exceptions.RequestException as e:
            print(f"API 请求失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"错误详情: {e.response.text}")
            raise

    def query_task(self, task_id: str) -> Dict[str, Any]:
        """
        查询任务状态

        Args:
            task_id: 任务 ID

        Returns:
            任务状态信息
        """
        url = f"{self.task_url}/{task_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"查询任务失败: {e}")
            raise

    def wait_for_completion(
        self,
        task_id: str,
        max_wait_time: int = 300,
        poll_interval: int = 2
    ) -> Dict[str, Any]:
        """
        等待任务完成

        Args:
            task_id: 任务 ID
            max_wait_time: 最大等待时间（秒）
            poll_interval: 轮询间隔（秒）

        Returns:
            完成的任务结果

        Raises:
            TimeoutError: 等待超时
            RuntimeError: 任务失败
        """
        start_time = time.time()

        while True:
            # 检查是否超时
            elapsed = time.time() - start_time
            if elapsed > max_wait_time:
                raise TimeoutError(f"任务超时 ({max_wait_time}秒)")

            # 查询任务状态
            result = self.query_task(task_id)
            status = result.get("output", {}).get("task_status", "UNKNOWN")

            print(f"任务状态: {status} (已等待 {elapsed:.1f}秒)")

            if status == "SUCCEEDED":
                return result
            elif status in ["FAILED", "CANCELED"]:
                error_msg = result.get("output", {}).get("message", "未知错误")
                raise RuntimeError(f"任务失败: {error_msg}")
            elif status in ["PENDING", "RUNNING"]:
                # 继续等待
                time.sleep(poll_interval)
            else:
                print(f"未知状态: {status}")
                time.sleep(poll_interval)

    def generate_image(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        image_size: str = DEFAULT_IMAGE_SIZE,
        num_images: int = DEFAULT_NUM_IMAGES,
        style: str = "<auto>",
        seed: Optional[int] = None,
        max_wait_time: int = 300,
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成图片（完整流程）

        Args:
            prompt: 图片描述文本
            model: 模型名称
            image_size: 图片尺寸
            num_images: 生成图片数量
            style: 图片风格
            seed: 随机种子
            max_wait_time: 最大等待时间（秒）
            **kwargs: 其他参数

        Returns:
            生成结果
        """
        print(f"提交图片生成任务...")
        task_id = self.submit_task(
            prompt=prompt,
            model=model,
            image_size=image_size,
            num_images=num_images,
            style=style,
            seed=seed,
            **kwargs
        )
        print(f"任务 ID: {task_id}")

        print(f"等待任务完成...")
        result = self.wait_for_completion(task_id, max_wait_time=max_wait_time)

        return result

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
        results = response_data.get("output", {}).get("results", [])

        if not results:
            print("警告: 响应中没有找到图片数据")
            print(f"响应内容: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            return saved_files

        for i, image_data in enumerate(results):
            # 生成文件名
            if len(results) == 1:
                filename = f"{filename_prefix}_{timestamp}.png"
            else:
                filename = f"{filename_prefix}_{timestamp}_{i+1}.png"

            filepath = output_path / filename

            # 获取图片 URL
            image_url = image_data.get("url")
            if not image_url:
                print(f"警告: 图片 {i+1} 没有 URL")
                continue

            # 下载图片
            try:
                img_response = requests.get(image_url, timeout=60)
                img_response.raise_for_status()

                with open(filepath, "wb") as f:
                    f.write(img_response.content)

                saved_files.append(str(filepath))
                print(f"✓ 图片已保存: {filepath}")

            except Exception as e:
                print(f"✗ 保存图片 {i+1} 失败: {e}")

        return saved_files


def get_api_key() -> str:
    """
    获取 API 密钥

    优先从环境变量获取，如果没有则提示用户输入

    Returns:
        API 密钥
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")

    if not api_key:
        api_key = input("请输入你的 DashScope API 密钥: ").strip()

    if not api_key:
        print("错误: 必须提供 API 密钥")
        print("获取方式: https://dashscope.console.aliyun.com/")
        sys.exit(1)

    return api_key


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="使用通义万相模型生成图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "一只可爱的猫咪坐在花园里"
  %(prog)s "A beautiful sunset" --size 1024*1024 --style "<anime>"
  %(prog)s "科幻城市" --num 4 --output ./my_images
  %(prog)s "风景画" --seed 42  # 使用固定种子可复现

支持的风格:
  <auto>              自动（默认）
  <3d cartoon>        3D卡通
  <anime>             动漫
  <oil painting>      油画
  <watercolor>        水彩
  <sketch>            素描
  <chinese painting>  中国画
  <flat illustration> 扁平插画

支持的尺寸:
  512*512   768*768   1024*1024   768*1024   1024*768
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
        help=f"图片尺寸 (默认: {DEFAULT_IMAGE_SIZE})"
    )

    parser.add_argument(
        "--num", "--num-images",
        type=int,
        default=DEFAULT_NUM_IMAGES,
        help=f"生成图片数量 (默认: {DEFAULT_NUM_IMAGES})"
    )

    parser.add_argument(
        "--style",
        default="<auto>",
        help=f"图片风格 (默认: <auto>)"
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
        default="tongyi",
        help="输出文件名前缀 (默认: tongyi)"
    )

    parser.add_argument(
        "--api-key",
        help="DashScope API 密钥（也可通过环境变量 DASHSCOPE_API_KEY 设置）"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="最大等待时间（秒）(默认: 300)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细信息"
    )

    args = parser.parse_args()

    # 获取 API 密钥
    api_key = args.api_key or os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误: 请通过 --api-key 参数或 DASHSCOPE_API_KEY 环境变量提供 API 密钥")
        print("获取 API 密钥: https://dashscope.console.aliyun.com/")
        sys.exit(1)

    # 创建生成器
    generator = TongyiImageGenerator(api_key)

    # 显示配置
    if args.verbose:
        print("\n" + "="*50)
        print("配置信息")
        print("="*50)
        print(f"模型: {args.model}")
        print(f"提示词: {args.prompt}")
        print(f"图片尺寸: {args.size}")
        print(f"生成数量: {args.num}")
        print(f"风格: {args.style}")
        if args.seed is not None:
            print(f"随机种子: {args.seed}")
        print(f"输出目录: {args.output}")
        print(f"超时时间: {args.timeout}秒")
        print("="*50 + "\n")

    # 生成图片
    print(f"正在生成图片...")
    print(f"提示词: {args.prompt}")

    try:
        response_data = generator.generate_image(
            prompt=args.prompt,
            model=args.model,
            image_size=args.size,
            num_images=args.num,
            style=args.style,
            seed=args.seed,
            max_wait_time=args.timeout
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
    except TimeoutError as e:
        print(f"\n✗ 超时: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"\n✗ 任务失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
