# Warp 自动注册工具 - Undetected-Chromedriver 版本

使用 Undetected-Chromedriver 绕过反机器人检测的 Warp 账号自动注册工具。

## 特点

- ✅ 使用 Undetected-Chromedriver（专门绕过检测）
- ✅ 支持多种临时邮箱服务（MoeMail / Skymail，均需自建）
- ✅ 自动发送注册请求
- ✅ 自动接收验证邮件
- ✅ 自动完成账号激活
- ✅ 更高的成功率（90-98%）
- ✅ GitHub Actions 自动化（每小时自动注册）

## 安装

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境
copy .env.example .env
# 编辑 .env 文件，填入邮箱服务 API Key
```

## 配置

推荐先复制示例配置文件并填入私有值：

```powershell
copy .env.example .env
# 或 (Linux/macOS)
cp .env.example .env
```

下面是可用的环境变量及说明（同时参考 `config.example.py`）：

```env
# ------------------ 邮箱服务 ------------------
# 邮箱服务类型：moemail（默认）、skymail 或 auto（自动随机选择）
EMAIL_SERVICE=moemail

# MoeMail 配置（需自建）
# 项目地址：https://github.com/beilunyang/moemail
MOEMAIL_URL=https://email.959585.xyz
MOEMAIL_API_KEY=your_api_key_here

# Skymail (Cloud Mail) 配置（备用，需自建）
# 项目地址：https://github.com/eoao/cloud-mail
# Token 获取：https://doc.skymail.ink/api/api-doc.html#生成token
SKYMAIL_URL=https://cloudmail.qixc.pp.ua
SKYMAIL_TOKEN=your_token_here
# 支持多域名（逗号分隔，随机选择）
SKYMAIL_DOMAIN=example.com,domain2.com,domain3.com
SKYMAIL_WILDCARD=false  # 通配符模式（无需注册）

# ------------------ Firebase ------------------
FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY     # Firebase API Key（如果使用相关功能）

# ------------------ Warp / 页面 ------------------
WARP_LOGIN_URL=https://app.warp.dev/login  # Warp 登录页面 URL（通常不需修改）

# ------------------ 浏览器 & 指纹 ------------------
HEADLESS=false                             # true=无头模式 (后台)；false=可视化
CHROME_BINARY_PATH=                         # 可选：Chrome 可执行文件绝对路径
CHROMEDRIVER_PATH=                          # 可选：ChromeDriver 可执行文件路径

FINGERPRINT_RANDOMIZE=true                  # 指纹随机化总开关（true/false）
FINGERPRINT_LEVEL=balanced                  # basic | balanced | aggressive
ENHANCED_PROFILES_ENABLED=true              # 是否使用增强配置文件
STRICT_CONSISTENCY_CHECK=true               # 是否启用严格一致性校验
FINGERPRINT_DEBUG=false                     # 是否输出指纹调试信息

# ------------------ 超时 & 批量 ------------------
EMAIL_TIMEOUT=120                           # 等待邮件的超时（秒）
REGISTER_COUNT=1                            # 每次运行注册账号数量
REGISTER_INTERVAL=5                         # 注册间隔（秒）

# ------------------ 代理（可选） ------------------
# 使用 HTTP/HTTPS 代理（大多数工具支持）
# 例如：HTTP_PROXY=http://127.0.0.1:7890
# Windows PowerShell 临时设置示例：
# $env:HTTP_PROXY = 'http://127.0.0.1:7890'
```

## 使用

### 首次运行前：环境检查（推荐）

```bash
# 运行环境检查脚本
python test\check_env.py
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

### 批量注册账号 🆕

使用 `batch_register.py` 可以批量注册到指定数量：

```bash
# 查看当前账号数量
python batch_register.py --count

# 注册到总共 20 个账号
python batch_register.py --target 20

# 增加 5 个账号（在当前基础上）
python batch_register.py --add 5

# 批量注册，使用无头模式
python batch_register.py --add 10 --headless true

# 列出所有账号信息
python batch_register.py --list
```

**批量注册特性**：
- ✅ 自动统计现有账号数量
- ✅ 失败后自动重试（默认最多连续失败 3 次）
- ✅ 连续失败 2 次自动重置环境（清理机器码）
- ✅ 实时显示进度和统计信息
- ✅ 支持随时中断（Ctrl+C）
- ✅ 智能间隔控制（避免频率过高）

**详细说明**: 查看 [BATCH_REGISTER.md](BATCH_REGISTER.md)

---

## GitHub Actions 自动化 🤖

本项目支持通过 GitHub Actions 实现全自动注册，无需本地运行。

### 功能特性

- ⏰ **定时执行**：每小时自动运行一次
- 📦 **累计模式**：每次增加 6 个账号，自动累计
- 🔄 **机器码随机化**：每次运行自动生成新的设备标识
- 📥 **Release 发布**：账号数据通过 GitHub Release 发布
- 🧹 **自动清理**：7 天前的旧数据自动删除

### 快速开始

#### 1. 配置 Secrets

进入仓库 **Settings** → **Secrets and variables** → **Actions**，添加：

