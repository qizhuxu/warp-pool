#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器指纹随机化模块 - 增强版
支持多级别指纹模拟：basic, balanced, aggressive
"""
import random
import json
import secrets
from datetime import datetime
from typing import Dict, Any, Optional


class FingerprintRandomizer:
    """浏览器指纹随机化器 - 增强版"""
    
    # 增强的浏览器配置文件（从 warp_register.py 提取的真实配置）
    BASE_PROFILES_ENHANCED = [
        {
            "name": "Win10_Chrome_NVIDIA_GTX1660Ti",
            "os": "Windows",
            "os_version": "10.0.0",
            "platform": "Win32",
            "architecture": "x86",
            "bitness": 64,
            "vendor": "Google Inc.",
            "gpu_vendor": "Google Inc. (NVIDIA)",
            "gpu_renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti (0x00002182) Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "resolution": (1707, 960),
            "hardware": {
                "memory": 8,
                "cores": 12
            },
            "hashes": {
                "prototype_hash": "5051906984991708",
                "math_hash": "4407615957639726",
                "offline_audio_hash": "733027540168168"
            }
        },
        {
            "name": "Win10_Chrome_AMD_Radeon",
            "os": "Windows",
            "os_version": "10.0.0",
            "platform": "Win32",
            "architecture": "x86",
            "bitness": 64,
            "vendor": "Google Inc.",
            "gpu_vendor": "Google Inc. (AMD)",
            "gpu_renderer": "ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "resolution": (1536, 864),
            "hardware": {
                "memory": 8,
                "cores": 16
            },
            "hashes": {
                "prototype_hash": "4842229194603551",
                "math_hash": "4407615957639726",
                "offline_audio_hash": "733027540168168"
            }
        },
        {
            "name": "Win10_Chrome_NVIDIA_RTX3060",
            "os": "Windows",
            "os_version": "10.0.0",
            "platform": "Win32",
            "architecture": "x86",
            "bitness": 64,
            "vendor": "Google Inc.",
            "gpu_vendor": "Google Inc. (NVIDIA)",
            "gpu_renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 (0x00002503) Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "resolution": (1920, 1080),
            "hardware": {
                "memory": 16,
                "cores": 8
            },
            "hashes": {
                "prototype_hash": "5051906984991708",
                "math_hash": "4407615957639726",
                "offline_audio_hash": "733027540168168"
            }
        }
    ]
    
    # Chrome 版本配置（从 warp_register.py 提取）
    BROWSER_VERSIONS = [
        {
            "major": 140,
            "full_version": "140.0.7339.208",
            "brands": [
                {"brand": "Chromium", "version": "140"},
                {"brand": "Not=A?Brand", "version": "24"},
                {"brand": "Google Chrome", "version": "140"}
            ]
        },
        {
            "major": 128,
            "full_version": "128.0.6613.137",
            "brands": [
                {"brand": "Chromium", "version": "128"},
                {"brand": "Not-A.Brand", "version": "24"},
                {"brand": "Google Chrome", "version": "128"}
            ]
        },
        {
            "major": 126,
            "full_version": "126.0.6478.126",
            "brands": [
                {"brand": "Chromium", "version": "126"},
                {"brand": "Not-A.Brand", "version": "24"},
                {"brand": "Google Chrome", "version": "126"}
            ]
        }
    ]
    
    # 常见的屏幕分辨率
    RESOLUTIONS = [
        (1920, 1080),  # Full HD
        (1366, 768),   # 最常见的笔记本分辨率
        (1536, 864),   # 常见笔记本
        (1440, 900),   # MacBook
        (1280, 720),   # HD
        (1600, 900),   # HD+
        (2560, 1440),  # 2K
    ]
    
    # 真实的 User-Agent 列表（Windows）
    USER_AGENTS_WINDOWS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    # 真实的 User-Agent 列表（Mac）
    USER_AGENTS_MAC = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    # 真实的 User-Agent 列表（Linux）
    USER_AGENTS_LINUX = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    # 语言列表
    LANGUAGES = [
        'en-US,en;q=0.9',
        'en-GB,en;q=0.9',
        'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'zh-CN,zh;q=0.9,en;q=0.8',
    ]
    
    # 时区列表
    TIMEZONES = [
        'America/New_York',    # UTC-5
        'America/Los_Angeles', # UTC-8
        'Europe/London',       # UTC+0
        'Europe/Paris',        # UTC+1
        'Asia/Shanghai',       # UTC+8
        'Asia/Tokyo',          # UTC+9
    ]
    
    def __init__(self, platform='windows', level='balanced', enhanced_profiles=True):
        """
        初始化指纹随机化器
        
        Args:
            platform: 操作系统平台 ('windows', 'mac', 'linux')
            level: 指纹级别 ('basic', 'balanced', 'aggressive')
            enhanced_profiles: 是否使用增强的配置文件
        """
        self.platform = platform.lower()
        self.level = level.lower()
        self.enhanced_profiles = enhanced_profiles
        self.profile = None
        self.fingerprint = self._generate_fingerprint()
    
    def _generate_fingerprint(self):
        """生成随机指纹（基于 warp_register.py 的逻辑）"""
        # 如果启用增强配置文件，从预定义配置中选择
        if self.enhanced_profiles and self.level in ['balanced', 'aggressive']:
            # 根据平台过滤配置文件
            if self.platform == 'mac':
                profiles = [p for p in self.BASE_PROFILES_ENHANCED if p['platform'] == 'MacIntel']
            else:
                profiles = [p for p in self.BASE_PROFILES_ENHANCED if p['platform'] == 'Win32']
            
            if profiles:
                self.profile = random.choice(profiles)
                browser_version = random.choice(self.BROWSER_VERSIONS)
                
                # 构建 User-Agent（与 warp_register.py 一致）
                ua_full_version = browser_version["full_version"]
                user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ua_full_version} Safari/537.36"
                
                width, height = self.profile['resolution']
                
                return {
                    'user_agent': user_agent,
                    'width': width,
                    'height': height,
                    'language': random.choice(self.LANGUAGES),
                    'timezone': random.choice(self.TIMEZONES),
                    'hardware_concurrency': self.profile['hardware']['cores'],
                    'device_memory': self.profile['hardware']['memory'],
                    'gpu_vendor': self.profile['gpu_vendor'],
                    'gpu_renderer': self.profile['gpu_renderer'],
                    'platform': self.profile['platform'],
                    'browser_version': browser_version,
                    'hashes': self.profile.get('hashes', {})
                }
        
        # 基础模式：随机生成
        if self.platform == 'mac':
            user_agent = random.choice(self.USER_AGENTS_MAC)
        elif self.platform == 'linux':
            user_agent = random.choice(self.USER_AGENTS_LINUX)
        else:
            user_agent = random.choice(self.USER_AGENTS_WINDOWS)
        
        width, height = random.choice(self.RESOLUTIONS)
        
        return {
            'user_agent': user_agent,
            'width': width,
            'height': height,
            'language': random.choice(self.LANGUAGES),
            'timezone': random.choice(self.TIMEZONES),
            'hardware_concurrency': random.choice([2, 4, 6, 8, 12, 16]),
            'device_memory': random.choice([4, 8, 16, 32]),
        }
    
    def get_chrome_options_args(self):
        """获取 Chrome 启动参数"""
        args = [
            f'--window-size={self.fingerprint["width"]},{self.fingerprint["height"]}',
            f'--user-agent={self.fingerprint["user_agent"]}',
            f'--lang={self.fingerprint["language"].split(",")[0]}',
        ]
        return args
    
    def get_canvas_noise_script(self):
        """获取 Canvas 指纹混淆脚本"""
        return """
        // Canvas 指纹混淆
        (function() {
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            const originalToBlob = HTMLCanvasElement.prototype.toBlob;
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            
            // 添加随机噪声
            function addNoise(canvas, context) {
                const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < imageData.data.length; i += 4) {
                    // 随机修改 RGB 值（微小变化，人眼不可见）
                    const noise = Math.floor(Math.random() * 3) - 1;
                    imageData.data[i] = Math.max(0, Math.min(255, imageData.data[i] + noise));
                    imageData.data[i + 1] = Math.max(0, Math.min(255, imageData.data[i + 1] + noise));
                    imageData.data[i + 2] = Math.max(0, Math.min(255, imageData.data[i + 2] + noise));
                }
                context.putImageData(imageData, 0, 0);
            }
            
            // 重写 toDataURL
            HTMLCanvasElement.prototype.toDataURL = function() {
                const context = this.getContext('2d');
                if (context) {
                    addNoise(this, context);
                }
                return originalToDataURL.apply(this, arguments);
            };
            
            // 重写 toBlob
            HTMLCanvasElement.prototype.toBlob = function() {
                const context = this.getContext('2d');
                if (context) {
                    addNoise(this, context);
                }
                return originalToBlob.apply(this, arguments);
            };
        })();
        """
    
    def get_webgl_noise_script(self):
        """获取 WebGL 指纹混淆脚本（增强版）"""
        # 如果有配置文件，使用配置的 GPU 信息
        if self.profile:
            gpu_vendor = self.profile['gpu_vendor']
            gpu_renderer = self.profile['gpu_renderer']
        else:
            gpu_vendor = 'Google Inc. (Intel)'
            gpu_renderer = 'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)'
        
        return f"""
        // WebGL 指纹混淆（增强版）
        (function() {{
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
            
            const spoofWebGL = function(parameter) {{
                if (parameter === 37445) {{  // UNMASKED_VENDOR_WEBGL
                    return '{gpu_vendor}';
                }}
                if (parameter === 37446) {{  // UNMASKED_RENDERER_WEBGL
                    return '{gpu_renderer}';
                }}
                return getParameter.apply(this, arguments);
            }};
            
            WebGLRenderingContext.prototype.getParameter = spoofWebGL;
            WebGL2RenderingContext.prototype.getParameter = spoofWebGL;
        }})();
        """
    
    def get_navigator_override_script(self):
        """获取 Navigator 对象覆盖脚本"""
        fp = self.fingerprint
        return f"""
        // 覆盖 Navigator 属性
        Object.defineProperty(navigator, 'hardwareConcurrency', {{
            get: () => {fp['hardware_concurrency']}
        }});
        
        Object.defineProperty(navigator, 'deviceMemory', {{
            get: () => {fp['device_memory']}
        }});
        
        Object.defineProperty(navigator, 'language', {{
            get: () => '{fp['language'].split(',')[0]}'
        }});
        
        Object.defineProperty(navigator, 'languages', {{
            get: () => {json.dumps(fp['language'].split(','))}
        }});
        """
    
    def get_timezone_override_script(self):
        """获取时区覆盖脚本"""
        return f"""
        // 覆盖时区
        Date.prototype.getTimezoneOffset = function() {{
            return {random.randint(-720, 720)};
        }};
        """
    
    def get_performance_timing_script(self):
        """获取 Performance Timing 注入脚本（与 warp_register.py 一致）"""
        # 完全按照 warp_register.py 的逻辑生成时间线
        now = int(datetime.now().timestamp() * 1000)
        navigation_start = now - random.randint(3000, 6000)
        fetch_start = navigation_start + random.randint(2, 10)
        domain_lookup_start = fetch_start + random.randint(1, 20)
        domain_lookup_end = domain_lookup_start + random.randint(10, 50)
        connect_start = domain_lookup_end
        secure_connection_start = connect_start + random.randint(5, 15) if random.random() > 0.3 else 0
        connect_end = (secure_connection_start if secure_connection_start else connect_start) + random.randint(20, 60)
        request_start = connect_end + random.randint(1, 5)
        response_start = request_start + random.randint(80, 200)
        response_end = response_start + random.randint(1, 10)
        dom_loading = response_end + random.randint(1, 10)
        unload_event_start = dom_loading + random.randint(1, 5)
        unload_event_end = unload_event_start + random.randint(1, 3)
        dom_interactive = dom_loading + random.randint(200, 500)
        dom_content_loaded_event_start = dom_interactive + random.randint(100, 300)
        dom_content_loaded_event_end = dom_content_loaded_event_start + random.randint(1, 5)
        
        # 50% 概率页面已完全加载
        if random.random() > 0.5:
            dom_complete = dom_content_loaded_event_end + random.randint(50, 200)
            load_event_start = dom_complete + random.randint(1, 5)
            load_event_end = load_event_start + random.randint(1, 5)
        else:
            dom_complete = 0
            load_event_start = 0
            load_event_end = 0
        
        return f"""
        // Performance Timing 注入（完整版）
        (function() {{
            const timing = {{
                navigationStart: {navigation_start},
                redirectStart: 0,
                redirectEnd: 0,
                fetchStart: {fetch_start},
                domainLookupStart: {domain_lookup_start},
                domainLookupEnd: {domain_lookup_end},
                connectStart: {connect_start},
                secureConnectionStart: {secure_connection_start},
                connectEnd: {connect_end},
                requestStart: {request_start},
                responseStart: {response_start},
                responseEnd: {response_end},
                unloadEventStart: {unload_event_start},
                unloadEventEnd: {unload_event_end},
                domLoading: {dom_loading},
                domInteractive: {dom_interactive},
                domContentLoadedEventStart: {dom_content_loaded_event_start},
                domContentLoadedEventEnd: {dom_content_loaded_event_end},
                domComplete: {dom_complete},
                loadEventStart: {load_event_start},
                loadEventEnd: {load_event_end}
            }};
            
            Object.keys(timing).forEach(key => {{
                Object.defineProperty(window.performance.timing, key, {{
                    get: () => timing[key],
                    configurable: true
                }});
            }});
        }})();
        """
    
    def get_audio_context_script(self):
        """获取 Audio Context 指纹混淆脚本"""
        return """
        // Audio Context 指纹混淆
        (function() {
            const originalGetChannelData = AudioBuffer.prototype.getChannelData;
            AudioBuffer.prototype.getChannelData = function(channel) {
                const data = originalGetChannelData.call(this, channel);
                // 添加微小噪声
                for (let i = 0; i < data.length; i++) {
                    data[i] += (Math.random() - 0.5) * 0.0001;
                }
                return data;
            };
        })();
        """
    
    def get_all_scripts(self):
        """获取所有混淆脚本（根据级别）"""
        scripts = []
        
        # basic 级别：基础功能
        if self.level in ['basic', 'balanced', 'aggressive']:
            scripts.append(self.get_canvas_noise_script())
            scripts.append(self.get_navigator_override_script())
            scripts.append(self.get_timezone_override_script())
        
        # balanced 级别：增加 WebGL 和 Performance Timing
        if self.level in ['balanced', 'aggressive']:
            scripts.append(self.get_webgl_noise_script())
            scripts.append(self.get_performance_timing_script())
        
        # aggressive 级别：增加 Audio Context
        if self.level == 'aggressive':
            scripts.append(self.get_audio_context_script())
        
        return "\n".join(scripts)
    
    def print_fingerprint(self):
        """打印当前指纹信息"""
        print("  🎭 浏览器指纹:")
        print(f"     级别: {self.level}")
        if self.profile:
            print(f"     配置: {self.profile['name']}")
        print(f"     分辨率: {self.fingerprint['width']}x{self.fingerprint['height']}")
        print(f"     User-Agent: {self.fingerprint['user_agent'][:80]}...")
        print(f"     语言: {self.fingerprint['language']}")
        print(f"     时区: {self.fingerprint['timezone']}")
        print(f"     CPU 核心: {self.fingerprint['hardware_concurrency']}")
        print(f"     内存: {self.fingerprint['device_memory']}GB")
        if self.fingerprint.get('gpu_vendor'):
            print(f"     GPU 厂商: {self.fingerprint['gpu_vendor']}")
            print(f"     GPU 渲染器: {self.fingerprint['gpu_renderer'][:60]}...")
    
    def validate_consistency(self) -> bool:
        """验证配置一致性"""
        if not self.profile:
            return True
        
        # 检查 Windows 系统不应该有 Apple GPU
        if 'Windows' in self.fingerprint['user_agent']:
            if 'Apple' in self.fingerprint.get('gpu_vendor', ''):
                print("  ⚠️ 配置不一致：Windows + Apple GPU")
                return False
        
        # 检查 Mac 系统不应该有 NVIDIA/AMD GPU
        if 'Macintosh' in self.fingerprint['user_agent']:
            gpu_vendor = self.fingerprint.get('gpu_vendor', '')
            if 'NVIDIA' in gpu_vendor or 'AMD' in gpu_vendor:
                print("  ⚠️ 配置不一致：Mac + NVIDIA/AMD GPU")
                return False
        
        # 检查分辨率
        width = self.fingerprint['width']
        height = self.fingerprint['height']
        if width < 800 or height < 600:
            print("  ⚠️ 分辨率过小")
            return False
        
        # 检查硬件参数
        if self.fingerprint['hardware_concurrency'] > 32:
            print("  ⚠️ CPU 核心数过多")
            return False
        
        if self.fingerprint['device_memory'] > 64:
            print("  ⚠️ 内存大小过大")
            return False
        
        return True
