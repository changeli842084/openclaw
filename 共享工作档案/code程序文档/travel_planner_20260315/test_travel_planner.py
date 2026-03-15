#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行程规划工具 - 测试脚本
用于验证主要功能是否正常工作
"""

import os
import sys
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, '.')

from travel_planner import TravelPlanner


def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试行程规划工具基本功能 ===")
    
    # 创建一个行程规划器实例
    planner = TravelPlanner("成都", 3, 2, 6000)
    
    print(f"目的地: {planner.destination}")
    print(f"天数: {planner.days}")
    print(f"人数: {planner.people}")
    print(f"总预算: ¥{planner.budget}")
    print(f"人均预算: ¥{planner.per_person_budget}")
    
    # 测试日期生成
    dates = planner.generate_dates()
    print(f"\n生成的日期: {dates}")
    
    # 测试行程模板生成
    itinerary = planner.generate_itinerary_template()
    print(f"\n行程天数: {len(itinerary)}")
    print(f"第一天活动数量: {len(itinerary[0]) if itinerary else 0}")
    
    # 测试Markdown报告生成
    report = planner.generate_markdown_report()
    print(f"\n报告长度: {len(report)} 字符")
    print(f"报告预览（前500字符）:")
    print(report[:500] + "..." if len(report) > 500 else report)
    
    # 保存测试报告
    test_output_path = "test_output.md"
    planner.save_report(test_output_path)
    print(f"\n测试报告已保存至: {test_output_path}")
    
    # 检查文件是否存在
    if os.path.exists(test_output_path):
        file_size = os.path.getsize(test_output_path)
        print(f"测试文件大小: {file_size} 字节")
        print("✓ 基本功能测试通过")
    else:
        print("✗ 基本功能测试失败")
    
    # 清理测试文件
    if os.path.exists(test_output_path):
        os.remove(test_output_path)
        print("测试文件已清理")


def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    
    # 测试1天行程
    planner_1day = TravelPlanner("北京", 1, 1, 1000)
    itinerary_1day = planner_1day.generate_itinerary_template()
    print(f"1天行程活动数量: {len(itinerary_1day[0]) if itinerary_1day else 0}")
    
    # 测试多人预算分配
    planner_many_people = TravelPlanner("上海", 5, 10, 20000)
    print(f"10人预算分配: 总预算¥{planner_many_people.budget}, 人均¥{planner_many_people.per_person_budget}")
    
    print("✓ 边界情况测试通过")


if __name__ == "__main__":
    test_basic_functionality()
    test_edge_cases()
    print("\n=== 所有测试完成 ===")