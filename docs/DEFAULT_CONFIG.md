# 默认配置说明

## 📋 概述

本文档说明 warp-pool 项目的所有默认配置值。如果你不在 `.env` 文件中设置这些参数，系统将使用这些默认值。

---

## 🎯 指纹随机化配置

### 默认值总览

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `FINGERPRINT_RANDOMIZE` | `true` | ✅ 默认启用 |
| `FINGERPRINT_LEVEL` | `balanced` | ⭐ 平衡模式 |
| `ENHANCED_PROFILES_ENABLED` | `true` | ✅ 默认启用 |
| `STRICT_CONSISTENCY_CHECK` | `true` | ✅ 默认启用 |
| `FINGERPRINT_DEBUG` | `false` | ❌ 默认关闭 |

### 详细说明

#### 1. FINGERPRINT_RANDOMIZE

```python
FINGERPRINT_RANDOMIZE = os.getenv('FINGERPRINT_RANDOMIZE', 'true').lower() == 'true'
```

**默认值：** `true`

**含义：**
- ✅ 默认启用指纹随机化
- ✅ 开箱即用，无需配置
- ✅ 提供基本的反检测能力

**如果不设置：**
```bash
# .env 文件中没有这一行
# 系统使用默认值 true
```

**等同于：**
```bash
FINGERPRINT_RANDOMIZE=true
```

---

#### 2. FINGERPRINT_LEVEL

```python
FINGERPRINT_LEVEL = os.getenv('FINGERPRINT_LEVEL', 'balanced')
```

**默认值：** `balanced`

**含义：**
- ⭐ 默认使用平衡模式
- ✅ 成功率 90-98%
- ✅ 包含 5 项增强功能
- ✅ 适合生产环境

**如果不设置：**
```bash
# .env 文件中没有这一行
# 系统使用默认值 balanced
```

**等同于：**
```bash
FINGERPRINT_LEVEL=balanced
```

**可选值：**
- `basic` - 基础模式（80-95%）
- `balanced` - 平衡模式（90-98%）⭐ 默认
- `aggressive` - 激进模式（92-99%）

---

#### 3. ENHANCED_PROFILES_ENABLED

```python
ENHANCED_PROFILES_ENABLED = os.getenv('ENHANCED_PROFILES_ENABLED', 'true').lower() == 'true'
```

**默认值：** `true`

**含义：**
- ✅ 默认使用增强的浏览器配置文件
- ✅ 使用从 warp_register.py 提取的真实配置
- ✅ 确保 GPU、User-Agent 等参数一致
- ✅ 提高成功率

**如果不设置：**
```bash
# .env 文件中没有这一行
# 系统使用默认值 true
```

**等同于：**
```bash
ENHANCED_PROFILES_ENABLED=true
```

---

#### 4. STRICT_CONSISTENCY_CHECK

```python
STRICT_CONSISTENCY_CHECK = os.getenv('STRICT_CONSISTENCY_CHECK', 'true').lower() == 'true'
```

**默认值：** `true`

**含义：**
- ✅ 默认启用配置一致性检查
- ✅ 自动验证配置的合理性
- ✅ 避免 Windows + Apple GPU 等错误组合
- ✅ 提高稳定性

**如果不设置：**
```bash
# .env 文件中没有这一行
# 系统使用默认值 true
```

**等同于：**
```bash
STRICT_CONSISTENCY_CHECK=true
```

---

#### 5. FINGERPRINT_DEBUG

```python
FINGERPRINT_DEBUG = os.getenv('FINGERPRINT_DEBUG', 'false').lower() == 'true'
```

**默认值：** `false`

**含义：**
- ❌ 默认不显示详细的指纹信息
- ✅ 保持日志简洁
- ✅ 适合正常使用

**如果不设置：**
```bash
# .env 文件中没有这一行
# 系统使用默认值 false
```

**等同于：**
```bash
FINGERPRINT_DEBUG=false
```

**何时启用：**
- 首次使用时（验证配置）
- 调试问题时
- 查看详细信息时

---

## 🎨 默认行为示例

### 场景 1：完全不配置

