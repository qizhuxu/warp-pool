# Warp 自动注册工具 - Undetected-Chromedriver 版本

使用 Undetected-Chromedriver 绕过反机器人检测的 Warp 账号自动注册工具。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Success Rate](https://img.shields.io/badge/success%20rate-90--98%25-brightgreen.svg)](https://github.com/your-username/warp-register)

## 📑 目录

- [核心特性](#-核心特性)
- [快速开始](#-快速开始)
- [配置说明](#️-配置说明)
- [使用方法](#使用)
- [邮箱服务详解](#-邮箱服务详解)
- [GitHub Actions 自动化](#github-actions-自动化-)
- [代理配置](#代理配置中国大陆用户必读)
- [常见问题](#-常见问题)
- [性能优化建议](#-性能优化建议)
- [文档导航](#-文档导航)

## ✨ 核心特性

### 🎯 智能邮箱服务
- ✅ **零配置使用** - GPTMail 开箱即用，无需 API Key
- ✅ **Auto 模式** - 自动健康检查 + 智能服务选择
- ✅ **故障转移** - 服务失败自动切换备用服务
- ✅ **多服务支持** - MoeMail / Skymail / GPTMail

### 🎭 增强反检测
- ✅ **Undetected-Chromedriver** - 专业反检测浏览器驱动
- ✅ **3 级指纹系统** - basic (80-95%) / balanced (90-98%) / aggressive (92-99%)
- ✅ **真实配置文件** - NVIDIA/AMD GPU + 一致性验证
- ✅ **性能时序注入** - 模拟真实页面加载

### 🚀 自动化流程
- ✅ **全自动注册** - 邮箱创建 → 验证 → 激活 → Token 提取
- ✅ **批量注册** - 目标控制 + 进度追踪 + 自动重置
- ✅ **GitHub Actions** - 每小时自动注册，无需本地运行
- ✅ **高成功率** - 90-98% 注册成功率

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/warp-register.git
cd warp-register
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境（零配置可用）

**方式 1：零配置使用（推荐新手）**

```bash
copy .env.example .env
# 默认使用 Auto 模式，GPTMail 零配置可用
python register.py
```

**方式 2：自定义配置（推荐生产）**

```bash
copy .env.example .env
# 编辑 .env 文件，配置多个邮箱服务
```

```env
# 推荐：Auto 模式（自动选择最佳服务）
EMAIL_SERVICE=auto

# 可选：配置额外服务作为备用
MOEMAIL_API_KEY=your_api_key_here
SKYMAIL_TOKEN=your_token_here
# GPTMail 自动可用，无需配置
```

### 4. 运行注册

```bash
# 单账号注册
python register.py

# 批量注册到 10 个账号
python batch_register.py --target 10
```

## ⚙️ 配置说明

### 📧 邮箱服务配置

| 服务 | 配置难度 | 成功率 | 响应速度 | 配置项 |
|------|----------|--------|----------|--------|
| **GPTMail** | 🟢 零配置 | 95-98% | ~0.3s | 无需配置 |
| **MoeMail** | 🟡 需要 API Key | 90-95% | ~0.5s | `MOEMAIL_API_KEY` |
| **Skymail** | 🟡 需要 Token | 85-90% | ~0.8s | `SKYMAIL_TOKEN` |
| **Auto 模式** | 🟢 推荐 | 95-99% | 自适应 | `EMAIL_SERVICE=auto` |

**推荐配置：**

```env
# 方式 1：零配置（新手推荐）
EMAIL_SERVICE=auto
# GPTMail 自动可用

# 方式 2：多服务备份（生产推荐）
EMAIL_SERVICE=auto
MOEMAIL_API_KEY=your_key_here
SKYMAIL_TOKEN=your_token_here
# 自动健康检查 + 故障转移

# 方式 3：单一服务
EMAIL_SERVICE=gptmail    # 或 moemail / skymail
```

### 🎭 指纹随机化配置

| 级别 | 配置 | 成功率 | 特点 | 适用场景 |
|------|------|--------|------|----------|
| **basic** | `FINGERPRINT_LEVEL=basic` | 80-95% | Canvas + Navigator + Timezone | 快速测试 |
| **balanced** | `FINGERPRINT_LEVEL=balanced` | 90-98% | + WebGL + 性能时序 + 增强配置 | 生产环境 ⭐ |
| **aggressive** | `FINGERPRINT_LEVEL=aggressive` | 92-99% | + 音频上下文 | 最大隐蔽 |

**推荐配置：**

```env
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=balanced
ENHANCED_PROFILES_ENABLED=true
STRICT_CONSISTENCY_CHECK=true
```

### 🔧 完整环境变量

```env
# ========== 邮箱服务 ==========
EMAIL_SERVICE=auto                          # auto | gptmail | moemail | skymail

# GPTMail（零配置）
GPTMAIL_URL=https://mail.chatgpt.org.uk    # 默认值，通常不需修改

# MoeMail（需自建）
MOEMAIL_URL=https://email.959585.xyz
MOEMAIL_API_KEY=your_api_key_here

# Skymail（需自建）
SKYMAIL_URL=https://cloudmail.qixc.pp.ua
SKYMAIL_TOKEN=your_token_here
SKYMAIL_DOMAIN=example.com,domain2.com
SKYMAIL_WILDCARD=false

# ========== 浏览器 & 指纹 ==========
HEADLESS=false                              # true=后台运行 | false=显示窗口
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=balanced                  # basic | balanced | aggressive
ENHANCED_PROFILES_ENABLED=true
STRICT_CONSISTENCY_CHECK=true
FINGERPRINT_DEBUG=false

# ========== 超时 & 批量 ==========
EMAIL_TIMEOUT=120                           # 邮件等待超时（秒）
REGISTER_INTERVAL=5                         # 注册间隔（秒）

# ========== 代理（可选） ==========
# HTTP_PROXY=http://127.0.0.1:7890
# HTTPS_PROXY=http://127.0.0.1:7890
```

**详细说明：** 查看 `.env.example` 文件中的注释

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

## 🆚 技术对比

### Undetected-Chromedriver vs 其他方案

| 特性 | Playwright | Selenium | Undetected-Chromedriver |
|------|-----------|----------|------------------------|
| **反检测能力** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **易用性** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **性能** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **成功率** | 70-80% | 60-70% | 90-98% |
| **配置复杂度** | 中等 | 简单 | 简单 |
| **维护成本** | 低 | 中等 | 低 |

### 为什么选择 Undetected-Chromedriver？

✅ **专业反检测**
- 专门为绕过反机器人检测设计
- 自动处理 Chrome DevTools Protocol 特征
- 隐藏自动化标识符

✅ **高成功率**
- 基础配置：80-95%
- 增强指纹：90-98%
- Auto 模式：95-99%

✅ **简单易用**
- 自动下载 ChromeDriver
- 无需复杂配置
- 开箱即用

✅ **持续更新**
- 跟进 Chrome 版本更新
- 及时修复检测问题
- 活跃的社区支持

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

## 代理配置（中国大陆用户必读）

### 为什么需要代理？

本项目需要访问 Google Firebase API (`securetoken.googleapis.com`)，该服务在中国大陆被封锁，必须使用代理。

### 推荐配置：TUN 模式 ✅

**最简单、最稳定的方式**

1. 在代理软件中开启 TUN 模式：
   - **Clash**: Settings → TUN Mode → Enable
   - **V2Ray**: Preferences → Core → Enable TUN
   - **Shadowsocks**: 系统代理 → 全局模式

2. 直接运行程序，无需任何配置：
   ```bash
   python register.py
   ```

**优点：**
- ✅ 无需配置环境变量
- ✅ 所有网络流量自动代理
- ✅ 包括 DNS 查询
- ✅ 最稳定可靠

### 备选方案：系统代理模式（不推荐）

如果无法使用 TUN 模式，可以尝试系统代理：

```powershell
# Windows PowerShell
$env:HTTP_PROXY = 'http://127.0.0.1:10808'
$env:HTTPS_PROXY = 'http://127.0.0.1:10808'
$env:NO_PROXY = 'localhost,127.0.0.1,::1'

python register.py
```

**注意：**
- ⚠️ 可能出现连接超时
- ⚠️ DNS 解析可能失败
- ⚠️ 不如 TUN 模式稳定

### 海外用户

无需配置代理，直接运行即可。

---

## 提高成功率

1. **使用稳定的代理**（中国大陆用户必需）
   - 推荐使用 TUN 模式
   - 确保代理稳定可用
   - 避免频繁切换代理

2. **降低注册频率**
   - 每次注册间隔 30-60 分钟
   - 避免短时间内大量注册

3. **更换邮箱服务**
   - 使用不同的临时邮箱服务
   - 或使用真实邮箱

4. **定期重置机器码**
   - 使用 `reset_warp.py` 重置设备标识
   - 避免长期使用同一设备标识

## ❓ 常见问题

### 🔧 安装和配置

**Q: 启动时卡住不动？**

A: 
1. **首次运行** - 正在下载 ChromeDriver（30-60 秒），请耐心等待
2. **网络问题** - 检查网络连接，可能需要配置代理
3. **防火墙** - 确保防火墙允许下载
4. **诊断工具** - 运行 `python tests/check_env.py` 检查环境

**确认下载进度：**
- 查看网络流量（任务管理器 → 性能 → 网络）
- 检查缓存目录：`%USERPROFILE%\.undetected_chromedriver` (Windows)
- 等待 2-3 分钟，如果还是卡住，按 Ctrl+C 终止并重试

**Q: 需要手动安装 Chrome 吗？**

A: 是的！请先安装 [Google Chrome 浏览器](https://www.google.com/chrome/)

**Q: ChromeDriver 下载失败？**

A: 
```bash
# 1. 检查网络连接
python tests/check_env.py

# 2. 配置代理（如果需要）
# 编辑 .env 文件
HTTP_PROXY=http://127.0.0.1:7890

# 3. 清理缓存后重试
# Windows: 删除 %USERPROFILE%\.undetected_chromedriver
# Linux/Mac: 删除 ~/.undetected_chromedriver
```

### 📧 邮箱服务

**Q: 邮箱服务不可用怎么办？**

A: 
```bash
# 使用 Auto 模式（推荐）
EMAIL_SERVICE=auto

# 测试服务可用性
python tests/test_gptmail.py
python tests/test_auto_failover.py
```

**Q: 验证邮件收不到？**

A:
- ✅ 使用 Auto 模式会自动切换服务
- ✅ GPTMail 通常最稳定（95-98% 成功率）
- ✅ 增加等待时间：`EMAIL_TIMEOUT=180`
- ✅ 检查邮箱服务状态

**Q: 如何配置多个邮箱服务？**

A:
```env
EMAIL_SERVICE=auto

# 配置所有服务作为备用
MOEMAIL_API_KEY=your_key
SKYMAIL_TOKEN=your_token
# GPTMail 自动可用
```

### 🎭 反检测和成功率

**Q: 为什么选择 Undetected-Chromedriver？**

A: 它专门为绕过反机器人检测设计，成功率比普通 Selenium 高 20-30%

**Q: 注册成功率低怎么办？**

A:
```bash
# 1. 使用推荐配置
FINGERPRINT_LEVEL=balanced
ENHANCED_PROFILES_ENABLED=true
EMAIL_SERVICE=auto

# 2. 重置环境
python reset_warp.py

# 3. 降低注册频率
# 每次注册间隔 30-60 分钟
```

**Q: 还是被检测怎么办？**

A:
1. ✅ 确保使用高质量代理（中国用户必需）
2. ✅ 降低注册频率（避免短时间大量注册）
3. ✅ 使用 Auto 模式切换邮箱服务
4. ✅ 重置环境：`python reset_warp.py`
5. ✅ 等待冷却期（24 小时）

**Q: 指纹随机化有什么用？**

A: 
- 模拟真实浏览器特征
- 避免被识别为自动化工具
- 提高注册成功率 20-30%

### 🌐 代理配置

**Q: 中国用户必须使用代理吗？**

A: 是的！Firebase API 在中国被封锁，必须使用代理

**推荐配置：**
```bash
# 方式 1：TUN 模式（推荐）
# 在代理软件中开启 TUN 模式
# 无需配置环境变量

# 方式 2：系统代理（备选）
$env:HTTP_PROXY = 'http://127.0.0.1:7890'
$env:HTTPS_PROXY = 'http://127.0.0.1:7890'
```

**Q: 使用代理后还是连接失败？**

A:
- ✅ 使用 TUN 模式代替系统代理
- ✅ 确保代理稳定可用
- ✅ 避免频繁切换代理
- ✅ 检查 DNS 解析

### 🔄 批量注册

**Q: 批量注册失败率高？**

A:
```bash
# 系统会自动处理：
# - 连续失败 2 次自动重置环境
# - 自动切换邮箱服务
# - 智能间隔控制

# 手动优化：
python batch_register.py --target 10 --headless true
```

**Q: 如何查看注册进度？**

A:
```bash
# 查看当前账号数量
python batch_register.py --count

# 列出所有账号
python batch_register.py --list

# 查看详细日志
# 日志文件在 accounts/YYYY-MM-DD/ 目录
```

### 🐛 调试和测试

**Q: 如何启用调试模式？**

A:
```bash
# 显示浏览器窗口
HEADLESS=false python register.py

# 启用指纹调试
FINGERPRINT_DEBUG=true python register.py

# 检查环境
python tests/check_env.py
```

**Q: 如何测试功能？**

A:
```bash
# 测试邮箱服务
python tests/test_gptmail.py
python tests/test_auto_failover.py

# 测试指纹随机化
python tests/test_fingerprint.py
python tests/test_enhanced_fingerprint.py

# 测试环境清理
python tests/test_cleanup.py
```

## 📧 邮箱服务详解

### 🎯 Auto 模式（强烈推荐）

**零配置使用：**
```env
EMAIL_SERVICE=auto  # 自动选择最佳服务
```

**工作原理：**
1. ✅ 启动时健康检查所有服务
2. ✅ 随机选择可用服务（负载均衡）
3. ✅ 服务失败自动切换备用
4. ✅ 失败计数管理（连续失败 3 次临时排除）

**优势：**
- 🚀 最高成功率（95-99%）
- 🔄 自动故障转移
- ⚖️ 负载均衡
- 🛡️ 容错能力强

### 📨 支持的邮箱服务

#### 1. GPTMail（零配置推荐）

**服务地址：** https://mail.chatgpt.org.uk

**特点：**
- 🟢 **零配置** - 无需 API Key，开箱即用
- 🌐 **Cloudflare CDN** - 全球加速，高可用
- 📱 **多域名** - 自动分配多个域名
- ⚡ **快速响应** - ~0.3 秒创建邮箱
- 🔒 **1 天保留** - 邮件保留 24 小时
- 📊 **高成功率** - 95-98%

**使用方式：**
```env
EMAIL_SERVICE=gptmail  # 或使用 auto 模式
```

#### 2. MoeMail（自建推荐）

**项目地址：** https://github.com/beilunyang/moemail

**特点：**
- 🔧 **开源项目** - 可自建部署
- 🔑 **需要 API Key** - 需要配置
- 📡 **API 稳定** - 成熟的 API 接口
- 📊 **成功率** - 90-95%

**配置方式：**
```env
EMAIL_SERVICE=moemail
MOEMAIL_URL=https://your-instance.com
MOEMAIL_API_KEY=your_api_key_here
```

**部署方式：**
1. 自建服务器部署
2. 使用公开实例（不保证稳定性）

#### 3. Skymail（多域名）

**项目地址：** https://github.com/eoao/cloud-mail  
**文档：** https://doc.skymail.ink/  
**Token 获取：** https://doc.skymail.ink/api/api-doc.html#生成token

**特点：**
- 🌐 **多域名支持** - 支持多个域名
- 🔀 **通配符模式** - 无需注册邮箱
- 📚 **文档完善** - 详细的 API 文档
- 📊 **成功率** - 85-90%

**配置方式：**
```env
EMAIL_SERVICE=skymail
SKYMAIL_URL=https://your-instance.com
SKYMAIL_TOKEN=your_token_here
SKYMAIL_DOMAIN=example.com,domain2.com
SKYMAIL_WILDCARD=true  # 启用通配符模式
```

### 🔄 服务切换策略

**推荐配置（最高成功率）：**
```env
EMAIL_SERVICE=auto

# 配置所有服务作为备用
MOEMAIL_API_KEY=your_key
SKYMAIL_TOKEN=your_token
# GPTMail 自动可用
```

**单一服务配置：**
```env
# 零配置
EMAIL_SERVICE=gptmail

# 或自建服务
EMAIL_SERVICE=moemail
MOEMAIL_API_KEY=your_key

# 或多域名服务
EMAIL_SERVICE=skymail
SKYMAIL_TOKEN=your_token
```

### 🧪 测试邮箱服务

```bash
# 测试 GPTMail
python tests/test_gptmail.py

# 测试 Auto 模式
python tests/test_auto_failover.py

# 测试 Skymail
python tests/test_skymail.py
```

## 📚 文档导航

### 🚀 快速入门
- [快速开始指南](docs/quick-start.md) - 3 分钟快速配置
- [环境检查工具](tests/check_env.py) - 一键诊断环境问题

### 📖 功能文档
- [邮箱服务更新](docs/EMAIL_SERVICE_UPDATE.md) - GPTMail + Auto 模式详解
- [批量注册说明](docs/BATCH_REGISTER.md) - 批量注册功能详解
- [浏览器指纹配置](docs/fingerprint-config-guide.md) - 指纹随机化详细说明
- [GitHub Actions 工作流](.github/workflows/README.md) - 自动化部署指南

### 🧪 测试脚本
- `tests/check_env.py` - 环境检查
- `tests/test_gptmail.py` - GPTMail 功能测试
- `tests/test_auto_failover.py` - Auto 模式测试
- `tests/test_fingerprint.py` - 指纹随机化测试
- `tests/test_enhanced_fingerprint.py` - 增强指纹测试

### 📋 完整文档
- [文档中心](docs/README.md) - 完整文档导航

## 📈 性能优化建议

### 🎯 最佳配置组合

**高成功率配置（推荐）：**
```env
# 邮箱服务
EMAIL_SERVICE=auto
MOEMAIL_API_KEY=your_key      # 可选
SKYMAIL_TOKEN=your_token      # 可选
# GPTMail 自动可用

# 指纹随机化
FINGERPRINT_LEVEL=balanced
ENHANCED_PROFILES_ENABLED=true
STRICT_CONSISTENCY_CHECK=true

# 其他
HEADLESS=true
EMAIL_TIMEOUT=120
```

**成功率对比：**
| 配置 | 成功率 | 说明 |
|------|--------|------|
| 单一服务 + basic 指纹 | 75-85% | 基础配置 |
| 单一服务 + balanced 指纹 | 85-95% | 标准配置 |
| Auto 模式 + balanced 指纹 | 90-98% | 推荐配置 ⭐ |
| Auto 多服务 + aggressive 指纹 | 95-99% | 最佳配置 |

### 🚀 提高成功率技巧

1. **使用 Auto 模式**
   - 自动健康检查
   - 智能服务选择
   - 自动故障转移

2. **配置多个邮箱服务**
   - 提供备用选项
   - 负载均衡
   - 容错能力强

3. **使用 balanced 指纹级别**
   - 平衡性能和隐蔽性
   - 90-98% 成功率
   - 生产环境推荐

4. **定期重置环境**
   - 避免设备标识被封
   - 保持"新设备"状态
   - 使用 `reset_warp.py`

5. **控制注册频率**
   - 每次间隔 30-60 分钟
   - 避免短时间大量注册
   - 使用批量注册的自动间隔

6. **使用稳定代理**（中国用户）
   - TUN 模式优先
   - 避免频繁切换
   - 确保 DNS 解析正常

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

### 运行测试

```bash
# 环境检查
python tests/check_env.py

# 功能测试
python tests/test_gptmail.py
python tests/test_auto_failover.py
python tests/test_fingerprint.py

# 完整测试套件
python -m pytest tests/
```

## 📊 更新日志

### v2.0.0 (2025-10-17)
- ✅ 新增 GPTMail 服务支持（零配置）
- ✅ 智能 Auto 模式（健康检查 + 故障转移）
- ✅ 增强指纹随机化（3 级别 + 真实配置）
- ✅ 批量注册优化（目标控制 + 自动重置）
- ✅ 完善测试套件
- ✅ 更新文档和配置

### v1.x.x
- ✅ 基础 Warp 注册功能
- ✅ MoeMail / Skymail 支持
- ✅ 基础指纹随机化
- ✅ GitHub Actions 自动化

## ⭐ 支持项目

如果这个项目对你有帮助，请给个 Star ⭐

### 相关项目

- [MoeMail](https://github.com/beilunyang/moemail) - 开源临时邮箱服务
- [Skymail](https://github.com/eoao/cloud-mail) - 多域名邮箱服务
- [Undetected ChromeDriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) - 反检测浏览器驱动

## 📄 许可证

MIT License

## ⚠️ 免责声明

本项目仅供学习和研究使用，请勿用于非法用途。使用本项目所产生的一切后果由使用者自行承担。

## 💬 联系方式

- 提交 Issue：[GitHub Issues](https://github.com/your-username/warp-register/issues)
- 讨论区：[GitHub Discussions](https://github.com/your-username/warp-register/discussions)
