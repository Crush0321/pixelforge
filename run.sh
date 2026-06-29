#!/bin/bash

# SiliconFlow 图片生成工具 - 快速启动脚本

set -e

echo "=========================================="
echo "SiliconFlow FLUX.1-schnell 图片生成工具"
echo "=========================================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "首次运行，正在创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    pip install requests
    echo "✓ 虚拟环境创建完成"
else
    source venv/bin/activate
fi

# 检查 API 密钥
if [ -z "$SILICONFLOW_API_KEY" ]; then
    echo ""
    echo "⚠️  未检测到 API 密钥"
    echo "请设置环境变量："
    echo "  export SILICONFLOW_API_KEY='sk-your-api-key-here'"
    echo ""
    echo "或使用 --api-key 参数"
    echo "获取 API 密钥: https://cloud.siliconflow.cn"
    echo ""
    exit 1
fi

# 运行主程序
python3 siliconflow_image_generator.py "$@"
