#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Undetected-Chromedriver 激活器
"""
import os
import time
import random
from typing import Dict, Any
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import config


class UCActivator:
    """Undetected-Chromedriver 激活器"""
    
    def __init__(self, headless: bool = None):
        if headless is None:
            headless = config.HEADLESS
        self.headless = headless
        self.driver = None
    
    def start(self):
        """启动浏览器"""
        print(f"启动 Undetected Chrome ({'无头模式' if self.headless else '显示窗口'})...")
        
        # 检测 Chrome 版本（跨平台）- 不启动浏览器
        try:
            import subprocess
            import platform
            
            system = platform.system()
            if system == 'Windows':
                # Windows 系统 - 使用 wmic 或读取注册表, 不启动浏览器
                try:
                    # 方法1: 读取注册表
                    import winreg
                    key_path = r"SOFTWARE\Google\Chrome\BLBeacon"
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                    version, _ = winreg.QueryValueEx(key, "version")
                    winreg.CloseKey(key)
                    print(f"  检测到 Chrome: Google Chrome {version}")
                except:
                    # 方法2: 检查文件版本（不启动浏览器）
                    chrome_paths = [
                        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                    ]
                    found = False
                    for path in chrome_paths:
                        if os.path.exists(path):
                            print(f"  检测到 Chrome: {path}")
                            found = True
                            break
                    if not found:
                        print(f"  ℹ️ 未找到 Chrome 安装路径, 将使用默认配置")
            else:
                # Linux/Mac 系统
                chrome_version = subprocess.check_output(
                    ['google-chrome', '--version'], 
                    stderr=subprocess.DEVNULL
                ).decode('utf-8').strip()
                print(f"  检测到 Chrome: {chrome_version}")
        except Exception as e:
            print(f"  ℹ️ 无法检测 Chrome 版本, 将使用默认配置")
        
        options = uc.ChromeOptions()
        
        # 无痕模式
        options.add_argument('--incognito')
        
        if self.headless:
            options.add_argument('--headless=new')
        
        # 指纹随机化（如果启用）
        if config.FINGERPRINT_RANDOMIZE:
            from fingerprint_randomizer import FingerprintRandomizer
            import platform
            
            system = platform.system().lower()
            if system == 'darwin':
                system = 'mac'
            
            # 获取指纹级别和增强配置
            level = getattr(config, 'FINGERPRINT_LEVEL', 'balanced')
            enhanced = getattr(config, 'ENHANCED_PROFILES_ENABLED', True)
            debug = getattr(config, 'FINGERPRINT_DEBUG', False)
            
            fingerprint = FingerprintRandomizer(
                platform=system,
                level=level,
                enhanced_profiles=enhanced
            )
            
            # 验证配置一致性
            if getattr(config, 'STRICT_CONSISTENCY_CHECK', True):
                if not fingerprint.validate_consistency():
                    print("  ⚠️ 配置一致性检查失败，使用基础配置")
                    fingerprint = FingerprintRandomizer(platform=system, level='basic', enhanced_profiles=False)
            
            if debug:
                fingerprint.print_fingerprint()
            
            # 应用随机化的指纹参数
            for arg in fingerprint.get_chrome_options_args():
                options.add_argument(arg)
            
            # 禁用 WebRTC（防止 IP 泄露）
            options.add_argument('--disable-webrtc')
            
            # 保存指纹对象供后续使用
            self.fingerprint = fingerprint
        else:
            # 不启用指纹随机化，使用固定配置
            options.add_argument('--window-size=1920,1080')
            self.fingerprint = None
        
        # 基础配置
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        
        # 代理配置
        proxy_server = os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY')
        if proxy_server:
            proxy_server = proxy_server.replace('http://', '').replace('https://', '')
            options.add_argument(f'--proxy-server={proxy_server}')
            print(f"  使用代理: {proxy_server}")
            
            # 排除本地地址不走代理（避免 ChromeDriver 连接失败）
            no_proxy = os.environ.get('NO_PROXY', 'localhost,127.0.0.1,::1')
            options.add_argument(f'--proxy-bypass-list={no_proxy}')
            print(f"  代理排除列表: {no_proxy}")
        
        print("  初始化 undetected-chromedriver...")
        print("  注意: 首次运行会自动下载匹配的 ChromeDriver, 可能需要 30-60 秒")
        print("  如果长时间卡住, 请检查网络连接或手动下载 ChromeDriver")
        
        # 从环境变量读取 Chrome 版本配置
        # 本地测试: CHROME_VERSION=121
        # GitHub Actions: 不设置（自动检测）
        chrome_version_env = os.environ.get('CHROME_VERSION')
        
        try:
            # 1. 确定 Chrome 二进制路径
            chrome_binary = None
            
            # 优先使用配置文件中的路径
            if config.CHROME_BINARY_PATH:
                if os.path.exists(config.CHROME_BINARY_PATH):
                    chrome_binary = config.CHROME_BINARY_PATH
                    print(f"  使用自定义 Chrome 路径: {chrome_binary}")
                else:
                    print(f"  ⚠️ 配置的 Chrome 路径不存在: {config.CHROME_BINARY_PATH}")
            
            # 如果没有配置，使用系统默认路径
            if not chrome_binary and os.path.exists('/usr/bin/google-chrome'):
                chrome_binary = '/usr/bin/google-chrome'
                print(f"  使用系统 Chrome 路径: {chrome_binary}")
            
            # 2. 确定 ChromeDriver 路径
            driver_path = None
            
            # 优先使用配置文件中的路径
            if config.CHROMEDRIVER_PATH:
                if os.path.exists(config.CHROMEDRIVER_PATH):
                    driver_path = config.CHROMEDRIVER_PATH
                    print(f"  使用自定义 ChromeDriver 路径: {driver_path}")
                else:
                    print(f"  ⚠️ 配置的 ChromeDriver 路径不存在: {config.CHROMEDRIVER_PATH}")
            
            # 3. 初始化浏览器
            if chrome_version_env:
                # 指定版本（本地测试）
                version_main = int(chrome_version_env)
                print(f"  使用指定的 Chrome 版本: {version_main}")
                print(f"  正在初始化浏览器...")
                
                self.driver = uc.Chrome(
                    options=options,
                    version_main=version_main,
                    browser_executable_path=chrome_binary,
                    driver_executable_path=driver_path,
                    use_subprocess=False,
                    suppress_welcome=True
                )
            else:
                # 自动检测版本（GitHub Actions）
                print(f"  自动检测 Chrome 版本")
                print(f"  正在初始化浏览器...")
                
                self.driver = uc.Chrome(
                    options=options,
                    browser_executable_path=chrome_binary,
                    driver_executable_path=driver_path,
                    use_subprocess=False,
                    suppress_welcome=True
                )
            
            self.driver.implicitly_wait(10)
            
            # 注入指纹混淆脚本（如果启用了指纹随机化）
            if config.FINGERPRINT_RANDOMIZE and self.fingerprint:
                level = getattr(config, 'FINGERPRINT_LEVEL', 'balanced')
                print(f"  🎭 注入指纹混淆脚本 (级别: {level})...")
                try:
                    # 使用 CDP (Chrome DevTools Protocol) 注入脚本
                    # 这样可以在页面加载前就注入，更隐蔽
                    scripts = self.fingerprint.get_all_scripts()
                    self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                        'source': scripts
                    })
                    
                    # 显示注入的功能
                    features = []
                    if level in ['basic', 'balanced', 'aggressive']:
                        features.extend(['Canvas', 'Navigator', 'Timezone'])
                    if level in ['balanced', 'aggressive']:
                        features.extend(['WebGL', 'Performance Timing'])
                    if level == 'aggressive':
                        features.append('Audio Context')
                    
                    print(f"  ✅ 指纹混淆脚本注入成功 ({', '.join(features)})")
                except Exception as e:
                    print(f"  ⚠️ 指纹混淆脚本注入失败: {e}")
            
            print("  ✅ 浏览器启动成功")
            
        except Exception as e:
            print(f"  ❌ 浏览器启动失败: {e}")
            print(f"  提示: 如果是首次运行, 可能需要下载 ChromeDriver")
            print(f"  请检查:")
            print(f"    1. 网络连接是否正常")
            print(f"    2. Chrome 是否已安装")
            print(f"    3. 防火墙是否阻止下载")
            raise
    
    def close(self):
        """关闭浏览器并清理进程"""
        if self.driver:
            try:
                # 先关闭所有窗口
                try:
                    self.driver.close()
                except:
                    pass
                
                # 然后退出浏览器
                try:
                    self.driver.quit()
                except:
                    pass
                
                # Windows 特殊处理：强制清理残留进程
                import platform
                if platform.system() == 'Windows':
                    try:
                        import subprocess
                        import psutil
                        
                        # 获取当前 driver 的进程 ID
                        if hasattr(self.driver, 'service') and hasattr(self.driver.service, 'process'):
                            driver_pid = self.driver.service.process.pid
                            
                            # 查找并终止所有相关的 Chrome 进程
                            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                                try:
                                    # 检查是否是 Chrome 或 ChromeDriver 进程
                                    if proc.info['name'] in ['chrome.exe', 'chromedriver.exe']:
                                        # 检查命令行参数，确保是我们启动的进程
                                        cmdline = proc.info.get('cmdline', [])
                                        if cmdline and any('--test-type' in arg or '--disable-blink-features' in arg for arg in cmdline):
                                            print(f"  清理残留进程: {proc.info['name']} (PID: {proc.info['pid']})")
                                            proc.kill()
                                except (psutil.NoSuchProcess, psutil.AccessDenied):
                                    pass
                    except ImportError:
                        # 如果没有 psutil，使用 taskkill（不太精确）
                        print("  ⚠️ 建议安装 psutil 以更好地清理进程: pip install psutil")
                    except Exception as e:
                        print(f"  ⚠️ 清理进程时出错: {e}")
                
                # 阻止 __del__ 方法被调用（避免 WinError 6）
                try:
                    # 移除 __del__ 方法，防止垃圾回收时再次调用 quit()
                    if hasattr(self.driver.__class__, '__del__'):
                        delattr(self.driver.__class__, '__del__')
                except:
                    pass
                
            except Exception as e:
                print(f"  ⚠️ 关闭浏览器时出错: {e}")
            finally:
                self.driver = None
    
    def register_account(self, email: str, email_id: str, email_service) -> Dict[str, Any]:
        """
        完整注册流程
        """
        if not self.driver:
            self.start()
        
        try:
            # 访问登录页面
            print(f"访问登录页面...")
            self.driver.get('https://app.warp.dev/login')
            time.sleep(3)
            
            # 输入邮箱
            print(f"输入邮箱: {email}")
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder*="email" i]'))
            )
            
            email_input.click()
            time.sleep(0.5)
            
            for char in email:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(1)
            
            # 点击发送按钮
            try:
                submit_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
                )
                submit_button.click()
                print("已点击发送按钮")
            except:
                from selenium.webdriver.common.keys import Keys
                email_input.send_keys(Keys.RETURN)
                print("已按回车发送")
            
            time.sleep(3)
            
            # 等待邮件
            print(f"\n步骤 3/4: 等待验证邮件")
            print("-" * 60)
            email_message = email_service.wait_for_email(email_id)
            
            if not email_message:
                return {"success": False, "error": "未收到验证邮件"}
            
            # 提取验证链接
            print(f"\n步骤 4/4: 激活账号")
            print("-" * 60)
            verification_link = email_service.extract_verification_link(email_message['html'])
            
            if not verification_link:
                return {"success": False, "error": "未找到验证链接"}
            
            print(f"访问验证链接...")
            self.driver.get(verification_link)
            time.sleep(5)
            
            # 如果在登录页面, 跳转到主页
            if 'login' in self.driver.current_url:
                print("跳转到主页...")
                self.driver.get('https://app.warp.dev')
                time.sleep(3)
            
            # 获取 Token
            print("获取 Token...")
            firebase_user = self.driver.execute_script("""
                const key = Object.keys(localStorage).find(k => k.includes('firebase:authUser'));
                if (key) {
                    const data = JSON.parse(localStorage.getItem(key));
                    return {
                        email: data.email,
                        uid: data.uid || data.localId,
                        idToken: data.stsTokenManager?.accessToken,
                        refreshToken: data.stsTokenManager?.refreshToken
                    };
                }
                return null;
            """)
            
            if not firebase_user or not firebase_user.get('idToken'):
                return {"success": False, "error": "未获取到 Token"}
            
            # 获取配额信息
            quota_info = self._get_quota_info(firebase_user['idToken'])
            
            return {
                "success": True,
                "uid": firebase_user.get("uid"),
                "email": firebase_user.get("email"),
                "id_token": firebase_user.get("idToken"),
                "refresh_token": firebase_user.get("refreshToken"),
                "quota_info": quota_info
            }
            
        except Exception as e:
            print(f"注册过程出错: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    def _get_quota_info(self, id_token: str) -> Dict[str, Any]:
        """获取配额信息"""
        try:
            print("获取账号配额信息...")
            import requests
            
            response = requests.post(
                'https://app.warp.dev/graphql/v2?op=GetRequestLimitInfo',
                headers={
                    'Authorization': f"Bearer {id_token}",
                    'Content-Type': 'application/json',
                    'x-warp-client-id': 'warp-app',
                    'x-warp-os-category': 'Web'
                },
                json={
                    "query": """query GetRequestLimitInfo($requestContext: RequestContext!) {
                        user(requestContext: $requestContext) {
                            __typename
                            ... on UserOutput {
                                user {
                                    requestLimitInfo {
                                        requestLimit
                                        requestsUsedSinceLastRefresh
                                        nextRefreshTime
                                    }
                                }
                            }
                        }
                    }""",
                    "variables": {
                        "requestContext": {
                            "clientContext": {"version": "v0.2025.10.08.08.12.stable_03"},
                            "osContext": {"category": "Web", "name": "Windows", "version": "NT 10.0"}
                        }
                    },
                    "operationName": "GetRequestLimitInfo"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                limit_info = data.get('data', {}).get('user', {}).get('user', {}).get('requestLimitInfo', {})
                if limit_info:
                    quota = {
                        'requestLimit': limit_info.get('requestLimit'),
                        'requestsUsed': limit_info.get('requestsUsedSinceLastRefresh'),
                        'nextRefresh': limit_info.get('nextRefreshTime')
                    }
                    print(f"  请求限额: {quota['requestLimit']}")
                    print(f"  已使用: {quota['requestsUsed']}")
                    return quota
        except Exception as e:
            print(f"  获取配额信息失败: {e}")
        
        return None
