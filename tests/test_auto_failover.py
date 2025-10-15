#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Auto 模式的故障转移功能
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_service import EmailService
from config import config


def test_auto_failover_simulation():
    """测试 Auto 模式故障转移（模拟）"""
    print("\n" + "="*60)
    print("Auto 模式故障转移测试")
    print("="*60)
    
    print(f"\n当前配置:")
    print(f"  EMAIL_SERVICE: {config.EMAIL_SERVICE}")
    print(f"  MOEMAIL_API_KEY: {'已配置' if config.MOEMAIL_API_KEY else '未配置'}")
    print(f"  SKYMAIL_TOKEN: {'已配置' if config.SKYMAIL_TOKEN else '未配置'}")
    
    # 检查是否为 auto 模式
    if config.EMAIL_SERVICE != 'auto':
        print(f"\n⚠️ 当前不是 auto 模式，请在 .env 中设置 EMAIL_SERVICE=auto")
        return False
    
    # 检查是否配置了多个服务
    services_count = 0
    if config.MOEMAIL_API_KEY:
        services_count += 1
    if config.SKYMAIL_TOKEN:
        services_count += 1
    
    if services_count < 2:
        print(f"\n⚠️ 只配置了 {services_count} 个服务，无法测试故障转移")
        print(f"   请配置至少两个邮箱服务")
        return False
    
    print(f"\n✅ 已配置 {services_count} 个服务，可以测试故障转移")
    
    # 测试失败记录功能
    print("\n" + "="*60)
    print("测试失败记录功能")
    print("="*60)
    
    # 手动记录失败
    print("\n模拟 moemail 连续失败 3 次...")
    for i in range(3):
        EmailService._record_service_failure('moemail')
    
    # 检查是否被标记为失败
    is_failed = EmailService._is_service_failed('moemail')
    print(f"\nmoemail 是否被标记为失败: {is_failed}")
    
    if is_failed:
        print("✅ 失败记录功能正常")
    else:
        print("❌ 失败记录功能异常")
    
    # 测试服务选择（应该排除 moemail）
    print("\n" + "="*60)
    print("测试服务选择（应排除失败的服务）")
    print("="*60)
    
    email_service = EmailService('auto')
    print(f"\n选中的服务: {email_service.service_type}")
    
    if email_service.service_type != 'moemail':
        print("✅ 成功排除失败的服务")
    else:
        print("⚠️ 未能排除失败的服务（可能是唯一可用的服务）")
    
    # 清除失败记录
    print("\n" + "="*60)
    print("清除失败记录")
    print("="*60)
    
    EmailService._clear_failed_services()
    is_failed_after_clear = EmailService._is_service_failed('moemail')
    print(f"\n清除后 moemail 是否仍被标记为失败: {is_failed_after_clear}")
    
    if not is_failed_after_clear:
        print("✅ 失败记录清除成功")
    else:
        print("❌ 失败记录清除失败")
    
    # 测试成功记录
    print("\n" + "="*60)
    print("测试成功记录功能")
    print("="*60)
    
    print("\n模拟 skymail 失败 2 次...")
    EmailService._record_service_failure('skymail')
    EmailService._record_service_failure('skymail')
    
    print("\n记录 skymail 成功...")
    EmailService._record_service_success('skymail')
    
    is_failed = EmailService._is_service_failed('skymail')
    print(f"\nskymail 是否被标记为失败: {is_failed}")
    
    if not is_failed:
        print("✅ 成功记录功能正常（失败记录已清除）")
    else:
        print("❌ 成功记录功能异常")
    
    print("\n" + "="*60)
    print("✅ 所有测试完成")
    print("="*60)
    
    print("\n功能说明:")
    print("  1. 失败记录 - 记录每个服务的失败次数")
    print("  2. 临时排除 - 连续失败 3 次后临时排除（5分钟）")
    print("  3. 自动恢复 - 5分钟后自动清除失败记录")
    print("  4. 成功清除 - 服务成功后立即清除失败记录")
    
    return True


if __name__ == "__main__":
    test_auto_failover_simulation()



