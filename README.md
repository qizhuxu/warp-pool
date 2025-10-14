# Warp 自动注册工具 - Undetected-Chromedriver 版本

使用 Undetected-Chromedriver 绕过反机器人检测的 Warp 账号自动注册工具。

## 特点

- ✅ 使用 Undetected-Chromedriver（专门绕过检测）
- ✅ 自动创建临时邮箱
- ✅ 自动发送注册请求
- ✅ 自动接收验证邮件
- ✅ 自动完成账号激活
- ✅ 更高的成功率

## 安装

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境
copy .env.example .env
# 编辑 .env 文件，填入邮箱服务 API Key
```

## 配置

编辑 `.env` 文件：

```env
# 临时邮箱服务配置
MOEMAIL_URL=https://email.959585.xyz
MOEMAIL_API_KEY=your_api_key

# Firebase API Key
FIREBASE_API_KEY=AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs

# 浏览器配置
HEADLESS=false  # true=后台运行，false=显示浏览器窗口

# Chrome 版本配置（可选）
# 如果本地使用 Chrome 121，取消注释此行
# CHROME_VERSION=121

# 代理配置（可选，强烈推荐）
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

## 使用

### 首次运行前：环境检查（推荐）

```bash
# 运行环境检查脚本
python check_env.py
```

这会检查：
- ✅ Chrome 是否已安装
- ✅ Python 依赖是否完整
- ✅ .env 配置是否正确
- ✅ 网络连接是否正常
- ✅ ChromeDriver 缓存状态

### 注册单个账号

```bash
# 显示浏览器窗口（推荐）
python register.py

# 后台运行
python register.py --headless true
```

**注意**: 首次运行会自动下载 ChromeDriver，可能需要 30-60 秒，请耐心等待。

## 优势对比

| 特性 | Playwright | Undetected-Chromedriver |
|------|-----------|------------------------|
| 反检测能力 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 易用性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 性能 | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 成功率 | 70-80% | 80-95% |

## 工作流程

1. 创建临时邮箱
2. 启动 Undetected Chrome
3. 访问 Warp 登录页面
4. 输入邮箱并发送
5. 等待验证邮件
6. 提取验证链接
7. 访问验证链接完成激活
8. 获取 Token

## 提高成功率

1. **使用高质量代理**（最重要）
   - 住宅代理 > 数据中心代理
   - 配置在 .env 文件中

2. **降低注册频率**
   - 每次注册间隔 30-60 分钟
   - 避免短时间内大量注册

3. **更换邮箱服务**
   - 使用不同的临时邮箱服务
   - 或使用真实邮箱

## 常见问题

### Q: 启动时卡住不动？
A: 
1. **首次运行**: 正在下载 ChromeDriver，需要 30-60 秒，请耐心等待
2. **网络问题**: 检查网络连接，可能需要配置代理
3. **防火墙**: 确保防火墙允许下载
4. **手动检查**: 运行 `python check_env.py` 诊断问题

### Q: 如何确认是否在下载？
A: 
- 查看网络流量（任务管理器 → 性能 → 网络）
- 检查缓存目录: `%USERPROFILE%\.undetected_chromedriver` (Windows)
- 等待 2-3 分钟，如果还是卡住，按 Ctrl+C 终止并重试

### Q: 为什么选择 Undetected-Chromedriver？
A: 它专门为绕过反机器人检测设计，成功率更高。

### Q: 需要手动安装 Chrome 吗？
A: 需要！请先安装 Google Chrome 浏览器。

### Q: 还是被检测怎么办？
A: 
1. 确保使用高质量代理
2. 降低注册频率
3. 更换邮箱服务
4. 等待一段时间（冷却期）

### Q: ChromeDriver 下载失败？
A: 
1. 检查网络连接
2. 配置代理: 在 .env 中设置 HTTP_PROXY
3. 手动下载: 访问 https://chromedriver.chromium.org/
4. 清理缓存后重试

## 许可证

MIT License