如果你的 `.env` 文件中完全没有指纹相关配置：

```bash
# .env 文件
MOEMAIL_API_KEY=your_api_key
FIREBASE_API_KEY=AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs

# 没有任何 FINGERPRINT_* 配置
```

**实际效果：**
```python
FINGERPRINT_RANDOMIZE = True          # 默认启用
FINGERPRINT_LEVEL = 'balanced'        # 默认平衡模式
ENHANCED_PROFILES_ENABLED = True      # 默认启用
STRICT_CONSISTENCY_CHECK = True       # 默认启用
FINGERPRINT_DEBUG = False             # 默认关闭
```

**运行时输出：**
```
启动 Undetected Chrome (无头模式)...
  检测到 Chrome: C:\Program Files\Google\Chrome\Application\chrome.exe
  初始化 undetected-chromedriver...
  使用指定的 Chrome 版本: 121
  正在初始化浏览器...
  🎭 注入指纹混淆脚本 (级别: balanced)...
  ✅ 指纹混淆脚本注入成功 (Canvas, Navigator, Timezone, WebGL, Performance Timing)
  ✅ 浏览器启动成功
```

**注意：** 不会显示详细的指纹信息（因为 DEBUG=false）

---

### 场景 2：只设置 DEBUG

```bash
# .env 文件
MOEMAIL_API_KEY=your_api_key
FIREBASE_API_KEY=AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs

# 只启用调试模式
FINGERPRINT_DEBUG=true
```

**实际效果：**
```python
FINGERPRINT_RANDOMIZE = True          # 默认启用
FINGERPRINT_LEVEL = 'balanced'        # 默认平衡模式
ENHANCED_PROFILES_ENABLED = True      # 默认启用
STRICT_CONSISTENCY_CHECK = True       # 默认启用
FINGERPRINT_DEBUG = True              # ✅ 启用调试
```

**运行时输出：**
```
启动 Undetected Chrome (无头模式)...
  检测到 Chrome: C:\Program Files\Google\Chrome\Application\chrome.exe
  初始化 undetected-chromedriver...
  🎭 浏览器指纹:
     级别: balanced
     配置: Win10_Chrome_NVIDIA_RTX3060
     分辨率: 1920x1080
     User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
     语言: en-GB,en;q=0.9
     时区: Europe/Paris
     CPU 核心: 8
     内存: 16GB
     GPU 厂商: Google Inc. (NVIDIA)
     GPU 渲染器: ANGLE (NVIDIA, NVIDIA GeForce RTX 3060...
  使用指定的 Chrome 版本: 121
  正在初始化浏览器...
  🎭 注入指纹混淆脚本 (级别: balanced)...
  ✅ 指纹混淆脚本注入成功 (Canvas, Navigator, Timezone, WebGL, Performance Timing)
  ✅ 浏览器启动成功
```

**注意：** 会显示详细的指纹信息

---

### 场景 3：自定义级别

```bash
# .env 文件
MOEMAIL_API_KEY=your_api_key
FIREBASE_API_KEY=AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs

# 使用基础模式
FINGERPRINT_LEVEL=basic
```

**实际效果：**
```python
FINGERPRINT_RANDOMIZE = True          # 默认启用
FINGERPRINT_LEVEL = 'basic'           # ✅ 使用基础模式
ENHANCED_PROFILES_ENABLED = True      # 默认启用（但 basic 模式不使用）
STRICT_CONSISTENCY_CHECK = True       # 默认启用
FINGERPRINT_DEBUG = False             # 默认关闭
```

**运行时输出：**
```
🎭 注入指纹混淆脚本 (级别: basic)...
✅ 指纹混淆脚本注入成功 (Canvas, Navigator, Timezone)
```

**注意：** 只注入 3 项功能（basic 级别）

---

## 📊 默认配置的设计理念

### 1. 开箱即用

```python
# 默认配置已经是最佳实践
FINGERPRINT_RANDOMIZE = True          # ✅ 启用
FINGERPRINT_LEVEL = 'balanced'        # ⭐ 最佳平衡
ENHANCED_PROFILES_ENABLED = True      # ✅ 使用真实配置
STRICT_CONSISTENCY_CHECK = True       # ✅ 自动检查
```

