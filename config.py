#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """配置类"""
    
    # 邮箱服务配置
    EMAIL_SERVICE = os.getenv('EMAIL_SERVICE', 'moemail')  # moemail 或 skymail
    
    # MoeMail 配置
    MOEMAIL_URL = os.getenv('MOEMAIL_URL', 'https://email.959585.xyz')
    MOEMAIL_API_KEY = os.getenv('MOEMAIL_API_KEY', '')
    
    # Skymail (Cloud Mail) 配置
    SKYMAIL_URL = os.getenv('SKYMAIL_URL', 'https://cloudmail.qixc.pp.ua')
    SKYMAIL_TOKEN = os.getenv('SKYMAIL_TOKEN', '')  # 管理员 Token
    SKYMAIL_DOMAIN = os.getenv('SKYMAIL_DOMAIN', 'qixc.pp.ua')  # 邮箱域名（支持多个域名，逗号分隔）
    SKYMAIL_WILDCARD = os.getenv('SKYMAIL_WILDCARD', 'false').lower() == 'true'  # 通配符模式（无需注册）
    
    # Firebase 配置
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY', 'AIzaSyBdy3O3S9hrdayLJxJ7mriBR4qgUaUygAs')
    
    # Warp 登录页面 URL
    WARP_LOGIN_URL = os.getenv('WARP_LOGIN_URL', 'https://app.warp.dev/login')
    
    # 浏览器配置
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    FINGERPRINT_RANDOMIZE = os.getenv('FINGERPRINT_RANDOMIZE', 'true').lower() == 'true'  # 指纹随机化总开关
    CHROME_BINARY_PATH = os.getenv('CHROME_BINARY_PATH', None)  # Chrome 可执行文件路径
    CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH', None)    # ChromeDriver 路径
    
    # 指纹增强配置
    FINGERPRINT_LEVEL = os.getenv('FINGERPRINT_LEVEL', 'balanced')  # basic, balanced, aggressive
    ENHANCED_PROFILES_ENABLED = os.getenv('ENHANCED_PROFILES_ENABLED', 'true').lower() == 'true'
    STRICT_CONSISTENCY_CHECK = os.getenv('STRICT_CONSISTENCY_CHECK', 'true').lower() == 'true'
    FINGERPRINT_DEBUG = os.getenv('FINGERPRINT_DEBUG', 'false').lower() == 'true'
    
    # 超时设置
    EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', '120'))
    
    # 批量注册配置
    REGISTER_COUNT = int(os.getenv('REGISTER_COUNT', '1'))
    REGISTER_INTERVAL = int(os.getenv('REGISTER_INTERVAL', '5'))
    
    def validate(self):
        """验证配置"""
        # 验证邮箱服务配置
        if self.EMAIL_SERVICE == 'moemail':
            if not self.MOEMAIL_API_KEY:
                raise ValueError("MOEMAIL_API_KEY not configured")
        elif self.EMAIL_SERVICE == 'skymail':
            if not self.SKYMAIL_TOKEN:
                raise ValueError("SKYMAIL_TOKEN must be configured")
        elif self.EMAIL_SERVICE == 'auto':
            # auto 模式：至少需要配置一个服务
            has_moemail = bool(self.MOEMAIL_API_KEY)
            has_skymail = bool(self.SKYMAIL_TOKEN)
            if not has_moemail and not has_skymail:
                raise ValueError("AUTO mode requires at least one email service configured (MOEMAIL_API_KEY or SKYMAIL_TOKEN)")
        else:
            raise ValueError(f"Invalid EMAIL_SERVICE: {self.EMAIL_SERVICE}. Must be 'moemail', 'skymail', or 'auto'")
        
        if not self.FIREBASE_API_KEY:
            raise ValueError("FIREBASE_API_KEY not configured")
        
        # 验证指纹级别
        if self.FINGERPRINT_LEVEL not in ['basic', 'balanced', 'aggressive']:
            raise ValueError(f"Invalid FINGERPRINT_LEVEL: {self.FINGERPRINT_LEVEL}. Must be 'basic', 'balanced', or 'aggressive'")
        
        return True


# 全局配置实例
config = Config()
