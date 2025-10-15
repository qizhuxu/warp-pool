#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Warp 注册主程序 - Undetected-Chromedriver 版本
"""
import sys
import time
import argparse
from typing import Dict, Any

from config import config
from email_service import EmailService
from uc_activator import UCActivator


def register_single_account(headless: bool = None) -> Dict[str, Any]:
    """
    注册单个账号
    """
    start_time = time.time()
    
    print("\n" + "="*60)
    print("🚀 开始注册 Warp 账号 (Undetected-Chromedriver)")
    print("="*60 + "\n")
    
    # 初始化服务（从配置读取邮箱服务类型）
    email_service = EmailService(service_type=config.EMAIL_SERVICE)
    activator = UCActivator(headless=headless)
    
    try:
        # 步骤1: 创建临时邮箱
        print("📧 步骤 1/5: 创建临时邮箱")
        print("-" * 60)
        email_info = email_service.create_email()
        
        if not email_info:
            return {"success": False, "error": "创建邮箱失败"}
        
        email_address = email_info['address']
        email_id = email_info['id']
        
        # 步骤2: 启动浏览器并发送邮件
        print(f"\n🌐 步骤 2/5: 启动浏览器")
        print("-" * 60)
        activator.start()
        
        # 访问登录页面并输入邮箱
        print(f"\n📝 步骤 3/5: 发送登录邮件")
        print("-" * 60)
        
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import random
        
        activator.driver.get(config.WARP_LOGIN_URL)
        time.sleep(3)
        
        # 直接使用正确的选择器
        try:
            email_input = WebDriverWait(activator.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder*="email" i]'))
            )
        except Exception as e:
            print(f"  ❌ 未找到邮箱输入框: {e}")
            os.makedirs('debug', exist_ok=True)
            activator.driver.save_screenshot('debug/login_page.png')
            return {"success": False, "error": "未找到邮箱输入框", "email": email_address}
        
        # 输入邮箱
        print(f"  输入邮箱: {email_address}")
        email_input.click()
        time.sleep(0.5)
        
        for char in email_address:
            email_input.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        
        time.sleep(1)
        
        # 点击发送按钮（多种方式尝试）
        button_clicked = False
        
        # 方式1: 查找并点击 submit 按钮
        try:
            submit_button = WebDriverWait(activator.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            # 滚动到按钮位置
            activator.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(0.5)
            # 尝试点击
            submit_button.click()
            button_clicked = True
            print("  ✅ 已点击发送按钮")
        except Exception as e:
            print(f"  ⚠️ 点击按钮失败: {e}")
        
        # 方式2: 如果点击失败，尝试 JavaScript 点击
        if not button_clicked:
            try:
                submit_button = activator.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                activator.driver.execute_script("arguments[0].click();", submit_button)
                button_clicked = True
                print("  ✅ 已通过 JS 点击按钮")
            except:
                pass
        
        # 方式3: 如果还是失败，按回车键
        if not button_clicked:
            try:
                from selenium.webdriver.common.keys import Keys
                email_input.send_keys(Keys.RETURN)
                button_clicked = True
                print("  ✅ 已按回车发送")
            except:
                pass
        
        if not button_clicked:
            print("  ⚠️ 所有发送方式都失败了")
            return {"success": False, "error": "无法点击发送按钮", "email": email_address}
        
        # 验证邮件是否发送成功（等待 Check 图标出现）
        print("  等待邮件发送确认...")
        try:
            # 等待 Check 图标出现（最多 15 秒）
            check_icon = WebDriverWait(activator.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="check.svg"], img[alt*="Check"]'))
            )
            print("  ✅ 邮件发送成功！")
        except Exception as e:
            print(f"  ❌ 邮件发送失败或网络超时")
            print(f"  错误信息: {e}")
            print("  可能原因:")
            print("    1. 网络连接不稳定")
            print("    2. Warp 服务器响应慢")
            print("    3. 邮箱地址被拒绝")
            print("  建议: 检查网络连接后重试")
            return {"success": False, "error": "邮件发送失败或网络超时", "email": email_address}
        
        time.sleep(2)
        
        # 步骤4: 等待邮件
        print(f"\n📬 步骤 4/5: 等待验证邮件")
        print("-" * 60)
        email_message = email_service.wait_for_email(email_info)
        
        if not email_message:
            return {"success": False, "error": "未收到验证邮件", "email": email_address}
        
        # 提取验证链接
        print(f"\n🔍 步骤 5/5: 提取验证链接并激活")
        print("-" * 60)
        verification_link = email_service.extract_verification_link(email_message['html'])
        
        if not verification_link:
            return {"success": False, "error": "未找到验证链接", "email": email_address}
        
        print(f"  ✅ 验证链接: {verification_link[:80]}...")
        
        # 访问验证链接完成激活
        print("  访问验证链接...")
        activator.driver.get(verification_link)
        time.sleep(3)
        
        print(f"  当前 URL: {activator.driver.current_url}")
        
        # 步骤1: 智能等待跳转到 onboarding 页面
        print("\n  🔄 等待页面跳转到 onboarding...")
        print("-" * 60)
        
        onboarding_reached = False
        for wait_attempt in range(3):  # 最多等待 9 秒
            current_url = activator.driver.current_url
            
            # 检查是否有账号违规错误
            try:
                page_source = activator.driver.page_source
                if 'This account violates our' in page_source or 'auth-error' in page_source:
                    print("  ❌ 检测到账号违规错误！")
                    print("  错误信息: 账号违反服务条款，激活失败")
                    return {
                        "success": False, 
                        "error": "账号违反服务条款 (Terms of Service violation)",
                        "email": email_address
                    }
            except Exception as e:
                pass
            
            # 检查是否到达 onboarding 页面
            if '/onboarding' in current_url:
                print(f"  ✅ 已到达 onboarding 页面！")
                onboarding_reached = True
                break
            
            # 识别中间页面
            if '/logged_in/download' in current_url:
                print(f"  ⏳ 当前在下载页面，等待自动跳转... (尝试 {wait_attempt + 1}/3)")
            elif '/referral/' in current_url:
                print(f"  ⏳ 当前在推荐页面，等待自动跳转... (尝试 {wait_attempt + 1}/3)")
            elif 'firebaseapp.com' in current_url:
                print(f"  ⏳ 当前在 Firebase 页面，等待重定向... (尝试 {wait_attempt + 1}/3)")
            else:
                print(f"  ⏳ 当前页面: {current_url[:60]}... (尝试 {wait_attempt + 1}/3)")
            
            time.sleep(3)
        
        # 步骤2: 如果还没到 onboarding，手动访问
        if not onboarding_reached:
            print("\n  ⚠️ 自动跳转超时，手动访问 onboarding 页面...")
            activator.driver.get('https://app.warp.dev/onboarding')
            time.sleep(5)
            
            current_url = activator.driver.current_url
            if '/onboarding' in current_url:
                print(f"  ✅ 已手动跳转到 onboarding 页面")
                onboarding_reached = True
            else:
                print(f"  ⚠️ 手动跳转后仍未到达 onboarding: {current_url[:80]}")
        
        # 步骤3: 在 onboarding 页面查找 Token（多次尝试）
        print("\n  🔍 在 onboarding 页面查找 Token...")
        print("-" * 60)
        
        firebase_user = None
        for attempt in range(5):
            print(f"  尝试 {attempt + 1}/5...")
            
            current_url = activator.driver.current_url
            print(f"     当前 URL: {current_url[:80]}...")
            
            # 再次检查是否有违规错误
            try:
                page_source = activator.driver.page_source
                if 'This account violates our' in page_source or 'auth-error' in page_source:
                    print("  ❌ 检测到账号违规错误！")
                    return {
                        "success": False, 
                        "error": "账号违反服务条款 (Terms of Service violation)",
                        "email": email_address
                    }
            except Exception as e:
                pass
            
            # 方式1: 检查页面内容中是否有 warp:// 链接
            try:
                page_source = activator.driver.page_source
                if 'warp://auth/desktop_redirect' in page_source:
                    print(f"  ✅ 页面中发现 warp:// 链接！")
                    # 尝试从页面中提取链接
                    import re
                    
                    # 方法1: 查找完整的 warp:// URL（匹配到引号或尖括号为止）
                    match = re.search(r'warp://auth/desktop_redirect\?([^"\'<>]+)', page_source)
                    if match:
                        params_str = match.group(1).strip()
                        warp_url = f"warp://auth/desktop_redirect?{params_str}"
                        print(f"  提取到链接: {warp_url[:100]}...")
                        
                        # 先解码 HTML 实体（&amp; -> &）
                        import html
                        params_str = html.unescape(params_str)
                        
                        # 解析所有参数
                        params = {}
                        for param in params_str.split('&'):
                            param = param.strip()
                            if '=' in param:
                                key, value = param.split('=', 1)
                                params[key] = value
                        
                        refresh_token = params.get('refresh_token')
                        user_uid = params.get('user_uid')
                        
                        print(f"  解析参数: refresh_token={'存在' if refresh_token else '不存在'}, user_uid={'存在' if user_uid else '不存在'}")
                        print(f"  所有参数: {list(params.keys())}")
                        
                        # 必须同时有 refresh_token 和 user_uid
                        if refresh_token and user_uid:
                            # 使用 refresh_token 获取 id_token
                            id_token = None
                            try:
                                print(f"  🔄 使用 refresh_token 获取 id_token...")
                                import requests
                                response = requests.post(
                                    'https://securetoken.googleapis.com/v1/token',
                                    params={'key': config.FIREBASE_API_KEY},
                                    json={
                                        'grant_type': 'refresh_token',
                                        'refresh_token': refresh_token
                                    }
                                )
                                
                                if response.status_code == 200:
                                    token_data = response.json()
                                    id_token = token_data.get('id_token')
                                    print(f"  ✅ 成功获取 id_token")
                                else:
                                    print(f"  ⚠️ 获取 id_token 失败: {response.status_code}")
                            except Exception as e:
                                print(f"  ⚠️ 获取 id_token 出错: {e}")
                            
                            firebase_user = {
                                'email': email_address,
                                'uid': user_uid,
                                'refreshToken': refresh_token,
                                'idToken': id_token,
                                'warp_url': warp_url  # 保存完整的 warp:// URL
                            }
                            print(f"  ✅ 从页面内容获取到完整 Token！")
                            break
                        elif refresh_token:
                            print(f"  ⚠️ 只找到 refresh_token，缺少 user_uid")
                        else:
                            print(f"  ⚠️ 未找到 refresh_token")
            except Exception as e:
                print(f"  ⚠️ 检查页面内容失败: {e}")
                import traceback
                traceback.print_exc()
            
            # 方式2: 检查 localStorage
            try:
                local_user = activator.driver.execute_script("""
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
                
                if local_user and (local_user.get('idToken') or local_user.get('refreshToken')):
                    firebase_user = local_user
                    print(f"  ✅ 从 localStorage 获取到 Token！")
                    break
            except Exception as e:
                print(f"  ⚠️ 检查 localStorage 失败: {e}")
            
            if attempt < 4:  # 最后一次不等待
                print(f"  ⏳ 未找到 Token，等待 2 秒后重试...")
                time.sleep(2)
        
        # 步骤4: 检查是否成功获取 Token
        if not firebase_user or not (firebase_user.get('idToken') or firebase_user.get('refreshToken')):
            print("\n  ❌ 无法获取认证 Token，注册失败")
            return {
                "success": False,
                "error": "无法获取认证 Token",
                "email": email_address
            }
        
        if firebase_user and (firebase_user.get('idToken') or firebase_user.get('refreshToken')):
            print("\n" + "="*60)
            print("✅ 激活成功！开始领取额度...")
            print("="*60 + "\n")
            
            # 访问主页触发额度领取
            try:
                print("🎁 访问主页触发额度领取...")
                activator.driver.get('https://app.warp.dev')
                print("  等待主页完全加载...")
                
                # 等待 Loading 消失并且 Canvas 出现
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                
                try:
                    # 1. 等待 Loading 消失（最多 15 秒）
                    print("  等待 Loading 消失...")
                    try:
                        WebDriverWait(activator.driver, 15).until_not(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.modal-container-header'))
                        )
                        print("  ✅ Loading 已消失")
                    except:
                        print("  ℹ️ 未检测到 Loading 元素（可能已加载完成）")
                    
                    # 2. 等待页面稳定（简单等待，不依赖特定元素）
                    print("  等待页面稳定...")
                    time.sleep(3)
                    
                    # 3. 检查页面是否加载成功（检查 URL）
                    current_url = activator.driver.current_url
                    if 'app.warp.dev' in current_url:
                        print("  ✅ 主页加载完成")
                    else:
                        print(f"  ⚠️ 当前页面: {current_url}")
                    
                except Exception as e:
                    print(f"  ⚠️ 页面加载检查出错: {e}")
                    print("  继续执行...")
                    time.sleep(3)
                
                # 重新获取 id_token（可能已更新）
                print("\n🔄 重新获取最新 Token...")
                new_firebase_user = activator.driver.execute_script("""
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
                
                if new_firebase_user and new_firebase_user.get('idToken'):
                    firebase_user['idToken'] = new_firebase_user['idToken']
                    print("  ✅ Token 已更新")
                
            except Exception as e:
                print(f"  ⚠️ 领取额度过程出错: {e}")
            
            duration = time.time() - start_time
            
            print("\n" + "="*60)
            print("✅ 注册完成！")
            print("="*60)
            print(f"📧 邮箱: {email_address}")
            print(f"🆔 UID: {firebase_user.get('uid', 'N/A')}")
            if firebase_user.get('idToken'):
                print(f"🔑 ID Token: {firebase_user['idToken'][:50]}...")
            if firebase_user.get('refreshToken'):
                print(f"🔄 Refresh Token: {firebase_user['refreshToken'][:50]}...")
            print(f"⏱️  耗时: {duration:.1f} 秒")
            print("="*60 + "\n")
            
            # 获取账号配额信息
            quota_info = None
            if firebase_user.get('idToken'):
                try:
                    print("📊 获取账号配额信息...")
                    import requests
                    
                    id_token = firebase_user['idToken']
                    print(f"  使用 ID Token: {id_token[:50]}...")
                    
                    quota_response = requests.post(
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
                                    "clientContext": {
                                        "version": "v0.2025.10.08.08.12.stable_03"
                                    },
                                    "osContext": {
                                        "category": "Web",
                                        "name": "Windows",
                                        "version": "NT 10.0"
                                    }
                                }
                            },
                            "operationName": "GetRequestLimitInfo"
                        }
                    )
                    
                    print(f"  响应状态码: {quota_response.status_code}")
                    
                    if quota_response.status_code == 200:
                        quota_data = quota_response.json()
                        print(f"  响应数据: {quota_data}")
                        
                        limit_info = quota_data.get('data', {}).get('user', {}).get('user', {}).get('requestLimitInfo', {})
                        if limit_info:
                            # 只保存关键信息
                            quota_info = {
                                'requestLimit': limit_info.get('requestLimit'),
                                'requestsUsed': limit_info.get('requestsUsedSinceLastRefresh'),
                                'nextRefresh': limit_info.get('nextRefreshTime')
                            }
                            print(f"  ✅ 请求限额: {quota_info['requestLimit']}")
                            print(f"  ✅ 已使用: {quota_info['requestsUsed']}")
                        else:
                            print(f"  ⚠️ 未找到 requestLimitInfo")
                    else:
                        print(f"  ⚠️ 请求失败: {quota_response.text}")
                except Exception as e:
                    print(f"  ⚠️ 获取配额信息失败: {e}")
                    import traceback
                    traceback.print_exc()
            
            # 保存账号信息到 JSON 文件
            account_data = {
                "email": email_address,
                "uid": firebase_user.get('uid'),
                "refresh_token": firebase_user.get('refreshToken'),
                "id_token": firebase_user.get('idToken'),
                "warp_url": firebase_user.get('warp_url'),
                "quota_info": quota_info,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "duration": duration
            }
            
            # 保存到文件
            import json
            import os
            
            # 创建按日期分类的目录结构（使用脚本所在目录的绝对路径）
            script_dir = os.path.dirname(os.path.abspath(__file__))
            accounts_dir = os.path.join(script_dir, 'accounts')
            
            # 按日期创建子目录（格式：YYYY-MM-DD）
            date_str = time.strftime("%Y-%m-%d")
            date_dir = os.path.join(accounts_dir, date_str)
            os.makedirs(date_dir, exist_ok=True)
            
            # 使用邮箱用户名作为文件名（@之前的部分）
            username = email_address.split('@')[0]
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(date_dir, f"{username}_{timestamp}.json")
            
            # 保存单个账号信息
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(account_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 账号信息已保存: {filename}")
            
            # 更新当天的汇总文件 all_accounts.json
            all_accounts_file = os.path.join(date_dir, 'all_accounts.json')
            
            # 读取现有的汇总数据
            if os.path.exists(all_accounts_file):
                try:
                    with open(all_accounts_file, 'r', encoding='utf-8') as f:
                        all_accounts = json.load(f)
                except:
                    all_accounts = []
            else:
                all_accounts = []
            
            # 添加新账号到汇总列表
            all_accounts.append(account_data)
            
            # 保存汇总文件
            with open(all_accounts_file, 'w', encoding='utf-8') as f:
                json.dump(all_accounts, f, indent=2, ensure_ascii=False)
            
            print(f"📋 已更新汇总文件: {all_accounts_file}")
            print(f"📊 今日已注册账号数: {len(all_accounts)}\n")
            
            return {
                "success": True,
                "email": email_address,
                "uid": firebase_user.get('uid'),
                "id_token": firebase_user.get('idToken'),
                "refresh_token": firebase_user.get('refreshToken'),
                "warp_url": firebase_user.get('warp_url'),
                "duration": duration,
                "saved_file": filename
            }
        else:
            return {"success": False, "error": "未获取到 Token", "email": email_address}
        
    except Exception as e:
        print(f"\n❌ 注册过程出错: {e}\n")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}
    
    finally:
        activator.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Warp 注册工具 (Undetected-Chromedriver)')
    parser.add_argument('--headless', type=str, choices=['true', 'false'], 
                       help='是否无头模式')
    args = parser.parse_args()
    
    # 验证配置
    try:
        config.validate()
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("请检查 .env 文件")
        sys.exit(1)
    
    # 确定 headless 模式
    headless = None
    if args.headless:
        headless = args.headless == 'true'
    
    # 执行注册
    register_single_account(headless=headless)


if __name__ == "__main__":
    main()
