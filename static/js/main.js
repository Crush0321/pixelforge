// PixelForge Frontend JavaScript

const PixelForge = {
    isGenerating: false,
    currentImageUrl: null,
    elements: {}
};

document.addEventListener('DOMContentLoaded', () => {
    PixelForge.init();
});

PixelForge.init = function() {
    this.elements = {
        promptInput: document.getElementById('promptInput'),
        modelSelect: document.getElementById('modelSelect'),
        sizeSelect: document.getElementById('sizeSelect'),
        stepsRange: document.getElementById('stepsRange'),
        stepsValue: document.getElementById('stepsValue'),
        seedInput: document.getElementById('seedInput'),
        generateBtn: document.getElementById('generateBtn'),
        resultSection: document.getElementById('resultSection'),
        loadingState: document.getElementById('loadingState'),
        imageDisplay: document.getElementById('imageDisplay'),
        errorState: document.getElementById('errorState'),
        generatedImage: document.getElementById('generatedImage'),
        generationTime: document.getElementById('generationTime'),
        usedModel: document.getElementById('usedModel'),
        usedSeed: document.getElementById('usedSeed'),
        errorMessage: document.getElementById('errorMessage'),
        downloadBtn: document.getElementById('downloadBtn'),
        regenerateBtn: document.getElementById('regenerateBtn'),
        refineBtn: document.getElementById('refineBtn'),
        retryBtn: document.getElementById('retryBtn'),
        historyToggle: document.getElementById('historyToggle'),
        historySection: document.getElementById('historySection'),
        historyGrid: document.getElementById('historyGrid'),
        historyEmpty: document.getElementById('historyEmpty'),
        clearHistoryBtn: document.getElementById('clearHistoryBtn'),
        toast: document.getElementById('toast'),
        toastMessage: document.getElementById('toastMessage')
    };
    this.bindEvents();
    this.loadHistory();
    console.log('PixelForge initialized');
};

PixelForge.bindEvents = function() {
    const el = this.elements;
    el.stepsRange.addEventListener('input', (e) => {
        el.stepsValue.textContent = e.target.value;
    });
    el.generateBtn.addEventListener('click', () => this.generate());
    el.regenerateBtn.addEventListener('click', () => this.generate());
    el.retryBtn.addEventListener('click', () => this.generate());
    el.downloadBtn.addEventListener('click', () => this.downloadImage());
    el.refineBtn.addEventListener('click', () => {
        el.promptInput.focus();
        this.showToast('info', '请修改提示词后重新生成');
    });
    el.historyToggle.addEventListener('click', () => {
        el.historySection.classList.toggle('hidden');
    });
    el.clearHistoryBtn.addEventListener('click', () => this.clearHistory());
    el.promptInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') this.generate();
    });
};

PixelForge.generate = async function() {
    if (this.isGenerating) return;
    const el = this.elements;
    const prompt = el.promptInput.value.trim();
    if (!prompt) {
        this.showToast('error', '请输入提示词');
        el.promptInput.focus();
        return;
    }
    const requestData = {
        prompt: prompt,
        model: el.modelSelect.value,
        size: el.sizeSelect.value,
        steps: parseInt(el.stepsRange.value)
    };
    const seed = el.seedInput.value.trim();
    if (seed) requestData.seed = parseInt(seed);
    this.setGenerating(true);
    el.resultSection.classList.remove('hidden');
    el.loadingState.classList.remove('hidden');
    el.imageDisplay.classList.add('hidden');
    el.errorState.classList.add('hidden');
    el.resultSection.scrollIntoView({ behavior: 'smooth' });
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
        const result = await response.json();
        if (result.success) {
            this.showResult(result.data);
            this.loadHistory();
            this.showToast('success', '图片生成成功！');
        } else {
            this.showError(result.error || '生成失败');
        }
    } catch (error) {
        this.showError('网络请求失败');
    } finally {
        this.setGenerating(false);
    }
};

