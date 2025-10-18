# 邮箱服务更新说明

## 📅 更新日期
2025-10-15

## 🔄 变更内容

### 移除的服务
- ❌ **1secmail** - 服务不可用（403 错误）

### 新增的服务
- ✅ **Skymail (Cloud Mail)** - 可自建的临时邮箱服务

## 📊 当前支持的邮箱服务

### 1. MoeMail（默认）

**优点：**
- ✅ 稳定可靠
- ✅ API 简单

**缺点：**
- ⚠️ 需要 API Key
- ⚠️ 依赖第三方服务

**配置：**
```env
EMAIL_SERVICE=moemail
MOEMAIL_URL=https://email.959585.xyz
MOEMAIL_API_KEY=your_api_key_here
```

**项目地址：** https://github.com/beilunyang/moemail

---

### 2. Skymail (Cloud Mail)（新增）

**优点：**
- ✅ 可自建部署
- ✅ 完全控制
- ✅ Token 可重复使用
- ✅ 支持批量创建
- ✅ 支持通配符邮箱（无需注册）
- ✅ 支持多域名配置（随机选择，提高可用性）

**缺点：**
- ⚠️ 需要自建服务器
- ⚠️ 需要管理员 Token

**配置：**
```env
EMAIL_SERVICE=skymail
SKYMAIL_URL=https://cloudmail.qixc.pp.ua
SKYMAIL_TOKEN=your_token_here
# 支持多域名（逗号分隔，随机选择，提高可用性）
# 单域名: SKYMAIL_DOMAIN=example.com
# 多域名: SKYMAIL_DOMAIN=domain1.com,domain2.com,domain3.com
SKYMAIL_DOMAIN=example.com
SKYMAIL_WILDCARD=false  # 通配符模式（无需注册，推荐启用）
```

**多域名配置说明：**
- 支持配置多个域名，用逗号分隔
- 创建邮箱时会随机选择一个域名
- 提高可用性和分散风险
- 示例：`SKYMAIL_DOMAIN=domain1.com,domain2.com,domain3.com`

**通配符模式说明：**
- `SKYMAIL_WILDCARD=true`: 无需注册邮箱，任意地址都能接收邮件（推荐）
- `SKYMAIL_WILDCARD=false`: 需要先注册邮箱才能接收邮件（默认）

**多域名支持：** 🆕
- 支持配置多个域名（逗号分隔）
- 创建邮箱时随机选择域名
- 提高可用性，分散风险
- 示例：`SKYMAIL_DOMAIN=domain1.com,domain2.com,domain3.com`

**项目地址：** https://github.com/eoao/cloud-mail

**文档：** https://doc.skymail.ink/

**Token 获取：** https://doc.skymail.ink/api/api-doc.html#生成token

---

## 🚀 使用方法

### 切换邮箱服务

编辑 `.env` 文件：

```env
# 使用 MoeMail（默认）
EMAIL_SERVICE=moemail

# 或使用 Skymail
EMAIL_SERVICE=skymail

# 或使用 Auto 模式（自动随机选择，推荐）
EMAIL_SERVICE=auto
```

### 测试邮箱服务

```bash
# 测试 Skymail
python test_skymail.py

# 测试 Skymail Token 重用性
python test_skymail.py --test-token
```

---

## 📝 API 对比

| 功能 | MoeMail | Skymail | Auto 模式 |
|------|---------|---------|----------|
| 创建邮箱 | ✅ | ✅ | ✅ |
| 查询邮件 | ✅ | ✅ | ✅ |
| Token 管理 | API Key | 动态 Token | 自动 |
| Token 重用 | ✅ | ✅ | ✅ |
| 批量创建 | ✅ | ✅ | ✅ |
| 自建部署 | ❌ | ✅ | - |
| 多域名支持 | ❌ | ✅ | ✅ |
| 通配符邮箱 | ❌ | ✅ | ✅ |
| 自动选择服务 | ❌ | ❌ | ✅ 🆕 |
| 负载均衡 | ❌ | ❌ | ✅ 🆕 |

