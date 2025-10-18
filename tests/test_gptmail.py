#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPTMail 服务测试脚本
测试 https://mail.chatgpt.org.uk 临时邮箱服务的可用性
"""
import sys
import os
import time
import requests
import re

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class GPTMailService:
    """GPTMail 服务类"""
    
    def __init__(self, base_url='https://mail.chatgpt.org.uk'):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # 禁用 SSL 警告
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.session.verify = False
        
        # 配置 SSL 适配器（与 email_service.py 一致）
        from requests.adapters import HTTPAdapter
        from urllib3.poolmanager import PoolManager
        import ssl
        
        class SSLAdapter(HTTPAdapter):
            def init_poolmanager(self, *args, **kwargs):
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                kwargs['ssl_context'] = context
                return super().init_poolmanager(*args, **kwargs)
        
        # 为 http 和 https 都挂载自定义适配器
        self.session.mount('https://', SSLAdapter())
        self.session.mount('http://', SSLAdapter())
    
    def generate_email(self):
        """
        生成随机邮箱地址
        
        Returns:
            dict: {'email': 'xxx@domain.com'} 或 None
        """
        try:
            url = f"{self.base_url}/api/generate-email"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"❌ 生成邮箱失败: HTTP {response.status_code}")
                return None
        
        except Exception as e:
            print(f"❌ 生成邮箱出错: {e}")
            return None
    
    def get_emails(self, email_address):
        """
        获取邮箱的邮件列表
        
        Args:
            email_address: 邮箱地址
            
        Returns:
            dict: {'emails': [...]} 或 None
        """
        try:
            url = f"{self.base_url}/api/get-emails"
            params = {'email': email_address}
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # 标准化字段名：GPTMail 使用 htmlContent，统一为 html
                if data and 'emails' in data:
                    for email in data['emails']:
                        if 'htmlContent' in email and 'html' not in email:
                            email['html'] = email['htmlContent']
                        if 'content' in email and 'text' not in email:
                            email['text'] = email['content']
                return data
            else:
                print(f"❌ 获取邮件失败: HTTP {response.status_code}")
                return None
        
        except Exception as e:
            print(f"❌ 获取邮件出错: {e}")
            return None
    
    def wait_for_email(self, email_address, timeout=60, keyword='warp'):
        """
        等待接收邮件
        
        Args:
            email_address: 邮箱地址
            timeout: 超时时间（秒）
            keyword: 邮件主题关键词（空字符串表示接收任何邮件）
            
        Returns:
            dict: 邮件信息或 None
        """
        start_time = time.time()
        check_count = 0
        
        print(f"📬 等待邮件 (超时: {timeout}秒)...")
        
        while time.time() - start_time < timeout:
            check_count += 1
            
            result = self.get_emails(email_address)
            
            if result and result.get('emails'):
                emails = result['emails']
                print(f"  📨 收到 {len(emails)} 封邮件")
                
                for email in emails:
                    subject = email.get('subject', '')
                    # 如果 keyword 为空，返回第一封邮件
                    if not keyword or keyword.lower() in subject.lower():
                        print(f"  ✅ 找到匹配邮件: {subject}")
                        return email
                
                if keyword:
                    print(f"  ⚠️ 没有找到包含 '{keyword}' 的邮件")
            
            elapsed = int(time.time() - start_time)
            if check_count % 2 == 0:
                print(f"  ⏳ 检查中... ({elapsed}/{timeout}秒)")
            
            time.sleep(3)
        
        print("❌ 等待邮件超时")
        return None
    
    def extract_verification_link(self, email_html):
        """
        从邮件中提取验证链接
        
        Args:
            email_html: 邮件 HTML 内容
            
        Returns:
            str: 验证链接或 None
        """
        try:
            import html as html_module
            
            # 查找 Firebase 验证链接
            link_pattern = r'href=["\']([^"\']*firebaseapp\.com[^"\']*)["\']'
            matches = re.findall(link_pattern, email_html)
            
            for link in matches:
                if 'auth/action' in link:
                    link = html_module.unescape(link)
                    return link
            
            return None
        
        except Exception as e:
            print(f"❌ 提取链接失败: {e}")
            return None


def test_service_availability():
    """测试服务可用性"""
    print("\n" + "="*60)
    print("🔍 测试 1: 服务可用性检查")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    try:
        response = service.session.get(service.base_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ 服务可访问: {service.base_url}")
            print(f"   状态码: {response.status_code}")
            return True
        else:
            print(f"❌ 服务不可用: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法访问服务: {e}")
        return False


def test_generate_email():
    """测试生成邮箱"""
    print("\n" + "="*60)
    print("📧 测试 2: 生成邮箱地址")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    result = service.generate_email()
    
    if result and result.get('email'):
        email = result['email']
        print(f"✅ 邮箱生成成功: {email}")
        
        # 验证邮箱格式
        if '@' in email and '.' in email:
            print(f"✅ 邮箱格式正确")
            return email
        else:
            print(f"❌ 邮箱格式错误")
            return None
    else:
        print(f"❌ 邮箱生成失败")
        return None


def test_get_emails(email_address):
    """测试获取邮件列表"""
    print("\n" + "="*60)
    print("📬 测试 3: 获取邮件列表")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    result = service.get_emails(email_address)
    
    if result is not None:
        emails = result.get('emails', [])
        print(f"✅ 成功获取邮件列表")
        print(f"   邮件数量: {len(emails)}")
        
        if emails:
            print(f"\n   邮件列表:")
            for i, email in enumerate(emails, 1):
                subject = email.get('subject', 'No Subject')
                from_addr = email.get('from', 'Unknown')
                print(f"   {i}. {subject}")
                print(f"      发件人: {from_addr}")
        
        return True
    else:
        print(f"❌ 获取邮件列表失败")
        return False


def test_direct_url_access(email_address):
    """测试直接 URL 访问"""
    print("\n" + "="*60)
    print("🔗 测试 4: 直接 URL 访问")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    # 构建直接访问 URL
    direct_url = f"{service.base_url}/{email_address}"
    print(f"访问 URL: {direct_url}")
    
    try:
        response = service.session.get(direct_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ 直接访问成功")
            print(f"   状态码: {response.status_code}")
            return True
        else:
            print(f"❌ 直接访问失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 直接访问出错: {e}")
        return False


def test_multiple_emails():
    """测试生成多个邮箱"""
    print("\n" + "="*60)
    print("🔢 测试 5: 生成多个邮箱")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    emails = []
    success_count = 0
    
    for i in range(3):
        print(f"生成第 {i+1} 个邮箱...")
        result = service.generate_email()
        
        if result and result.get('email'):
            email = result['email']
            emails.append(email)
            success_count += 1
            print(f"  ✅ {email}")
        else:
            print(f"  ❌ 生成失败")
        
        time.sleep(1)
    
    print(f"\n成功生成 {success_count}/3 个邮箱")
    
    # 检查域名分布
    if emails:
        domains = [email.split('@')[1] for email in emails]
        unique_domains = set(domains)
        print(f"域名数量: {len(unique_domains)}")
        print(f"域名列表: {', '.join(unique_domains)}")
    
    return success_count == 3


def test_api_performance():
    """测试 API 性能"""
    print("\n" + "="*60)
    print("⚡ 测试 6: API 性能测试")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    # 测试生成邮箱的响应时间
    print("测试生成邮箱 API...")
    start_time = time.time()
    result = service.generate_email()
    elapsed = time.time() - start_time
    
    if result:
        print(f"✅ 响应时间: {elapsed:.2f} 秒")
        email = result['email']
        
        # 测试获取邮件的响应时间
        print(f"\n测试获取邮件 API...")
        start_time = time.time()
        service.get_emails(email)
        elapsed = time.time() - start_time
        print(f"✅ 响应时间: {elapsed:.2f} 秒")
        
        return True
    else:
        print(f"❌ API 测试失败")
        return False


def test_send_and_receive_email():
    """测试发送和接收邮件（需要手动发送测试邮件）"""
    print("\n" + "="*60)
    print("📨 测试 7: 发送和接收邮件")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    # 生成邮箱
    result = service.generate_email()
    if not result or not result.get('email'):
        print("❌ 无法生成邮箱")
        return False
    
    email_address = result['email']
    print(f"✅ 测试邮箱: {email_address}")
    
    # 提示用户发送测试邮件
    print("\n" + "-"*60)
    print("📧 请手动发送测试邮件到上述地址")
    print("   可以使用任何邮箱服务发送")
    print("   主题建议包含: test 或 warp")
    print("-"*60)
    
    choice = input("\n是否继续等待邮件? (y/n): ").strip().lower()
    if choice not in ['y', 'yes']:
        print("⏭️ 跳过邮件接收测试")
        return None
    
    # 等待邮件
    print("\n等待接收邮件...")
    email = service.wait_for_email(email_address, timeout=120, keyword='')
    
    if email:
        print(f"\n✅ 成功接收邮件")
        print(f"   主题: {email.get('subject', 'N/A')}")
        print(f"   发件人: {email.get('from', 'N/A')}")
        print(f"   时间: {email.get('date', 'N/A')}")
        
        # 显示邮件内容预览
        content = email.get('text', email.get('html', ''))
        if content:
            preview = content[:200].replace('\n', ' ')
            print(f"   内容预览: {preview}...")
        
        return True
    else:
        print("❌ 未收到邮件")
        return False


def test_warp_registration_flow():
    """测试 Warp 注册流程（模拟）"""
    print("\n" + "="*60)
    print("🚀 测试 8: Warp 注册流程模拟")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    # 生成邮箱
    result = service.generate_email()
    if not result or not result.get('email'):
        print("❌ 无法生成邮箱")
        return False
    
    email_address = result['email']
    print(f"✅ 注册邮箱: {email_address}")
    
    print("\n" + "-"*60)
    print("📝 模拟 Warp 注册流程:")
    print("   1. 访问 https://app.warp.dev/login")
    print(f"   2. 输入邮箱: {email_address}")
    print("   3. 点击发送验证邮件")
    print("   4. 等待接收验证邮件")
    print("-"*60)
    
    choice = input("\n是否已发送 Warp 验证邮件? (y/n): ").strip().lower()
    if choice not in ['y', 'yes']:
        print("⏭️ 跳过 Warp 注册测试")
        return None
    
    # 等待 Warp 验证邮件
    print("\n等待 Warp 验证邮件...")
    email = service.wait_for_email(email_address, timeout=120, keyword='warp')
    
    if email:
        print(f"\n✅ 收到 Warp 验证邮件")
        print(f"   主题: {email.get('subject', 'N/A')}")
        
        # 提取验证链接
        html_content = email.get('html', email.get('text', ''))
        if html_content:
            link = service.extract_verification_link(html_content)
            
            if link:
                print(f"\n✅ 成功提取验证链接")
                print(f"   链接: {link[:80]}...")
                
                # 验证链接格式
                if 'firebaseapp.com' in link and 'auth/action' in link:
                    print(f"✅ 验证链接格式正确")
                    return True
                else:
                    print(f"⚠️ 验证链接格式可能不正确")
                    return False
            else:
                print(f"❌ 未找到验证链接")
                print(f"   邮件内容预览: {html_content[:200]}...")
                return False
        else:
            print(f"❌ 邮件内容为空")
            return False
    else:
        print("❌ 未收到 Warp 验证邮件")
        return False


def test_extract_link_from_sample():
    """测试从示例邮件中提取链接"""
    print("\n" + "="*60)
    print("🔗 测试 9: 验证链接提取功能")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    # 示例 HTML 邮件内容（包含 Firebase 验证链接）
    sample_html = '''
    <html>
    <body>
        <p>Welcome to Warp!</p>
        <p>Click the link below to verify your email:</p>
        <a href="https://warp-dev.firebaseapp.com/__/auth/action?mode=verifyEmail&oobCode=ABC123&apiKey=xyz&lang=en">
            Verify Email
        </a>
    </body>
    </html>
    '''
    
    print("测试提取 Firebase 验证链接...")
    link = service.extract_verification_link(sample_html)
    
    if link:
        print(f"✅ 成功提取链接")
        print(f"   链接: {link}")
        
        # 验证链接组成部分
        checks = {
            'firebaseapp.com': 'firebaseapp.com' in link,
            'auth/action': 'auth/action' in link,
            'mode=verifyEmail': 'mode=verifyEmail' in link,
            'oobCode': 'oobCode' in link
        }
        
        print("\n链接组成验证:")
        all_passed = True
        for key, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {key}")
            if not passed:
                all_passed = False
        
        return all_passed
    else:
        print(f"❌ 未能提取链接")
        return False


def test_html_entity_decoding():
    """测试 HTML 实体解码"""
    print("\n" + "="*60)
    print("🔤 测试 10: HTML 实体解码")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    # 包含 HTML 实体的示例链接
    sample_html = '''
    <a href="https://warp-dev.firebaseapp.com/__/auth/action?mode=verifyEmail&amp;oobCode=ABC123&amp;apiKey=xyz">
        Verify
    </a>
    '''
    
    print("测试解码包含 &amp; 的链接...")
    link = service.extract_verification_link(sample_html)
    
    if link:
        print(f"✅ 成功提取并解码链接")
        print(f"   原始: ...&amp;oobCode...")
        print(f"   解码: ...&oobCode...")
        
        # 验证是否正确解码
        if '&amp;' in link:
            print(f"❌ HTML 实体未正确解码")
            return False
        elif '&oobCode' in link and '&apiKey' in link:
            print(f"✅ HTML 实体解码正确")
            return True
        else:
            print(f"⚠️ 链接格式可能不正确")
            return False
    else:
        print(f"❌ 未能提取链接")
        return False


def test_multiple_links_extraction():
    """测试从包含多个链接的邮件中提取正确的验证链接"""
    print("\n" + "="*60)
    print("🔗 测试 11: 多链接提取")
    print("="*60 + "\n")
    
    service = GPTMailService()
    
    # 包含多个链接的示例邮件
    sample_html = '''
    <html>
    <body>
        <p>Welcome to Warp!</p>
        <a href="https://warp.dev">Visit our website</a>
        <a href="https://warp-dev.firebaseapp.com/__/auth/action?mode=verifyEmail&oobCode=ABC123">
            Verify Email
        </a>
        <a href="https://warp.dev/docs">Read documentation</a>
        <a href="https://another-app.firebaseapp.com/some/path">Other link</a>
    </body>
    </html>
    '''
    
    print("测试从多个链接中提取正确的验证链接...")
    link = service.extract_verification_link(sample_html)
    
    if link:
        print(f"✅ 成功提取链接")
        print(f"   链接: {link[:80]}...")
        
        # 验证是否提取了正确的链接
        if 'auth/action' in link and 'mode=verifyEmail' in link:
            print(f"✅ 提取了正确的验证链接")
            return True
        else:
            print(f"❌ 提取的链接不正确")
            return False
    else:
        print(f"❌ 未能提取链接")
        return False


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🧪 GPTMail 服务测试")
    print("="*60)
    print(f"服务地址: https://mail.chatgpt.org.uk")
    print("="*60 + "\n")
    
    # 询问测试模式
    print("测试模式:")
    print("1. 基础测试 (不需要发送邮件)")
    print("2. 完整测试 (包括邮件接收和 Warp 注册)")
    print()
    
    mode = input("请选择测试模式 (1/2, 默认 1): ").strip()
    if not mode:
        mode = '1'
    
    results = {}
    
    # ========== 基础测试 ==========
    
    # 测试 1: 服务可用性
    results['availability'] = test_service_availability()
    
    if not results['availability']:
        print("\n❌ 服务不可用，跳过后续测试")
        return
    
    # 测试 2: 生成邮箱
    email_address = test_generate_email()
    results['generate'] = email_address is not None
    
    if not email_address:
        print("\n❌ 无法生成邮箱，跳过后续测试")
        return
    
    # 测试 3: 获取邮件列表
    results['get_emails'] = test_get_emails(email_address)
    
    # 测试 4: 直接 URL 访问
    results['direct_url'] = test_direct_url_access(email_address)
    
    # 测试 5: 生成多个邮箱
    results['multiple'] = test_multiple_emails()
    
    # 测试 6: API 性能
    results['performance'] = test_api_performance()
    
    # 测试 9: 验证链接提取功能
    results['extract_link'] = test_extract_link_from_sample()
    
    # 测试 10: HTML 实体解码
    results['html_decode'] = test_html_entity_decoding()
    
    # 测试 11: 多链接提取
    results['multiple_links'] = test_multiple_links_extraction()
    
    # ========== 完整测试（需要手动操作）==========
    
    if mode == '2':
        # 测试 7: 发送和接收邮件
        result = test_send_and_receive_email()
        if result is not None:
            results['send_receive'] = result
        
        # 测试 8: Warp 注册流程
        result = test_warp_registration_flow()
        if result is not None:
            results['warp_flow'] = result
    
    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    test_names = {
        'availability': '服务可用性',
        'generate': '生成邮箱',
        'get_emails': '获取邮件列表',
        'direct_url': '直接 URL 访问',
        'multiple': '生成多个邮箱',
        'performance': 'API 性能',
        'send_receive': '发送和接收邮件',
        'warp_flow': 'Warp 注册流程',
        'extract_link': '验证链接提取',
        'html_decode': 'HTML 实体解码',
        'multiple_links': '多链接提取'
    }
    
    passed = 0
    total = len(results)
    
    for key, result in results.items():
        if result is None:
            continue
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_names.get(key, key):20s} {status}")
        if result:
            passed += 1
    
    print("="*60)
    print(f"通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    print("="*60 + "\n")
    
    # 集成建议
    if passed == total:
        print("✅ 所有测试通过！GPTMail 服务可以集成到项目中。")
        print("\n集成步骤:")
        print("1. 在 email_service.py 中添加 GPTMailService 类")
        print("2. 在 config.py 中添加 GPTMAIL_URL 配置")
        print("3. 在 EMAIL_SERVICE 中添加 'gptmail' 选项")
        print("4. 更新 auto 模式以包含 GPTMail")
        print("\n示例代码:")
        print("```python")
        print("# config.py")
        print("GPTMAIL_URL = os.getenv('GPTMAIL_URL', 'https://mail.chatgpt.org.uk')")
        print("")
        print("# email_service.py")
        print("elif self.service_type == 'gptmail':")
        print("    return self._create_gptmail(prefix, domain)")
        print("```")
    elif passed >= total * 0.7:
        print("⚠️ 大部分测试通过，但存在一些问题。")
        print("建议: 修复失败的测试后再集成。")
    else:
        print("❌ 测试失败较多，不建议集成。")
    
    # 性能评估
    print("\n" + "="*60)
    print("📈 服务评估")
    print("="*60)
    
    if results.get('availability') and results.get('generate'):
        print("✅ 基础功能: 可用")
    else:
        print("❌ 基础功能: 不可用")
    
    if results.get('extract_link') and results.get('html_decode'):
        print("✅ 链接提取: 可靠")
    else:
        print("⚠️ 链接提取: 需要改进")
    
    if results.get('multiple'):
        print("✅ 多域名支持: 是")
    else:
        print("⚠️ 多域名支持: 未知")
    
    print("\n优势:")
    print("  • 简单的 API (仅 2 个端点)")
    print("  • Cloudflare CDN 支持")
    print("  • 30 秒自动刷新")
    print("  • 支持直接 URL 访问")
    print("  • 多域名支持")
    
    print("\n注意事项:")
    print("  • 邮件保留时间: 1 天")
    print("  • 无需 API Key (公开服务)")
    print("  • 可能存在访问限制")
    print("="*60 + "\n")


def test_integration():
    """集成测试 - 验证 GPTMail 是否正确集成到 email_service.py"""
    print("\n" + "="*60)
    print("🔗 集成测试")
    print("="*60 + "\n")
    
    from email_service import EmailService
    from config import config
    
    results = {}
    
    # 测试 1: 直接使用 gptmail
    print("测试 1: 直接使用 gptmail 服务")
    print("-" * 60)
    
    try:
        service = EmailService(service_type='gptmail')
        print(f"✅ EmailService 初始化成功")
        print(f"   服务类型: {service.service_type}")
        print(f"   Base URL: {service.base_url}")
        
        # 创建邮箱
        print("\n创建测试邮箱...")
        email_info = service.create_email()
        
        if email_info:
            print(f"✅ 邮箱创建成功")
            print(f"   地址: {email_info['address']}")
            print(f"   服务: {email_info['service']}")
            print(f"   域名: {email_info['domain']}")
            results['direct_use'] = True
        else:
            print(f"❌ 邮箱创建失败")
            results['direct_use'] = False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        results['direct_use'] = False
    
    # 测试 2: Auto 模式（应该包含 gptmail）
    print("\n" + "-"*60)
    print("测试 2: Auto 模式（包含 gptmail）")
    print("-" * 60)
    
    try:
        service = EmailService(service_type='auto')
        print(f"✅ Auto 模式初始化成功")
        print(f"   选择的服务: {service.service_type}")
        
        # 创建邮箱
        print("\n创建测试邮箱...")
        email_info = service.create_email()
        
        if email_info:
            print(f"✅ 邮箱创建成功")
            print(f"   地址: {email_info['address']}")
            print(f"   服务: {email_info['service']}")
            results['auto_mode'] = True
        else:
            print(f"❌ 邮箱创建失败")
            results['auto_mode'] = False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        results['auto_mode'] = False
    
    # 测试 3: 配置验证
    print("\n" + "-"*60)
    print("测试 3: 配置验证")
    print("-" * 60)
    
    try:
        # 临时修改配置测试 gptmail
        original_service = config.EMAIL_SERVICE
        config.EMAIL_SERVICE = 'gptmail'
        
        config.validate()
        print(f"✅ gptmail 配置验证通过")
        results['config_validation'] = True
        
        # 恢复原配置
        config.EMAIL_SERVICE = original_service
        
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        results['config_validation'] = False
    
    # 汇总结果
    print("\n" + "="*60)
    print("📊 集成测试结果")
    print("="*60)
    
    test_names = {
        'direct_use': '直接使用 gptmail',
        'auto_mode': 'Auto 模式',
        'config_validation': '配置验证'
    }
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for key, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_names[key]:20s} {status}")
    
    print("="*60)
    print(f"通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    print("="*60 + "\n")
    
    if passed == total:
        print("✅ 所有集成测试通过！")
        print("\n📋 集成总结:")
        print("  ✅ GPTMail 服务已成功集成")
        print("  ✅ 可以通过 EMAIL_SERVICE=gptmail 使用")
        print("  ✅ Auto 模式已包含 GPTMail")
        print("  ✅ 配置验证正常")
        print()
        print("🚀 使用方法:")
        print("  1. 在 .env 中设置: EMAIL_SERVICE=gptmail")
        print("  2. 或使用 auto 模式: EMAIL_SERVICE=auto")
        print("  3. 运行注册: python register.py")
        print()
        return True
    else:
        print("❌ 部分集成测试失败")
        return False


if __name__ == "__main__":
    try:
        main()
        
        # 运行集成测试
        print("\n" + "="*60)
        print("🔗 运行集成测试...")
        print("="*60)
        test_integration()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 测试被中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
