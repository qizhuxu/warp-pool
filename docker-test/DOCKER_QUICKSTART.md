# Docker 快速开始指南

## 🚀 5 分钟快速部署

### 前置要求

- ✅ Docker 已安装（20.10+）
- ✅ Docker Compose 已安装（2.0+）
- ✅ 至少 2GB 可用内存
- ✅ 至少 5GB 可用磁盘空间

---

## 📝 步骤 1：准备配置

### 1.1 克隆或下载项目

```bash
cd warp-pool
```

### 1.2 配置环境变量

编辑 `.env` 文件：

```bash
# 必需配置
MOEMAIL_API_KEY=your_api_key_here

# 可选配置（已有默认值）
HEADLESS=true
FINGERPRINT_LEVEL=balanced
```

---

## 🐳 步骤 2：构建和运行

### 方式 1：使用 docker-compose（推荐）

```bash
# 构建镜像
docker-compose build

# 启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 方式 2：使用 docker 命令

```bash
# 构建镜像
docker build -t warp-pool:latest .

# 运行容器
docker run -d \
  --name warp-pool \
  --env-file .env \
  -v $(pwd)/accounts:/app/accounts \
  -v $(pwd)/logs:/app/logs \
  --shm-size=2gb \
  --security-opt seccomp=unconfined \
  warp-pool:latest

# 查看日志
docker logs -f warp-pool
```

---

## 📊 步骤 3：查看结果

### 查看日志

```bash
# docker-compose
docker-compose logs -f

# docker
docker logs -f warp-pool
```

### 查看账号

```bash
# 账号保存在 accounts 目录
ls -la accounts/

# 查看今天的账号
ls -la accounts/$(date +%Y-%m-%d)/
```

---

## 🛑 步骤 4：停止和清理

### 停止容器

```bash
# docker-compose
docker-compose stop

# docker
docker stop warp-pool
```

### 删除容器

```bash
# docker-compose
docker-compose down

# docker
docker rm warp-pool
```

### 清理镜像（可选）

```bash
docker rmi warp-pool:latest
```

---

## 🔧 常用命令

### 查看容器状态

```bash
docker-compose ps
# 或
docker ps
```

### 进入容器

```bash
docker-compose exec warp-pool bash
# 或
docker exec -it warp-pool bash
```

### 重启容器

```bash
docker-compose restart
# 或
docker restart warp-pool
```

### 查看资源使用

```bash
docker stats warp-pool
```

---

## 🐛 故障排查

### 问题 1：构建失败

```bash
# 清理缓存重新构建
docker-compose build --no-cache
```

### 问题 2：容器启动失败

```bash
# 查看详细日志
docker-compose logs

# 检查配置
docker-compose config
```

### 问题 3：Chrome 崩溃

```bash
# 检查共享内存
docker inspect warp-pool | grep ShmSize

# 应该显示 2147483648 (2GB)
```

### 问题 4：权限问题

```bash
# 修复 accounts 目录权限
chmod 777 accounts logs
```

---

## 📈 批量注册

### 修改注册数量

编辑 `docker-compose.yml`：

```yaml
services:
  warp-pool:
    command: ["python", "register.py", "--count", "10"]
```

然后重启：

```bash
docker-compose up -d
```

---

## 🎯 生产环境建议

### 1. 使用环境变量文件

```bash
# 创建生产环境配置
cp .env .env.production

# 使用生产配置
docker-compose --env-file .env.production up -d
```

### 2. 持久化数据

```yaml
volumes:
  - /data/warp-pool/accounts:/app/accounts
  - /data/warp-pool/logs:/app/logs
```

### 3. 监控和告警

```bash
# 添加健康检查
docker-compose ps

# 查看资源使用
docker stats warp-pool
```

---

## 📚 更多信息

- **[完整部署文档](./docs/DOCKER_DEPLOYMENT.md)** - 详细的容器化方案
- **[配置说明](./docs/DEFAULT_CONFIG.md)** - 环境变量说明
- **[故障排查](./docs/DOCKER_DEPLOYMENT.md#常见问题)** - 常见问题解决

---

## ✅ 验证清单

部署完成后，检查以下项目：

- [ ] 容器正常运行（`docker ps`）
- [ ] 日志无错误（`docker logs`）
- [ ] Chrome 正常启动
- [ ] 指纹功能正常
- [ ] 账号成功保存到 `accounts/` 目录
- [ ] 日志保存到 `logs/` 目录

---

**快速开始完成！** 🎉

如有问题，查看 [完整文档](./docs/DOCKER_DEPLOYMENT.md) 或提交 Issue。
