#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试增强的指纹随机化功能
"""
from fingerprint_randomizer import FingerprintRandomizer


def test_fingerprint_level(level: str):
    """测试指定级别的指纹"""
    print(f"\n{'='*60}")
    print(f"测试级别: {level.upper()}")
    print(f"{'='*60}\n")
    
    # 创建指纹随机化器
    fingerprint = FingerprintRandomizer(
        platform='windows',
        level=level,
        enhanced_profiles=True
    )
    
    # 打印指纹信息
    fingerprint.print_fingerprint()
    
    # 验证一致性
    print(f"\n配置一致性检查: ", end='')
    if fingerprint.validate_consistency():
        print("✅ 通过")
    else:
        print("❌ 失败")
    
    # 显示注入的功能
    print(f"\n注入的功能:")
    features = []
    if level in ['basic', 'balanced', 'aggressive']:
        features.extend(['Canvas 指纹混淆', 'Navigator 属性覆盖', 'Timezone 随机化'])
    if level in ['balanced', 'aggressive']:
        features.extend(['WebGL 指纹混淆', 'Performance Timing 注入'])
    if level == 'aggressive':
        features.append('Audio Context 指纹混淆')
    
    for i, feature in enumerate(features, 1):
        print(f"  {i}. {feature}")
    
    # 显示脚本长度
    scripts = fingerprint.get_all_scripts()
    print(f"\n脚本总长度: {len(scripts)} 字符")
    print(f"脚本行数: {scripts.count(chr(10)) + 1} 行")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("增强指纹随机化功能测试")
    print("="*60)
    
    # 测试三个级别
    for level in ['basic', 'balanced', 'aggressive']:
        test_fingerprint_level(level)
    
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)
    print("\n推荐配置:")
    print("  - 新手/测试: basic")
    print("  - 生产环境: balanced ⭐")
    print("  - 追求极致: aggressive")
    print("\n配置方法:")
    print("  在 .env 文件中设置:")
    print("  FINGERPRINT_LEVEL=balanced")
    print()


if __name__ == "__main__":
    main()
