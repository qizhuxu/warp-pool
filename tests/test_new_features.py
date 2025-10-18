#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新增的指纹模拟功能
"""
from fingerprint_randomizer import FingerprintRandomizer

def test_new_features():
    """测试新增的指纹功能"""
    print("🧪 测试新增的指纹模拟功能...")
    
    # 创建 balanced 级别的随机化器
    randomizer = FingerprintRandomizer(level='balanced', enhanced_profiles=True)
    
    print("\n📊 指纹信息:")
    randomizer.print_fingerprint()
    
    print("\n🔍 新增功能验证:")
    
    # 1. 检查哈希指纹
    if randomizer.profile and 'hashes' in randomizer.profile:
        hashes = randomizer.profile['hashes']
        print(f"  ✅ 哈希指纹: {len(hashes)} 个")
        for key, value in hashes.items():
            print(f"     - {key}: {value}")
    
    # 2. 检查 JS 堆内存信息
    fp = randomizer.fingerprint
    print(f"  ✅ JS 堆内存信息:")
    print(f"     - 堆内存限制: {fp.get('js_heap_size_limit', 0):,} bytes")
    print(f"     - 已用堆内存: {fp.get('used_js_heap_size', 0):,} bytes")
    print(f"     - 总堆内存: {fp.get('total_js_heap_size', 0):,} bytes")
    
    # 3. 检查 Window Keys
    window_keys = fp.get('window_keys', [])
    print(f"  ✅ Window Keys: {len(window_keys)} 个")
    print(f"     - 前10个: {window_keys[:10]}")
    print(f"     - 包含 WebGL: {'WebGLRenderingContext' in window_keys}")
    print(f"     - 包含 Audio: {'AudioContext' in window_keys}")
    print(f"     - 包含 WebRTC: {'RTCPeerConnection' in window_keys}")
    
    # 4. 检查脚本生成
    all_scripts = randomizer.get_all_scripts()
    print(f"\n📜 生成的脚本:")
    print(f"  ✅ 总长度: {len(all_scripts):,} 字符")
    
    # 检查新增脚本是否包含
    new_features = {
        'JS 堆内存指纹': 'JS 堆内存指纹已注入',
        'Window Keys 指纹': 'Window Keys 指纹已注入', 
        '哈希指纹': '哈希指纹已注入'
    }
    
    for feature, keyword in new_features.items():
        included = keyword in all_scripts
        status = "✅" if included else "❌"
        print(f"  {status} {feature}: {'包含' if included else '不包含'}")
    
    print(f"\n🎯 总结:")
    print(f"  - 配置文件: {randomizer.profile['name'] if randomizer.profile else 'N/A'}")
    print(f"  - 指纹级别: {randomizer.level}")
    print(f"  - 哈希指纹: {len(randomizer.profile.get('hashes', {})) if randomizer.profile else 0} 个")
    print(f"  - Window Keys: {len(fp.get('window_keys', []))} 个")
    print(f"  - JS 堆内存: 已配置")
    print(f"  - 脚本长度: {len(all_scripts):,} 字符")

if __name__ == "__main__":
    test_new_features()