def test_service_health_check():
    """测试邮箱服务健康检查"""
    import requests
    import time
    
    print("\n" + "="*60)
    print("邮箱服务健康检查测试")
    print("="*60)
    
    print(f"\n当前配置:")
    print(f"  EMAIL_SERVICE: {config.EMAIL_SERVICE}")
    print(f"  MOEMAIL_URL: {config.MOEMAIL_URL}")
    print(f"  MOEMAIL_API_KEY: {'已配置' if config.MOEMAIL_API_KEY else '未配置'}")
    print(f"  SKYMAIL_URL: {getattr(config, 'SKYMAIL_URL', 'N/A')}")
    print(f"  SKYMAIL_TOKEN: {'已配置' if getattr(config, 'SKYMAIL_TOKEN', '') else '未配置'}")
    
    results = {}
    
    # 检查 MoeMail
    if config.MOEMAIL_API_KEY:
        print("\n" + "-"*60)
        print("检查 MoeMail 服务")
        print("-"*60)
        
        try:
            start_time = time.time()
            url = f"{config.MOEMAIL_URL}/api/config"
            
            print(f"  请求 URL: {url}")
            print(f"  超时时间: 5秒")
            
            response = requests.get(
                url,
                headers={'X-API-Key': config.MOEMAIL_API_KEY},
                timeout=5
            )
            
            elapsed = time.time() - start_time
            
            print(f"  响应状态码: {response.status_code}")
            print(f"  响应时间: {elapsed:.2f}秒")
            
            if response.status_code == 200:
                print(f"  ✅ MoeMail 服务可用")
                results['moemail'] = {'available': True, 'response_time': elapsed}
            else:
                print(f"  ❌ MoeMail 服务不可用 (HTTP {response.status_code})")
                results['moemail'] = {'available': False, 'error': f'HTTP {response.status_code}'}
                
        except requests.Timeout:
            print(f"  ❌ MoeMail 服务超时")
            results['moemail'] = {'available': False, 'error': 'Timeout'}
        except Exception as e:
            print(f"  ❌ MoeMail 服务异常: {e}")
            results['moemail'] = {'available': False, 'error': str(e)}
    else:
        print("\n⚠️ MoeMail 未配置，跳过检查")
        results['moemail'] = {'available': False, 'error': 'Not configured'}
    
    # 检查 Skymail
    skymail_token = getattr(config, 'SKYMAIL_TOKEN', '')
    if skymail_token:
        print("\n" + "-"*60)
        print("检查 Skymail 服务")
        print("-"*60)
        
        try:
            # 禁用 SSL 警告
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            start_time = time.time()
            skymail_url = getattr(config, 'SKYMAIL_URL', 'https://cloudmail.qixc.pp.ua')
            url = f"{skymail_url}/api/public/emailList"
            
            print(f"  请求 URL: {url}")
            print(f"  超时时间: 5秒")
            
            # 使用查询邮件接口测试（不会创建任何数据）
            response = requests.post(
                url,
                headers={
                    'Authorization': skymail_token,
                    'Content-Type': 'application/json'
                },
                json={
                    'toEmail': 'test@test.com',
                    'type': 0,
                    'isDel': 0,
                    'timeSort': 'desc',
                    'num': 1,
                    'size': 1
                },
                verify=False,
                timeout=5
            )
            
            elapsed = time.time() - start_time
            
            print(f"  响应状态码: {response.status_code}")
            print(f"  响应时间: {elapsed:.2f}秒")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    print(f"  ✅ Skymail 服务可用")
                    results['skymail'] = {'available': True, 'response_time': elapsed}
                else:
                    print(f"  ❌ Skymail 服务不可用 (API code: {result.get('code')})")
                    print(f"     消息: {result.get('message')}")
                    results['skymail'] = {'available': False, 'error': result.get('message')}
            else:
                print(f"  ❌ Skymail 服务不可用 (HTTP {response.status_code})")
                results['skymail'] = {'available': False, 'error': f'HTTP {response.status_code}'}
                
        except requests.Timeout:
            print(f"  ❌ Skymail 服务超时")
            results['skymail'] = {'available': False, 'error': 'Timeout'}
        except Exception as e:
            print(f"  ❌ Skymail 服务异常: {e}")
            results['skymail'] = {'available': False, 'error': str(e)}
    else:
        print("\n⚠️ Skymail 未配置，跳过检查")
        results['skymail'] = {'available': False, 'error': 'Not configured'}
    
    # 汇总结果
    print("\n" + "="*60)
    print("健康检查结果汇总")
    print("="*60)
    
    available_count = 0
    for service, info in results.items():
        status = "✅ 可用" if info['available'] else "❌ 不可用"
        print(f"\n{service}:")
        print(f"  状态: {status}")
        
        if info['available']:
            print(f"  响应时间: {info['response_time']:.2f}秒")
            available_count += 1
        else:
            print(f"  错误: {info['error']}")
    
    print(f"\n可用服务数: {available_count}/{len(results)}")
    
    # 给出建议
    print("\n" + "="*60)
    print("建议")
    print("="*60)
    
    if available_count == 0:
        print("\n❌ 没有可用的邮箱服务")
        print("   请检查:")
        print("   1. 网络连接是否正常")
        print("   2. 服务 URL 是否正确")
        print("   3. API Key/Token 是否有效")
        print("   4. 服务是否在线")
    elif available_count == 1:
        available_service = [s for s, i in results.items() if i['available']][0]
        print(f"\n⚠️ 只有一个服务可用: {available_service}")
        print("   建议:")
        print("   1. 配置多个邮箱服务提高可用性")
        print("   2. 检查其他服务的配置")
    else:
        print(f"\n✅ 有 {available_count} 个服务可用")
        print("   可以使用 EMAIL_SERVICE=auto 模式")
        print("   系统会自动在可用服务间负载均衡")
    
    return results


