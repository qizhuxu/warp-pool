#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮箱服务
支持 MoeMail 和 Skymail (Cloud Mail) 两种临时邮箱服务
"""
import time
import requests
import random
import string
from typing import Optional, Dict, Any
from config import config


class EmailService:
    """邮箱服务类"""
    
    # 类级别的失败记录（所有实例共享）
    _failed_services = {}  # {service_name: {'count': int, 'last_fail_time': float}}
    _failure_threshold = 3  # 连续失败次数阈值
    _failure_timeout = 300  # 失败记录超时时间（秒），5分钟后重新尝试
    
    def __init__(self, service_type: str = 'moemail'):
        """
        初始化邮箱服务
        
        Args:
            service_type: 邮箱服务类型
                - 'moemail': MoeMail 服务（默认）
                - 'skymail': Skymail (Cloud Mail) 服务
                - 'auto': 自动选择可用服务
        """
        self.original_service_type = service_type.lower()
        self.session = requests.Session()
        
        # 配置 SSL 验证（适用于自建服务）
        self.session.verify = False
        
        # 禁用 SSL 警告
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self.token = None  # Skymail 使用
        self.retry_count = 0  # 当前重试次数
        self.max_retries = 2  # 最大重试次数（切换服务）
        
        # 实例级别：健康检查结果（每个实例独立）
        self._health_check_results = {}  # {'moemail': True, 'skymail': False}
        
        # 如果是 auto 模式，先进行健康检查，然后随机选择一个可用的服务
        if self.original_service_type == 'auto':
            print("🔍 检查邮箱服务可用性...")
            self._check_all_services_health()
            self.service_type = self._select_available_service()
            print(f"🎲 Auto 模式: 随机选择 {self.service_type}")
        else:
            self.service_type = self.original_service_type
        
        if self.service_type == 'skymail':
            self._init_skymail()
        else:
            self._init_moemail()
    
    def _select_available_service(self, exclude_services: list = None) -> str:
        """
        从可用服务中随机选择一个（排除失败的服务）
        
        Args:
            exclude_services: 要排除的服务列表
            
        Returns:
            选中的服务类型 ('moemail' 或 'skymail')
        """
        if exclude_services is None:
            exclude_services = []
        
        available_services = []
        
        # 检查 MoeMail 是否配置且未被排除
        if config.MOEMAIL_API_KEY and 'moemail' not in exclude_services:
            # 第一层：检查健康检查结果（实例级别）
            if not self._health_check_results.get('moemail', True):
                # 健康检查失败，跳过
                pass
            # 第二层：检查运行时失败记录（类级别）
            elif not self._is_service_failed('moemail'):
                available_services.append('moemail')
        
        # 检查 Skymail 是否配置且未被排除
        if getattr(config, 'SKYMAIL_TOKEN', '') and 'skymail' not in exclude_services:
            # 第一层：检查健康检查结果（实例级别）
            if not self._health_check_results.get('skymail', True):
                # 健康检查失败，跳过
                pass
            # 第二层：检查运行时失败记录（类级别）
            elif not self._is_service_failed('skymail'):
                available_services.append('skymail')
        
        if not available_services:
            # 如果所有服务都失败了，清除失败记录并重试
            print("⚠️ 所有服务都暂时不可用，清除失败记录并重试...")
            self._clear_failed_services()
            
            # 重新检查可用服务
            if config.MOEMAIL_API_KEY and 'moemail' not in exclude_services:
                available_services.append('moemail')
            if config.SKYMAIL_TOKEN and 'skymail' not in exclude_services:
                available_services.append('skymail')
            
            if not available_services:
                print("⚠️ 没有可用的邮箱服务，使用默认 moemail")
                return 'moemail'
        
        # 随机选择一个服务
        selected = random.choice(available_services)
        return selected
    
    @classmethod
    def _is_service_failed(cls, service_name: str) -> bool:
        """
        检查服务是否在失败记录中
        
        Args:
            service_name: 服务名称
            
        Returns:
            True 如果服务失败次数超过阈值且未超时
        """
        if service_name not in cls._failed_services:
            return False
        
        failure_info = cls._failed_services[service_name]
        current_time = time.time()
        
        # 检查是否超时（超时后重新尝试）
        if current_time - failure_info['last_fail_time'] > cls._failure_timeout:
            # 超时，清除该服务的失败记录
            del cls._failed_services[service_name]
            return False
        
        # 检查失败次数是否超过阈值
        return failure_info['count'] >= cls._failure_threshold
    
    @classmethod
    def _record_service_failure(cls, service_name: str):
        """
        记录服务失败
        
        Args:
            service_name: 服务名称
        """
        current_time = time.time()
        
        if service_name not in cls._failed_services:
            cls._failed_services[service_name] = {
                'count': 1,
                'last_fail_time': current_time
            }
            print(f"  ⚠️ 记录 {service_name} 失败 (1/{cls._failure_threshold})")
        else:
            cls._failed_services[service_name]['count'] += 1
            cls._failed_services[service_name]['last_fail_time'] = current_time
            count = cls._failed_services[service_name]['count']
            print(f"  ⚠️ 记录 {service_name} 失败 ({count}/{cls._failure_threshold})")
            
            if count >= cls._failure_threshold:
                print(f"  ❌ {service_name} 连续失败 {count} 次，临时排除（{cls._failure_timeout}秒后重试）")
    
    @classmethod
    def _record_service_success(cls, service_name: str):
        """
        记录服务成功（清除失败记录）
        
        Args:
            service_name: 服务名称
        """
        if service_name in cls._failed_services:
            del cls._failed_services[service_name]
            print(f"  ✅ {service_name} 恢复正常，清除失败记录")
    
    @classmethod
    def _clear_failed_services(cls):
        """清除所有失败记录"""
        cls._failed_services.clear()
        print("  🔄 已清除所有服务失败记录")
    
    @classmethod
    def _check_service_health(cls, service_name: str) -> bool:
        """
        检查服务健康状态
        
        Args:
            service_name: 服务名称 ('moemail' 或 'skymail')
            
        Returns:
            True 如果服务可用
        """
        try:
            if service_name == 'moemail':
                # 检查 MoeMail
                if not config.MOEMAIL_API_KEY:
                    return False
                
                url = f"{config.MOEMAIL_URL.rstrip('/')}/api/config"
                response = requests.get(
                    url,
                    headers={'X-API-Key': config.MOEMAIL_API_KEY},
                    timeout=3
                )
                return response.status_code == 200
                
            elif service_name == 'skymail':
                # 检查 Skymail
                skymail_token = getattr(config, 'SKYMAIL_TOKEN', '')
                if not skymail_token:
                    return False
                
                skymail_url = getattr(config, 'SKYMAIL_URL', 'https://cloudmail.qixc.pp.ua')
                url = f"{skymail_url.rstrip('/')}/api/public/emailList"
                
                # 使用配置的域名生成测试邮箱地址
                domains_str = getattr(config, 'SKYMAIL_DOMAIN', 'qixc.pp.ua')
                domains = [d.strip() for d in domains_str.split(',') if d.strip()]
                test_domain = domains[0] if domains else 'qixc.pp.ua'
                test_email = f"healthcheck@{test_domain}"
                
                # 禁用 SSL 警告
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                
                response = requests.post(
                    url,
                    headers={
                        'Authorization': skymail_token,
                        'Content-Type': 'application/json'
                    },
                    json={
                        'toEmail': test_email,
                        'type': 0,
                        'isDel': 0,
                        'timeSort': 'desc',
                        'num': 1,
                        'size': 1
                    },
                    timeout=3
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('code') == 200
                return False
                
        except Exception:
            return False
        
        return False
    
    def _check_all_services_health(self):
        """检查所有已配置服务的健康状态并存储结果"""
        services_to_check = []
        
        if config.MOEMAIL_API_KEY:
            services_to_check.append('moemail')
        if getattr(config, 'SKYMAIL_TOKEN', ''):
            services_to_check.append('skymail')
        
        if not services_to_check:
            return
        
        for service in services_to_check:
            is_healthy = self._check_service_health(service)
            
            # 存储到实例级别
            self._health_check_results[service] = is_healthy
            
            if is_healthy:
                print(f"  ✅ {service} - 可用")
            else:
                print(f"  ❌ {service} - 不可用（本次实例排除）")
    
    def _init_moemail(self):
        """初始化 MoeMail 服务"""
        self.base_url = config.MOEMAIL_URL.rstrip('/')
        self.api_key = config.MOEMAIL_API_KEY
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        })
    
    def _init_skymail(self):
        """初始化 Skymail 服务"""
        # 从配置读取 Skymail 设置
        self.base_url = getattr(config, 'SKYMAIL_URL', 'https://cloudmail.qixc.pp.ua').rstrip('/')
        self.token = getattr(config, 'SKYMAIL_TOKEN', '')
        
        # 解析域名列表（支持逗号分隔的多个域名）
        domains_str = getattr(config, 'SKYMAIL_DOMAIN', 'qixc.pp.ua')
        self.domains = [d.strip() for d in domains_str.split(',') if d.strip()]
        
        if not self.token:
            print("⚠️ SKYMAIL_TOKEN 未配置")
            return
        
        if not self.domains:
            print("⚠️ SKYMAIL_DOMAIN 未配置")
            return
        
        # 禁用 SSL 警告
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # 配置 SSL 适配器
        from requests.adapters import HTTPAdapter
        from urllib3.util.ssl_ import create_urllib3_context
        
        class SSLAdapter(HTTPAdapter):
            def init_poolmanager(self, *args, **kwargs):
                context = create_urllib3_context()
                context.load_default_certs()
                context.set_ciphers('DEFAULT@SECLEVEL=1')
                kwargs['ssl_context'] = context
                return super().init_poolmanager(*args, **kwargs)
        
        self.session.mount('https://', SSLAdapter())
    
    def create_email(self, prefix: str = None, domain: str = None) -> Optional[Dict[str, Any]]:
        """创建临时邮箱（支持故障转移）"""
        print("📧 创建临时邮箱...")
        
        # 尝试创建邮箱
        result = self._create_email_internal(prefix, domain)
        
        # 如果是 auto 模式且创建失败，尝试切换服务
        if result is None and self.original_service_type == 'auto' and self.retry_count < self.max_retries:
            print(f"\n⚠️ {self.service_type} 创建失败，尝试切换服务...")
            
            # 记录当前服务失败
            self._record_service_failure(self.service_type)
            
            # 排除当前失败的服务
            excluded = [self.service_type]
            
            # 选择另一个服务
            new_service = self._select_available_service(exclude_services=excluded)
            
            if new_service != self.service_type:
                print(f"🔄 切换到 {new_service} 服务")
                self.service_type = new_service
                self.retry_count += 1
                
                # 重新初始化服务
                if self.service_type == 'skymail':
                    self._init_skymail()
                else:
                    self._init_moemail()
                
                # 递归调用，重新尝试创建
                return self.create_email(prefix, domain)
            else:
                print(f"❌ 没有其他可用服务")
        
        # 如果成功，记录成功
        if result is not None:
            self._record_service_success(self.service_type)
        
        return result
    
    def _create_email_internal(self, prefix: str = None, domain: str = None) -> Optional[Dict[str, Any]]:
        """内部创建邮箱方法"""
        if self.service_type == 'skymail':
            return self._create_skymail(prefix, domain)
        else:
            return self._create_moemail(prefix, domain)
    
    def _create_moemail(self, prefix: str = None, domain: str = None) -> Optional[Dict[str, Any]]:
        """使用 MoeMail 创建邮箱"""
        try:
            # 生成随机前缀
            if not prefix:
                words = ['warp', 'test', 'demo', 'user', 'temp']
                word = random.choice(words)
                chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                prefix = f"{word}{chars}"
            
            # 获取可用域名
            if not domain:
                try:
                    config_response = self.session.get(f"{self.base_url}/api/config")
                    if config_response.status_code == 200:
                        config_data = config_response.json()
                        domains = [d.strip() for d in config_data.get('emailDomains', '959585.xyz').split(',')]
                        domain = random.choice(domains)
                    else:
                        domain = '959585.xyz'
                except:
                    domain = '959585.xyz'
            
            # 创建邮箱
            data = {
                "name": prefix,
                "domain": domain,
                "expiryTime": 3600000  # 1小时
            }
            
            response = self.session.post(
                f"{self.base_url}/api/emails/generate",
                json=data
            )
            
            if response.status_code != 200:
                print(f"❌ 创建失败: HTTP {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                return None
            
            result = response.json()
            email_info = {
                "id": result["id"],
                "address": result["email"],
                "prefix": prefix,
                "domain": domain,
                "service": "moemail"
            }
            
            print(f"✅ 邮箱创建成功: {email_info['address']}")
            return email_info
            
        except Exception as e:
            print(f"❌ 创建邮箱失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_skymail(self, prefix: str = None, domain: str = None) -> Optional[Dict[str, Any]]:
        """使用 Skymail 创建邮箱"""
        try:
            if not self.token:
                print("❌ Skymail Token 未生成")
                return None
            
            # 生成随机前缀
            if not prefix:
                words = ['warp', 'test', 'demo', 'user', 'temp']
                word = random.choice(words)
                chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                prefix = f"{word}{chars}"
            
            # 使用配置的域名或随机选择一个域名
            if not domain:
                if hasattr(self, 'domains') and self.domains:
                    domain = random.choice(self.domains)
                    if len(self.domains) > 1:
                        print(f"  🎲 随机选择域名: {domain} (共 {len(self.domains)} 个可用)")
                    else:
                        print(f"  📧 使用域名: {domain}")
                else:
                    domain = 'qixc.pp.ua'
            
            email_address = f"{prefix}@{domain}"
            
            # 检查是否启用通配符模式
            wildcard_mode = getattr(config, 'SKYMAIL_WILDCARD', False)
            
            if wildcard_mode:
                # 通配符模式：无需注册，直接返回邮箱信息
                print(f"✅ 邮箱创建成功（通配符模式）: {email_address}")
                email_info = {
                    "id": email_address,
                    "address": email_address,
                    "prefix": prefix,
                    "domain": domain,
                    "service": "skymail",
                    "wildcard": True
                }
                return email_info
            
            # 普通模式：需要注册邮箱
            # 生成随机密码
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            # 添加用户
            url = f"{self.base_url}/api/public/addUser"
            headers = {
                "Authorization": self.token,
                "Content-Type": "application/json"
            }
            data = {
                "list": [
                    {
                        "email": email_address,
                        "password": password
                    }
                ]
            }
            
            response = self.session.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ 创建失败: HTTP {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                return None
            
            result = response.json()
            if result.get('code') != 200:
                print(f"❌ 创建失败: {result.get('message')}")
                return None
            
            email_info = {
                "id": email_address,  # Skymail 使用邮箱地址作为 ID
                "address": email_address,
                "prefix": prefix,
                "domain": domain,
                "password": password,
                "service": "skymail",
                "wildcard": False
            }
            
            print(f"✅ 邮箱创建成功: {email_info['address']}")
            return email_info
            
        except Exception as e:
            print(f"❌ 创建邮箱失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def wait_for_email(self, email_info: Dict[str, Any], timeout: int = None) -> Optional[Dict[str, Any]]:
        """等待接收邮件"""
        if timeout is None:
            timeout = config.EMAIL_TIMEOUT
        
        print(f"📬 等待验证邮件 (超时: {timeout}秒)...")
        
        service = email_info.get('service', 'moemail')
        
        if service == 'skymail':
            return self._wait_for_skymail(email_info['address'], timeout)
        else:
            return self._wait_for_moemail(email_info['id'], timeout)
    
    def _wait_for_moemail(self, email_id: str, timeout: int) -> Optional[Dict[str, Any]]:
        """等待 MoeMail 邮件"""
        start_time = time.time()
        check_count = 0
        
        while time.time() - start_time < timeout:
            check_count += 1
            
            try:
                response = self.session.get(f"{self.base_url}/api/emails/{email_id}")
                
                if response.status_code == 200:
                    result = response.json()
                    messages = result.get("messages", [])
                    
                    if messages:
                        print(f"  📨 收到 {len(messages)} 封邮件")
                        
                        for msg in messages:
                            subject = msg.get("subject", "")
                            if "warp" in subject.lower() or "sign in" in subject.lower():
                                print(f"  ✅ 找到验证邮件: {subject}")
                                return {
                                    "subject": msg.get("subject", ""),
                                    "html": msg.get("html", ""),
                                    "text": msg.get("content", "")
                                }
                        
                        print(f"  ⚠️ 没有找到匹配的验证邮件")
                
                elapsed = int(time.time() - start_time)
                if check_count % 2 == 0:
                    print(f"  ⏳ 检查中... ({elapsed}/{timeout}秒)")
                
                sleep_time = 3 if elapsed < 30 else 5
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"⚠️ 检查邮件出错: {e}")
                time.sleep(5)
        
        print("❌ 等待邮件超时")
        return None
    
    def _wait_for_skymail(self, email_address: str, timeout: int) -> Optional[Dict[str, Any]]:
        """等待 Skymail 邮件"""
        if not self.token:
            print("❌ Skymail Token 未生成")
            return None
        
        start_time = time.time()
        check_count = 0
        
        while time.time() - start_time < timeout:
            check_count += 1
            
            try:
                url = f"{self.base_url}/api/public/emailList"
                headers = {
                    "Authorization": self.token,
                    "Content-Type": "application/json"
                }
                data = {
                    "toEmail": email_address,
                    "type": 0,  # 0 收件
                    "isDel": 0,  # 0 正常
                    "timeSort": "desc",
                    "num": 1,
                    "size": 20
                }
                
                response = self.session.post(url, json=data, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('code') == 200:
                        emails = result.get('data', [])
                        
                        if emails:
                            print(f"  📨 收到 {len(emails)} 封邮件")
                            
                            for email in emails:
                                subject = email.get('subject', '')
                                if "warp" in subject.lower() or "sign in" in subject.lower():
                                    print(f"  ✅ 找到验证邮件: {subject}")
                                    return {
                                        "subject": email.get('subject', ''),
                                        "html": email.get('content', ''),
                                        "text": email.get('text', '')
                                    }
                            
                            print(f"  ⚠️ 没有找到匹配的验证邮件")
                
                elapsed = int(time.time() - start_time)
                if check_count % 2 == 0:
                    print(f"  ⏳ 检查中... ({elapsed}/{timeout}秒)")
                
                sleep_time = 3 if elapsed < 30 else 5
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"⚠️ 检查邮件出错: {e}")
                time.sleep(5)
        
        print("❌ 等待邮件超时")
        return None
    
    def extract_verification_link(self, email_html: str) -> Optional[str]:
        """从邮件中提取验证链接"""
        import re
        import html as html_module
        
        try:
            link_pattern = r'href=["\']([^"\']*firebaseapp\.com[^"\']*)["\']'
            matches = re.findall(link_pattern, email_html)
            
            for link in matches:
                if 'auth/action' in link:
                    link = html_module.unescape(link)
                    print(f"✅ 提取到验证链接")
                    return link
            
            print("❌ 未找到验证链接")
            return None
            
        except Exception as e:
            print(f"❌ 提取链接失败: {e}")
            return None
