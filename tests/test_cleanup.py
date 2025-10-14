#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试浏览器进程清理
"""
import time
import psutil
from uc_activator import UCActivator


def count_chrome_processes():
    """统计 Chrome 相关进程数量"""
    count = 0
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] in ['chrome.exe', 'chromedriver.exe']:
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return count


def main():
    print("="*60)
    print("测试浏览器进程清理")
    print("="*60)
    
    # 启动前统计
    before_count = count_chrome_processes()
    print(f"\n启动前 Chrome 进程数: {before_count}")
    
    # 启动浏览器
    print("\n启动浏览器...")
    activator = UCActivator(headless=True)
    activator.start()
    
    time.sleep(2)
    
    # 启动后统计
    after_start = count_chrome_processes()
    print(f"启动后 Chrome 进程数: {after_start}")
    
    # 访问一个页面
    print("\n访问测试页面...")
    activator.driver.get('https://www.google.com')
    time.sleep(2)
    
    # 关闭浏览器
    print("\n关闭浏览器...")
    activator.close()
    
    time.sleep(2)
    
    # 关闭后统计
    after_close = count_chrome_processes()
    print(f"关闭后 Chrome 进程数: {after_close}")
    
    # 检查是否有残留
    if after_close > before_count:
        print(f"\n⚠️ 警告: 有 {after_close - before_count} 个进程未清理")
        print("残留进程列表:")
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] in ['chrome.exe', 'chromedriver.exe']:
                    print(f"  - {proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    else:
        print("\n✅ 所有进程已正确清理")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
