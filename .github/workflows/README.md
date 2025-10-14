# GitHub Actions 自动注册工作流

## 📋 功能说明

`auto-register.yml` 工作流会自动执行 Warp 账号注册，并将生成的账号信息保存到仓库中。

## ⏰ 执行时间

- **自动执行**: 每 2 小时执行一次（UTC 时间）
- **手动触发**: 可在 GitHub Actions 页面手动运行

## 🔧 工作流程

1. **环境准备**
   - 检出代码仓库
   - 安装 Python 3.11
   - 安装 Chrome 浏览器及依赖
   - 安装 Python 依赖包

2. **执行注册**
   - 运行 `warp-pool/register.py --headless true`
   - 使用无头模式（后台运行）
   - 生成账号 JSON 文件到 `warp-pool/accounts/` 目录

3. **保存结果**
   - 自动提交新生成的账号文件
   - 上传日志和截图作为 Artifacts
   - 生成执行摘要报告

## 📦 输出文件

### 提交到仓库
- `warp-pool/accounts/account_YYYYMMDD_HHMMSS.json` - 账号信息

### Artifacts（保留 30 天）
- 账号 JSON 文件
- 注册日志 `registration.log`
- 调试截图（如果有）

## 🚀 手动触发

1. 进入仓库的 **Actions** 页面
2. 选择 **Auto Register Warp Account** 工作流
3. 点击 **Run workflow** 按钮
4. 选择分支并点击 **Run workflow**

## 📊 查看结果

### 方法 1: 查看提交历史
```bash
git log --oneline --grep="Auto-register"
```

### 方法 2: 查看 Actions 摘要
在 Actions 运行详情页面查看 Summary，包含：
- 注册状态（成功/失败）
- 总账号数量
- 最新账号信息

### 方法 3: 下载 Artifacts
在 Actions 运行详情页面下载 `registration-run-*` 文件

## 🔐 环境配置

工作流使用仓库中的 `.env` 文件，需要包含：

```env
# 临时邮箱服务配置
MOEMAIL_URL=https://email.959585.xyz
MOEMAIL_API_KEY=your_api_key

# Firebase API Key
FIREBASE_API_KEY=AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs

# 浏览器配置
HEADLESS=true

# 代理配置（可选）
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
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
2. 下载 Artifacts 查看 `registration.log`
3. 检查 `.env` 配置是否正确
4. 检查 `debug/` 目录中的截图

### Chrome 版本配置
- **本地测试**: 在 `.env` 文件中设置 `CHROME_VERSION=121`（如果使用 Chrome 121）
- **GitHub Actions**: 自动检测 Chrome 版本，无需配置
- `undetected-chromedriver` 会自动下载匹配的 ChromeDriver

如果出现版本问题：
1. 本地测试：在 `.env` 中设置 `CHROME_VERSION` 为你的 Chrome 主版本号
2. GitHub Actions：工作流会自动处理版本匹配
3. 更新 `undetected-chromedriver` 到最新版本：`pip install -U undetected-chromedriver`

### 账号被封
- 降低执行频率（改为每 4-6 小时）
- 使用代理服务器
- 更换临时邮箱服务

## 📈 监控建议

1. **定期检查**: 每周查看一次 Actions 执行情况
2. **账号统计**: 定期统计 `warp-pool/accounts/` 目录中的账号数量
3. **成功率**: 关注 Actions 的成功/失败比例

## 🔒 安全注意事项

- ✅ 私有仓库：`.env` 文件可以直接提交
- ✅ 账号文件：包含敏感信息，确保仓库为私有
- ⚠️ 不要将仓库设为公开，避免泄露账号信息
- ⚠️ 定期清理过期或无效的账号

## 📝 提交信息格式

工作流会自动生成详细的提交信息：

```
🤖 Auto-register: New account example@959585.xyz

📊 Total accounts: 42
⏰ Time: 2025-10-12 14:30:00 UTC
🔗 Run: https://github.com/user/repo/actions/runs/12345
```

## 🎯 最佳实践

1. **首次运行**: 手动触发测试，确保配置正确
2. **监控频率**: 前几天密切关注，确保稳定运行
3. **备份账号**: 定期备份 `accounts/` 目录
4. **清理日志**: Artifacts 会自动保留 30 天后删除
5. **调整策略**: 根据成功率调整执行频率和配置
