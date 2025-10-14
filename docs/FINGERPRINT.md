# 浏览器指纹随机化说明

## 功能概述

浏览器指纹随机化可以让每次注册使用不同的浏览器特征，避免被 Warp 识别为同一设备的批量注册。

## 随机化的特征

### 1. 基础特征（Chrome 启动参数）
- ✅ **窗口大小**：从常见分辨率中随机选择
- ✅ **User-Agent**：从真实的 UA 列表中随机选择
- ✅ **语言设置**：随机选择语言偏好
- ✅ **WebRTC**：禁用（防止 IP 泄露）

### 2. JavaScript 注入混淆
- ✅ **Canvas 指纹**：添加随机噪声
- ✅ **WebGL 指纹**：随机化 GPU 信息
- ✅ **Navigator 属性**：随机化 CPU 核心数、内存大小
- ✅ **时区**：随机化时区偏移

## 配置方法

### 启用指纹随机化（默认启用）

在 `.env` 文件中：

```bash
FINGERPRINT_RANDOMIZE=true
```

### 禁用指纹随机化

```bash
FINGERPRINT_RANDOMIZE=false
```

## 测试指纹随机化

运行测试脚本查看效果：

```bash
cd warp-pool
python test_fingerprint.py
```

输出示例：

```
指纹 #1:
------------------------------------------------------------
  🎭 浏览器指纹:
     分辨率: 1366x768
     User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0...
     语言: en-US,en;q=0.9
     时区: America/New_York
     CPU 核心: 8
     内存: 16GB

指纹 #2:
------------------------------------------------------------
  🎭 浏览器指纹:
     分辨率: 1920x1080
     User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0...
     语言: zh-CN,zh;q=0.9,en;q=0.8
     时区: Asia/Shanghai
     CPU 核心: 4
     内存: 8GB
```

## 运行效果

### 启用指纹随机化时

```
启动 Undetected Chrome (无头模式)...
  检测到 Chrome: C:\Program Files\Google\Chrome\Application\chrome.exe
  初始化 undetected-chromedriver...
  🎭 浏览器指纹:
     分辨率: 1536x864
     User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0...
     语言: en-GB,en;q=0.9
     时区: Europe/London
     CPU 核心: 6
     内存: 16GB
  使用指定的 Chrome 版本: 121
  正在初始化浏览器...
  🎭 注入指纹混淆脚本...
  ✅ 指纹混淆脚本注入成功
  ✅ 浏览器启动成功
```

### 禁用指纹随机化时

```
启动 Undetected Chrome (无头模式)...
  检测到 Chrome: C:\Program Files\Google\Chrome\Application\chrome.exe
  初始化 undetected-chromedriver...
  使用指定的 Chrome 版本: 121
  正在初始化浏览器...
  ✅ 浏览器启动成功
```

## 技术细节

### 1. Chrome 启动参数随机化

```python
options.add_argument(f'--window-size={width},{height}')
options.add_argument(f'--user-agent={user_agent}')
options.add_argument(f'--lang={language}')
options.add_argument('--disable-webrtc')
```

### 2. CDP 脚本注入

使用 Chrome DevTools Protocol 在页面加载前注入混淆脚本：

```python
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': fingerprint.get_all_scripts()
})
```

### 3. Canvas 指纹混淆

在 Canvas 输出时添加微小的随机噪声（人眼不可见）：

```javascript
const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
for (let i = 0; i < imageData.data.length; i += 4) {
    const noise = Math.floor(Math.random() * 3) - 1;
    imageData.data[i] += noise;  // RGB 值微调
}
```

### 4. WebGL 指纹混淆

随机化 GPU 渲染器信息：

```javascript
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    if (parameter === 37446) {  // UNMASKED_RENDERER_WEBGL
        return renderers[Math.floor(Math.random() * renderers.length)];
    }
    return originalGetParameter.apply(this, arguments);
};
```

## 注意事项

### 1. 资源消耗

指纹随机化本身不会增加明显的资源消耗。

### 2. 成功率影响

- **启用指纹随机化**：可以显著提高批量注册的成功率
- **禁用指纹随机化**：同一设备多次注册容易被识别

### 3. 与其他措施配合

指纹随机化应该配合以下措施使用：

- ✅ 修改机器码（系统级别）
- ✅ 使用代理 IP（网络级别）
- ✅ 控制注册频率（行为级别）
- ✅ 随机化操作行为（输入速度、停留时间等）

## 常见问题

### Q: 指纹随机化会影响浏览器性能吗？

A: 不会。只是修改了一些参数和注入了轻量级的 JavaScript 代码。

### Q: 每次注册都会生成不同的指纹吗？

A: 是的。每次启动浏览器都会生成全新的随机指纹。

### Q: 可以自定义指纹参数吗？

A: 可以。修改 `fingerprint_randomizer.py` 中的列表即可。

### Q: 指纹随机化能保证 100% 不被检测吗？

A: 不能。但可以大幅降低被识别的概率。建议配合其他反检测措施使用。

## 扩展阅读

- [浏览器指纹识别技术](https://en.wikipedia.org/wiki/Device_fingerprint)
- [Canvas Fingerprinting](https://browserleaks.com/canvas)
- [WebGL Fingerprinting](https://browserleaks.com/webgl)
