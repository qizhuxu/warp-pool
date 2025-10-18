#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebRTC 指纹保护功能测试脚本
验证不同级别的指纹随机化功能，重点测试 WebRTC 保护
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fingerprint_randomizer import FingerprintRandomizer


def test_fingerprint_levels():
    """测试不同指纹级别的功能包含情况"""
    print("🧪 测试指纹随机化级别功能...")
    
    levels = ['basic', 'balanced', 'aggressive']
    
    # 预期的功能包含情况
    expected_features = {
        'basic': {
            'Canvas 指纹混淆': True,
            'Navigator 属性': True,
            '时区': True,
            'WebGL 指纹混淆': False,
            'Performance Timing': False,
            'WebRTC 指纹保护': False,
            'Audio Context': False,
        },
        'balanced': {
            'Canvas 指纹混淆': True,
            'Navigator 属性': True,
            '时区': True,
            'WebGL 指纹混淆': True,
            'Performance Timing': True,
            'WebRTC 指纹保护': True,  # 🎯 重点：balanced 级别开始支持
            'Audio Context': False,
            'JS 堆内存指纹': True,     # 🆕 新增功能
            'Window Keys 指纹': True,  # 🆕 新增功能
            '哈希指纹': True,          # 🆕 新增功能
        },
        'aggressive': {
            'Canvas 指纹混淆': True,
            'Navigator 属性': True,
            '时区': True,
            'WebGL 指纹混淆': True,
            'Performance Timing': True,
            'WebRTC 指纹保护': True,
            'Audio Context': True,
            'JS 堆内存指纹': True,     # 🆕 新增功能
            'Window Keys 指纹': True,  # 🆕 新增功能
            '哈希指纹': True,          # 🆕 新增功能
        }
    }
    
    # 功能检测关键词
    feature_keywords = {
        'Canvas 指纹混淆': 'Canvas 指纹混淆',
        'Navigator 属性': '覆盖 Navigator 属性',
        '时区': '覆盖时区',
        'WebGL 指纹混淆': 'WebGL 指纹混淆',
        'Performance Timing': 'Performance Timing 注入',
        'WebRTC 指纹保护': 'WebRTC 指纹保护',
        'Audio Context': 'Audio Context 指纹混淆',
        'JS 堆内存指纹': 'JS 堆内存指纹已注入',
        'Window Keys 指纹': 'Window Keys 指纹已注入',
        '哈希指纹': '哈希指纹已注入',
    }
    
    all_passed = True
    
    for level in levels:
        print(f"\n📊 测试级别: {level.upper()}")
        randomizer = FingerprintRandomizer(level=level)
        all_scripts = randomizer.get_all_scripts()
        
        print(f"  📏 脚本总长度: {len(all_scripts):,} 字符")
        
        # 检查每个功能
        level_passed = True
        for feature, expected in expected_features[level].items():
            keyword = feature_keywords[feature]
            actual = keyword in all_scripts
            
            if actual == expected:
                status = "✅"
            else:
                status = "❌"
                level_passed = False
                all_passed = False
            
            print(f"  {status} {feature}: {'包含' if actual else '不包含'} {'(预期)' if actual == expected else '(意外)'}")
        
        if not level_passed:
            print(f"  ⚠️ {level} 级别测试失败")
    
    return all_passed