| Secret 名称 | 必需性 | 说明 | 获取方式 |
|------------|--------|------|---------|
| `FIREBASE_API_KEY` | ✅ 必需 | Firebase API Key | `AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs` |
| `MOEMAIL_URL` | ⚠️ 可选 | MoeMail 服务 URL | `https://email.959585.xyz` |
| `MOEMAIL_API_KEY` | ⚠️ 可选* | MoeMail API Key | 参考 [MoeMail](https://github.com/beilunyang/moemail) 项目 |
| `SKYMAIL_URL` | ⚠️ 可选 | Skymail 服务 URL | 参考 [Skymail](https://github.com/eoao/cloud-mail) 项目 |
| `SKYMAIL_TOKEN` | ⚠️ 可选* | Skymail 管理员 Token | 参考 [Token 获取](https://doc.skymail.ink/api/api-doc.html#生成token) |
| `SKYMAIL_DOMAIN` | ⚠️ 可选 | Skymail 域名列表 | `example.com,domain2.com` |

**注意**: 至少需要配置一个邮箱服务（MoeMail 或 Skymail）

**推荐配置两个服务（自动故障转移）**:
- 配置 `MOEMAIL_API_KEY` 和 `SKYMAIL_TOKEN`
- 工作流将自动使用 `auto` 模式
- 启动时健康检查，自动选择可用服务
- 运行时故障自动切换

**也可以只配置一个服务**:
- 只配置 `MOEMAIL_API_KEY` → 使用 MoeMail
- 只配置 `SKYMAIL_TOKEN` → 使用 Skymail

#### 2. 启用 Actions 权限

进入 **Settings** → **Actions** → **General**：
- 在 "Workflow permissions" 中选择 **"Read and write permissions"**
- 勾选 **"Allow GitHub Actions to create and approve pull requests"**

#### 3. 手动触发测试

进入 **Actions** 页面 → 选择 **"Auto Register Warp Account"** → 点击 **"Run workflow"**

**可选参数**（手动触发时可调整）：
- **注册账号数量**: 默认 6，可自定义
- **最大连续失败次数**: 默认 6，可自定义

#### 4. 下载账号数据

注册完成后，访问仓库的 **Releases** 页面：
- 找到对应日期的 release（如 `2025-10-15`）
- 下载 `all_accounts.json` 文件
- 查看 release 说明了解统计信息

### 工作流程

```
每小时触发
    ↓
随机化机器码和 hostname
    ↓
下载今天已有的账号数据
    ↓
批量注册 6 个新账号
    ↓
更新 all_accounts.json（累计）
    ↓
创建/更新 GitHub Release
    ↓
自动清理 7 天前的旧 releases
```

### 查看结果

**方法 1：Release 页面（推荐）**
- 访问仓库的 Releases 页面
- 下载对应日期的 `all_accounts.json`

**方法 2：Actions 日志**
- 查看执行日志了解详细过程
- 查看成功率和统计信息

**方法 3：Artifacts（调试用）**
- 下载 `debug-logs-*` 查看完整日志
- 查看截图（如果有错误）

### 自定义配置

#### 方法 1: 手动触发时调整参数（推荐）
在 Actions 页面手动触发时，可以直接调整：
- 注册账号数量（默认 6）
- 最大连续失败次数（默认 6）

#### 方法 2: 修改默认值（永久生效）
编辑 `.github/workflows/auto-register.yml` 文件顶部的配置区域：

```yaml
# ============================================
# 📝 配置区域 - 修改默认值请在此处修改
# ============================================
env:
  DEFAULT_REGISTER_COUNT: 10     # 改为默认 10 个
  DEFAULT_MAX_FAILS: 3            # 改为默认最多失败 3 次
```

#### 方法 3: 修改执行频率
编辑 `.github/workflows/auto-register.yml`：

```yaml
schedule:
  - cron: '0 */2 * * *'  # 改为每 2 小时
```

**详细说明**: 查看 [.github/workflows/README.md](.github/workflows/README.md)

---

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

## 工具脚本

### 重置 Warp 机器码

如果需要重置 Warp 的设备标识符（例如账号被封后重新开始）：

```bash
# Windows
python reset_warp.py

# Linux/macOS
python reset_warp.py
```

**功能**：
- 🗑️ 删除 Warp 注册表配置（Windows）
- 🗑️ 删除本地数据目录
- 🆕 生成新的设备标识符
- 🔄 重置为全新设备状态

**注意**：
- Windows 建议以管理员权限运行
- 操作前会要求确认
- 重置后 Warp 将识别为新设备

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

4. **定期重置机器码**
   - 使用 `reset_warp.py` 重置设备标识
   - 避免长期使用同一设备标识

## 常见问题

### Q: 启动时卡住不动？
A: 
1. **首次运行**: 正在下载 ChromeDriver，需要 30-60 秒，请耐心等待
2. **网络问题**: 检查网络连接，可能需要配置代理
3. **防火墙**: 确保防火墙允许下载
4. **手动检查**: 运行 `python test\check_env.py` 诊断问题

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

## 临时邮箱服务

本项目支持两种临时邮箱服务（均需自建）：

### MoeMail（默认）
- **项目地址**: https://github.com/beilunyang/moemail
- **配置**: 需要 API Key
- **优点**: 简单易用，API 稳定

### Skymail (Cloud Mail)
- **项目地址**: https://github.com/eoao/cloud-mail
- **文档**: https://doc.skymail.ink/
- **Token 获取**: https://doc.skymail.ink/api/api-doc.html#生成token
- **配置**: 需要管理员 Token
- **优点**: 功能完整，可自建部署，支持通配符邮箱（无需注册）

### 切换邮箱服务

编辑 `.env` 文件：
```env
# 使用 MoeMail
EMAIL_SERVICE=moemail

# 或使用 Skymail
EMAIL_SERVICE=skymail
```

## 文档

- [快速开始指南](docs/quick-start.md) - 3 分钟快速配置
- [浏览器指纹配置](docs/fingerprint-config-guide.md) - 详细的指纹配置说明
- [批量注册说明](docs/BATCH_REGISTER.md) - 批量注册功能详解
- [GitHub Actions 工作流](.github/workflows/README.md) - 自动化部署指南
- [文档中心](docs/README.md) - 完整文档导航

## 许可证

MIT License
