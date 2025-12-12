#!/usr/bin/env python3
"""
添加WiFi设备数据到数据库
"""

import os
import sys

# 添加Django项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wifirating.settings')

import django
# 初始化Django
django.setup()

from api.models import WifiModel

def add_wifi_devices():
    """添加WiFi设备数据"""
    wifi_devices = [
        {
            'name': '华为路由器AX3 Pro',
            'brand': '华为',
            'model': 'AX3 Pro',
            'signalStrength': 9.5,
            'speed': 3000.0,
            'price': 299.0,
            'description': '华为WiFi 6路由器，支持3000Mbps高速率，配备凌霄双核处理器，覆盖范围广，穿墙性能强，支持Mesh组网。',
            'rating': 4.8,
            'reviewCount': 1256
        },
        {
            'name': '小米路由器AX6000',
            'brand': '小米',
            'model': 'AX6000',
            'signalStrength': 9.2,
            'speed': 6000.0,
            'price': 599.0,
            'description': '小米WiFi 6增强版路由器，搭载高通6核处理器，支持6000Mbps超高速率，160MHz频宽，支持Mesh组网，APP智能管理。',
            'rating': 4.7,
            'reviewCount': 987
        },
        {
            'name': 'TP-Link Archer C5400X',
            'brand': 'TP-Link',
            'model': 'Archer C5400X',
            'signalStrength': 9.0,
            'speed': 5400.0,
            'price': 1299.0,
            'description': 'TP-Link旗舰级路由器，支持三频并发，配备高通4核处理器，内置游戏加速引擎，适合游戏玩家使用。',
            'rating': 4.6,
            'reviewCount': 543
        },
        {
            'name': '华硕RT-AX86U',
            'brand': '华硕',
            'model': 'RT-AX86U',
            'signalStrength': 9.3,
            'speed': 5700.0,
            'price': 899.0,
            'description': '华硕WiFi 6电竞路由器，支持5700Mbps速率，配备双2.5G网口，内置AiProtection安全系统，游戏加速功能强大。',
            'rating': 4.9,
            'reviewCount': 789
        },
        {
            'name': '荣耀路由器3',
            'brand': '荣耀',
            'model': '路由器3',
            'signalStrength': 8.8,
            'speed': 2976.0,
            'price': 199.0,
            'description': '荣耀WiFi 6路由器，支持2976Mbps速率，搭载凌霄双核心处理器，覆盖范围广，支持NFC一碰联网。',
            'rating': 4.5,
            'reviewCount': 1034
        },
        {
            'name': '水星MAC1200R',
            'brand': '水星',
            'model': 'MAC1200R',
            'signalStrength': 8.0,
            'speed': 1200.0,
            'price': 89.0,
            'description': '水星双频千兆路由器，支持2.4G/5G双频并发，覆盖范围适中，适合小户型使用，性价比高。',
            'rating': 4.2,
            'reviewCount': 2345
        },
        {
            'name': 'Netgear RAX80',
            'brand': 'Netgear',
            'model': 'RAX80',
            'signalStrength': 9.4,
            'speed': 6000.0,
            'price': 1599.0,
            'description': 'Netgear WiFi 6路由器，支持6000Mbps速率，配备1.8GHz四核处理器，8个千兆LAN口，适合大型家庭使用。',
            'rating': 4.7,
            'reviewCount': 456
        },
        {
            'name': '腾达AC10',
            'brand': '腾达',
            'model': 'AC10',
            'signalStrength': 8.5,
            'speed': 1200.0,
            'price': 129.0,
            'description': '腾达双频千兆路由器，支持MU-MIMO技术，配备5dBi高增益天线，覆盖范围广，支持APP远程管理。',
            'rating': 4.3,
            'reviewCount': 1567
        }
    ]
    
    for device in wifi_devices:
        try:
            wifi = WifiModel.objects.create(**device)
            print(f"成功添加: {wifi.brand} {wifi.model}")
        except Exception as e:
            print(f"添加失败 {device['brand']} {device['model']}: {e}")

def main():
    print("开始添加WiFi设备数据...")
    add_wifi_devices()
    print("WiFi设备数据添加完成！")
    
    # 显示已添加的设备数量
    count = WifiModel.objects.count()
    print(f"\n数据库中共有 {count} 台WiFi设备")

if __name__ == "__main__":
    main()
