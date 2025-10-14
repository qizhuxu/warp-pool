#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Warp 批量注册脚本
支持注册到指定目标数量
"""
import os
import sys
import time
import glob
import random
import argparse
from typing import Dict, Any, List
from datetime import datetime

from config import config
from register import register_single_account


def count_existing_accounts() -> int:
    """
    统计已注册的账号总数
    
    Returns:
        int: 账号总数
    """
    if not os.path.exists('accounts'):
        return 0
    
    count = 0
    try:
        for date_dir in os.listdir('accounts'):
            date_path = os.path.join('accounts', date_dir)
            if os.path.isdir(date_path):
                # 查找所有 JSON 文件，排除 all_accounts.json
                json_files = glob.glob(os.path.join(date_path, '*.json'))
                count += len([f for f in json_files if 'all_accounts' not in os.path.basename(f)])
    except Exception as e:
        print(f"⚠️ 统计账号时出错: {e}")
    
    return count


def get_account_list() -> List[Dict[str, Any]]:
    """
    获取所有账号的详细信息
    
    Returns:
        List[Dict]: 账号信息列表
    """
    accounts = []
    
    if not os.path.exists('accounts'):
        return accounts
    
    try:
        import json
        for date_dir in os.listdir('accounts'):
            date_path = os.path.join('accounts', date_dir)
            if os.path.isdir(date_path):
                json_files = glob.glob(os.path.join(date_path, '*.json'))
                for json_file in json_files:
                    if 'all_accounts' not in os.path.basename(json_file):
                        try:
                            with open(json_file, 'r', encoding='utf-8') as f:
                                account_data = json.load(f)
                                accounts.append(account_data)
                        except:
                            pass
    except Exception as e:
        print(f"⚠️ 读取账号列表时出错: {e}")
    
    return accounts


def print_statistics(current: int, target: int, success: int, fail: int, elapsed: float):
    """
    打印统计信息
    
    Args:
        current: 当前账号总数
        target: 目标账号数
        success: 成功注册数
        fail: 失败次数
        elapsed: 已用时间（秒）
    """
    print("\n" + "="*60)
    print("📊 批量注册统计")
    print("="*60)
    print(f"📦 当前账号总数: {current}")
    print(f"🎯 目标账号数量: {target}")
    print(f"✅ 本次成功注册: {success}")
    print(f"❌ 本次失败次数: {fail}")
    print(f"⏱️  已用时间: {elapsed:.1f} 秒 ({elapsed/60:.1f} 分钟)")
    
    if success > 0:
        avg_time = elapsed / success
        print(f"⚡ 平均每个账号: {avg_time:.1f} 秒")
    
    remaining = target - current
    if remaining > 0 and success > 0:
        est_time = remaining * (elapsed / success)
        print(f"🕐 预计剩余时间: {est_time/60:.1f} 分钟")
    
    print("="*60 + "\n")


def batch_register(target_count: int, headless: bool = None, max_fails: int = 3) -> Dict[str, Any]:
    """
    批量注册到目标数量
    
    Args:
        target_count: 目标账号总数
        headless: 是否无头模式
        max_fails: 最大连续失败次数
    
    Returns:
        Dict: 批量注册结果
    """
    start_time = time.time()
    
    print("\n" + "="*60)
    print("🚀 Warp 批量注册工具")
    print("="*60 + "\n")
    
    # 1. 统计当前账号数
    current_count = count_existing_accounts()
    print(f"📊 当前账号总数: {current_count}")
    print(f"🎯 目标账号数量: {target_count}")
    
    # 2. 检查是否已达到目标
    if current_count >= target_count:
        print(f"\n✅ 已达到目标数量！无需继续注册。")
        return {
            "success": True,
            "message": "已达到目标数量",
            "current_count": current_count,
            "target_count": target_count,
            "registered": 0
        }
    
    # 3. 计算需要注册的数量
    need_count = target_count - current_count
    print(f"📝 需要注册: {need_count} 个账号")
    
    # 4. 预估时间
    avg_time_per_account = 180  # 平均 3 分钟
    estimated_time = need_count * avg_time_per_account
    print(f"⏱️  预计耗时: {estimated_time/60:.1f} 分钟")
    
    # 5. 确认开始
    print(f"\n{'='*60}")
    print(f"⚠️  注意事项:")
    print(f"  1. 建议间隔时间: {config.REGISTER_INTERVAL} 秒")
    print(f"  2. 连续失败 {max_fails} 次将自动停止")
    print(f"  3. 可随时按 Ctrl+C 中断")
    print(f"{'='*60}\n")
    
    input("按 Enter 键开始批量注册...")
    
    # 6. 开始批量注册
    success_count = 0
    fail_count = 0
    consecutive_fails = 0
    results = []
    attempt = 0
    
    # 使用 while 循环，直到成功数量达到目标
    while success_count < need_count:
        attempt += 1
        
        print(f"\n{'='*60}")
        print(f"📌 进度: 成功 {success_count}/{need_count} | 尝试 #{attempt} (总账号: {current_count + success_count})")
        print(f"{'='*60}")
        
        try:
            # 注册单个账号
            result = register_single_account(headless=headless)
            results.append(result)
            
            if result.get('success'):
                success_count += 1
                consecutive_fails = 0
                print(f"\n✅ 注册成功！邮箱: {result.get('email', 'unknown')}")
                print(f"🎯 已完成: {success_count}/{need_count}")
            else:
                fail_count += 1
                consecutive_fails += 1
                error = result.get('error', '未知错误')
                print(f"\n❌ 注册失败: {error}")
                print(f"⚠️  连续失败: {consecutive_fails}/{max_fails}")
                
                # 检查连续失败次数
                if consecutive_fails >= max_fails:
                    print(f"\n⚠️ 连续失败 {max_fails} 次，停止注册")
                    break
            
            # 打印当前统计
            elapsed = time.time() - start_time
            current_total = current_count + success_count
            print_statistics(current_total, target_count, success_count, fail_count, elapsed)
            
            # 间隔等待（如果还需要继续注册）
            if success_count < need_count:
                # 使用配置的间隔，或随机间隔
                if config.REGISTER_INTERVAL > 0:
                    interval = config.REGISTER_INTERVAL
                else:
                    interval = random.randint(5, 15)
                
                print(f"⏳ 等待 {interval} 秒后继续...")
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ 用户中断，停止注册")
            break
        
        except Exception as e:
            print(f"\n❌ 发生异常: {e}")
            fail_count += 1
            consecutive_fails += 1
            
            if consecutive_fails >= max_fails:
                print(f"\n⚠️ 连续失败 {max_fails} 次，停止注册")
                break
            
            # 异常后也等待一下再重试
            if success_count < need_count:
                interval = config.REGISTER_INTERVAL if config.REGISTER_INTERVAL > 0 else 5
                print(f"⏳ 等待 {interval} 秒后重试...")
                time.sleep(interval)
    
    # 7. 最终统计
    total_time = time.time() - start_time
    final_count = count_existing_accounts()
    
    print("\n" + "="*60)
    print("🎉 批量注册完成")
    print("="*60)
    print(f"📊 最终账号总数: {final_count}")
    print(f"✅ 本次成功注册: {success_count}")
    print(f"❌ 本次失败次数: {fail_count}")
    print(f"⏱️  总耗时: {total_time/60:.1f} 分钟")
    
    if success_count > 0:
        avg_time = total_time / success_count
        print(f"⚡ 平均每个账号: {avg_time:.1f} 秒")
        success_rate = (success_count / (success_count + fail_count)) * 100
        print(f"📈 成功率: {success_rate:.1f}%")
    
    print("="*60 + "\n")
    
    return {
        "success": True,
        "current_count": final_count,
        "target_count": target_count,
        "registered": success_count,
        "failed": fail_count,
        "total_time": total_time,
        "results": results
    }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Warp 批量注册工具 - 注册到指定目标数量',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 注册到总共 10 个账号
  python batch_register.py --target 10
  
  # 增加 5 个账号（在当前基础上）
  python batch_register.py --add 5
  
  # 注册到 20 个账号，使用无头模式
  python batch_register.py --target 20 --headless true
  
  # 查看当前账号数量
  python batch_register.py --count
  
  # 列出所有账号
  python batch_register.py --list
        """
    )
    
    parser.add_argument('--target', type=int,
                       help='目标账号总数')
    parser.add_argument('--add', type=int,
                       help='增加指定数量的账号（在当前基础上）')
    parser.add_argument('--headless', type=str, choices=['true', 'false'],
                       help='是否无头模式（默认使用配置文件）')
    parser.add_argument('--max-fails', type=int, default=3,
                       help='最大连续失败次数（默认: 3）')
    parser.add_argument('--count', action='store_true',
                       help='仅显示当前账号数量')
    parser.add_argument('--list', action='store_true',
                       help='列出所有账号信息')
    
    args = parser.parse_args()
    
    # 仅显示账号数量
    if args.count:
        count = count_existing_accounts()
        print(f"📊 当前账号总数: {count}")
        return
    
    # 列出所有账号
    if args.list:
        accounts = get_account_list()
        print(f"\n📋 账号列表 (共 {len(accounts)} 个):")
        print("="*80)
        for i, acc in enumerate(accounts, 1):
            email = acc.get('email', 'unknown')
            uid = acc.get('uid', 'unknown')
            created = acc.get('created_at', 'unknown')
            print(f"{i:3d}. {email:40s} | UID: {uid[:20]:20s} | {created}")
        print("="*80 + "\n")
        return
    
    # 检查必需参数
    if not args.target and not args.add:
        parser.error("必须指定 --target 或 --add 参数（或使用 --count / --list）")
    
    # 不能同时使用 --target 和 --add
    if args.target and args.add:
        parser.error("--target 和 --add 不能同时使用")
    
    # 计算目标数量
    if args.add:
        current_count = count_existing_accounts()
        target_count = current_count + args.add
        print(f"📊 当前账号: {current_count}")
        print(f"➕ 增加数量: {args.add}")
        print(f"🎯 目标总数: {target_count}\n")
    else:
        target_count = args.target
    
    # 验证目标数量
    if target_count < 1:
        print("❌ 目标数量必须大于 0")
        sys.exit(1)
    
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
    
    # 执行批量注册
    try:
        result = batch_register(
            target_count=target_count,
            headless=headless,
            max_fails=args.max_fails
        )
        
        if result['success']:
            sys.exit(0)
        else:
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        sys.exit(130)
    
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
