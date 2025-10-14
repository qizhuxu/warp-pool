# 批量注册使用指南

## 功能说明

`batch_register.py` 是一个批量注册工具，可以自动注册 Warp 账号直到达到指定的目标数量。

## 主要特性

- ✅ 自动统计现有账号数量
- ✅ 注册到指定目标数量（自动计算需要注册的数量）
- ✅ 实时显示进度和统计信息
- ✅ 智能间隔控制（避免频率过高）
- ✅ 连续失败自动停止（默认 3 次）
- ✅ 支持随时中断（Ctrl+C）
- ✅ 详细的成功率统计

## 使用方法

### 1. 基本用法

```bash
# 注册到总共 10 个账号
python batch_register.py --target 10

# 如果当前已有 3 个账号，将自动注册 7 个
```

### 2. 使用无头模式

```bash
# 后台运行（推荐用于批量注册）
python batch_register.py --target 20 --headless true

# 显示浏览器窗口
python batch_register.py --target 20 --headless false
```

### 3. 调整失败容忍度

```bash
# 连续失败 5 次才停止（默认 3 次）
python batch_register.py --target 50 --max-fails 5
```

### 4. 查看账号信息

```bash
# 查看当前账号总数
python batch_register.py --count

# 列出所有账号详细信息
python batch_register.py --list
```

## 工作流程

1. **统计现有账号**：自动扫描 `accounts/` 目录
2. **计算需要数量**：目标数量 - 当前数量
3. **确认开始**：显示预估时间，等待用户确认
4. **循环注册**：
   - 调用 `register_single_account()` 注册单个账号
   - 每次注册后等待间隔时间（默认 5 秒）
   - 实时显示进度和统计
5. **智能停止**：
   - 达到目标数量
   - 连续失败达到上限
   - 用户手动中断（Ctrl+C）
6. **最终统计**：显示成功率、耗时等信息

## 输出示例

```
============================================================
🚀 Warp 批量注册工具
============================================================

📊 当前账号总数: 5
🎯 目标账号数量: 10
📝 需要注册: 5 个账号
⏱️  预计耗时: 15.0 分钟

============================================================
⚠️  注意事项:
  1. 建议间隔时间: 5 秒
  2. 连续失败 3 次将自动停止
  3. 可随时按 Ctrl+C 中断
============================================================

按 Enter 键开始批量注册...

============================================================
📌 进度: 1/5 (总账号: 6)
============================================================

🚀 开始注册 Warp 账号 (Undetected-Chromedriver)
...

✅ 注册成功！邮箱: test123@959585.xyz

============================================================
📊 批量注册统计
============================================================
📦 当前账号总数: 6
🎯 目标账号数量: 10
✅ 本次成功注册: 1
❌ 本次失败次数: 0
⏱️  已用时间: 180.5 秒 (3.0 分钟)
⚡ 平均每个账号: 180.5 秒
🕐 预计剩余时间: 12.0 分钟
============================================================

⏳ 等待 5 秒后继续...
```

## 配置说明

批量注册使用 `.env` 文件中的配置：

```env
# 注册间隔（秒）
REGISTER_INTERVAL=5

# 其他配置与单次注册相同
HEADLESS=true
FINGERPRINT_RANDOMIZE=true
...
```

## 注意事项

### 1. 频率控制 ⚠️

- **建议间隔**：5-15 秒
- **避免**：短时间内大量注册（可能被封 IP）
- **推荐**：分批次执行，每批 10-20 个

### 2. 成功率 📈

- **正常成功率**：80-95%
- **影响因素**：
  - 网络环境
  - IP 质量（代理）
  - 邮箱服务稳定性
  - 注册频率

### 3. 资源占用 💻

- **内存**：每个浏览器实例约 500MB
- **时间**：每个账号平均 2-5 分钟
- **建议**：
  - 10 个账号：约 30 分钟
  - 50 个账号：约 2.5 小时
  - 100 个账号：约 5 小时

### 4. 错误处理 🔧

- **连续失败**：默认 3 次后自动停止
- **可调整**：使用 `--max-fails` 参数
- **建议**：
  - 失败后检查网络和配置
  - 更换代理或邮箱服务
  - 降低注册频率

### 5. 中断恢复 🔄

- **随时中断**：按 Ctrl+C 安全停止
- **自动恢复**：下次运行会从当前数量继续
- **示例**：
  ```bash
  # 第一次：注册到 50 个（中断在 30 个）
  python batch_register.py --target 50
  # Ctrl+C 中断
  
  # 第二次：继续注册剩余的 20 个
  python batch_register.py --target 50
  ```

## 最佳实践

### 本地批量注册

```bash
# 1. 小批量测试（3-5 个）
python batch_register.py --target 5

# 2. 检查成功率
python batch_register.py --list

# 3. 逐步增加
python batch_register.py --target 10
python batch_register.py --target 20
python batch_register.py --target 50
```

### 使用代理

```bash
# 在 .env 中配置代理
HTTP_PROXY=http://127.0.0.1:7890

# 或临时设置（Windows PowerShell）
$env:HTTP_PROXY = 'http://127.0.0.1:7890'
python batch_register.py --target 20

# Linux/Mac
export HTTP_PROXY=http://127.0.0.1:7890
python batch_register.py --target 20
```

### 后台运行（Linux/Mac）

```bash
# 使用 nohup 后台运行
nohup python batch_register.py --target 100 --headless true > batch.log 2>&1 &

# 查看进度
tail -f batch.log

# 查看当前数量
python batch_register.py --count
```

## 故障排查

### 问题 1：连续失败

**可能原因**：
- 网络问题
- IP 被限制
- 邮箱服务不可用

**解决方案**：
```bash
# 1. 检查网络
ping app.warp.dev

# 2. 更换代理
# 修改 .env 中的 HTTP_PROXY

# 3. 检查邮箱服务
# 访问 MOEMAIL_URL 确认可用

# 4. 降低频率
# 修改 .env: REGISTER_INTERVAL=15
```

### 问题 2：成功率低

**可能原因**：
- 频率过高
- 指纹被识别

**解决方案**：
```bash
# 1. 增加间隔
REGISTER_INTERVAL=10

# 2. 调整指纹级别
FINGERPRINT_LEVEL=aggressive

# 3. 分批次执行
python batch_register.py --target 10  # 先注册 10 个
# 等待 1 小时
python batch_register.py --target 20  # 再注册 10 个
```

### 问题 3：内存不足

**解决方案**：
```bash
# 使用无头模式（节省内存）
python batch_register.py --target 50 --headless true

# 或分批次执行
python batch_register.py --target 10
python batch_register.py --target 20
python batch_register.py --target 30
```

## 与 GitHub Actions 集成

虽然批量注册主要用于本地，但也可以在 GitHub Actions 中使用：

```yaml
- name: Batch register
  run: |
    python batch_register.py --target 10 --headless true
```

**注意**：GitHub Actions 环境成功率可能较低，建议：
- 设置较小的目标数量（5-10 个）
- 增加失败容忍度（--max-fails 5）
- 使用代理

## 总结

批量注册工具适合：
- ✅ 本地批量创建账号
- ✅ 测试和开发
- ✅ 需要大量账号的场景

不适合：
- ❌ GitHub Actions 大批量注册（成功率低）
- ❌ 没有代理的高频注册（容易被封）
- ❌ 追求极致速度（建议稳定优先）

**推荐策略**：稳定、分批、适度间隔 🎯
