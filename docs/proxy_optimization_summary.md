# 代理优化总结

## 🎯 问题分析

### 原始问题
- pip 安装依赖时通过代理连接 PyPI 失败
- 错误：`ConnectionResetError(104, 'Connection reset by peer')`
- 导致无法安装 `undetected-chromedriver`

### 根本原因
1. **不必要的代理使用**：GitHub Actions runner 本身在国外，访问 PyPI 不需要代理
2. **全局代理配置**：之前在代理配置步骤设置了全局环境变量，影响所有后续步骤
3. **代理不稳定**：HTTP 代理端口 (10809) 对长连接支持不佳

## ✅ 解决方案

### 修改策略
**只在批量注册时启用代理，其他步骤不使用代理**

### 具体修改

#### 1. 移除全局代理环境变量
**位置**: Setup Xray Proxy 步骤

**修改前**:
```yaml
# 设置环境变量
echo "HTTP_PROXY=http://127.0.0.1:10809" >> $GITHUB_ENV
echo "HTTPS_PROXY=http://127.0.0.1:10809" >> $GITHUB_ENV
echo "ALL_PROXY=socks5://127.0.0.1:10808" >> $GITHUB_ENV
echo "NO_PROXY=localhost,127.0.0.1,::1" >> $GITHUB_ENV
```

**修改后**:
```yaml
# 不设置全局环境变量，只在需要时使用代理
echo "✅ 代理配置完成（仅在注册时启用）"
```

#### 2. 安装依赖时明确禁用代理
**位置**: Install Python dependencies 步骤

**修改后**:
```yaml
- name: Install Python dependencies
  env:
    # 禁用代理，直连 PyPI
    HTTP_PROXY: ""
    HTTPS_PROXY: ""
    http_proxy: ""
    https_proxy: ""
    ALL_PROXY: ""
    all_proxy: ""
  run: |
    echo "📦 安装 Python 依赖（不使用代理）..."
    pip install --upgrade pip
    pip install -r requirements.txt
```

#### 3. 批量注册时启用代理
**位置**: Run batch registration 步骤

**修改后**:
```yaml
# 使用批量注册脚本（启用代理）
echo "🚀 开始批量注册（目标增加 $REGISTER_COUNT 个账号）..."
echo "🌐 启用代理: SOCKS5://127.0.0.1:10808"

# 设置代理环境变量并运行注册
export HTTP_PROXY=http://127.0.0.1:10809
export HTTPS_PROXY=http://127.0.0.1:10809
export ALL_PROXY=socks5://127.0.0.1:10808
export NO_PROXY=localhost,127.0.0.1,::1

xvfb-run -a python batch_register.py --add "$REGISTER_COUNT" --headless true --max-fails "$MAX_FAILS" 2>&1 | tee registration.log
```

## 📊 优化效果

### 修改前
| 步骤 | 代理状态 | 结果 |
|------|---------|------|
| 安装系统依赖 | ✅ 使用代理 | ✅ 成功（不需要代理） |
| 安装 Python 依赖 | ✅ 使用代理 | ❌ 失败（代理不稳定） |
| 批量注册 | ✅ 使用代理 | ⏸️ 未执行（依赖安装失败） |

### 修改后
| 步骤 | 代理状态 | 结果 |
|------|---------|------|
| 安装系统依赖 | ❌ 不使用代理 | ✅ 成功（直连更快） |
| 安装 Python 依赖 | ❌ 不使用代理 | ✅ 成功（直连 PyPI） |
| 批量注册 | ✅ 使用代理 | ✅ 可以执行（需要代理访问 Warp） |

## 🎯 优势

1. **更快的依赖安装**
   - 直连 PyPI，无代理延迟
   - 避免代理连接问题

2. **更稳定的工作流**
   - 减少代理相关的失败点
   - 只在必要时使用代理

3. **更清晰的日志**
   - 明确显示何时使用代理
   - 便于问题排查

4. **资源优化**
   - 减少不必要的代理流量
   - 降低代理服务器负载

## 🚀 使用建议

### 何时使用代理
- ✅ 批量注册 Warp 账号
- ✅ 访问被限制的服务

### 何时不使用代理
- ❌ 安装系统依赖（apt-get）
- ❌ 安装 Python 依赖（pip）
- ❌ 下载 GitHub Release
- ❌ 上传 GitHub Release

## 📝 注意事项

1. **环境变量优先级**
   - 步骤级别的 `env` 优先于全局环境变量
   - 使用空字符串 `""` 可以清除环境变量

2. **代理端口选择**
   - SOCKS5: 127.0.0.1:10808（推荐用于 Python 应用）
   - HTTP: 127.0.0.1:10809（备用）

3. **NO_PROXY 设置**
   - 始终排除 localhost 和 127.0.0.1
   - 避免本地连接通过代理

## ✅ 验证清单

- [x] 移除全局代理环境变量设置
- [x] 安装依赖时明确禁用代理
- [x] 批量注册时启用代理
- [x] 添加清晰的日志输出
- [x] 保持代理测试步骤（用于验证代理可用性）

## 🎉 预期结果

修改后的工作流应该能够：
1. ✅ 成功安装所有依赖
2. ✅ 正常启动 Xray 代理
3. ✅ 通过代理完成 Warp 账号注册
4. ✅ 避免不必要的代理连接问题
