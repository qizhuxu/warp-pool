# Warp 机器码重置工具

## 功能说明

`reset_warp.py` 用于重置 Warp 的设备标识符，删除所有本地配置和数据，使 Warp 将你的设备识别为全新设备。

## 使用场景

### 1. 账号被封后重新开始
如果你的账号因为某些原因被封禁，重置机器码可以让你重新注册。

### 2. 清理旧数据
清理 Warp 的所有本地数据和配置。

### 3. 测试不同配置
在测试不同指纹配置时，重置为干净状态。

## 使用方法

### Windows

```bash
# 普通运行
python reset_warp.py

# 以管理员权限运行（推荐）
# 右键 PowerShell -> 以管理员身份运行
python reset_warp.py
```

### Linux

```bash
python reset_warp.py
```

### macOS

```bash
python reset_warp.py
```

## 执行流程

### 1. 确认操作

```
============================================================
🔄 Warp 机器码重置工具
============================================================

[23:18:45] 检测到 Windows 系统

⚠️  此操作将:
  1. 删除 Warp 注册表配置
  2. 删除本地数据目录
  3. 生成新的设备标识符

确认继续? (yes/no):
```

输入 `yes` 或 `y` 确认。

### 2. 执行重置

```
[23:18:45] 开始软件初始化...
[23:18:45] 正在删除注册表项...
[23:18:45] 已删除: 注册表项Warp.dev\Warp
[23:18:45] 已删除: 注册表项Warp.dev
[23:18:45] 正在删除数据目录: C:\Users\qyk\AppData\Local\warp
[23:18:45] 数据目录已删除
[23:18:45] 已生成新的 ExperimentId: a1b2c3d4...
[23:18:45] 软件初始化成功完成

============================================================
✅ 重置完成！
============================================================

提示: 下次启动 Warp 时将被识别为新设备
```

## 重置内容

### Windows

1. **注册表项**：
   - `HKEY_CURRENT_USER\Software\Warp.dev\Warp`
   - `HKEY_CURRENT_USER\Software\Warp.dev`

2. **本地数据目录**：
   - `%LOCALAPPDATA%\warp`
   - 通常是 `C:\Users\{用户名}\AppData\Local\warp`

3. **设备标识符**：
   - 生成新的 `ExperimentId`（UUID 格式）

### Linux

1. **配置目录**：
   - `~/.config/warp`
   - `~/.local/share/warp`
   - `~/.cache/warp`

### macOS

1. **配置和缓存**：
   - `~/Library/Application Support/warp`
   - `~/Library/Preferences/dev.warp.Warp-Stable.plist`
   - `~/Library/Caches/warp`

## 注意事项

### 1. 数据备份 ⚠️

重置操作会**永久删除**所有 Warp 本地数据，包括：
- 配置文件
- 缓存数据
- 设备标识符

**建议**：如果需要保留某些数据，请先备份。

### 2. 管理员权限（Windows）

虽然不是必需的，但建议以管理员权限运行以确保：
- 完全删除注册表项
- 删除所有受保护的文件
- 避免权限错误

### 3. 关闭 Warp

在运行重置脚本前，请确保：
- ✅ 关闭 Warp 应用程序
- ✅ 关闭所有 Warp 相关进程

### 4. 重置后的效果

重置后：
- ✅ Warp 将你识别为新设备
- ✅ 可以重新注册账号
- ✅ 之前的设备限制被清除
- ⚠️ 需要重新配置所有设置

## 使用示例

### 场景 1：账号被封后重新注册

```bash
# 1. 重置机器码
python reset_warp.py
# 输入 yes 确认

# 2. 等待几分钟

# 3. 重新注册
python register.py
```

### 场景 2：批量注册前清理

```bash
# 1. 重置机器码
python reset_warp.py

# 2. 批量注册
python batch_register.py --add 10
```

### 场景 3：定期维护

```bash
# 每注册 50 个账号后重置一次
python batch_register.py --add 50
python reset_warp.py
python batch_register.py --add 50
```

## 故障排查

### 问题 1：权限不足

**错误信息**：
```
⚠️ 删除注册表项失败: Access is denied
```

**解决方案**：
- 以管理员权限运行 PowerShell
- 右键 PowerShell → 以管理员身份运行

### 问题 2：文件被占用

**错误信息**：
```
⚠️ 删除数据目录失败: The process cannot access the file
```

**解决方案**：
1. 关闭 Warp 应用程序
2. 打开任务管理器，结束所有 Warp 进程
3. 重新运行脚本

### 问题 3：目录不存在

**日志信息**：
```
[23:18:45] 数据目录不存在，跳过
```

**说明**：
- 这是正常的，表示 Warp 从未安装或已被清理
- 不影响重置流程

## 高级用法

### 仅删除注册表（Windows）

如果只想删除注册表而保留数据：

```python
import winreg

# 删除注册表项
try:
    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Warp.dev\Warp")
    print("已删除注册表项")
except:
    print("注册表项不存在")
```

### 仅删除数据目录

如果只想删除数据而保留注册表：

```python
import os
import shutil

# 删除数据目录
warp_dir = os.path.join(os.environ['LOCALAPPDATA'], 'warp')
if os.path.exists(warp_dir):
    shutil.rmtree(warp_dir)
    print("数据目录已删除")
```

### 批量重置（多台机器）

如果需要在多台机器上重置：

```bash
# 创建批处理脚本 reset_all.bat
@echo off
python reset_warp.py
pause
```

## 安全性

### 数据隐私

重置脚本会删除：
- ✅ 设备标识符（安全）
- ✅ 本地配置（安全）
- ✅ 缓存数据（安全）

**不会**：
- ❌ 上传任何数据
- ❌ 连接到外部服务器
- ❌ 修改系统关键设置

### 代码审查

脚本是开源的，你可以：
1. 查看源代码 `reset_warp.py`
2. 审查所有操作
3. 根据需要修改

## 最佳实践

### 1. 定期重置

```bash
# 建议每 50-100 个账号重置一次
python batch_register.py --add 50
python reset_warp.py
```

### 2. 配合代理使用

```bash
# 重置后更换代理
python reset_warp.py
# 修改 .env 中的代理配置
python register.py
```

### 3. 记录重置时间

```bash
# 创建日志
echo "Reset at $(date)" >> reset_log.txt
python reset_warp.py
```

## 常见问题

### Q: 重置后需要重启电脑吗？

A: 不需要，重置后立即生效。

### Q: 重置会影响其他软件吗？

A: 不会，只删除 Warp 相关的数据。

### Q: 可以撤销重置操作吗？

A: 不可以，删除的数据无法恢复。建议提前备份。

### Q: 重置后账号还在吗？

A: 账号信息保存在 `accounts/` 目录，不会被删除。

### Q: 多久重置一次比较好？

A: 建议每 50-100 个账号重置一次，或者发现成功率下降时重置。

## 相关工具

- `register.py` - 单个账号注册
- `batch_register.py` - 批量注册
- `test/check_env.py` - 环境检查

## 反馈

如果遇到问题或有改进建议，欢迎反馈！
