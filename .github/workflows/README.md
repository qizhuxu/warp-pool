# GitHub Actions 自动注册工作流

## 📋 功能说明

`auto-register.yml` 工作流会自动执行 Warp 账号批量注册，每次增加 6 个账号，并通过 **GitHub Release** 发布账号数据（按日期累计）。

## ⏰ 执行时间

- **自动执行**: 每 1 小时执行一次（UTC 时间）
- **手动触发**: 可在 GitHub Actions 页面手动运行

## 🔧 工作流程

1. **环境准备**
   - 检出代码仓库
   - 安装 Python 3.11
   - 随机化机器码（machine-id 和 hostname）
   - 完全卸载旧版 Chrome，安装最新版
   - 安装 Python 依赖包
   - 清理 ChromeDriver 缓存

2. **账号数据同步**
   - 下载今天已有的 `all_accounts.json`（如果存在）
   - 统计已有账号数量
   - 为累计注册做准备

3. **批量注册** 🆕
   - 运行 `batch_register.py --add 6 --headless true --max-fails 6`
   - 每次增加 6 个账号
   - 连续失败 2 次自动重置环境
   - 最多允许连续失败 6 次
   - 使用无头模式（后台运行）
   - 生成账号 JSON 文件到 `accounts/YYYY-MM-DD/` 目录

4. **发布到 Release**
   - 创建或更新当天的 GitHub Release（标签格式：`YYYY-MM-DD`）
   - 上传 `all_accounts.json`（包含当天所有账号，累计）
   - 生成详细的发布说明（统计信息、下载说明）
   - 自动清理 7 天前的旧 releases

## 📦 输出文件

### GitHub Release（推荐下载方式）
- **Release 标签**: `YYYY-MM-DD`（每天一个）
- **文件**: `all_accounts.json` - 当天所有账号的累计数据
- **保留期**: 自动清理 7 天前的 releases
- **下载**: 访问仓库的 Releases 页面下载

### Artifacts（调试用，保留 7 天）
- 注册日志 `registration.log`
- 调试截图 `debug/*.png`（如果有）

## 🚀 手动触发

1. 进入仓库的 **Actions** 页面
2. 选择 **Auto Register Warp Account** 工作流
3. 点击 **Run workflow** 按钮
4. 选择分支并点击 **Run workflow**

## 📊 查看和下载结果

### 方法 1: 下载 Release（推荐）
1. 访问仓库的 **Releases** 页面
2. 找到对应日期的 release（如 `2025-10-15`）
3. 下载 `all_accounts.json` 文件
4. 查看 release 说明了解统计信息

### 方法 2: 查看 Actions 日志
在 Actions 运行详情页面查看执行日志，包含：
- 注册进度和状态
- 新增账号数量
- 总账号数量
- 失败重试信息

### 方法 3: 下载 Artifacts（调试用）
在 Actions 运行详情页面下载 `debug-logs-*` 文件，包含：
- 完整注册日志
- 调试截图（如果有错误）

## 🔐 环境配置

工作流通过 **GitHub Secrets** 配置敏感信息，需要在仓库设置中添加：

### 必需的 Secrets
1. 进入仓库 **Settings** → **Secrets and variables** → **Actions**
2. 添加以下 secrets：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `MOEMAIL_API_KEY` | 临时邮箱服务 API Key | `your_api_key_here` |
| `FIREBASE_API_KEY` | Firebase API Key | `AIzaSy...` |

### 可选的 Secrets
| Secret 名称 | 说明 | 默认值 |
|------------|------|--------|
| `MOEMAIL_URL` | 临时邮箱服务 URL | `https://email.959585.xyz` |

### 自动配置的环境变量
工作流会自动创建 `.env` 文件，包含：
```env
MOEMAIL_URL=https://email.959585.xyz
MOEMAIL_API_KEY=<from secrets>
FIREBASE_API_KEY=<from secrets>
WARP_LOGIN_URL=https://app.warp.dev/referral/EWP6QD
HEADLESS=true
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=balanced
ENHANCED_PROFILES_ENABLED=true
STRICT_CONSISTENCY_CHECK=true
FINGERPRINT_DEBUG=false
EMAIL_TIMEOUT=120
REGISTER_COUNT=1
REGISTER_INTERVAL=5
```

## ⚙️ 自定义配置

