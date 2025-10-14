# warp-pool 文档中心

## 📚 文档导航

### 🚀 快速开始

- **[快速开始指南](./quick-start.md)** - 3 分钟快速配置（推荐从这里开始）
- **[浏览器指纹配置指南](./fingerprint-config-guide.md)** - 详细的参数说明

### 📖 技术文档

- **[实现总结](./IMPLEMENTATION_SUMMARY.md)** - 增强指纹模拟实现总结 🎯
- **[配置对比](./configuration-comparison.md)** - 主项目 vs warp-pool 详细对比
- **[指纹随机化说明](./FINGERPRINT.md)** - 浏览器指纹随机化功能详解

---

## 🎯 核心特点

### 简化配置（只需 3 个参数）

```bash
FINGERPRINT_RANDOMIZE=true    # 总开关
FINGERPRINT_LEVEL=balanced    # 级别：basic | balanced | aggressive
FINGERPRINT_DEBUG=false       # 调试模式
```

### 成功率提升

| 级别 | 成功率 | 推荐度 |
|------|--------|--------|
| basic | 80-95% | ⭐⭐⭐ |
| balanced | 90-98% | ⭐⭐⭐⭐⭐ |
| aggressive | 92-99% | ⭐⭐⭐⭐ |

---

## 🚀 3 分钟快速开始

### 1. 编辑配置

编辑 `.env` 文件：

```bash
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=balanced
FINGERPRINT_DEBUG=false
```

### 2. 开始注册

```bash
python register.py --count 5
```

### 3. 观察成功率

预期成功率：**90-98%**

---

## 📊 级别说明

### 🟢 basic - 基础模式

**包含功能：**
- Canvas 指纹混淆
- User-Agent 随机化
- 屏幕分辨率随机化
- 语言和时区随机化
- 硬件参数随机化

**成功率：** 80-95%  
**适合：** 测试和学习

---

### 🟡 balanced - 平衡模式（推荐）⭐

**包含功能：**
- basic 的所有功能
- + 增强的浏览器配置文件
- + WebGL 指纹混淆
- + Performance Timing 注入
- + 增强的 Navigator 属性
- + 配置一致性检查

**成功率：** 90-98%  
**适合：** 生产环境

---

### 🔴 aggressive - 激进模式

**包含功能：**
- balanced 的所有功能
- + Audio Context 指纹混淆

**成功率：** 92-99%  
**适合：** 追求极致

**注意：** 可能影响音频功能

---

## 💡 推荐配置

### 新手

```bash
FINGERPRINT_LEVEL=basic
FINGERPRINT_DEBUG=true  # 开启调试
```

### 一般用户（推荐）

```bash
FINGERPRINT_LEVEL=balanced
FINGERPRINT_DEBUG=false
```

### 高级用户

```bash
FINGERPRINT_LEVEL=aggressive
FINGERPRINT_DEBUG=false
```

---

## 🐛 故障排查

### 成功率没有提升？

1. 启用调试模式：`FINGERPRINT_DEBUG=true`
2. 运行：`python test_fingerprint.py`
3. 检查输出

### 浏览器启动失败？

1. 更新 Chrome 到最新版本
2. 切换到 basic 模式
3. 逐步升级

---

## 📚 详细文档

- [浏览器指纹配置指南](./fingerprint-config-guide.md) - 参数详解
- [配置对比文档](./configuration-comparison.md) - 技术对比

---

**最后更新：** 2025-10-14  
**版本：** 2.0.0（简化版）
