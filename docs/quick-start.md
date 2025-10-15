# 快速开始指南

## 🚀 3 分钟快速配置

### 步骤 1：编辑配置文件

编辑 `.env` 文件，添加以下配置：

```bash
# ==================== 浏览器指纹配置 ====================

# 推荐配置（复制粘贴即可）
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=balanced
FINGERPRINT_DEBUG=false
```

**就这么简单！** 只需 3 个参数。

---

### 步骤 2：测试配置（可选）

```bash
python test_fingerprint.py
```

**预期输出：**
```
✓ 指纹随机化: 已启用
✓ 增强级别: balanced
✓ 配置一致性检查: 通过

当前配置:
  - GPU: ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti...)
  - User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
  - 分辨率: 1920x1080
  - CPU 核心: 12
  - 内存: 8GB
```

---

### 步骤 3：开始注册

```bash
# 单个账号
python register.py

# 批量注册（增加 5 个账号）
python batch_register.py --add 5
```

观察成功率是否提升到 **90-98%**。

---

## 📊 配置选项

### 🟢 基础模式（测试用）

```bash
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=basic
FINGERPRINT_DEBUG=false
```

**成功率：** 80-95%

---

### 🟡 平衡模式（推荐）⭐

```bash
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=balanced
FINGERPRINT_DEBUG=false
```

**成功率：** 90-98%

---

### 🔴 激进模式（追求极致）

```bash
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=aggressive
FINGERPRINT_DEBUG=false
```

**成功率：** 92-99%

---

## 🎯 参数说明

### `FINGERPRINT_RANDOMIZE`

- `true`: 启用指纹随机化（推荐）
- `false`: 关闭（不推荐）

### `FINGERPRINT_LEVEL`

- `basic`: 基础模式（80-95%）
- `balanced`: 平衡模式（90-98%）⭐
- `aggressive`: 激进模式（92-99%）

### `FINGERPRINT_DEBUG`

- `false`: 正常模式
- `true`: 调试模式（首次使用建议开启）

---

## 💡 常见问题

### Q1: 我应该选哪个级别？

**A:** 推荐 `balanced`

- 成功率高（90-98%）
- 风险低
- 适合生产环境

### Q2: 需要修改其他配置吗？

**A:** 不需要

只需修改这 3 个参数即可。

### Q3: 如何知道配置是否生效？

**A:** 启用调试模式

```bash
FINGERPRINT_DEBUG=true
python test_fingerprint.py
```

---

## 📈 预期效果

| 级别 | 成功率 | 适用场景 |
|------|--------|---------|
| basic | 80-95% | 测试学习 |
| balanced | 90-98% | 生产环境 ⭐ |
| aggressive | 92-99% | 追求极致 |

---

## 🔄 切换级别

### 从 basic 升级到 balanced

```bash
# 修改 .env 文件
FINGERPRINT_LEVEL=balanced
```

重新运行即可，无需其他操作。

---

## 🔧 高级配置

### 自定义指纹级别

如果需要更精细的控制，可以使用以下环境变量：

```bash
# 增强功能（balanced 级别自动启用）
ENHANCED_PROFILES_ENABLED=true
WEBGL_SPOOFING_ENABLED=true
PERFORMANCE_TIMING_ENABLED=true
ENHANCED_NAVIGATOR_ENABLED=true
AUDIO_CONTEXT_SPOOFING_ENABLED=false  # aggressive 级别才启用

# 一致性检查
STRICT_CONSISTENCY_CHECK=true
```

**注意：** 通常不需要手动配置这些，`FINGERPRINT_LEVEL` 会自动处理。

---

## 📚 更多信息

详细的技术文档请参考：
- [浏览器指纹配置指南](./fingerprint-config-guide.md) - 完整的参数说明
- [Verisoul 反检测增强指南](./verisoul-enhancement-guide.md) - 技术细节
- [配置对比文档](./configuration-comparison.md) - 不同配置的对比

---

**最后更新：** 2025-10-15  
**版本：** 2.1.0
