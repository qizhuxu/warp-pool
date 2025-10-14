#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Warp 机器码重置工具
用于重置 Warp 的设备标识符，删除注册表配置和本地数据
"""
import os
import sys
import shutil
import platform
from datetime import datetime


def log(message: str):
    """打印带时间戳的日志"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def reset_windows():
    """Windows 系统重置"""
    import winreg
    
    log("开始软件初始化...")
    
    # 1. 删除注册表项
    log("正在删除注册表项...")
    
    registry_paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Warp.dev\Warp"),
        (winreg.HKEY_CURRENT_USER, r"Software\Warp.dev"),
    ]
    
    for hkey, path in registry_paths:
        try:
            winreg.DeleteKey(hkey, path)
            log(f"已删除: 注册表项{path.replace('Software\\', '')}")
        except FileNotFoundError:
            # 注册表项不存在，跳过
            pass
        except Exception as e:
            log(f"⚠️ 删除注册表项失败 {path}: {e}")
    
    # 2. 删除本地数据目录
    local_appdata = os.environ.get('LOCALAPPDATA')
    if local_appdata:
        warp_data_dir = os.path.join(local_appdata, 'warp')
        
        if os.path.exists(warp_data_dir):
            log(f"正在删除数据目录: {warp_data_dir}")
            try:
                shutil.rmtree(warp_data_dir)
                log("数据目录已删除")
            except Exception as e:
                log(f"⚠️ 删除数据目录失败: {e}")
        else:
            log("数据目录不存在，跳过")
    
    # 3. 生成新的 ExperimentId（可选）
    try:
        import uuid
        new_experiment_id = str(uuid.uuid4())
        
        # 尝试创建新的注册表项
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Warp.dev\Warp")
            winreg.SetValueEx(key, "ExperimentId", 0, winreg.REG_SZ, new_experiment_id)
            winreg.CloseKey(key)
            log(f"已生成新的 ExperimentId: {new_experiment_id[:8]}...")
        except Exception as e:
            log(f"⚠️ 设置 ExperimentId 失败: {e}")
    except Exception as e:
        log(f"⚠️ 生成 ExperimentId 失败: {e}")
    
    log("软件初始化成功完成")


def reset_linux():
    """Linux 系统重置"""
    log("开始软件初始化...")
    
    # 1. 删除配置目录
    config_dirs = [
        os.path.expanduser("~/.config/warp"),
        os.path.expanduser("~/.local/share/warp"),
        os.path.expanduser("~/.cache/warp"),
    ]
    
    for config_dir in config_dirs:
        if os.path.exists(config_dir):
            log(f"正在删除配置目录: {config_dir}")
            try:
                shutil.rmtree(config_dir)
                log("配置目录已删除")
            except Exception as e:
                log(f"⚠️ 删除配置目录失败: {e}")
        else:
            log(f"配置目录不存在: {config_dir}")
    
    log("软件初始化成功完成")


def reset_macos():
    """macOS 系统重置"""
    log("开始软件初始化...")
    
    # 1. 删除配置目录
    config_dirs = [
        os.path.expanduser("~/Library/Application Support/warp"),
        os.path.expanduser("~/Library/Preferences/dev.warp.Warp-Stable.plist"),
        os.path.expanduser("~/Library/Caches/warp"),
    ]
    
    for config_path in config_dirs:
        if os.path.exists(config_path):
            log(f"正在删除: {config_path}")
            try:
                if os.path.isdir(config_path):
                    shutil.rmtree(config_path)
                else:
                    os.remove(config_path)
                log("已删除")
            except Exception as e:
                log(f"⚠️ 删除失败: {e}")
        else:
            log(f"不存在: {config_path}")
    
    log("软件初始化成功完成")


def main(silent=False):
    """
    主函数
    
    Args:
        silent: 静默模式，不需要用户确认
    """
    if not silent:
        print("\n" + "="*60)
        print("🔄 Warp 机器码重置工具")
        print("="*60 + "\n")
    
    system = platform.system()
    
    if system == "Windows":
        if not silent:
            log("检测到 Windows 系统")
            
            # 检查管理员权限
            try:
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
                if not is_admin:
                    log("⚠️ 警告: 建议以管理员权限运行以确保完全清理")
            except:
                pass
            
            # 确认操作
            print("\n⚠️  此操作将:")
            print("  1. 删除 Warp 注册表配置")
            print("  2. 删除本地数据目录")
            print("  3. 生成新的设备标识符")
            print()
            
            confirm = input("确认继续? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                log("操作已取消")
                return
            
            print()
        
        reset_windows()
    
    elif system == "Linux":
        if not silent:
            log("检测到 Linux 系统")
            
            print("\n⚠️  此操作将删除 Warp 配置和缓存目录")
            print()
            
            confirm = input("确认继续? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                log("操作已取消")
                return
            
            print()
        
        reset_linux()
    
    elif system == "Darwin":
        if not silent:
            log("检测到 macOS 系统")
            
            print("\n⚠️  此操作将删除 Warp 配置和缓存")
            print()
            
            confirm = input("确认继续? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                log("操作已取消")
                return
            
            print()
        
        reset_macos()
    
    else:
        log(f"❌ 不支持的操作系统: {system}")
        sys.exit(1)
    
    if not silent:
        print("\n" + "="*60)
        print("✅ 重置完成！")
        print("="*60)
        print("\n提示: 下次启动 Warp 时将被识别为新设备\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Warp 机器码重置工具')
    parser.add_argument('--silent', action='store_true',
                       help='静默模式，不需要用户确认')
    args = parser.parse_args()
    
    try:
        main(silent=args.silent)
    except KeyboardInterrupt:
        print("\n\n⚠️ 操作已取消")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
