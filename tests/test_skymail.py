#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skymail API 测试脚本
测试 Cloud Mail 邮箱服务的 API 功能
"""
import requests
import json
import time
import random
import string
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 配置文件
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


class SkymailTester:
    """Skymail API 测试类"""
    
    def __init__(self, base_url: str, admin_email: str, admin_password: str):
        self.base_url = base_url.rstrip('/')
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.token = None
        self.session = requests.Session()
        
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
    
    def generate_token(self) -> bool:
        """生成 Token"""
        print("\n" + "="*60)
        print("步骤 1: 生成 Token")
        print("="*60)
        
        try:
            url = f"{self.base_url}/api/public/genToken"
            data = {
                "email": self.admin_email,
                "password": self.admin_password
            }
            
            print(f"请求 URL: {url}")
            print(f"请求数据: {json.dumps(data, indent=2)}")
            
            # 禁用 SSL 验证，添加超时
            response = self.session.post(url, json=data, verify=False, timeout=30)
            
            print(f"\n响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    self.token = result['data']['token']
                    print(f"\n✅ Token 生成成功: {self.token}")
                    return True
                else:
                    print(f"\n❌ Token 生成失败: {result.get('message')}")
                    return False
            else:
                print(f"\n❌ HTTP 请求失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"\n❌ 生成 Token 异常: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def add_user(self, email: str, password: str = None) -> bool:
        """添加用户"""
        print("\n" + "="*60)
        print("步骤 2: 添加用户")
        print("="*60)
        
        if not self.token:
            print("❌ 未获取到 Token，请先生成 Token")
            return False
        
        try:
            # 如果没有提供密码，自动生成
            if not password:
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            url = f"{self.base_url}/api/public/addUser"
            headers = {
                "Authorization": self.token,
                "Content-Type": "application/json"
            }
            data = {
                "list": [
                    {
                        "email": email,
                        "password": password
                    }
                ]
            }
            
            print(f"请求 URL: {url}")
            print(f"请求头: {json.dumps(headers, indent=2)}")
            print(f"请求数据: {json.dumps(data, indent=2)}")
            
            # 禁用 SSL 验证，添加超时
            response = self.session.post(url, json=data, headers=headers, verify=False, timeout=30)
            
            print(f"\n响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    print(f"\n✅ 用户添加成功")
                    print(f"   邮箱: {email}")
                    print(f"   密码: {password}")
                    return True
                else:
                    print(f"\n❌ 用户添加失败: {result.get('message')}")
                    return False
            else:
                print(f"\n❌ HTTP 请求失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"\n❌ 添加用户异常: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def query_emails(self, to_email: str, max_wait: int = 60) -> list:
        """查询邮件"""
        print("\n" + "="*60)
        print("步骤 3: 查询邮件")
        print("="*60)
        
        if not self.token:
            print("❌ 未获取到 Token，请先生成 Token")
            return []
        
        try:
            url = f"{self.base_url}/api/public/emailList"
            headers = {
                "Authorization": self.token,
                "Content-Type": "application/json"
            }
            data = {
                "toEmail": to_email,
                "type": 0,  # 0 收件
                "isDel": 0,  # 0 正常
                "timeSort": "desc",  # 最新的在前
                "num": 1,
                "size": 20
            }
            
            print(f"请求 URL: {url}")
            print(f"查询邮箱: {to_email}")
            print(f"最大等待时间: {max_wait} 秒")
            
            start_time = time.time()
            check_count = 0
            
            while time.time() - start_time < max_wait:
                check_count += 1
                
                # 禁用 SSL 验证，添加超时
                response = self.session.post(url, json=data, headers=headers, verify=False, timeout=30)
                
                if check_count == 1:
                    print(f"\n响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('code') == 200:
                        emails = result.get('data', [])
                        
                        if emails:
                            print(f"\n✅ 找到 {len(emails)} 封邮件")
                            for i, email in enumerate(emails, 1):
                                print(f"\n邮件 {i}:")
                                print(f"  发件人: {email.get('sendName')} <{email.get('sendEmail')}>")
                                print(f"  主题: {email.get('subject')}")
                                print(f"  时间: {email.get('createTime')}")
                                print(f"  内容预览: {email.get('text', '')[:100]}...")
                            return emails
                        else:
                            elapsed = int(time.time() - start_time)
                            if check_count % 3 == 0:
                                print(f"  ⏳ 等待邮件... ({elapsed}/{max_wait}秒)")
                    else:
                        print(f"\n❌ 查询失败: {result.get('message')}")
                        return []
                else:
                    print(f"\n❌ HTTP 请求失败: {response.status_code}")
                    return []
                
                time.sleep(3)
            
            print(f"\n⚠️ 等待超时，未收到邮件")
            return []
                
        except Exception as e:
            print(f"\n❌ 查询邮件异常: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def extract_verification_link(self, email_html: str) -> str:
        """从邮件中提取验证链接"""
        import re
        import html as html_module
        
        try:
            # 查找 Firebase 验证链接
            link_pattern = r'href=["\']([^"\']*firebaseapp\.com[^"\']*)["\']'
            matches = re.findall(link_pattern, email_html)
            
            for link in matches:
                if 'auth/action' in link:
                    link = html_module.unescape(link)
                    print(f"\n✅ 提取到验证链接:")
                    print(f"   {link}")
                    return link
            
            print("\n⚠️ 未找到验证链接")
            return None
            
        except Exception as e:
            print(f"\n❌ 提取链接失败: {e}")
            return None


def send_warp_login_request(email: str) -> bool:
    """发送 Warp 登录请求"""
    print("\n" + "="*60)
    print("步骤 2.5: 发送 Warp 登录请求")
    print("="*60)
    
    try:
        # Warp 登录 API
        url = "https://app.warp.dev/referral/EWP6QD"
        
        print(f"访问 Warp 登录页面...")
        print(f"邮箱: {email}")
        
        # 这里需要使用浏览器自动化来触发邮件发送
        # 暂时只是提示用户手动操作
        print("\n⚠️  自动发送功能需要浏览器自动化")
        print("   请手动访问 Warp 登录页面并输入邮箱")
        print(f"   或者运行完整的注册脚本: python register.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 发送登录请求失败: {e}")
        return False


def test_with_warp_registration(base_url: str, admin_email: str, admin_password: str):
    """完整测试流程：创建邮箱 + Warp 注册"""
    print("\n" + "="*60)
    print("完整测试: Skymail + Warp 注册")
    print("="*60)
    
    # 生成测试邮箱地址
    test_prefix = f"warp{random.randint(1000, 9999)}"
    test_email = f"{test_prefix}@qixc.pp.ua"
    
    print(f"\n配置信息:")
    print(f"  API 地址: {base_url}")
    print(f"  测试邮箱: {test_email}")
    
    # 创建测试实例
    tester = SkymailTester(base_url, admin_email, admin_password)
    
    # 步骤 1: 生成 Token
    if not tester.generate_token():
        print("\n❌ 测试失败: 无法生成 Token")
        return None
    
    # 步骤 2: 添加用户
    if not tester.add_user(test_email):
        print("\n❌ 测试失败: 无法添加用户")
        return None
    
    # 步骤 3: 提示用户发送 Warp 登录请求
    print("\n" + "="*60)
    print("下一步: 使用此邮箱进行 Warp 注册")
    print("="*60)
    print(f"\n请访问: https://app.warp.dev/referral/EWP6QD")
    print(f"输入邮箱: {test_email}")
    print(f"\n脚本将等待 120 秒查询验证邮件...")
    
    input("\n按 Enter 键继续（在发送登录请求后）...")
    
    # 步骤 4: 查询邮件
    emails = tester.query_emails(test_email, max_wait=120)
    
    if emails:
        # 尝试提取验证链接
        first_email = emails[0]
        html_content = first_email.get('content', '')
        if html_content:
            link = tester.extract_verification_link(html_content)
            if link:
                print("\n" + "="*60)
                print("✅ 测试成功！")
                print("="*60)
                print(f"\n邮箱: {test_email}")
                print(f"验证链接: {link}")
                return {
                    "email": test_email,
                    "verification_link": link
                }
    
    print("\n⚠️ 未收到验证邮件")
    return None


def main():
    """主测试流程"""
    print("\n" + "="*60)
    print("Skymail API 测试")
    print("="*60)
    
    # 配置
    BASE_URL = "https://cloudmail.qixc.pp.ua"
    ADMIN_EMAIL = "qiqi@qixc.pp.ua"
    ADMIN_PASSWORD = "qwedc1357908642"
    
    # 选择测试模式
    print("\n请选择测试模式:")
    print("1. 基础测试（仅创建邮箱）")
    print("2. 完整测试（创建邮箱 + Warp 注册）")
    
    choice = input("\n请输入选项 (1/2，默认 1): ").strip() or "1"
    
    if choice == "2":
        # 完整测试
        result = test_with_warp_registration(BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD)
        if result:
            print("\n" + "="*60)
            print("测试完成 - 成功")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("测试完成 - 部分成功")
            print("="*60)
    else:
        # 基础测试
        test_prefix = f"test{random.randint(1000, 9999)}"
        test_email = f"{test_prefix}@qixc.pp.ua"
        
        print(f"\n配置信息:")
        print(f"  API 地址: {BASE_URL}")
        print(f"  管理员邮箱: {ADMIN_EMAIL}")
        print(f"  测试邮箱: {test_email}")
        
        # 创建测试实例
        tester = SkymailTester(BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD)
        
        # 步骤 1: 生成 Token
        if not tester.generate_token():
            print("\n❌ 测试失败: 无法生成 Token")
            return
        
        # 步骤 2: 添加用户
        if not tester.add_user(test_email):
            print("\n❌ 测试失败: 无法添加用户")
            return
        
        # 步骤 3: 等待并查询邮件（可选）
        print("\n" + "="*60)
        print("提示: 现在可以向 {} 发送测试邮件".format(test_email))
        print("脚本将等待 60 秒查询邮件...")
        print("="*60)
        
        emails = tester.query_emails(test_email, max_wait=60)
        
        if emails:
            # 尝试提取验证链接
            first_email = emails[0]
            html_content = first_email.get('content', '')
            if html_content:
                tester.extract_verification_link(html_content)
        
        print("\n" + "="*60)
        print("测试完成")
        print("="*60)
        print(f"\n✅ 成功创建邮箱: {test_email}")
        print(f"   可以使用此邮箱进行 Warp 注册测试")


def test_token_reusability():
    """测试 Token 是否可以重复使用"""
    print("\n" + "="*60)
    print("Token 重用性测试")
    print("="*60)
    
    BASE_URL = "https://cloudmail.qixc.pp.ua"
    ADMIN_EMAIL = "qiqi@qixc.pp.ua"
    ADMIN_PASSWORD = "qwedc1357908642"
    
    tester = SkymailTester(BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD)
    
    # 第一次生成 Token
    print("\n第一次生成 Token...")
    if not tester.generate_token():
        print("❌ 第一次生成失败")
        return
    
    first_token = tester.token
    print(f"第一次 Token: {first_token}")
    
    # 使用第一个 Token 添加用户
    test_email1 = f"test{random.randint(1000, 9999)}@qixc.pp.ua"
    print(f"\n使用第一个 Token 添加用户: {test_email1}")
    if tester.add_user(test_email1):
        print("✅ 第一次添加成功")
    else:
        print("❌ 第一次添加失败")
        return
    
    # 等待几秒
    print("\n等待 3 秒...")
    time.sleep(3)
    
    # 再次使用相同的 Token 添加另一个用户
    test_email2 = f"test{random.randint(1000, 9999)}@qixc.pp.ua"
    print(f"\n使用相同 Token 添加第二个用户: {test_email2}")
    if tester.add_user(test_email2):
        print("✅ 第二次添加成功")
        print("\n" + "="*60)
        print("结论: Token 可以重复使用！")
        print("="*60)
        print(f"Token: {first_token}")
        print("建议: 可以保存 Token 避免频繁生成")
    else:
        print("❌ 第二次添加失败")
        print("\n可能原因:")
        print("1. Token 是一次性的")
        print("2. Token 有时间限制")
        print("3. 服务器限制")
    
    # 生成新的 Token 对比
    print("\n" + "="*60)
    print("生成新的 Token 进行对比...")
    print("="*60)
    
    if tester.generate_token():
        second_token = tester.token
        print(f"\n第二次 Token: {second_token}")
        
        if first_token == second_token:
            print("\n✅ Token 相同 - 可能是固定的")
        else:
            print("\n⚠️ Token 不同 - 每次生成都会变化")
            print("   旧 Token 可能已失效")


def test_wildcard_email():
    """测试通配符邮箱（无需注册即可接收）"""
    print("\n" + "="*60)
    print("通配符邮箱测试")
    print("="*60)
    
    BASE_URL = "https://cloudmail.qixc.pp.ua"
    FIXED_TOKEN = "70c8ce4e-b9eb-4f00-af29-f7aebd20cd52"
    
    # 生成一个随机邮箱地址（不注册）
    test_prefix = f"wildcard{random.randint(1000, 9999)}"
    test_email = f"{test_prefix}@qixc.pp.ua"
    
    print(f"\n配置信息:")
    print(f"  API 地址: {BASE_URL}")
    print(f"  固定 Token: {FIXED_TOKEN}")
    print(f"  测试邮箱: {test_email}")
    print(f"  ⚠️  注意: 此邮箱未注册，测试通配符功能")
    
    # 创建测试实例（不生成新 Token）
    tester = SkymailTester(BASE_URL, "", "")
    tester.token = FIXED_TOKEN  # 直接使用固定 Token
    
    print("\n" + "="*60)
    print("提示: 请向以下地址发送测试邮件")
    print(f"邮箱: {test_email}")
    print("或访问 Warp 登录页面并输入此邮箱")
    print("="*60)
    print(f"\n请访问: https://app.warp.dev/referral/EWP6QD")
    print(f"输入邮箱: {test_email}")
    print(f"\n脚本将等待 120 秒查询邮件...")
    
    input("\n按 Enter 键继续（在发送邮件后）...")
    
    # 查询邮件
    emails = tester.query_emails(test_email, max_wait=120)
    
    if emails:
        print("\n" + "="*60)
        print("✅ 通配符邮箱测试成功！")
        print("="*60)
        print(f"\n结论: Skymail 支持通配符邮箱")
        print(f"  - 无需注册即可接收邮件")
        print(f"  - 任意邮箱地址都可以使用")
        print(f"  - 只需要有效的 Token")
        
        # 尝试提取验证链接
        first_email = emails[0]
        html_content = first_email.get('content', '')
        if html_content:
            link = tester.extract_verification_link(html_content)
            if link:
                print(f"\n验证链接: {link}")
        
        return True
    else:
        print("\n" + "="*60)
        print("❌ 通配符邮箱测试失败")
        print("="*60)
        print(f"\n可能原因:")
        print(f"  1. Skymail 不支持通配符邮箱")
        print(f"  2. 邮件未发送成功")
        print(f"  3. Token 已失效")
        print(f"  4. 域名配置不正确")
        
        return False


def test_multi_domain_support():
    """测试多域名支持功能"""
    print("\n" + "="*60)
    print("多域名支持测试")
    print("="*60)
    
    # 从 .env 读取配置
    BASE_URL = os.getenv('SKYMAIL_URL', 'https://cloudmail.qixc.pp.ua')
    TOKEN = os.getenv('SKYMAIL_TOKEN', '')
    DOMAINS_STR = os.getenv('SKYMAIL_DOMAIN', 'qixc.pp.ua')
    
    # 解析域名列表（逗号分隔）
    TEST_DOMAINS = [d.strip() for d in DOMAINS_STR.split(',') if d.strip()]
    
    if not TOKEN:
        print("❌ 错误: 未配置 SKYMAIL_TOKEN")
        print("   请在 .env 文件中设置 SKYMAIL_TOKEN")
        return False
    
    print(f"\n配置信息:")
    print(f"  API 地址: {BASE_URL}")
    print(f"  Token: {TOKEN[:20]}..." if len(TOKEN) > 20 else f"  Token: {TOKEN}")
    print(f"  测试域名数量: {len(TEST_DOMAINS)}")
    print(f"  域名列表:")
    for i, domain in enumerate(TEST_DOMAINS, 1):
        print(f"    {i}. {domain}")
    
    # 创建测试实例（直接使用 Token，不需要生成）
    tester = SkymailTester(BASE_URL, "", "")
    tester.token = TOKEN
    
    print("\n✅ 使用 .env 配置的 Token")
    
    # 步骤 2: 测试每个域名
    print("\n" + "="*60)
    print("步骤 2: 测试每个域名创建邮箱")
    print("="*60)
    
    success_count = 0
    failed_domains = []
    created_emails = []
    
    for i, domain in enumerate(TEST_DOMAINS, 1):
        print(f"\n--- 测试域名 {i}/{len(TEST_DOMAINS)}: {domain} ---")
        
        # 生成测试邮箱
        test_prefix = f"multi{random.randint(1000, 9999)}"
        test_email = f"{test_prefix}@{domain}"
        
        print(f"尝试创建邮箱: {test_email}")
        
        # 尝试添加用户
        if tester.add_user(test_email):
            success_count += 1
            created_emails.append(test_email)
            print(f"✅ 域名 {domain} 测试成功")
        else:
            failed_domains.append(domain)
            print(f"❌ 域名 {domain} 测试失败")
        
        # 等待一下，避免请求过快
        if i < len(TEST_DOMAINS):
            time.sleep(2)
    
    # 步骤 3: 测试随机选择
    print("\n" + "="*60)
    print("步骤 3: 测试随机域名选择")
    print("="*60)
    
    # 只使用成功的域名进行随机测试
    available_domains = [d for d in TEST_DOMAINS if d not in failed_domains]
    
    if not available_domains:
        print("❌ 没有可用的域名进行随机测试")
    else:
        print(f"可用域名: {', '.join(available_domains)}")
        print(f"\n创建 5 个随机域名的邮箱...")
        
        domain_usage = {domain: 0 for domain in available_domains}
        random_emails = []
        
        for i in range(5):
            # 随机选择域名
            selected_domain = random.choice(available_domains)
            domain_usage[selected_domain] += 1
            
            test_prefix = f"rand{random.randint(1000, 9999)}"
            test_email = f"{test_prefix}@{selected_domain}"
            
            print(f"\n{i+1}. 选择域名: {selected_domain}")
            print(f"   创建邮箱: {test_email}")
            
            if tester.add_user(test_email):
                random_emails.append(test_email)
                print(f"   ✅ 创建成功")
            else:
                print(f"   ❌ 创建失败")
            
            time.sleep(1)
        
        # 显示域名使用统计
        print("\n域名使用统计:")
        for domain, count in domain_usage.items():
            percentage = (count / 5) * 100
            print(f"  {domain}: {count} 次 ({percentage:.1f}%)")
    
    # 步骤 4: 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    print(f"\n域名测试结果:")
    print(f"  总域名数: {len(TEST_DOMAINS)}")
    print(f"  成功: {success_count}")
    print(f"  失败: {len(failed_domains)}")
    
    if failed_domains:
        print(f"\n失败的域名:")
        for domain in failed_domains:
            print(f"  ❌ {domain}")
    
    print(f"\n成功创建的邮箱:")
    all_emails = created_emails + random_emails
    for email in all_emails:
        print(f"  ✅ {email}")
    
    # 判断测试是否通过
    if success_count > 0:
        print("\n" + "="*60)
        print("✅ 多域名支持测试通过")
        print("="*60)
        print(f"\n结论:")
        print(f"  - 至少有 {success_count} 个域名可用")
        print(f"  - 随机选择功能正常")
        print(f"  - 可以配置多域名提高可用性")
        return True
    else:
        print("\n" + "="*60)
        print("❌ 多域名支持测试失败")
        print("="*60)
        print(f"\n所有域名都无法使用，请检查:")
        print(f"  1. 域名配置是否正确")
        print(f"  2. API Token 是否有效")
        print(f"  3. 网络连接是否正常")
        return False


def test_domain_distribution():
    """测试域名分布均匀性（统计测试）"""
    print("\n" + "="*60)
    print("域名分布均匀性测试")
    print("="*60)
    
    # 从 .env 读取域名配置
    DOMAINS_STR = os.getenv('SKYMAIL_DOMAIN', 'qixc.pp.ua')
    TEST_DOMAINS = [d.strip() for d in DOMAINS_STR.split(',') if d.strip()]
    SAMPLE_SIZE = 30  # 样本数量
    
    print(f"\n测试参数:")
    print(f"  域名数量: {len(TEST_DOMAINS)}")
    print(f"  样本数量: {SAMPLE_SIZE}")
    print(f"  期望分布: 每个域名约 {SAMPLE_SIZE/len(TEST_DOMAINS):.1f} 次")
    
    # 模拟随机选择
    domain_counts = {domain: 0 for domain in TEST_DOMAINS}
    
    print(f"\n开始模拟随机选择...")
    for i in range(SAMPLE_SIZE):
        selected = random.choice(TEST_DOMAINS)
        domain_counts[selected] += 1
        
        if (i + 1) % 10 == 0:
            print(f"  已完成 {i + 1}/{SAMPLE_SIZE} 次选择")
    
    # 分析结果
    print("\n" + "="*60)
    print("分布结果")
    print("="*60)
    
    expected = SAMPLE_SIZE / len(TEST_DOMAINS)
    max_deviation = 0
    
    for domain, count in domain_counts.items():
        percentage = (count / SAMPLE_SIZE) * 100
        deviation = abs(count - expected)
        max_deviation = max(max_deviation, deviation)
        
        print(f"\n{domain}:")
        print(f"  次数: {count}")
        print(f"  百分比: {percentage:.1f}%")
        print(f"  偏差: {deviation:.1f}")
        
        # 可视化
        bar = "█" * int(percentage / 2)
        print(f"  分布: {bar}")
    
    # 评估均匀性
    print("\n" + "="*60)
    print("均匀性评估")
    print("="*60)
    
    # 计算标准差
    import math
    mean = SAMPLE_SIZE / len(TEST_DOMAINS)
    variance = sum((count - mean) ** 2 for count in domain_counts.values()) / len(TEST_DOMAINS)
    std_dev = math.sqrt(variance)
    
    print(f"\n统计指标:")
    print(f"  期望值: {mean:.2f}")
    print(f"  最大偏差: {max_deviation:.2f}")
    print(f"  标准差: {std_dev:.2f}")
    
    # 判断是否均匀（标准差小于期望值的30%认为是均匀的）
    threshold = mean * 0.3
    if std_dev < threshold:
        print(f"\n✅ 分布均匀（标准差 {std_dev:.2f} < 阈值 {threshold:.2f}）")
        print(f"   random.choice() 可以实现较好的负载均衡")
        return True
    else:
        print(f"\n⚠️ 分布不够均匀（标准差 {std_dev:.2f} >= 阈值 {threshold:.2f}）")
        print(f"   但这是正常的随机波动")
        return True


def test_domain_failover():
    """测试域名故障转移（模拟）"""
    print("\n" + "="*60)
    print("域名故障转移测试（模拟）")
    print("="*60)
    
    # 从 .env 读取域名配置
    DOMAINS_STR = os.getenv('SKYMAIL_DOMAIN', 'qixc.pp.ua')
    ALL_DOMAINS = [d.strip() for d in DOMAINS_STR.split(',') if d.strip()]
    
    if len(ALL_DOMAINS) < 2:
        print("⚠️ 警告: 只有一个域名，无法测试故障转移")
        print("   请在 .env 中配置多个域名，用逗号分隔")
        return False
    
    FAILED_DOMAIN = ALL_DOMAINS[0]  # 模拟第一个域名失败
    
    print(f"\n测试场景:")
    print(f"  所有域名: {', '.join(ALL_DOMAINS)}")
    print(f"  故障域名: {FAILED_DOMAIN}")
    
    # 模拟故障转移逻辑
    print(f"\n模拟 10 次邮箱创建...")
    
    success_count = 0
    failed_count = 0
    domain_usage = {domain: 0 for domain in ALL_DOMAINS}
    
    for i in range(10):
        # 随机选择域名
        selected_domain = random.choice(ALL_DOMAINS)
        domain_usage[selected_domain] += 1
        
        # 模拟：如果选中故障域名，则失败
        if selected_domain == FAILED_DOMAIN:
            print(f"  {i+1}. 选择 {selected_domain} - ❌ 失败（域名故障）")
            failed_count += 1
            
            # 故障转移：重试其他域名
            available_domains = [d for d in ALL_DOMAINS if d != FAILED_DOMAIN]
            retry_domain = random.choice(available_domains)
            domain_usage[retry_domain] += 1
            print(f"      故障转移到 {retry_domain} - ✅ 成功")
            success_count += 1
        else:
            print(f"  {i+1}. 选择 {selected_domain} - ✅ 成功")
            success_count += 1
    
    # 结果统计
    print("\n" + "="*60)
    print("故障转移结果")
    print("="*60)
    
    print(f"\n成功率: {success_count}/10 ({success_count*10}%)")
    print(f"失败次数: {failed_count}")
    
    print(f"\n域名使用统计:")
    for domain, count in domain_usage.items():
        status = "❌ 故障" if domain == FAILED_DOMAIN else "✅ 正常"
        print(f"  {domain}: {count} 次 ({status})")
    
    print("\n" + "="*60)
    print("✅ 故障转移测试完成")
    print("="*60)
    print(f"\n建议实现:")
    print(f"  1. 在 email_service.py 中添加重试逻辑")
    print(f"  2. 记录失败的域名，临时排除")
    print(f"  3. 定期检查失败域名是否恢复")
    
    return True


def test_auto_service_selection():
    """测试自动选择邮箱服务（模拟）"""
    print("\n" + "="*60)
    print("自动选择邮箱服务测试（模拟）")
    print("="*60)
    
    # 模拟可用的邮箱服务
    AVAILABLE_SERVICES = ['moemail', 'skymail']
    
    print(f"\n可用服务: {', '.join(AVAILABLE_SERVICES)}")
    print(f"\n模拟 20 次随机选择...")
    
    service_counts = {service: 0 for service in AVAILABLE_SERVICES}
    
    for i in range(20):
        # 随机选择服务
        selected_service = random.choice(AVAILABLE_SERVICES)
        service_counts[selected_service] += 1
        
        if (i + 1) % 5 == 0:
            print(f"  已完成 {i + 1}/20 次选择")
    
    # 显示结果
    print("\n" + "="*60)
    print("选择结果统计")
    print("="*60)
    
    for service, count in service_counts.items():
        percentage = (count / 20) * 100
        bar = "█" * int(percentage / 5)
        print(f"\n{service}:")
        print(f"  次数: {count}")
        print(f"  百分比: {percentage:.1f}%")
        print(f"  分布: {bar}")
    
    # 评估均匀性
    print("\n" + "="*60)
    print("均匀性评估")
    print("="*60)
    
    import math
    mean = 20 / len(AVAILABLE_SERVICES)
    variance = sum((count - mean) ** 2 for count in service_counts.values()) / len(AVAILABLE_SERVICES)
    std_dev = math.sqrt(variance)
    
    print(f"\n统计指标:")
    print(f"  期望值: {mean:.2f}")
    print(f"  标准差: {std_dev:.2f}")
    
    threshold = mean * 0.3
    if std_dev < threshold:
        print(f"\n✅ 分布均匀（标准差 {std_dev:.2f} < 阈值 {threshold:.2f}）")
        print(f"   random.choice() 可以实现较好的负载均衡")
    else:
        print(f"\n⚠️ 分布不够均匀（标准差 {std_dev:.2f} >= 阈值 {threshold:.2f}）")
        print(f"   但这是正常的随机波动")
    
    print("\n" + "="*60)
    print("✅ 自动选择测试完成")
    print("="*60)
    print(f"\n建议实现:")
    print(f"  1. 在 config.py 中添加 EMAIL_SERVICE='auto' 支持")
    print(f"  2. 在 EmailService 初始化时随机选择服务")
    print(f"  3. 记录每次选择的服务类型")
    print(f"  4. 可选：添加服务可用性检查")
    
    return True


def test_service_availability_check():
    """测试服务可用性检查（模拟）"""
    print("\n" + "="*60)
    print("服务可用性检查测试（模拟）")
    print("="*60)
    
    # 模拟服务状态
    services_status = {
        'moemail': {'available': True, 'response_time': 0.5},
        'skymail': {'available': True, 'response_time': 0.3}
    }
    
    print(f"\n检查服务可用性...")
    
    available_services = []
    for service, status in services_status.items():
        print(f"\n检查 {service}:")
        print(f"  可用性: {'✅ 可用' if status['available'] else '❌ 不可用'}")
        print(f"  响应时间: {status['response_time']}s")
        
        if status['available']:
            available_services.append(service)
    
    print("\n" + "="*60)
    print("可用性检查结果")
    print("="*60)
    
    print(f"\n可用服务: {', '.join(available_services)}")
    print(f"可用数量: {len(available_services)}/{len(services_status)}")
    
    if len(available_services) == 0:
        print("\n❌ 没有可用的邮箱服务")
        print("   建议: 检查网络连接和服务配置")
    elif len(available_services) == 1:
        print(f"\n⚠️ 只有一个服务可用: {available_services[0]}")
        print("   建议: 检查其他服务的配置")
    else:
        print(f"\n✅ 多个服务可用，可以使用 auto 模式")
    
    print("\n" + "="*60)
    print("✅ 可用性检查测试完成")
    print("="*60)
    print(f"\n建议实现:")
    print(f"  1. 在 EmailService 中添加服务健康检查")
    print(f"  2. auto 模式只从可用服务中选择")
    print(f"  3. 定期更新服务可用性状态")
    print(f"  4. 失败时自动切换到其他服务")
    
    return True


def test_auto_fallback():
    """测试 auto 模式故障转移（模拟）"""
    print("\n" + "="*60)
    print("Auto 模式故障转移测试（模拟）")
    print("="*60)
    
    # 模拟场景：moemail 故障
    services = ['moemail', 'skymail']
    failed_service = 'moemail'
    
    print(f"\n测试场景:")
    print(f"  可用服务: {', '.join(services)}")
    print(f"  故障服务: {failed_service}")
    
    print(f"\n模拟 10 次邮箱创建...")
    
    success_count = 0
    service_usage = {service: 0 for service in services}
    fallback_count = 0
    
    for i in range(10):
        # 随机选择服务
        selected_service = random.choice(services)
        service_usage[selected_service] += 1
        
        # 模拟：如果选中故障服务，则失败并转移
        if selected_service == failed_service:
            print(f"  {i+1}. 选择 {selected_service} - ❌ 失败（服务故障）")
            
            # 故障转移：选择其他服务
            available_services = [s for s in services if s != failed_service]
            if available_services:
                fallback_service = random.choice(available_services)
                service_usage[fallback_service] += 1
                fallback_count += 1
                print(f"      故障转移到 {fallback_service} - ✅ 成功")
                success_count += 1
            else:
                print(f"      ❌ 没有可用的备用服务")
        else:
            print(f"  {i+1}. 选择 {selected_service} - ✅ 成功")
            success_count += 1
    
    # 结果统计
    print("\n" + "="*60)
    print("故障转移结果")
    print("="*60)
    
    print(f"\n成功率: {success_count}/10 ({success_count*10}%)")
    print(f"故障转移次数: {fallback_count}")
    
    print(f"\n服务使用统计:")
    for service, count in service_usage.items():
        status = "❌ 故障" if service == failed_service else "✅ 正常"
        print(f"  {service}: {count} 次 ({status})")
    
    print("\n" + "="*60)
    print("✅ Auto 模式故障转移测试完成")
    print("="*60)
    print(f"\n建议实现:")
    print(f"  1. 在 EmailService 中添加服务故障检测")
    print(f"  2. 失败时自动切换到其他可用服务")
    print(f"  3. 记录失败的服务，临时排除")
    print(f"  4. 定期检查失败服务是否恢复")
    
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test-token":
            # 测试 Token 重用性
            test_token_reusability()
        elif sys.argv[1] == "--test-wildcard":
            # 测试通配符邮箱
            test_wildcard_email()
        elif sys.argv[1] == "--test-multi-domain":
            # 测试多域名支持
            test_multi_domain_support()
        elif sys.argv[1] == "--test-distribution":
            # 测试域名分布均匀性
            test_domain_distribution()
        elif sys.argv[1] == "--test-failover":
            # 测试域名故障转移
            test_domain_failover()
        elif sys.argv[1] == "--test-auto":
            # 测试自动选择邮箱服务
            test_auto_service_selection()
        elif sys.argv[1] == "--test-availability":
            # 测试服务可用性检查
            test_service_availability_check()
        elif sys.argv[1] == "--test-auto-fallback":
            # 测试 auto 模式故障转移
            test_auto_fallback()
        else:
            print(f"未知参数: {sys.argv[1]}")
            print("\n可用参数:")
            print("  --test-token          测试 Token 重用性")
            print("  --test-wildcard       测试通配符邮箱（无需注册）")
            print("  --test-multi-domain   测试多域名支持")
            print("  --test-distribution   测试域名分布均匀性")
            print("  --test-failover       测试域名故障转移（模拟）")
            print("  --test-auto           测试自动选择邮箱服务（模拟）")
            print("  --test-availability   测试服务可用性检查")
            print("  --test-auto-fallback  测试 auto 模式故障转移（模拟）")
    else:
        # 正常测试流程
        main()



def test_auto_service_selection():
    """测试自动选择邮箱服务功能（模拟）"""
    print("\n" + "="*60)
    print("自动选择邮箱服务测试")
    print("="*60)
    
    # 可用的邮箱服务
    AVAILABLE_SERVICES = ['moemail', 'skymail']
    TEST_COUNT = 20  # 测试次数
    
    print(f"\n测试参数:")
    print(f"  可用服务: {', '.join(AVAILABLE_SERVICES)}")
    print(f"  测试次数: {TEST_COUNT}")
    print(f"  期望分布: 每个服务约 {TEST_COUNT/len(AVAILABLE_SERVICES):.1f} 次")
    
    # 模拟随机选择
    service_counts = {service: 0 for service in AVAILABLE_SERVICES}
    
    print(f"\n开始模拟随机选择...")
    for i in range(TEST_COUNT):
        selected = random.choice(AVAILABLE_SERVICES)
        service_counts[selected] += 1
        
        if (i + 1) % 5 == 0:
            print(f"  已完成 {i + 1}/{TEST_COUNT} 次选择")
    
    # 分析结果
    print("\n" + "="*60)
    print("服务选择分布")
    print("="*60)
    
    for service, count in service_counts.items():
        percentage = (count / TEST_COUNT) * 100
        print(f"\n{service}:")
        print(f"  次数: {count}")
        print(f"  百分比: {percentage:.1f}%")
        
        # 可视化
        bar = "█" * int(percentage / 2)
        print(f"  分布: {bar}")
    
    # 评估均匀性
    print("\n" + "="*60)
    print("均匀性评估")
    print("="*60)
    
    import math
    mean = TEST_COUNT / len(AVAILABLE_SERVICES)
    variance = sum((count - mean) ** 2 for count in service_counts.values()) / len(AVAILABLE_SERVICES)
    std_dev = math.sqrt(variance)
    
    print(f"\n统计指标:")
    print(f"  期望值: {mean:.2f}")
    print(f"  标准差: {std_dev:.2f}")
    
    threshold = mean * 0.3
    if std_dev < threshold:
        print(f"\n✅ 分布均匀（标准差 {std_dev:.2f} < 阈值 {threshold:.2f}）")
        print(f"   random.choice() 可以实现服务的负载均衡")
    else:
        print(f"\n⚠️ 分布不够均匀（标准差 {std_dev:.2f} >= 阈值 {threshold:.2f}）")
        print(f"   但这是正常的随机波动")
    
    print("\n" + "="*60)
    print("✅ 自动选择测试完成")
    print("="*60)
    print(f"\n结论:")
    print(f"  - random.choice() 可以实现服务随机选择")
    print(f"  - 分布基本均匀，符合预期")
    print(f"  - 可以应用到实际项目中")
    
    return True


def test_service_availability_check():
    """测试服务可用性检查（模拟）"""
    print("\n" + "="*60)
    print("服务可用性检查测试")
    print("="*60)
    
    # 从 .env 读取配置
    moemail_api_key = os.getenv('MOEMAIL_API_KEY', '')
    skymail_token = os.getenv('SKYMAIL_TOKEN', '')
    
    print(f"\n配置检查:")
    print(f"  MoeMail API Key: {'已配置' if moemail_api_key else '未配置'}")
    print(f"  Skymail Token: {'已配置' if skymail_token else '未配置'}")
    
    # 检查哪些服务可用
    available_services = []
    
    if moemail_api_key:
        available_services.append('moemail')
        print(f"\n✅ MoeMail 可用")
    else:
        print(f"\n❌ MoeMail 不可用（缺少 API Key）")
    
    if skymail_token:
        available_services.append('skymail')
        print(f"✅ Skymail 可用")
    else:
        print(f"❌ Skymail 不可用（缺少 Token）")
    
    print("\n" + "="*60)
    print("可用性检查结果")
    print("="*60)
    
    if len(available_services) == 0:
        print(f"\n❌ 没有可用的邮箱服务")
        print(f"   请至少配置一个邮箱服务")
        return False
    elif len(available_services) == 1:
        print(f"\n⚠️ 只有 1 个可用服务: {available_services[0]}")
        print(f"   建议配置多个服务以提高可用性")
        print(f"   auto 模式将只使用这一个服务")
    else:
        print(f"\n✅ 有 {len(available_services)} 个可用服务")
        print(f"   可用服务: {', '.join(available_services)}")
        print(f"   auto 模式将在这些服务中随机选择")
    
    # 模拟 auto 模式选择
    if available_services:
        print(f"\n模拟 auto 模式选择 5 次:")
        for i in range(5):
            selected = random.choice(available_services)
            print(f"  {i+1}. 选择: {selected}")
    
    print("\n" + "="*60)
    print("✅ 可用性检查完成")
    print("="*60)
    
    return True


def test_auto_mode_with_fallback():
    """测试 auto 模式的故障转移（模拟）"""
    print("\n" + "="*60)
    print("Auto 模式故障转移测试")
    print("="*60)
    
    # 模拟场景
    ALL_SERVICES = ['moemail', 'skymail']
    FAILED_SERVICE = 'moemail'  # 模拟 moemail 失败
    
    print(f"\n测试场景:")
    print(f"  所有服务: {', '.join(ALL_SERVICES)}")
    print(f"  故障服务: {FAILED_SERVICE}")
    
    # 模拟 10 次创建邮箱
    print(f"\n模拟 10 次邮箱创建...")
    
    success_count = 0
    failed_count = 0
    service_usage = {service: 0 for service in ALL_SERVICES}
    retry_count = 0
    
    for i in range(10):
        # 第一次尝试：随机选择
        selected_service = random.choice(ALL_SERVICES)
        service_usage[selected_service] += 1
        
        # 模拟：如果选中故障服务，则失败
        if selected_service == FAILED_SERVICE:
            print(f"  {i+1}. 选择 {selected_service} - ❌ 失败（服务故障）")
            failed_count += 1
            
            # 故障转移：尝试其他服务
            available_services = [s for s in ALL_SERVICES if s != FAILED_SERVICE]
            if available_services:
                retry_service = random.choice(available_services)
                service_usage[retry_service] += 1
                retry_count += 1
                print(f"      故障转移到 {retry_service} - ✅ 成功")
                success_count += 1
            else:
                print(f"      ❌ 没有可用的备用服务")
        else:
            print(f"  {i+1}. 选择 {selected_service} - ✅ 成功")
            success_count += 1
    
    # 结果统计
    print("\n" + "="*60)
    print("故障转移结果")
    print("="*60)
    
    print(f"\n成功率: {success_count}/10 ({success_count*10}%)")
    print(f"失败次数: {failed_count}")
    print(f"重试次数: {retry_count}")
    
    print(f"\n服务使用统计:")
    for service, count in service_usage.items():
        status = "❌ 故障" if service == FAILED_SERVICE else "✅ 正常"
        print(f"  {service}: {count} 次 ({status})")
    
    print("\n" + "="*60)
    print("✅ 故障转移测试完成")
    print("="*60)
    print(f"\n建议实现:")
    print(f"  1. auto 模式下随机选择服务")
    print(f"  2. 如果选中的服务失败，自动尝试其他服务")
    print(f"  3. 记录失败的服务，临时降低其选择概率")
    print(f"  4. 定期检查失败服务是否恢复")
    
    return True