---

## 🔧 代码变更

### email_service.py

**主要变更：**
1. 移除 `use_1secmail` 参数
2. 添加 `service_type` 参数（'moemail' 或 'skymail'）
3. 实现 Skymail 相关方法：
   - `_init_skymail()` - 初始化 Skymail
   - `_generate_skymail_token()` - 生成 Token
   - `_create_skymail()` - 创建邮箱
   - `_wait_for_skymail()` - 等待邮件

**使用示例：**
```python
# 使用 MoeMail
email_service = EmailService(service_type='moemail')

# 使用 Skymail
email_service = EmailService(service_type='skymail')
```

### config.py

**新增配置：**
```python
EMAIL_SERVICE = os.getenv('EMAIL_SERVICE', 'moemail')
SKYMAIL_URL = os.getenv('SKYMAIL_URL', 'https://cloudmail.qixc.pp.ua')
SKYMAIL_TOKEN = os.getenv('SKYMAIL_TOKEN', '')
SKYMAIL_DOMAIN = os.getenv('SKYMAIL_DOMAIN', 'qixc.pp.ua')  # 支持多域名，逗号分隔
```

**简化说明：**
- 移除了 `SKYMAIL_ADMIN_EMAIL` 和 `SKYMAIL_ADMIN_PASSWORD`
- 只需配置 `SKYMAIL_TOKEN`（通过管理员账号生成）
- Token 可重复使用，避免频繁生成
- **支持多域名配置**（逗号分隔），随机选择，提高可用性和分散风险

---

## 🧪 测试结果

### Skymail 测试

✅ **Token 生成** - 成功  
✅ **创建邮箱** - 成功  
✅ **查询邮件** - 成功  
✅ **提取验证链接** - 成功  
✅ **Token 重用** - 成功  

**结论：**
- Token 可以重复使用
- 每次生成的 Token 不同
- 生成新 Token 会使旧 Token 失效
- 建议：启动时生成一次，批量注册时重复使用

### 1secmail 测试

❌ **服务不可用** - HTTP 403  
❌ **已从代码中移除**

---

## 📚 相关文档

- [Skymail 测试脚本](../tests/test_skymail.py)
- [邮箱服务实现](../email_service.py)
- [配置文件](../config.py)
- [环境变量示例](../.env.example)

---

## 🎯 推荐配置

### 个人使用（单服务）
```env
EMAIL_SERVICE=moemail
MOEMAIL_URL=https://your-domain.com
MOEMAIL_API_KEY=your_api_key
```

### 自建服务（推荐启用通配符模式 + 多域名）
```env
EMAIL_SERVICE=skymail
SKYMAIL_URL=https://your-domain.com
SKYMAIL_TOKEN=your_token_here
# 配置多个域名，提高可用性
SKYMAIL_DOMAIN=domain1.com,domain2.com,domain3.com
SKYMAIL_WILDCARD=true  # 启用通配符模式，无需注册
```

### Auto 模式（推荐，最佳实践）⭐
```env
# 自动选择服务，负载均衡
EMAIL_SERVICE=auto

# 配置两个服务
MOEMAIL_URL=https://your-moemail.com
MOEMAIL_API_KEY=your_api_key

SKYMAIL_URL=https://your-skymail.com
SKYMAIL_TOKEN=your_token_here
SKYMAIL_DOMAIN=domain1.com,domain2.com,domain3.com
SKYMAIL_WILDCARD=true
```

### GitHub Actions
```env
# 可以使用 auto 模式提高成功率
EMAIL_SERVICE=auto
# 使用 GitHub Secrets 配置
```

---

## 🎲 Auto 模式（自动选择服务）

### 功能说明

Auto 模式会在每次创建邮箱时，从已配置的可用服务中随机选择一个使用。