PixelForge.setGenerating = function(isGenerating) {
    this.isGenerating = isGenerating;
    const el = this.elements;
    el.generateBtn.disabled = isGenerating;
    el.generateBtn.textContent = isGenerating ? '⏳ 生成中...' : '✨ 开始生成';
    el.generateBtn.classList.toggle('opacity-50', isGenerating);
    el.generateBtn.classList.toggle('cursor-not-allowed', isGenerating);
};

PixelForge.showResult = function(data) {
    const el = this.elements;
    this.currentImageUrl = data.image_url;
    el.generatedImage.src = data.image_url;
    el.generationTime.textContent = data.generation_time;
    el.usedModel.textContent = data.model;
    el.usedSeed.textContent = data.seed || '随机';
    el.loadingState.classList.add('hidden');
    el.imageDisplay.classList.remove('hidden');
    el.errorState.classList.add('hidden');
};

PixelForge.showError = function(message) {
    const el = this.elements;
    el.errorMessage.textContent = message;
    el.loadingState.classList.add('hidden');
    el.imageDisplay.classList.add('hidden');
    el.errorState.classList.remove('hidden');
};

PixelForge.downloadImage = function() {
    if (!this.currentImageUrl) return;
    const link = document.createElement('a');
    link.href = this.currentImageUrl;
    link.download = `pixelforge_${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    this.showToast('success', '图片下载已开始');
};

PixelForge.loadHistory = async function() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        this.renderHistory(data.records || []);
    } catch (error) {
        console.error('Failed to load history:', error);
    }
};

PixelForge.renderHistory = function(records) {
    const el = this.elements;
    if (records.length === 0) {
        el.historyGrid.classList.add('hidden');
        el.historyEmpty.classList.remove('hidden');
        return;
    }
    el.historyGrid.classList.remove('hidden');
    el.historyEmpty.classList.add('hidden');
    el.historyGrid.innerHTML = '';
    records.forEach(record => {
        const item = document.createElement('div');
        item.className = 'history-item relative group cursor-pointer rounded-xl overflow-hidden bg-dark-900 aspect-square';
        item.innerHTML = `
            <img src="/static/images/generated/${record.image_filename}" alt="${this.escapeHtml(record.prompt)}" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity p-3 flex flex-col justify-end">
                <p class="text-white text-xs line-clamp-2">${this.escapeHtml(record.prompt)}</p>
                <p class="text-gray-400 text-xs mt-1">${record.model.split('/')[1]}</p>
            </div>
        `;
        item.addEventListener('click', () => {
            this.elements.promptInput.value = record.prompt;
            this.showResult({
                image_url: `/static/images/generated/${record.image_filename}`,
                generation_time: record.generation_time,
                model: record.model,
                seed: record.seed
            });
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        el.historyGrid.appendChild(item);
    });
};

PixelForge.clearHistory = async function() {
    if (!confirm('确定要清空所有历史记录吗？')) return;
    try {
        const response = await fetch('/api/history', { method: 'DELETE' });
        const result = await response.json();
        if (result.success) {
            this.showToast('success', '历史记录已清空');
            this.loadHistory();
        } else {
            this.showToast('error', result.error || '清空失败');
        }
    } catch (error) {
        this.showToast('error', '操作失败');
    }
};

PixelForge.showToast = function(type, message) {
    const el = this.elements;
    const colors = {
        success: 'border-green-500',
        error: 'border-red-500',
        info: 'border-blue-500'
    };
    el.toast.className = `fixed bottom-8 right-8 z-50 bg-dark-800 ${colors[type] || colors.info} border-l-4 rounded-lg px-6 py-4 shadow-xl`;
    el.toastMessage.textContent = message;
    el.toast.classList.remove('hidden');
    el.toast.style.opacity = '0';
    el.toast.style.transform = 'translateY(20px)';
    requestAnimationFrame(() => {
        el.toast.style.transition = 'all 0.3s ease';
        el.toast.style.opacity = '1';
        el.toast.style.transform = 'translateY(0)';
    });
    setTimeout(() => {
        el.toast.style.opacity = '0';
        el.toast.style.transform = 'translateY(20px)';
        setTimeout(() => el.toast.classList.add('hidden'), 300);
    }, 3000);
};

PixelForge.escapeHtml = function(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
};
