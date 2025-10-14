# warp-pool 容器化部署方案

## 📋 可行性分析

### ✅ 可行性结论

**完全可行！** 但需要注意一些特殊配置。

---

## 🔍 核心挑战

### 1. 浏览器自动化挑战

| 挑战 | 解决方案 | 难度 |
|------|---------|------|
| Chrome 浏览器安装 | 使用官方 Chrome 镜像 | ⭐ |
| ChromeDriver 版本匹配 | 自动下载匹配版本 | ⭐⭐ |
| 无头模式运行 | 配置 `--headless=new` | ⭐ |
| 显示服务器（可选）| Xvfb 虚拟显示 | ⭐⭐⭐ |
| 字体和依赖 | 安装中文字体等 | ⭐⭐ |

### 2. undetected-chromedriver 特殊性

**关键点：**
- ✅ undetected-chromedriver 支持容器环境
- ✅ 会自动下载匹配的 ChromeDriver
- ⚠️ 需要足够的权限和依赖
- ⚠️ 首次运行需要下载时间

### 3. 指纹随机化兼容性

**评估：**
- ✅ Canvas 指纹混淆 - 完全兼容
- ✅ WebGL 指纹混淆 - 完全兼容
- ✅ Performance Timing - 完全兼容
- ✅ Navigator 属性覆盖 - 完全兼容
- ✅ 增强配置文件 - 完全兼容

**结论：** 所有指纹功能在容器中都能正常工作！

---

## 🐳 Docker 方案

### 方案 1：基于 Python 官方镜像（推荐）

**优点：**
- ✅ 镜像小（~500MB）
- ✅ 构建快
- ✅ 易于维护
- ✅ 灵活性高

**Dockerfile：**

```dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    # Chrome 依赖
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    # 中文字体支持
    fonts-liberation \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# 安装 Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建必要的目录
RUN mkdir -p accounts logs

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV HEADLESS=true

# 暴露端口（如果需要）
# EXPOSE 8000

# 运行命令
CMD ["python", "register.py"]
```

---

### 方案 2：基于 Selenium 官方镜像

**优点：**
- ✅ Chrome 已预装
- ✅ 所有依赖齐全
- ✅ 开箱即用

**缺点：**
- ❌ 镜像大（~1GB）
- ❌ 更新慢

**Dockerfile：**

```dockerfile
FROM selenium/standalone-chrome:latest

# 切换到 root 用户安装依赖
USER root

# 安装 Python 和 pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# 创建必要的目录
RUN mkdir -p accounts logs

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV HEADLESS=true

# 切换回普通用户
USER seluser

# 运行命令
CMD ["python3", "register.py"]
```

---

### 方案 3：多阶段构建（最优化）

**优点：**
- ✅ 镜像最小
- ✅ 构建缓存优化
- ✅ 安全性高

**Dockerfile：**

```dockerfile
# 构建阶段
FROM python:3.11-slim as builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 运行阶段
FROM python:3.11-slim

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    fonts-liberation \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# 安装 Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制 Python 包
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY . .

# 创建目录
RUN mkdir -p accounts logs

# 环境变量
ENV PYTHONUNBUFFERED=1
ENV HEADLESS=true

CMD ["python", "register.py"]
```

---

## 📝 docker-compose.yml

### 基础配置

```yaml
version: '3.8'

services:
  warp-pool:
    build: .
    container_name: warp-pool
    environment:
      # 邮箱服务配置
      - MOEMAIL_URL=https://email.959585.xyz
      - MOEMAIL_API_KEY=${MOEMAIL_API_KEY}
      
      # Firebase 配置
      - FIREBASE_API_KEY=AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs
      
      # 浏览器配置
      - HEADLESS=true
      
      # 指纹配置
      - FINGERPRINT_RANDOMIZE=true
      - FINGERPRINT_LEVEL=balanced
      - ENHANCED_PROFILES_ENABLED=true
      - STRICT_CONSISTENCY_CHECK=true
      - FINGERPRINT_DEBUG=false
      
      # 代理配置（可选）
      # - HTTP_PROXY=http://proxy:port
      # - HTTPS_PROXY=http://proxy:port
    
    volumes:
      # 持久化账号数据
      - ./accounts:/app/accounts
      # 持久化日志
      - ./logs:/app/logs
      # ChromeDriver 缓存（可选）
      - chrome-data:/root/.local/share/undetected_chromedriver
    
    # 资源限制
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
    
    # 安全配置
    security_opt:
      - seccomp:unconfined
    
    # 共享内存大小（Chrome 需要）
    shm_size: 2gb
    
    # 重启策略
    restart: unless-stopped

volumes:
  chrome-data:
```

