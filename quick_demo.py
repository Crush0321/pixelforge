#!/usr/bin/env python3
"""
SiliconFlow 图片生成工具 - 快速演示

这是一个最简单的使用示例
"""

import os
from siliconflow_image_generator import SiliconFlowImageGenerator

# ============================================================
# 使用前请设置 API 密钥:
# export SILICONFLOW_API_KEY="sk-your-api-key-here"
# ============================================================

def main():
    """快速演示"""

    # 从环境变量获取 API 密钥
    api_key = os.environ.get("SILICONFLOW_API_KEY")

    if not api_key:
        print("请先设置 API 密钥:")
        print('export SILICONFLOW_API_KEY="sk-your-api-key-here"')
        print("\n获取 API 密钥: https://cloud.siliconflow.cn")
        return

    # 创建生成器
    generator = SiliconFlowImageGenerator(api_key)

    # 生成图片
    prompt = "一只可爱的橘猫坐在阳光明媚的窗台上"
    print(f"正在生成图片: {prompt}")
    print("请稍候...")

    try:
        # 调用 API
        response = generator.generate_image(
            prompt=prompt,
            image_size="1024x1024",
            num_inference_steps=20
        )

        # 保存图片
        saved_files = generator.save_images(
            response,
            output_dir="./demo_output",
            filename_prefix="demo"
        )

        if saved_files:
            print(f"\n✓ 成功生成 {len(saved_files)} 张图片!")
            print(f"图片已保存到: {saved_files[0]}")
        else:
            print("\n✗ 未能生成图片")

    except Exception as e:
        print(f"\n✗ 发生错误: {e}")


if __name__ == "__main__":
    main()