def test_health_check_timing():
    """测试健康检查耗时（方案A：实例级别）"""
    import time
    
    print("\n" + "="*60)
    print("健康检查耗时测试（方案A：实例级别）")
    print("="*60)
    
    print(f"\n当前配置:")
    print(f"  EMAIL_SERVICE: {config.EMAIL_SERVICE}")
    print(f"  MOEMAIL_API_KEY: {'已配置' if config.MOEMAIL_API_KEY else '未配置'}")
    print(f"  SKYMAIL_TOKEN: {'已配置' if getattr(config, 'SKYMAIL_TOKEN', '') else '未配置'}")
    
    # 测试多次实例化，记录每次耗时
    test_rounds = 5
    timing_results = []
    
    print(f"\n模拟 {test_rounds} 次注册（每次创建新实例）...")
    print("-"*60)
    
    for i in range(test_rounds):
        print(f"\n第 {i+1} 次注册:")
        
        # 记录开始时间
        start_time = time.time()
        
        # 创建新实例（会触发健康检查）
        try:
            email_service = EmailService('auto')
            init_time = time.time() - start_time
            
            print(f"  初始化耗时: {init_time:.3f}秒")
            print(f"  选中服务: {email_service.service_type}")
            
            timing_results.append({
                'round': i + 1,
                'init_time': init_time,
                'selected_service': email_service.service_type,
                'success': True
            })
            
        except Exception as e:
            init_time = time.time() - start_time
            print(f"  初始化失败: {e}")
            print(f"  耗时: {init_time:.3f}秒")
            
            timing_results.append({
                'round': i + 1,
                'init_time': init_time,
                'selected_service': None,
                'success': False
            })
        
        # 等待一下，模拟真实场景
        if i < test_rounds - 1:
            time.sleep(1)
    
    # 统计结果
    print("\n" + "="*60)
    print("耗时统计")
    print("="*60)
    
    successful_times = [r['init_time'] for r in timing_results if r['success']]
    
    if successful_times:
        avg_time = sum(successful_times) / len(successful_times)
        min_time = min(successful_times)
        max_time = max(successful_times)
        
        print(f"\n成功次数: {len(successful_times)}/{test_rounds}")
        print(f"平均耗时: {avg_time:.3f}秒")
        print(f"最快耗时: {min_time:.3f}秒")
        print(f"最慢耗时: {max_time:.3f}秒")
        
        # 详细列表
        print(f"\n详细耗时:")
        for r in timing_results:
            if r['success']:
                print(f"  第{r['round']}次: {r['init_time']:.3f}秒 - {r['selected_service']}")
            else:
                print(f"  第{r['round']}次: {r['init_time']:.3f}秒 - 失败")
    else:
        print("\n所有测试都失败了")
    
    # 分析
    print("\n" + "="*60)
    print("方案A分析")
    print("="*60)
    
    print(f"\n特点:")
    print(f"  ✅ 每次实例化都重新检查")
    print(f"  ✅ 自动隔离，互不影响")
    print(f"  ✅ 自动恢复，下次重新检查")
    
    if successful_times:
        if avg_time < 1.0:
            print(f"\n性能评估: ✅ 优秀")
            print(f"  平均耗时 {avg_time:.3f}秒，对用户体验影响很小")
        elif avg_time < 3.0:
            print(f"\n性能评估: ✅ 良好")
            print(f"  平均耗时 {avg_time:.3f}秒，可接受")
        else:
            print(f"\n性能评估: ⚠️ 需要优化")
            print(f"  平均耗时 {avg_time:.3f}秒，可能影响用户体验")
            print(f"  建议: 考虑使用缓存方案（方案B或C）")
    
    print(f"\n适用场景:")
    print(f"  ✅ 单次注册")
    print(f"  ✅ 小批量注册（< 10个）")
    if successful_times and avg_time > 2.0:
        print(f"  ⚠️ 大批量注册（可能较慢）")
    else:
        print(f"  ✅ 大批量注册")
    
    return timing_results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--health-check":
            # 健康检查测试
            test_service_health_check()
        elif sys.argv[1] == "--timing":
            # 健康检查耗时测试
            test_health_check_timing()
        elif sys.argv[1] == "--help":
            print("\n可用参数:")
            print("  (无参数)         运行故障转移模拟测试")
            print("  --health-check   运行邮箱服务健康检查")
            print("  --timing         测试健康检查耗时（方案A）")
            print("  --help           显示帮助信息")
        else:
            print(f"未知参数: {sys.argv[1]}")
            print("使用 --help 查看可用参数")
    else:
        # 默认运行故障转移测试
        test_auto_failover_simulation()