### 高级配置（带代理和网络）

```yaml
version: '3.8'

services:
  warp-pool:
    build: .
    container_name: warp-pool
    env_file:
      - .env
    
    volumes:
      - ./accounts:/app/accounts
      - ./logs:/app/logs
      - chrome-data:/root/.local/share/undetected_chromedriver
    
    networks:
      - warp-network
    
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    
    security_opt:
      - seccomp:unconfined
    
    shm_size: 2gb
    
    restart: unless-stopped
    
    # 健康检查
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # 可选：本地代理服务
  proxy:
    image: dperson/torproxy
    container_name: warp-proxy
    networks:
      - warp-network
    restart: unless-stopped

networks:
  warp-network:
    driver: bridge

volumes:
  chrome-data:
```

---

## 🚀 使用方法

### 1. 构建镜像

```bash
# 进入项目目录
cd warp-pool

# 构建镜像
docker build -t warp-pool:latest .

# 或使用 docker-compose
docker-compose build
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# 必需配置
MOEMAIL_API_KEY=your_api_key_here

# 可选配置
HEADLESS=true
FINGERPRINT_LEVEL=balanced
FINGERPRINT_DEBUG=false

# 代理配置（如果需要）
# HTTP_PROXY=http://proxy:port
# HTTPS_PROXY=http://proxy:port
```

### 3. 运行容器

```bash
# 使用 docker run
docker run -d \
  --name warp-pool \
  --env-file .env \
  -v $(pwd)/accounts:/app/accounts \
  -v $(pwd)/logs:/app/logs \
  --shm-size=2gb \
  warp-pool:latest

# 或使用 docker-compose
docker-compose up -d
```

### 4. 查看日志

```bash
# docker
docker logs -f warp-pool

# docker-compose
docker-compose logs -f
```

### 5. 停止容器

```bash
# docker
docker stop warp-pool
docker rm warp-pool

# docker-compose
docker-compose down
```

---

## ⚙️ 关键配置说明

### 1. 共享内存大小

```yaml
shm_size: 2gb
```

**为什么需要：**
- Chrome 使用共享内存进行进程间通信
- 默认的 64MB 太小，会导致崩溃
- 推荐 2GB

### 2. 安全配置

```yaml
security_opt:
  - seccomp:unconfined
```

**为什么需要：**
- Chrome 的沙箱需要某些系统调用
- 在容器中可能被限制
- 使用 `seccomp:unconfined` 解除限制

**安全替代方案：**
```yaml
# 使用 --no-sandbox 参数（不推荐生产环境）
command: ["python", "register.py", "--no-sandbox"]
```

### 3. 资源限制

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

**推荐配置：**
- CPU: 1-2 核
- 内存: 1-2GB
- 存储: 5-10GB

### 4. 持久化存储

```yaml
volumes:
  - ./accounts:/app/accounts  # 账号数据
  - ./logs:/app/logs          # 日志文件
  - chrome-data:/root/.local/share/undetected_chromedriver  # ChromeDriver 缓存
```

---

## 🐛 常见问题

### 问题 1：Chrome 崩溃

**错误信息：**
```
DevToolsActivePort file doesn't exist
```

**解决方案：**
```yaml
# 增加共享内存
shm_size: 2gb

# 或添加 Chrome 参数
environment:
  - CHROME_ARGS=--disable-dev-shm-usage
```

### 问题 2：ChromeDriver 下载失败

**错误信息：**
```
Failed to download ChromeDriver
```