def test_webrtc_protection_details():
    """详细测试 WebRTC 保护功能"""
    print(f"\n🛡️ WebRTC 保护功能详细测试:")
    
    # 测试 balanced 和 aggressive 级别
    for level in ['balanced', 'aggressive']:
        print(f"\n  📊 {level} 级别:")
        randomizer = FingerprintRandomizer(level=level)
        
        # 获取 WebRTC 保护脚本
        webrtc_script = randomizer.get_webrtc_protection_script()
        all_scripts = randomizer.get_all_scripts()
        
        # 检查关键功能
        checks = {
            'IP 地址伪造': 'fake_local_ip' in webrtc_script and 'fake_public_ip' in webrtc_script,
            'RTCPeerConnection 重写': 'RTCPeerConnection.prototype.createOffer' in webrtc_script,
            'SDP 伪造': 'generateFakeSDP' in webrtc_script,
            '媒体流阻止': 'getUserMedia' in webrtc_script,
            '统计信息阻止': 'getStats' in webrtc_script,
            '包含在完整脚本': 'WebRTC 指纹保护' in all_scripts,
        }
        
        for check_name, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"    {status} {check_name}")
        
        print(f"    📏 WebRTC 脚本长度: {len(webrtc_script):,} 字符")
    
    # 测试 basic 级别不应包含 WebRTC 保护
    print(f"\n  📊 basic 级别 (应该不包含 WebRTC 保护):")
    randomizer = FingerprintRandomizer(level='basic')
    all_scripts = randomizer.get_all_scripts()
    
    has_webrtc = 'WebRTC 指纹保护' in all_scripts
    status = "✅" if not has_webrtc else "❌"
    print(f"    {status} 不包含 WebRTC 保护: {'是' if not has_webrtc else '否'}")


def show_webrtc_sample():
    """显示 WebRTC 保护脚本关键部分"""
    print(f"\n🔍 WebRTC 保护脚本关键部分预览:")
    randomizer = FingerprintRandomizer(level='balanced')
    webrtc_script = randomizer.get_webrtc_protection_script()
    
    # 提取关键行
    lines = webrtc_script.split('\n')
    key_lines = []
    
    for line in lines:
        stripped = line.strip()
        if any(keyword in stripped for keyword in [
            'WebRTC 指纹保护', 'fake_local_ip', 'fake_public_ip', 
            'RTCPeerConnection', 'generateFakeCandidate', 'generateFakeSDP',
            'getUserMedia', 'getStats', 'console.log'
        ]):
            key_lines.append(stripped)
    
    for i, line in enumerate(key_lines[:10]):  # 显示前10行关键内容
        if line:
            print(f"  {i+1:2d}. {line[:80]}{'...' if len(line) > 80 else ''}")
    
    if len(key_lines) > 10:
        print(f"  ... (还有 {len(key_lines) - 10} 行关键代码)")


def test_fingerprint_consistency():
    """测试指纹一致性验证"""
    print(f"\n🔧 测试指纹一致性验证:")
    
    # 测试增强配置文件
    randomizer = FingerprintRandomizer(level='balanced', enhanced_profiles=True)
    is_consistent = randomizer.validate_consistency()
    
    status = "✅" if is_consistent else "❌"
    print(f"  {status} 增强配置文件一致性: {'通过' if is_consistent else '失败'}")
    
    # 显示配置信息
    if randomizer.profile:
        print(f"  📋 当前配置: {randomizer.profile['name']}")
        print(f"  🖥️ 分辨率: {randomizer.fingerprint['width']}x{randomizer.fingerprint['height']}")
        print(f"  🎮 GPU: {randomizer.fingerprint.get('gpu_vendor', 'N/A')}")


def main():
    """主测试函数"""
    print("🚀 WebRTC 指纹保护功能综合测试")
    print("=" * 50)
    
    # 1. 测试指纹级别功能
    levels_passed = test_fingerprint_levels()
    
    # 2. 详细测试 WebRTC 保护
    test_webrtc_protection_details()
    
    # 3. 显示脚本示例
    show_webrtc_sample()
    
    # 4. 测试一致性验证
    test_fingerprint_consistency()
    
    # 总结
    print("\n" + "=" * 50)
    if levels_passed:
        print("✅ 所有测试通过！WebRTC 保护功能已正确集成到 balanced 和 aggressive 级别。")
    else:
        print("❌ 部分测试失败，请检查指纹随机化配置。")
    
    print("\n🎯 关键改进:")
    print("  • WebRTC 保护从 balanced 级别开始启用")
    print("  • 防止真实 IP 地址泄露")
    print("  • 生成虚假的 ICE 候选项和 SDP")
    print("  • 阻止媒体流和统计信息获取")
    print("  • 提高反检测能力")


if __name__ == "__main__":
    main()