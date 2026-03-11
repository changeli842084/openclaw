#!/usr/bin/env python3
"""
天气查询工具 (Weather Query Tool)

一个简单的命令行天气查询工具，支持输入城市名称返回模拟天气数据。
包含温度、天气状况和出行建议。

使用方法:
    python weather_tool.py <城市名称>
    
示例:
    python weather_tool.py 上海
    # 输出：上海：晴天，25°C，适合出行

作者: Coder Agent
版本: 1.0.0
"""

import sys
import random
from typing import Dict, Tuple


# 天气类型配置
WEATHER_TYPES: Dict[str, Dict[str, str]] = {
    "晴天": {"icon": "☀️", "suggestion": "适合出行，注意防晒"},
    "多云": {"icon": "⛅", "suggestion": "天气舒适，适合户外活动"},
    "阴天": {"icon": "☁️", "suggestion": "适合室内活动或短途出行"},
    "小雨": {"icon": "🌧️", "suggestion": "记得带伞，适合室内活动"},
    "大雨": {"icon": "⛈️", "suggestion": "建议减少外出，注意防雨"},
    "雷阵雨": {"icon": "🌩️", "suggestion": "避免户外活动，注意安全"},
    "雪天": {"icon": "❄️", "suggestion": "注意保暖，路滑小心行走"},
    "雾霾": {"icon": "🌫️", "suggestion": "建议佩戴口罩，减少户外运动"},
}

# 城市温度范围配置 (最低温度, 最高温度)
CITY_TEMP_RANGES: Dict[str, Tuple[int, int]] = {
    "北京": (-5, 35),
    "上海": (0, 35),
    "广州": (10, 38),
    "深圳": (12, 36),
    "杭州": (0, 36),
    "成都": (2, 33),
    "重庆": (5, 40),
    "武汉": (0, 38),
    "西安": (-3, 38),
    "南京": (0, 37),
    "天津": (-5, 35),
    "苏州": (0, 36),
    "青岛": (-2, 32),
    "厦门": (8, 35),
    "昆明": (5, 28),
    "哈尔滨": (-25, 30),
    "长春": (-20, 30),
    "沈阳": (-18, 32),
    "大连": (-5, 30),
    "济南": (-3, 37),
}


def get_random_weather() -> str:
    """
    随机获取一种天气类型。
    
    Returns:
        str: 天气类型名称
    """
    return random.choice(list(WEATHER_TYPES.keys()))


def generate_temperature(city: str) -> int:
    """
    根据城市生成随机温度。
    
    如果城市在配置中，使用该城市的温度范围；
    否则使用默认温度范围 (0, 35)。
    
    Args:
        city: 城市名称
        
    Returns:
        int: 生成的温度值
    """
    temp_range = CITY_TEMP_RANGES.get(city, (0, 35))
    return random.randint(temp_range[0], temp_range[1])


def generate_weather_data(city: str) -> Dict[str, str]:
    """
    生成指定城市的天气数据。
    
    Args:
        city: 城市名称
        
    Returns:
        Dict[str, str]: 包含城市、天气、温度和建议的字典
        
    Raises:
        ValueError: 如果城市名称为空
    """
    if not city or not city.strip():
        raise ValueError("城市名称不能为空")
    
    city = city.strip()
    weather = get_random_weather()
    temperature = generate_temperature(city)
    suggestion = WEATHER_TYPES[weather]["suggestion"]
    
    return {
        "city": city,
        "weather": weather,
        "temperature": temperature,
        "suggestion": suggestion,
        "icon": WEATHER_TYPES[weather]["icon"],
    }


def format_output(weather_data: Dict[str, str]) -> str:
    """
    格式化天气数据输出。
    
    Args:
        weather_data: 天气数据字典
        
    Returns:
        str: 格式化后的输出字符串
    """
    return f"{weather_data['city']}：{weather_data['weather']}{weather_data['icon']}，{weather_data['temperature']}°C，{weather_data['suggestion']}"


def display_help():
    """显示帮助信息。"""
    help_text = """
天气查询工具 - 使用帮助

用法:
    python weather_tool.py <城市名称>

参数:
    城市名称    要查询天气的城市（支持中文城市名）

示例:
    python weather_tool.py 上海
    python weather_tool.py 北京
    python weather_tool.py 广州

支持的城市（部分）:
    北京、上海、广州、深圳、杭州、成都、重庆
    武汉、西安、南京、天津、苏州、青岛、厦门
    昆明、哈尔滨、长春、沈阳、大连、济南
    
注意: 其他城市将使用默认温度范围生成模拟数据。
"""
    print(help_text)


def main():
    """
    主函数，处理命令行参数并执行天气查询。
    
    支持以下用法:
    - python weather_tool.py <城市名称>: 查询指定城市天气
    - python weather_tool.py --help 或 -h: 显示帮助信息
    """
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("错误: 请提供城市名称")
        print("\n用法: python weather_tool.py <城市名称>")
        print("      python weather_tool.py --help  显示帮助信息")
        sys.exit(1)
    
    # 获取城市名称
    city_arg = sys.argv[1]
    
    # 处理帮助选项
    if city_arg in ("--help", "-h", "help"):
        display_help()
        sys.exit(0)
    
    try:
        # 生成并输出天气数据
        weather_data = generate_weather_data(city_arg)
        output = format_output(weather_data)
        print(output)
        
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生未知错误: {e}")
        sys.exit(1)


# 示例代码
if __name__ == "__main__":
    # 示例1: 命令行查询
    # python weather_tool.py 上海
    # 输出示例: 上海：晴天☀️，25°C，适合出行，注意防晒
    
    # 示例2: 程序内调用
    # from weather_tool import generate_weather_data, format_output
    # data = generate_weather_data("北京")
    # print(format_output(data))
    
    main()
