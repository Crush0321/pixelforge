# pixelforge/app.py
import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from config import Config
from image_generator import ImageGenerator

# 初始化配置
Config.init_data_dir()

# 创建 Flask 应用
app = Flask(__name__)
app.config.from_object(Config)

# 图片生成器（延迟初始化）
generator = None

def get_generator():
    """获取或创建图片生成器实例"""
    global generator
    if generator is None:
        if not Config.SILICONFLOW_API_KEY:
            raise ValueError('请配置 SILICONFLOW_API_KEY')
        generator = ImageGenerator(Config.SILICONFLOW_API_KEY)
    return generator


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html',
                         models=Config.MODELS,
                         sizes=Config.SIZES)


# ==================== API 路由 ====================

@app.route('/api/models')
def get_models():
    """获取可用模型列表"""
    return jsonify({'models': Config.MODELS})


@app.route('/api/history')
def get_history():
    """获取历史记录"""
    try:
        history = Config.load_json(Config.HISTORY_FILE)
        return jsonify(history)
    except Exception as e:
        return jsonify({'records': [], 'total': 0})


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """清空历史记录"""
    try:
        Config._save_json(Config.HISTORY_FILE, {'records': [], 'total': 0})

        # 删除图片文件
        for filename in os.listdir(Config.IMAGE_DIR):
            filepath = os.path.join(Config.IMAGE_DIR, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)

        return jsonify({'success': True, 'message': '历史记录已清空'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/generate', methods=['POST'])
def generate_image():
    """生成图片"""
    data = request.get_json()

    # 验证参数
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({'success': False, 'error': '请输入提示词'}), 400

    model = data.get('model', 'Kwai-Kolors/Kolors')
    size = data.get('size', '1024x576')
    steps = data.get('steps', 25)
    seed = data.get('seed')

    # 验证模型
    valid_models = [m['id'] for m in Config.MODELS]
    if model not in valid_models:
        return jsonify({'success': False, 'error': '无效的模型选择'}), 400

    # 验证步数
    if not isinstance(steps, int) or steps < 1 or steps > 50:
        return jsonify({'success': False, 'error': '步数应在 1-50 之间'}), 400

    try:
        # 调用生成器
        gen = get_generator()
        result = gen.generate(
            prompt=prompt,
            model=model,
            size=size,
            steps=steps,
            seed=seed
        )

        if not result['success']:
            return jsonify(result), 500

        # 下载图片
        filename = gen.download_image(result['image_url'], Config.IMAGE_DIR)
        if not filename:
            return jsonify({'success': False, 'error': '图片下载失败'}), 500

        # 保存历史记录
        record = {
            'id': str(uuid.uuid4()),
            'prompt': prompt,
            'model': model,
            'size': size,
            'steps': steps,
            'seed': result.get('seed'),
            'image_filename': filename,
            'generation_time': result['generation_time'],
            'created_at': datetime.now().isoformat()
        }

        history = Config.load_json(Config.HISTORY_FILE)
        history['records'].insert(0, record)

        # 限制历史记录数量
        if len(history['records']) > Config.MAX_HISTORY:
            # 删除旧图片
            for old_record in history['records'][Config.MAX_HISTORY:]:
                old_path = os.path.join(Config.IMAGE_DIR, old_record['image_filename'])
                if os.path.exists(old_path):
                    os.remove(old_path)
            history['records'] = history['records'][:Config.MAX_HISTORY]

        history['total'] = len(history['records'])
        Config._save_json(Config.HISTORY_FILE, history)

        # 返回结果
        return jsonify({
            'success': True,
            'data': {
                'image_url': f'/static/images/generated/{filename}',
                'filename': filename,
                'model': model,
                'prompt': prompt,
                'size': size,
                'steps': steps,
                'seed': result.get('seed'),
                'generation_time': result['generation_time']
            }
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'生成失败: {str(e)}'}), 500


# ==================== 静态文件 ====================

@app.route('/static/images/generated/<filename>')
def serve_generated_image(filename):
    """提供生成的图片"""
    return send_from_directory(Config.IMAGE_DIR, filename)


# ==================== 启动 ====================

if __name__ == '__main__':
    print(f'PixelForge 启动中...')
    print(f'访问地址: http://localhost:{Config.PORT}')
    print(f'API 密钥: {"已配置" if Config.SILICONFLOW_API_KEY else "未配置"}')
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
