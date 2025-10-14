# Chrome 版本配置说明

## 概述

代码支持两种模式：
1. **指定版本模式**（本地测试）：通过环境变量指定 Chrome 版本
2. **自动检测模式**（GitHub Actions）：自动检测并匹配 Chrome 版本

## 配置方法

### 本地测试（使用 Chrome 121）

在 `.env` 文件中添加：
```env
CHROME_VERSION=121
```

### GitHub Actions（自动检测）

不需要配置，工作流会自动检测 Chrome 版本。

## 工作原理

### 代码逻辑（uc_activator.py）

```python
chrome_version_env = os.environ.get('CHROME_VERSION')

if chrome_version_env:
    # 指定版本（本地测试）
    version_main = int(chrome_version_env)
    driver = uc.Chrome(options=options, version_main=version_main, ...)
else:
    # 自动检测版本（GitHub Actions）
    driver = uc.Chrome(options=options, ...)
```

### 版本匹配流程

```
1. 读取环境变量 CHROME_VERSION
   ├─ 有值 → 使用指定版本
   └─ 无值 → 自动检测

2. undetected-chromedriver 下载对应的 ChromeDriver
   ├─ 指定版本 → 下载 ChromeDriver {version}
   └─ 自动检测 → 检测系统 Chrome → 下载匹配的 ChromeDriver

3. 启动浏览器
```

## 常见问题

### Q: 为什么本地需要指定版本？
A: 本地可能使用特定版本的 Chrome（如 121），指定版本可以确保 ChromeDriver 匹配。

### Q: GitHub Actions 为什么不需要指定？
A: GitHub Actions 每次都安装最新版 Chrome，自动检测可以确保始终匹配。

### Q: 如何查看我的 Chrome 版本？

**Windows**:
1. 打开 Chrome 浏览器
2. 点击右上角三个点 → 帮助 → 关于 Google Chrome
3. 查看版本号（如：121.0.6167.184）

**Linux/Mac**:
```bash
google-chrome --version
# 或
chrome --version
```

### Q: 版本不匹配会怎样？
A: 会出现错误：
```
This version of ChromeDriver only supports Chrome version X
Current browser version is Y
```

### Q: 如何解决版本不匹配？
A: 
1. **本地**: 在 `.env` 中设置正确的 `CHROME_VERSION`
2. **GitHub Actions**: 清理缓存，工作流会自动重新下载
3. **更新库**: `pip install -U undetected-chromedriver`

## 示例

### 本地测试配置

`.env` 文件：
```env
# 使用 Chrome 121
CHROME_VERSION=121
HEADLESS=false
```

运行：
```bash
python register.py
```

### GitHub Actions 配置

不需要额外配置，工作流自动处理：
```yaml
# 工作流会：
1. 安装最新版 Chrome
2. 清理 ChromeDriver 缓存
3. 预下载匹配的 ChromeDriver
4. 运行注册脚本（自动检测版本）
```

## 调试

### 查看使用的版本

运行脚本时会显示：
```
启动 Undetected Chrome (无头模式)...
  检测到 Chrome: Google Chrome 121.0.6167.184
  使用指定的 Chrome 版本: 121
  初始化 undetected-chromedriver...
  ✅ 浏览器启动成功
```

或：
```
启动 Undetected Chrome (无头模式)...
  检测到 Chrome: Google Chrome 141.0.7390.76
  自动检测 Chrome 版本
  初始化 undetected-chromedriver...
  ✅ 浏览器启动成功
```

### 强制重新下载 ChromeDriver

**Windows (PowerShell)**:
```powershell
# 清理缓存
Remove-Item -Recurse -Force "$env:USERPROFILE\.undetected_chromedriver" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:TEMP\.com.google.Chrome.*" -ErrorAction SilentlyContinue

# 重新运行
python register.py
```

**Linux/Mac**:
```bash
# 清理缓存
rm -rf ~/.undetected_chromedriver
rm -rf /tmp/.com.google.Chrome.*

# 重新运行
python register.py
```

## Windows 特别说明

### Chrome 版本检测

Windows 系统下，脚本会自动检测以下路径：
- `C:\Program Files\Google\Chrome\Application\chrome.exe`
- `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`

如果显示 "无法检测 Chrome 版本"，不影响使用，只是无法显示版本信息。

### 常见 Chrome 安装路径

- **标准安装**: `C:\Program Files\Google\Chrome\Application\`
- **32位系统**: `C:\Program Files (x86)\Google\Chrome\Application\`
- **用户安装**: `%LOCALAPPDATA%\Google\Chrome\Application\`

### 手动查看版本

1. 打开 Chrome
2. 地址栏输入: `chrome://version/`
3. 查看第一行的版本号

## 最佳实践

1. **本地开发**: 设置 `CHROME_VERSION` 匹配你的 Chrome 版本
2. **CI/CD**: 不设置 `CHROME_VERSION`，让系统自动检测
3. **版本升级**: Chrome 升级后，更新 `.env` 中的 `CHROME_VERSION`
4. **问题排查**: 查看日志中的版本信息，确认是否匹配
5. **Windows 用户**: 如果检测失败，手动在 `.env` 中设置 `CHROME_VERSION`