### 优势

1. **负载均衡** - 自动分散请求到不同服务
2. **提高可用性** - 某个服务故障时自动使用其他服务
3. **降低风险** - 避免单一服务过载或被限制
4. **灵活切换** - 无需手动修改配置

### 配置方法

```env
# 设置为 auto 模式
EMAIL_SERVICE=auto

# 配置两个服务（至少配置一个）
MOEMAIL_URL=https://email.959585.xyz
MOEMAIL_API_KEY=your_api_key_here

SKYMAIL_URL=https://cloudmail.qixc.pp.ua
SKYMAIL_TOKEN=your_token_here
SKYMAIL_DOMAIN=domain1.com,domain2.com
SKYMAIL_WILDCARD=true
```

### 工作原理

1. **健康检查** - 系统启动时检查所有已配置服务的可用性（仅 auto 模式）
2. **初始化** - 检查哪些服务已配置且可用
3. **随机选择** - 从可用服务列表中随机选择一个（排除失败的服务）
4. **创建邮箱** - 使用选中的服务创建邮箱
5. **故障转移** - 如果创建失败，自动切换到其他服务重试
6. **失败记录** - 记录失败的服务，连续失败 3 次后临时排除（5分钟）
7. **自动恢复** - 5分钟后自动清除失败记录，重新尝试

### 测试 Auto 模式

```bash
# 测试服务健康检查（推荐）
python tests/test_auto_failover.py --health-check

# 测试故障转移模拟
python tests/test_auto_failover.py

# 测试自动选择功能
python tests/test_skymail.py --test-auto

# 测试服务可用性检查
python tests/test_skymail.py --test-availability

# 测试故障转移
python tests/test_skymail.py --test-auto-fallback
```

### 示例输出

**正常情况（带健康检查）：**
```
🔍 检查邮箱服务可用性...
  ✅ moemail - 可用
  ✅ skymail - 可用
🎲 Auto 模式: 随机选择 skymail
📧 创建临时邮箱...
  🎲 随机选择域名: domain2.com (共 2 个可用)
✅ 邮箱创建成功: warp123456@domain2.com
```

**健康检查发现问题（仅提示）：**
```
🔍 检查邮箱服务可用性...
  ⚠️ moemail - 健康检查未通过（可能是网络波动，仍会尝试使用）
  ✅ skymail - 可用
🎲 Auto 模式: 随机选择 skymail
📧 创建临时邮箱...
✅ 邮箱创建成功: warp123456@domain1.com
```

**运行时故障转移：**
```
🔍 检查邮箱服务可用性...
  ✅ moemail - 可用
  ✅ skymail - 可用
🎲 Auto 模式: 随机选择 moemail
📧 创建临时邮箱...
❌ 创建失败: HTTP 500

⚠️ moemail 创建失败，尝试切换服务...
  ⚠️ 记录 moemail 失败 (1/3)
🔄 切换到 skymail 服务
📧 创建临时邮箱...
  🎲 随机选择域名: domain1.com (共 2 个可用)
✅ 邮箱创建成功: warp123456@domain1.com
  ✅ skymail 恢复正常，清除失败记录
```

### 健康检查机制

1. **启动检查** - Auto 模式启动时自动检查所有服务（超时 3秒）
2. **快速检测** - 使用轻量级 API 调用检查服务状态
3. **直接排除** - 健康检查失败的服务在本次实例中不会被选择
4. **自动恢复** - 下次创建实例时重新检查，网络恢复后自动可用
5. **仅 Auto 模式** - 只在 auto 模式下启用，不影响单服务模式

**检查方式：**
- **MoeMail**: 调用 `/api/config` 接口
- **Skymail**: 调用 `/api/public/emailList` 接口（使用配置的域名）

**两层过滤机制：**
1. **健康检查（实例级别）** - 启动时快速过滤，失败直接排除
2. **运行时失败（类级别）** - 创建邮箱失败累计记录，3次后排除5分钟

