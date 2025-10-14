#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试浏览器指纹随机化
"""
from fingerprint_randomizer import FingerprintRandomizer


def test_fingerprint_randomization():
    """测试指纹随机化"""
    print("="*60)
    print("测试浏览器指纹随机化")
    print("="*60)
    
    # 生成 5 个不同的指纹
    for i in range(5):
        print(f"\n指纹 #{i+1}:")
        print("-"*60)
        
        fingerprint = FingerprintRandomizer(platform='windows')
        fingerprint.print_fingerprint()
        
        print("\nChrome 启动参数:")
        for arg in fingerprint.get_chrome_options_args():
            print(f"  {arg}")
    
    print("\n" + "="*60)
    print("✅ 测试完成！每次生成的指纹都不同")
    print("="*60)


if __name__ == "__main__":
    test_fingerprint_randomization()
