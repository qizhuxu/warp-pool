# 🚀 快速参考卡片

## 📋 配置速查

### 推荐配置（复制到 .env）

```bash
# 指纹随机化配置
FINGERPRINT_RANDOMIZE=true
FINGERPRINT_LEVEL=balanced
ENHANCED_PROFILES_ENABLED=true
STRICT_CONSISTENCY_CHECK=true
FINGERPRINT_DEBUG=false
```

---

## 📊 级别对比

| 级别 | 功能 | 成功率 | 适合 |
|------|------|--------|------|
| **basic** | 3 项 | 80-95% | 测试 |
| **balanced** ⭐ | 5 项 | 90-98% | 生产 |
| **aggressive** | 6 项 | 92-99% | 极致 |

---

## 🔧 常用命令

```bash
# 测试增强功能
python test_enhanced_fingerprint.py

# 注册单个账号
python register.py

# 批量注册（5个）
python register.py --count 5

# 无头模式
python register.py --headless true
```

---

## 🎯 功能清单

### basic 级别
- ✅ Canvas 指纹混淆
- ✅ Navigator 属性覆盖
- ✅ Timezone 随机化

### balanced 级别（推荐）
- ✅ basic 的所有功能
- ✅ 增强的浏览器配置文件
- ✅ WebGL 指纹混淆
- ✅ Performance Timing 注入

### aggressive 级别
- ✅ balanced 的所有功能
- ✅ Audio Context 指纹混淆

---

## 🐛 故障排查

### 问题：成功率没提升

**解决：**
```bash
# 1. 启用调试
FINGERPRINT_DEBUG=true

# 2. 测试配置
python test_enhanced_fingerprint.py

# 3. 检查输出
```

### 问题：浏览器启动失败

**解决：**
```bash
# 1. 更新 Chrome
# 2. 降级到 basic
FINGERPRINT_LEVEL=basic

# 3. 逐步升级
```

---

## 📚 文档链接

- [实现总结](./docs/IMPLEMENTATION_SUMMARY.md) - 完整说明
- [配置指南](./docs/FINGERPRINT_CONFIG.md) - 参数详解
- [文档中心](./docs/README.md) - 所有文档

---

## 💡 最佳实践

### 新手
```bash
FINGERPRINT_LEVEL=basic
FINGERPRINT_DEBUG=true
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

**快速开始：** 复制推荐配置 → 运行 `python register.py` 🚀