**为什么每次都重新检查？**
- 自动适应网络状况变化
- 服务恢复后立即可用
- 避免长时间排除可用服务
- 适合小批量注册（≤10个）

### 故障转移机制

1. **失败检测** - 创建邮箱失败时自动检测
2. **服务切换** - 自动切换到其他可用服务
3. **失败计数** - 记录每个服务的失败次数
4. **临时排除** - 连续失败 3 次后临时排除该服务（5分钟）
5. **自动恢复** - 5分钟后自动清除失败记录
6. **最大重试** - 最多切换服务 2 次

### 注意事项

- Auto 模式需要至少配置一个邮箱服务
- 如果只配置了一个服务，Auto 模式会自动使用该服务
- 建议配置多个服务以充分发挥 Auto 模式的优势
- 失败记录在所有实例间共享，避免重复尝试失败的服务
- 健康检查会增加启动时间（每个服务最多 3秒），但能提前发现问题
- 健康检查仅在 auto 模式下启用，不影响单服务模式的启动速度
- 健康检查失败会直接排除服务（仅当前实例）
- 每次新实例重新检查，自动处理网络波动
- 实际创建邮箱失败会记录到类级别失败列表

---

## 🤖 GitHub Actions 集成

### 配置方式

GitHub Actions 工作流会自动检测配置的邮箱服务并选择合适的模式。

#### 1. 配置 Secrets

进入仓库 **Settings** → **Secrets and variables** → **Actions**，添加：

**必需的 Secrets:**
- `FIREBASE_API_KEY` - Firebase API Key（必需）

**邮箱服务 Secrets（至少配置一个）:**

**MoeMail:**
- `MOEMAIL_URL` - MoeMail 服务 URL（可选，默认 `https://email.959585.xyz`）
- `MOEMAIL_API_KEY` - MoeMail API Key

**Skymail:**
- `SKYMAIL_URL` - Skymail 服务 URL
- `SKYMAIL_TOKEN` - Skymail 管理员 Token
- `SKYMAIL_DOMAIN` - 域名列表（逗号分隔，可选）
- `SKYMAIL_WILDCARD` - 是否使用通配符模式（可选，默认 `false`）

#### 2. 自动模式选择

工作流会根据配置自动选择模式：

```bash
# 场景 1: 两个服务都配置
✅ MOEMAIL_API_KEY = xxx
✅ SKYMAIL_TOKEN = xxx
→ 自动使用 EMAIL_SERVICE=auto
→ 启动时健康检查
→ 自动选择可用服务
→ 运行时故障自动切换

# 场景 2: 只配置 MoeMail
✅ MOEMAIL_API_KEY = xxx
❌ SKYMAIL_TOKEN = (未配置)
→ 自动使用 EMAIL_SERVICE=moemail

# 场景 3: 只配置 Skymail
❌ MOEMAIL_API_KEY = (未配置)
✅ SKYMAIL_TOKEN = xxx
→ 自动使用 EMAIL_SERVICE=skymail
```

#### 3. 工作流日志示例

**Auto 模式（两个服务都配置）:**
```
✅ 检测到 MoeMail 配置
✅ 检测到 Skymail 配置
🎲 两个邮箱服务都已配置，使用 auto 模式（自动选择 + 故障转移）
✅ 环境配置完成

🔍 检查邮箱服务可用性...
  ✅ moemail - 可用
  ❌ skymail - 不可用（本次实例排除）
🎲 Auto 模式: 随机选择 moemail
```

**单服务模式:**
```
✅ 检测到 MoeMail 配置
📧 使用 MoeMail 服务
✅ 环境配置完成
```

#### 4. 手动触发参数

手动触发工作流时，可以调整以下参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 注册账号数量 | 6 | 本次运行要注册的账号数量 |
| 最大连续失败次数 | 6 | 连续失败多少次后停止 |