**用户只需要：**
1. 配置邮箱 API Key
2. 运行 `python register.py`
3. 就能获得 90-98% 的成功率

### 2. 安全优先

```python
FINGERPRINT_DEBUG = False  # 默认不显示敏感信息
```

**原因：**
- 避免日志中泄露详细的指纹信息
- 保持日志简洁
- 适合生产环境

### 3. 性能平衡

```python
FINGERPRINT_LEVEL = 'balanced'  # 不是 aggressive
```

**原因：**
- `balanced` 已经有 90-98% 成功率
- `aggressive` 只多 2-4%，但可能影响音频功能
- 性价比最高

### 4. 智能检查

```python
STRICT_CONSISTENCY_CHECK = True  # 默认启用
```

**原因：**
- 自动避免配置错误
- 提高稳定性
- 减少用户困惑

---

## 🎯 推荐配置

### 新手（首次使用）

```bash
# 启用调试，查看详细信息
FINGERPRINT_DEBUG=true

# 其他使用默认值
```

### 一般用户（日常使用）

```bash
# 完全使用默认值，不需要配置任何 FINGERPRINT_* 参数
# 或者明确写出（与默认值相同）：
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=balanced
FINGERPRINT_DEBUG=false
```

### 高级用户（追求极致）

```bash
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=aggressive
ENHANCED_PROFILES_ENABLED=true
STRICT_CONSISTENCY_CHECK=true
FINGERPRINT_DEBUG=false
```

### 测试/调试

```bash
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=basic
FINGERPRINT_DEBUG=true
```

---

## 🔍 如何查看当前配置

### 方法 1：启用调试模式

```bash
FINGERPRINT_DEBUG=true
```

运行后会显示完整的指纹信息。

### 方法 2：运行测试脚本

```bash
python test_enhanced_fingerprint.py
```

会显示所有级别的配置。

### 方法 3：查看代码

```python
from config import config

print(f"FINGERPRINT_RANDOMIZE: {config.FINGERPRINT_RANDOMIZE}")
print(f"FINGERPRINT_LEVEL: {config.FINGERPRINT_LEVEL}")
print(f"ENHANCED_PROFILES_ENABLED: {config.ENHANCED_PROFILES_ENABLED}")
print(f"STRICT_CONSISTENCY_CHECK: {config.STRICT_CONSISTENCY_CHECK}")
print(f"FINGERPRINT_DEBUG: {config.FINGERPRINT_DEBUG}")
```

---

## 📝 总结

### 默认配置一览

```python
# 指纹随机化配置（默认值）
FINGERPRINT_RANDOMIZE = True          # ✅ 启用
FINGERPRINT_LEVEL = 'balanced'        # ⭐ 平衡模式
ENHANCED_PROFILES_ENABLED = True      # ✅ 使用真实配置
STRICT_CONSISTENCY_CHECK = True       # ✅ 自动检查
FINGERPRINT_DEBUG = False             # ❌ 不显示详细信息
```

### 关键点

1. **✅ 默认已启用增强功能**
   - 无需配置即可获得 90-98% 成功率

2. **⭐ 默认使用平衡模式**
   - 最佳的性价比
   - 适合大多数场景

3. **🔒 默认启用安全检查**
   - 自动验证配置一致性
   - 避免常见错误

4. **📊 默认关闭调试模式**
   - 保持日志简洁
   - 适合生产环境

### 何时需要修改

**需要修改的情况：**
- 🐛 调试问题 → 启用 `FINGERPRINT_DEBUG=true`
- 🎯 追求极致 → 使用 `FINGERPRINT_LEVEL=aggressive`
- 🧪 测试学习 → 使用 `FINGERPRINT_LEVEL=basic`

**不需要修改的情况：**
- ✅ 日常使用
- ✅ 生产环境
- ✅ 首次使用

---

**文档版本：** 1.0.0  
**最后更新：** 2025-10-14  
**适用版本：** warp-pool v2.0.0+
