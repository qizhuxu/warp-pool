#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例配置（不要把真实密钥提交到仓库）
复制此文件为 `config.py` 并填写你的私有值，或使用环境变量。
"""
import os

class Config:
    # 邮箱服务配置
    MOEMAIL_URL = os.getenv('MOEMAIL_URL', 'https://email.example.com')
    MOEMAIL_API_KEY = os.getenv('MOEMAIL_API_KEY', '')  # 在 .env 或 CI 中设置

    # Firebase 配置
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY', '')

    # Warp 登录页面 URL
    WARP_LOGIN_URL = os.getenv('WARP_LOGIN_URL', 'https://app.warp.dev/login')

    # 浏览器配置
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    FINGERPRINT_RANDOMIZE = os.getenv('FINGERPRINT_RANDOMIZE', 'true').lower() == 'true'
    CHROME_BINARY_PATH = os.getenv('CHROME_BINARY_PATH', None)
    CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH', None)

    # 指纹增强配置
    FINGERPRINT_LEVEL = os.getenv('FINGERPRINT_LEVEL', 'balanced')
    ENHANCED_PROFILES_ENABLED = os.getenv('ENHANCED_PROFILES_ENABLED', 'true').lower() == 'true'
    STRICT_CONSISTENCY_CHECK = os.getenv('STRICT_CONSISTENCY_CHECK', 'true').lower() == 'true'
    FINGERPRINT_DEBUG = os.getenv('FINGERPRINT_DEBUG', 'false').lower() == 'true'

    # 超时设置
    EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', '120'))

    # 批量注册配置
    REGISTER_COUNT = int(os.getenv('REGISTER_COUNT', '1'))
    REGISTER_INTERVAL = int(os.getenv('REGISTER_INTERVAL', '5'))

    def validate(self):
        # 不在示例中强制校验密钥，实际运行时应在 `config.py` 或环境变量中提供
        return True


# 全局配置实例（可选）
config = Config()