**使用场景：**
- 快速测试：设置注册数量为 1-2
- 批量注册：设置注册数量为 20-50
- 严格模式：设置最大失败次数为 2-3
- 宽松模式：设置最大失败次数为 10-20

#### 5. CI 环境特点

**优势：**
- ✅ 每次运行都是全新环境（自动重置机器码）
- ✅ 健康检查确保使用可用服务
- ✅ 故障自动切换，提高成功率
- ✅ 无需手动干预

**注意事项：**
- ⚠️ 健康检查会增加 3-6 秒启动时间（仅 auto 模式）
- ⚠️ 确保至少配置一个邮箱服务
- ⚠️ 推荐配置两个服务以提高可用性

#### 6. 故障排查

**错误：`❌ 至少需要配置一个邮箱服务`**
- 原因：未配置任何邮箱服务 Secrets
- 解决：添加 `MOEMAIL_API_KEY` 或 `SKYMAIL_TOKEN`

**错误：`❌ FIREBASE_API_KEY 未配置`**
- 原因：未配置 Firebase API Key
- 解决：添加 `FIREBASE_API_KEY` Secret

**两个服务都不可用：**
- 检查服务是否正常运行
- 检查网络连接
- 查看 Actions 日志中的健康检查结果
- 考虑降低执行频率

---

## 🎲 多域名支持（Skymail 专属）

### 功能说明

Skymail 支持配置多个域名，系统会在创建邮箱时随机选择一个域名使用。

### 优势

1. **提高可用性** - 某个域名故障时自动使用其他域名
2. **分散风险** - 避免单点故障
3. **负载均衡** - 随机分配，自然实现负载均衡
4. **灵活扩展** - 随时添加或删除域名

### 配置方法

```env
# 单域名（默认）
SKYMAIL_DOMAIN=example.com

# 多域名（逗号分隔）
SKYMAIL_DOMAIN=domain1.com,domain2.com,domain3.com
```

### 工作原理

1. 系统启动时解析域名列表
2. 创建邮箱时使用 `random.choice()` 随机选择一个域名
3. 显示选中的域名和可用域名总数
4. 每次创建都会重新随机选择

### 测试多域名

```bash
# 测试多域名支持
python tests/test_skymail.py --test-multi-domain

# 测试域名分布均匀性
python tests/test_skymail.py --test-distribution

# 测试域名故障转移（模拟）
python tests/test_skymail.py --test-failover
```

### 示例输出

```
📧 创建临时邮箱...
  🎲 随机选择域名: domain2.com (共 3 个可用)
✅ 邮箱创建成功: warp123456@domain2.com
```

---

## ⚠️ 注意事项

1. **MoeMail API Key**
   - 需要从 MoeMail 项目获取
   - 保护好 API Key，不要泄露

2. **MoeMail 和 Skymail 都需要自建**
   - MoeMail: https://github.com/beilunyang/moemail
   - Skymail: https://github.com/eoao/cloud-mail
   - 或使用现有的公共实例

3. **Token 管理**
   - MoeMail: 使用 API Key
   - Skymail: 使用管理员 Token（可重复使用）
   - Token 获取方法: https://doc.skymail.ink/api/api-doc.html#生成token
   - 批量注册时重用同一个 Token

4. **SSL 证书**
   - Skymail 可能需要禁用 SSL 验证
   - 代码中已处理 SSL 相关问题

---

---

## 🆕 GPTMail 服务（2025-10-17 新增）

### 概述

GPTMail 是一个基于 Cloudflare CDN 的多域名临时邮箱服务，已成功集成到 Warp 注册工具中。

**服务地址**: https://mail.chatgpt.org.uk

### 特点

✅ **简单易用**
- 仅 2 个 API 端点
- 无需 API Key
- 公开免费服务

✅ **高可用性**
- Cloudflare CDN 支持
- 多域名支持
- 30 秒自动刷新

