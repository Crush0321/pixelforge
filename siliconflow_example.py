#!/usr/bin/env python3
"""
SiliconFlow 图片生成示例

展示如何使用 SiliconFlowImageGenerator 类进行图片生成
"""

import os
import sys
from siliconflow_image_generator import SiliconFlowImageGenerator

# ============================================================
# 配置区域 - 请修改以下配置
# ============================================================

# 从环境变量获取 API 密钥，或者直接在这里设置
API_KEY = os.environ.get("SILICONFLOW_API_KEY", "sk-your-api-key-here")

# 输出目录
OUTPUT_DIR = "./example_output"


def example_basic():
    """基础示例：生成单张图片"""
    print("\n" + "="*60)
    print("示例 1: 基础图片生成")
    print("="*60)

    generator = SiliconFlowImageGenerator(API_KEY)

    prompt = "一只可爱的橘猫坐在阳光明媚的窗台上，背景是绿植"

    print(f"提示词: {prompt}")
    print("正在生成...")

    try:
        response = generator.generate_image(
            prompt=prompt,
            image_size="1024x1024",
            num_inference_steps=20
        )

        saved_files = generator.save_images(
            response,
            output_dir=OUTPUT_DIR,
            filename_prefix="example_basic"
        )

        print(f"✓ 成功生成 {len(saved_files)} 张图片")

    except Exception as e:
        print(f"✗ 生成失败: {e}")


def example_multiple():
    """批量示例：一次生成多张图片"""
    print("\n" + "="*60)
    print("示例 2: 批量生成图片")
    print("="*60)

    generator = SiliconFlowImageGenerator(API_KEY)

    prompt = "未来科技城市的夜景，霓虹灯闪烁，飞行汽车穿梭"

    print(f"提示词: {prompt}")
    print("批量生成 4 张图片...")

    try:
        response = generator.generate_image(
            prompt=prompt,
            image_size="1024x1024",
            num_inference_steps=25,
            batch_size=4
        )

        saved_files = generator.save_images(
            response,
            output_dir=OUTPUT_DIR,
            filename_prefix="example_batch"
        )

        print(f"✓ 成功生成 {len(saved_files)} 张图片")

    except Exception as e:
        print(f"✗ 生成失败: {e}")


def example_custom_size():
    """自定义尺寸示例：生成不同比例的图片"""
    print("\n" + "="*60)
    print("示例 3: 自定义图片尺寸")
    print("="*60)

    generator = SiliconFlowImageGenerator(API_KEY)

    # 竖版图片
    prompt_vertical = "高山流水，中国水墨画风格"

    print(f"提示词: {prompt_vertical}")
    print("生成竖版图片 (768x1024)...")

    try:
        response = generator.generate_image(
            prompt=prompt_vertical,
            image_size="768x1024",
            num_inference_steps=20
        )

        saved_files = generator.save_images(
            response,
            output_dir=OUTPUT_DIR,
            filename_prefix="example_vertical"
        )

        print(f"✓ 成功生成 {len(saved_files)} 张图片")

    except Exception as e:
        print(f"✗ 生成失败: {e}")

    # 横版图片
    prompt_horizontal = "广阔的草原，远处是雪山，蓝天白云"

    print(f"\n提示词: {prompt_horizontal}")
    print("生成横版图片 (1024x768)...")

    try:
        response = generator.generate_image(
            prompt=prompt_horizontal,
            image_size="1024x768",
            num_inference_steps=20
        )

        saved_files = generator.save_images(
            response,
            output_dir=OUTPUT_DIR,
            filename_prefix="example_horizontal"
        )

        print(f"✓ 成功生成 {len(saved_files)} 张图片")

    except Exception as e:
        print(f"✗ 生成失败: {e}")


def example_with_seed():
    """种子示例：使用固定种子生成可复现的图片"""
    print("\n" + "="*60)
    print("示例 4: 使用固定种子")
    print("="*60)

    generator = SiliconFlowImageGenerator(API_KEY)

    prompt = "一朵盛开的玫瑰，露珠在花瓣上，微距摄影"
    seed = 42

    print(f"提示词: {prompt}")
    print(f"随机种子: {seed}")
    print("生成图片...")

    try:
        # 第一次生成
        response1 = generator.generate_image(
            prompt=prompt,
            image_size="1024x1024",
            num_inference_steps=20,
            seed=seed
        )

        saved_files1 = generator.save_images(
            response1,
            output_dir=OUTPUT_DIR,
            filename_prefix="example_seed_first"
        )

        # 第二次生成（相同种子）
        print("\n使用相同种子再次生成...")
        response2 = generator.generate_image(
            prompt=prompt,
            image_size="1024x1024",
            num_inference_steps=20,
            seed=seed
        )

        saved_files2 = generator.save_images(
            response2,
            output_dir=OUTPUT_DIR,
            filename_prefix="example_seed_second"
        )

        print(f"✓ 成功生成 {len(saved_files1) + len(saved_files2)} 张图片")
        print("提示: 使用相同种子和参数应生成相似的图片")

    except Exception as e:
        print(f"✗ 生成失败: {e}")


def example_english_prompts():
    """英文提示词示例"""
    print("\n" + "="*60)
    print("示例 5: 英文提示词")
    print("="*60)

    generator = SiliconFlowImageGenerator(API_KEY)

    prompts = [
        "A cozy coffee shop interior with warm lighting, autumn vibes",
        "Abstract digital art with vibrant neon colors",
        "Cute robot character, Pixar style, friendly expression"
    ]

    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] 提示词: {prompt}")
        print("正在生成...")

        try:
            response = generator.generate_image(
                prompt=prompt,
                image_size="1024x1024",
                num_inference_steps=20
            )

            saved_files = generator.save_images(
                response,
                output_dir=OUTPUT_DIR,
                filename_prefix=f"example_english_{i}"
            )

            print(f"✓ 成功生成 {len(saved_files)} 张图片")

        except Exception as e:
            print(f"✗ 生成失败: {e}")


def main():
    """运行所有示例"""
    print("\n" + "*"*60)
    print("SiliconFlow FLUX.1-schnell 图片生成示例")
    print("*"*60)

    # 检查 API 密钥
    if API_KEY == "sk-your-api-key-here":
        print("\n⚠️  请先设置 API 密钥!")
        print("方法 1: 设置环境变量 SILICONFLOW_API_KEY")
        print("方法 2: 修改本文件中的 API_KEY 变量")
        print("\n获取 API 密钥: https://cloud.siliconflow.cn")
        sys.exit(1)

    # 运行示例
    print("\n选择要运行的示例:")
    print("1. 基础图片生成")
    print("2. 批量生成图片")
    print("3. 自定义图片尺寸")
    print("4. 使用固定种子")
    print("5. 英文提示词")
    print("6. 运行所有示例")
    print("0. 退出")

    while True:
        choice = input("\n请输入选项 (0-6): ").strip()

        if choice == "0":
            print("再见!")
            break
        elif choice == "1":
            example_basic()
        elif choice == "2":
            example_multiple()
        elif choice == "3":
            example_custom_size()
        elif choice == "4":
            example_with_seed()
        elif choice == "5":
            example_english_prompts()
        elif choice == "6":
            example_basic()
            example_multiple()
            example_custom_size()
            example_with_seed()
            example_english_prompts()
            print("\n" + "*"*60)
            print("所有示例运行完成!")
            print("*"*60)
        else:
            print("无效选项，请重新输入")


if __name__ == "__main__":
    main()
