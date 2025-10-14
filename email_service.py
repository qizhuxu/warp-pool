#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮箱服务
"""
import time
import requests
from typing import Optional, Dict, Any
from config import config


class EmailService:
    """邮箱服务类"""
    
    def __init__(self, use_1secmail: bool = False):
        self.use_1secmail = use_1secmail
        
        if use_1secmail:
            self.base_url = 'https://www.1secmail.com/api/v1/'
            self.session = requests.Session()
        else:
            self.base_url = config.MOEMAIL_URL.rstrip('/')
            self.api_key = config.MOEMAIL_API_KEY
            self.session = requests.Session()
            self.session.headers.update({
                'X-API-Key': self.api_key,  # 使用 X-API-Key 而不是 Bearer
                'Content-Type': 'application/json'
            })
    
    def create_email(self, prefix: str = None, domain: str = None) -> Optional[Dict[str, Any]]:
        """创建临时邮箱"""
        print("📧 创建临时邮箱...")
        
        if self.use_1secmail:
            return self._create_1secmail()
        else:
            return self._create_moemail(prefix, domain)
    
    def _create_1secmail(self) -> Optional[Dict[str, Any]]:
        """使用 1secmail 创建邮箱"""
        try:
            # 获取随机邮箱
            response = self.session.get(
                f"{self.base_url}?action=genRandomMailbox&count=1"
            )
            
            if response.status_code != 200:
                print(f"❌ 创建失败: HTTP {response.status_code}")
                return None
            
            emails = response.json()
            if not emails:
                print("❌ 未获取到邮箱")
                return None
            
            email_address = emails[0]
            # 分离用户名和域名
            username, domain = email_address.split('@')
            
            email_info = {
                "id": email_address,  # 1secmail 使用完整邮箱地址作为 ID
                "address": email_address,
                "username": username,
                "domain": domain
            }
            
            print(f"✅ 邮箱创建成功: {email_info['address']}")
            return email_info
            
        except Exception as e:
            print(f"❌ 创建邮箱失败: {e}")
            return None
    
    def _create_moemail(self, prefix: str = None, domain: str = None) -> Optional[Dict[str, Any]]:
        """使用 MoeMail 创建邮箱"""
        import random
        import string
        
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
                f"{self.base_url}/api/emails/generate",  # 使用正确的端点
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
                "domain": domain
            }
            
            print(f"✅ 邮箱创建成功: {email_info['address']}")
            return email_info
            
        except Exception as e:
            print(f"❌ 创建邮箱失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def wait_for_email(self, email_id: str, timeout: int = None) -> Optional[Dict[str, Any]]:
        """等待接收邮件"""
        if timeout is None:
            timeout = config.EMAIL_TIMEOUT
        
        print(f"📬 等待验证邮件 (超时: {timeout}秒)...")
        
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