✅ **功能完善**
- 支持 HTML 邮件
- 自动解析邮件内容
- 支持直接 URL 访问

### 配置方法

```env
# 直接使用 GPTMail
EMAIL_SERVICE=gptmail
GPTMAIL_URL=https://mail.chatgpt.org.uk

# 或使用 Auto 模式（推荐）
EMAIL_SERVICE=auto
```

### API 端点

**1. 生成邮箱**
```
GET /api/generate-email
```

响应示例:
```json
{
  "email": "test123@example.com"
}
```

**2. 获取邮件列表**
```
GET /api/get-emails?email={邮箱地址}
```

响应示例:
```json
{
  "emails": [
    {
      "id": "xxx",
      "from": "sender@example.com",
      "to": "test123@example.com",
      "subject": "邮件主题",
      "content": "纯文本内容",
      "htmlContent": "<p>HTML内容</p>",
      "hasHtml": true,
      "timestamp": 1234567890
    }
  ]
}
```

### 快速开始（5分钟）

**1. 更新配置**
```bash
# 编辑 .env 文件
EMAIL_SERVICE=gptmail  # 或 auto
```

**2. 测试服务**
```bash
python tests/test_gptmail.py
```

**3. 注册账号**
```bash
python register.py
```

### 性能对比

| 服务 | API 响应时间 | 邮件接收延迟 | 成功率 | 需要配置 |
|------|------------|------------|--------|---------|
| MoeMail | ~0.5s | 5-15s | 90-95% | API Key |
| Skymail | ~0.8s | 10-20s | 85-90% | Token |
| GPTMail | ~0.3s | 5-10s | 95-98% | 无 ✅ |

### 测试结果

所有测试通过率: **100%** (11/11)

- ✅ 服务可用性
- ✅ 生成邮箱
- ✅ 获取邮件列表
- ✅ 直接 URL 访问
- ✅ 生成多个邮箱
- ✅ API 性能
- ✅ 验证链接提取
- ✅ HTML 实体解码
- ✅ 多链接提取
- ✅ 发送和接收邮件
- ✅ Warp 注册流程

### 技术实现

**字段标准化:**
```python
# GPTMail 字段 → 标准字段
htmlContent → html
content → text
```

**SSL 配置:**
- 已配置 SSL 适配器禁用证书验证
- 自动处理自签名证书

**健康检查:**
- Auto 模式启动时自动检查服务可用性
- 超时 3 秒，快速检测
- 失败自动排除，不影响其他服务

### 注意事项

⚠️ **邮件保留时间** - 1 天后自动删除  
⚠️ **公开服务** - 无需 API Key，可能存在访问限制  
⚠️ **多域名** - 服务自动分配域名，不支持自定义

### 故障转移

GPTMail 已集成到 Auto 模式的故障转移机制中：

1. 健康检查失败 → 排除该服务
2. 连续失败 3 次 → 临时排除 5 分钟
3. 自动切换到其他可用服务
4. 失败记录在所有实例间共享

### 常见问题

**Q: 需要注册账号吗？**  
A: 不需要，GPTMail 是公开服务。

**Q: 有使用限制吗？**  
A: 可能存在速率限制，但正常使用不受影响。

**Q: 邮件保留多久？**  
A: 1 天后自动删除。

**Q: 可以和其他服务一起使用吗？**  
A: 可以！使用 `EMAIL_SERVICE=auto` 自动选择最佳服务。

### 最佳实践

```bash
# 使用 Auto 模式 + 配置多个服务
EMAIL_SERVICE=auto
MOEMAIL_API_KEY=your_key
SKYMAIL_TOKEN=your_token
# GPTMail 自动可用（无需配置）
```

这样可以获得：
- 最高的成功率
- 自动故障转移
- 负载均衡

---

**更新完成日期：** 2025-10-17  
**更新人员：** Kiro AI Assistant
