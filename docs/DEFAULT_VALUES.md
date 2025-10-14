# 默认配置快速参考

## 📋 指纹随机化默认值

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `FINGERPRINT_RANDOMIZE` | ✅ `true` | 默认启用指纹随机化 |
| `FINGERPRINT_LEVEL` | ⭐ `balanced` | 默认平衡模式（90-98%）|
| `ENHANCED_PROFILES_ENABLED` | ✅ `true` | 默认使用真实配置文件 |
| `STRICT_CONSISTENCY_CHECK` | ✅ `true` | 默认启用一致性检查 |
| `FINGERPRINT_DEBUG` | ❌ `false` | 默认不显示详细信息 |

---

## 🎯 这意味着什么？

### 如果你不配置任何参数

```bash
# .env 文件中只有必需的配置
MOEMAIL_API_KEY=your_api_key
FIREBASE_API_KEY=AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs

# 没有任何 FINGERPRINT_* 配置
```

**系统会自动使用：**
- ✅ 启用指纹随机化
- ⭐ 使用 balanced 级别（5 项功能）
- ✅ 使用真实的浏览器配置文件
- ✅ 自动检查配置一致性
- ❌ 不显示详细的指纹信息

**预期成功率：** 90-98%

---

## 💡 常见场景

### 场景 1：完全默认（推荐）

```bash
# 不需要配置任何 FINGERPRINT_* 参数
# 系统自动使用最佳配置
```

**效果：** 90-98% 成功率，开箱即用

---

### 场景 2：首次使用（查看详情）

```bash
# 只启用调试模式
FINGERPRINT_DEBUG=true
```

**效果：** 显示详细的指纹信息，其他使用默认值

---

### 场景 3：追求极致

```bash
# 使用激进模式
FINGERPRINT_LEVEL=aggressive
```

**效果：** 92-99% 成功率，其他使用默认值

---

### 场景 4：测试学习

```bash
# 使用基础模式
FINGERPRINT_LEVEL=basic
FINGERPRINT_DEBUG=true
```

**效果：** 80-95% 成功率，显示详细信息

---

## 📊 级别对比

| 级别 | 成功率 | 功能数 | 是否默认 |
|------|--------|--------|---------|
| basic | 80-95% | 3 项 | ❌ |
| balanced | 90-98% | 5 项 | ✅ 默认 |
| aggressive | 92-99% | 6 项 | ❌ |

---

## 🚀 快速开始

### 最简配置（推荐）

```bash
# .env 文件
MOEMAIL_API_KEY=your_api_key
FIREBASE_API_KEY=AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs

# 就这么简单！其他都是默认值
```

然后运行：
```bash
python register.py
```

**预期效果：**
- ✅ 自动使用 balanced 级别
- ✅ 成功率 90-98%
- ✅ 无需额外配置

---

## 📚 详细文档

查看完整说明：
- **[DEFAULT_CONFIG.md](./docs/DEFAULT_CONFIG.md)** - 详细的默认配置说明
- **[FINGERPRINT_CONFIG.md](./docs/FINGERPRINT_CONFIG.md)** - 配置指南
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - 快速参考

---

**记住：** 默认配置已经是最佳实践，大多数情况下不需要修改！✨