### 修改执行频率

编辑 `.github/workflows/auto-register.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 */2 * * *'  # 每2小时
  # - cron: '0 */4 * * *'  # 每4小时
  # - cron: '0 0 * * *'    # 每天午夜
  # - cron: '0 0,12 * * *' # 每天 0:00 和 12:00
```

### 修改 Chrome 版本

如果需要特定版本的 Chrome，修改安装步骤：

```yaml
- name: Install Chrome and dependencies
  run: |
    # 下载特定版本
    wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_VERSION_amd64.deb
    sudo dpkg -i google-chrome-stable_VERSION_amd64.deb
```

## 🐛 故障排查

### 注册失败
1. 查看 Actions 日志了解详细错误
2. 下载 Artifacts 中的 `registration.log`
3. 检查 GitHub Secrets 配置是否正确
4. 查看 Artifacts 中的 `debug/*.png` 截图

### Secrets 未配置
如果看到错误 `❌ MOEMAIL_API_KEY 未配置`：
1. 进入仓库 Settings → Secrets and variables → Actions
2. 添加 `MOEMAIL_API_KEY` 和 `FIREBASE_API_KEY`
3. 重新运行工作流

### Chrome 版本问题
- 工作流会自动安装最新版 Chrome
- 自动清理旧版本和缓存
- `undetected-chromedriver` 会自动下载匹配的 ChromeDriver
- 如果仍有问题，检查 Actions 日志中的 Chrome 版本信息

### Release 创建失败
如果看到 `gh: command not found` 或权限错误：
1. 确保仓库启用了 Actions 写权限
2. 进入 Settings → Actions → General
3. 在 "Workflow permissions" 中选择 "Read and write permissions"

### 账号被封或成功率低
- 降低执行频率（改为每 2-4 小时）
- 检查是否触发了 Warp 的频率限制
- 等待冷却期（24-48 小时）

## 📈 监控建议

1. **定期检查**: 每周查看一次 Actions 执行情况
2. **账号统计**: 查看 Releases 页面，每个 release 说明中有统计信息
3. **成功率**: 关注 Actions 的成功/失败比例
4. **存储空间**: Releases 会自动清理 7 天前的数据，无需担心空间占用

## 🔒 安全注意事项

- ✅ 使用 GitHub Secrets 存储敏感信息（API Keys）
- ✅ 账号文件通过 Release 发布，包含敏感信息
- ⚠️ **确保仓库为私有**，避免泄露账号信息
- ⚠️ 不要在公开仓库中使用此工作流
- ⚠️ 定期检查 Secrets 是否泄露
- ✅ 旧数据自动清理（7 天），降低泄露风险

## 📝 Release 说明格式

工作流会自动生成详细的 Release 说明：

```markdown
# 📅 2025-10-15 账号数据

## 📊 统计信息
- ➕ 本次新增: **6** 个账号
- 📦 今日总计: **24** 个账号
- 📋 之前已有: **18** 个账号
- ⏰ 更新时间: 2025-10-15 14:30:00 UTC

## 📥 下载说明
下载 `all_accounts.json` 文件即可获取今日所有账号数据（累计）。

## 🔗 相关链接
- [查看工作流运行](...)
- [查看所有发布](...)
```

## 🎯 最佳实践

1. **首次运行**: 手动触发测试，确保 Secrets 配置正确
2. **监控频率**: 前几天密切关注，确保稳定运行
3. **备份账号**: 定期下载 Release 中的 `all_accounts.json` 备份
4. **清理策略**: 
   - Releases 自动保留 7 天
   - Artifacts 自动保留 7 天
   - 如需长期保存，请手动下载备份
5. **调整策略**: 根据成功率调整执行频率和配置
6. **权限设置**: 确保 Actions 有 "Read and write permissions"

## 💡 工作流特性

### 累计模式
- 每次运行会下载今天已有的账号数据
- 在现有基础上增加 6 个新账号
- 更新 Release 中的 `all_accounts.json`
- 同一天内多次运行会累计账号数量

### 自动清理
- 7 天前的 Releases 自动删除
- 避免占用过多存储空间
- 保持数据新鲜度

### 机器码随机化
- 每次运行自动生成新的 machine-id
- 随机化 hostname
- 清理缓存和临时文件
- 降低被识别为同一设备的风险
