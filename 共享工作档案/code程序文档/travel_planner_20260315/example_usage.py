#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行程规划工具 - 示例运行脚本
演示如何使用行程规划工具
"""

import subprocess
import sys
import os

def run_example():
    """运行示例"""
    print("=== 行程规划工具示例 ===\n")
    
    # 示例1：成都3日游
    print("示例1：成都3日游规划")
    print("命令：python3 travel_planner.py 成都 3 2 6000 -o chengdu_trip.md")
    
    try:
        result = subprocess.run([
            'python3', 'travel_planner.py', '成都', '3', '2', '6000', 
            '-o', 'chengdu_trip.md'
        ], capture_output=True, text=True, check=True)
        
        print("执行成功！")
        print(result.stdout)
        
        # 显示生成的文件内容
        if os.path.exists('chengdu_trip.md'):
            print("\n生成的行程规划内容预览：")
            with open('chengdu_trip.md', 'r', encoding='utf-8') as f:
                content = f.read()
                print(content[:1000] + "...") if len(content) > 1000 else print(content)
            
            # 清理示例文件
            os.remove('chengdu_trip.md')
            print("\n示例文件已清理")
    
    except subprocess.CalledProcessError as e:
        print(f"执行出错: {e}")
        print(f"错误输出: {e.stderr}")
    
    print("\n" + "="*50 + "\n")
    
    # 示例2：北京5日游
    print("示例2：北京5日游规划")
    print("命令：python3 travel_planner.py 北京 5 4 12000 -o beijing_trip.md")
    
    try:
        result = subprocess.run([
            'python3', 'travel_planner.py', '北京', '5', '4', '12000', 
            '-o', 'beijing_trip.md'
        ], capture_output=True, text=True, check=True)
        
        print("执行成功！")
        print(result.stdout)
        
        # 显示生成的文件内容
        if os.path.exists('beijing_trip.md'):
            print("\n生成的行程规划内容预览：")
            with open('beijing_trip.md', 'r', encoding='utf-8') as f:
                content = f.read()
                print(content[:1000] + "...") if len(content) > 1000 else print(content)
            
            # 清理示例文件
            os.remove('beijing_trip.md')
            print("\n示例文件已清理")
    
    except subprocess.CalledProcessError as e:
        print(f"执行出错: {e}")
        print(f"错误输出: {e.stderr}")

if __name__ == "__main__":
    run_example()