#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本
用于诊断 Chrome 和 ChromeDriver 相关问题
"""
import os
import sys
import platform
import subprocess


def check_chrome():
    """检查 Chrome 是否安装"""
    print("=" * 60)
    print("检查 Chrome 安装")
    print("=" * 60)
    
    system = platform.system()
    chrome_found = False
    chrome_version = None
    
    if system == 'Windows':
        chrome_paths = [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✅ 找到 Chrome: {path}")
                chrome_found = True
                try:
                    result = subprocess.check_output(
                        [path, '--version'],
                        stderr=subprocess.DEVNULL
                    ).decode('utf-8').strip()
                    chrome_version = result
                    print(f"   版本: {chrome_version}")
                except Exception as e:
                    print(f"   ⚠️ 无法获取版本: {e}")
                break
    else:
        try:
            result = subprocess.check_output(
                ['google-chrome', '--version'],
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
            chrome_version = result
            print(f"✅ 找到 Chrome: {chrome_version}")
            chrome_found = True
        except Exception:
            try:
                result = subprocess.check_output(
                    ['chromium-browser', '--version'],
                    stderr=subprocess.DEVNULL
                ).decode('utf-8').strip()
                chrome_version = result
                print(f"✅ 找到 Chromium: {chrome_version}")
                chrome_found = True
            except Exception:
                pass
    
    if not chrome_found:
        print("❌ 未找到 Chrome 安装")
        print("   请先安装 Google Chrome: https://www.google.com/chrome/")
        return False
    
    return True


def check_python_packages():
    """检查 Python 依赖包"""
    print("\n" + "=" * 60)
    print("检查 Python 依赖包")
    print("=" * 60)
    
    required_packages = [
        'undetected_chromedriver',
        'selenium',
        'requests',
        'dotenv'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            all_installed = False
    
    if not all_installed:
        print("\n请运行: pip install -r requirements.txt")
        return False
    
    return True


def check_env_file():
    """检查 .env 文件"""
    print("\n" + "=" * 60)
    print("检查 .env 配置")
    print("=" * 60)
    
    if not os.path.exists('.env'):
        print("❌ .env 文件不存在")
        print("   请复制 .env.example 并配置:")
        print("   copy .env.example .env  (Windows)")
        print("   cp .env.example .env    (Linux/Mac)")
        return False
    
    print("✅ .env 文件存在")
    
    # 检查关键配置
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        'MOEMAIL_API_KEY': '临时邮箱 API Key',
        'FIREBASE_API_KEY': 'Firebase API Key',
    }
    
    all_configured = True
    
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if not value or value == 'your_api_key_here' or value == 'your_api_key':
            print(f"⚠️ {var} 未配置 ({desc})")
            all_configured = False
        else:
            print(f"✅ {var} 已配置")
    
    # 检查可选配置
    chrome_version = os.getenv('CHROME_VERSION')
    if chrome_version:
        print(f"ℹ️ CHROME_VERSION = {chrome_version}")
    else:
        print(f"ℹ️ CHROME_VERSION 未设置（将自动检测）")
    
    return all_configured


def check_network():
    """检查网络连接"""
    print("\n" + "=" * 60)
    print("检查网络连接")
    print("=" * 60)
    
    import requests
    
    test_urls = [
        ('Google', 'https://www.google.com'),
        ('ChromeDriver', 'https://chromedriver.storage.googleapis.com'),
        ('GitHub', 'https://github.com'),
    ]
    
    all_ok = True
    
    for name, url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 400:
                print(f"✅ {name} 连接正常")
            else:
                print(f"⚠️ {name} 返回状态码: {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"❌ {name} 连接失败: {e}")
            all_ok = False
    
    return all_ok


def check_chromedriver_cache():
    """检查 ChromeDriver 缓存"""
    print("\n" + "=" * 60)
    print("检查 ChromeDriver 缓存")
    print("=" * 60)
    
    # Windows 和 Linux/Mac 的缓存路径不同
    if platform.system() == 'Windows':
        cache_dir = os.path.expanduser('~/.undetected_chromedriver')
    else:
        cache_dir = os.path.expanduser('~/.undetected_chromedriver')
    
    if os.path.exists(cache_dir):
        print(f"✅ 缓存目录存在: {cache_dir}")
        
        # 列出缓存的 ChromeDriver
        try:
            files = os.listdir(cache_dir)
            if files:
                print(f"   已缓存的文件:")
                for f in files:
                    file_path = os.path.join(cache_dir, f)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        print(f"   - {f} ({size:,} bytes)")
            else:
                print(f"   缓存目录为空")
        except Exception as e:
            print(f"   ⚠️ 无法读取缓存: {e}")
    else:
        print(f"ℹ️ 缓存目录不存在（首次运行会自动创建）")
        print(f"   {cache_dir}")
    
    return True  # 这只是信息检查，不影响结果


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Warp 注册工具 - 环境检查")
    print("=" * 60)
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python 版本: {sys.version}")
    print()
    
    checks = [
        ("Chrome 安装", check_chrome),
        ("Python 依赖", check_python_packages),
        ("配置文件", check_env_file),
        ("网络连接", check_network),
        ("ChromeDriver 缓存", check_chromedriver_cache),
    ]
    
    results = {}
    
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ {name} 检查失败: {e}")
            results[name] = False
    
    # 总结
    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)
    
    all_passed = True
    for name, result in results.items():
        if result is False:
            print(f"❌ {name}: 失败")
            all_passed = False
        elif result is True:
            print(f"✅ {name}: 通过")
        else:
            print(f"ℹ️ {name}: 已检查")
    
    print()
    
    if all_passed:
        print("🎉 所有检查通过！可以运行注册脚本了:")
        print("   python register.py")
    else:
        print("⚠️ 部分检查未通过，请先解决上述问题")
        print("\n常见问题:")
        print("1. Chrome 未安装 → 下载安装 Google Chrome")
        print("2. 依赖未安装 → pip install -r requirements.txt")
        print("3. .env 未配置 → 复制 .env.example 并填写配置")
        print("4. 网络问题 → 检查代理设置或防火墙")
    
    print()


if __name__ == "__main__":
    main()