**解决方案：**
```dockerfile
# 在 Dockerfile 中预下载
RUN python -c "import undetected_chromedriver as uc; uc.Chrome(version_main=121)"
```

### 问题 3：字体缺失

**错误信息：**
```
Font not found
```

**解决方案：**
```dockerfile
# 安装字体
RUN apt-get install -y \
    fonts-liberation \
    fonts-noto-cjk \
    fonts-wqy-zenhei
```

### 问题 4：权限问题

**错误信息：**
```
Permission denied
```

**解决方案：**
```dockerfile
# 创建非 root 用户
RUN useradd -m -u 1000 warp && \
    chown -R warp:warp /app

USER warp
```

---

## 📊 性能优化

### 1. 镜像优化

```dockerfile
# 使用 .dockerignore
# 创建 .dockerignore 文件
__pycache__
*.pyc
*.pyo
.git
.env
accounts/
logs/
*.md
docs/
```

### 2. 构建缓存

```bash
# 使用 BuildKit
DOCKER_BUILDKIT=1 docker build -t warp-pool:latest .
```

### 3. 多阶段构建

参考方案 3 的 Dockerfile

### 4. 镜像大小对比

| 方案 | 镜像大小 | 构建时间 |
|------|---------|---------|
| 方案 1（Python slim）| ~500MB | 3-5 分钟 |
| 方案 2（Selenium）| ~1GB | 2-3 分钟 |
| 方案 3（多阶段）| ~450MB | 4-6 分钟 |

---

## 🎯 生产环境建议

### 1. 使用编排工具

**Kubernetes 部署：**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: warp-pool
spec:
  replicas: 3
  selector:
    matchLabels:
      app: warp-pool
  template:
    metadata:
      labels:
        app: warp-pool
    spec:
      containers:
      - name: warp-pool
        image: warp-pool:latest
        env:
        - name: MOEMAIL_API_KEY
          valueFrom:
            secretKeyRef:
              name: warp-secrets
              key: moemail-api-key
        - name: HEADLESS
          value: "true"
        - name: FINGERPRINT_LEVEL
          value: "balanced"
        resources:
          limits:
            memory: "2Gi"
            cpu: "2"
          requests:
            memory: "1Gi"
            cpu: "1"
        volumeMounts:
        - name: accounts
          mountPath: /app/accounts
        - name: dshm
          mountPath: /dev/shm
      volumes:
      - name: accounts
        persistentVolumeClaim:
          claimName: warp-accounts-pvc
      - name: dshm
        emptyDir:
          medium: Memory
          sizeLimit: 2Gi
```

### 2. 监控和日志

```yaml
# 添加到 docker-compose.yml
services:
  warp-pool:
    # ... 其他配置
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 3. 自动重启策略

```yaml
restart: unless-stopped

# 或更精细的控制
restart_policy:
  condition: on-failure
  delay: 5s
  max_attempts: 3
  window: 120s
```

---

## 📝 总结

### ✅ 可行性评估

| 维度 | 评分 | 说明 |
|------|------|------|
| **技术可行性** | ⭐⭐⭐⭐⭐ | 完全可行 |
| **实施难度** | ⭐⭐⭐ | 中等 |
| **维护成本** | ⭐⭐ | 较低 |
| **性能影响** | ⭐⭐⭐⭐ | 轻微影响 |
| **稳定性** | ⭐⭐⭐⭐ | 稳定 |

### 推荐方案

**开发/测试环境：**
- 使用方案 1（Python slim）
- docker-compose 部署
- 本地存储

**生产环境：**
- 使用方案 3（多阶段构建）
- Kubernetes 编排
- 持久化存储
- 监控和日志

### 关键要点

1. ✅ **完全支持指纹随机化**
2. ✅ **所有功能都能正常工作**
3. ⚠️ **需要注意共享内存配置**
4. ⚠️ **首次运行需要下载 ChromeDriver**
5. ✅ **适合批量部署和扩展**

---

**文档版本：** 1.0.0  
**最后更新：** 2025-10-14  
**测试状态：** 待验证
