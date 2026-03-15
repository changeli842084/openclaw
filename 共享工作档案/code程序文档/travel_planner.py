#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行程规划工具
功能：根据目的地、天数、人数、预算生成旅游行程规划
作者：Coder
日期：2026-03-15
"""

import argparse
import datetime
from typing import Dict, List


class TravelPlanner:
    """行程规划器类"""
    
    def __init__(self, destination: str, days: int, people: int, budget: float):
        """
        初始化行程规划器
        
        Args:
            destination: 目的地
            days: 天数
            people: 人数
            budget: 总预算
        """
        self.destination = destination
        self.days = days
        self.people = people
        self.budget = budget
        self.per_person_budget = budget / people if people > 0 else 0
    
    def generate_dates(self) -> List[str]:
        """生成行程日期列表"""
        start_date = datetime.date.today() + datetime.timedelta(days=7)  # 假设一周后出发
        dates = []
        for i in range(self.days):
            current_date = start_date + datetime.timedelta(days=i)
            dates.append(current_date.strftime("%Y-%m-%d"))
        return dates
    
    def generate_itinerary_template(self) -> List[List[Dict]]:
        """生成行程模板"""
        dates = self.generate_dates()
        itinerary = []
        
        for day_idx, date in enumerate(dates):
            day_plan = []
            
            # 根据天数和预算分配每日活动
            daily_budget = self.budget * 0.8 / self.days  # 80%预算用于日常开销
            transport_budget = self.budget * 0.1 / self.days  # 10%预算用于交通
            food_budget = self.budget * 0.1 / self.days  # 10%预算用于餐饮
            
            # 第一天通常是抵达
            if day_idx == 0:
                day_plan.extend([
                    {
                        "time": "上午",
                        "activity": f"抵达{self.destination}",
                        "location": f"{self.destination}机场/火车站",
                        "budget": round(transport_budget * 0.6, 2),
                        "category": "交通"
                    },
                    {
                        "time": "中午",
                        "activity": "入住酒店",
                        "location": "预订酒店",
                        "budget": round(daily_budget * 0.4, 2),
                        "category": "住宿"
                    },
                    {
                        "time": "下午",
                        "activity": f"适应{self.destination}，休息",
                        "location": "酒店附近",
                        "budget": round(food_budget * 0.5, 2),
                        "category": "餐饮"
                    },
                    {
                        "time": "晚上",
                        "activity": f"夜游{self.destination}特色街区",
                        "location": "市中心",
                        "budget": round(food_budget * 0.5, 2),
                        "category": "餐饮"
                    }
                ])
            # 最后一天通常是返程
            elif day_idx == len(dates) - 1:
                day_plan.extend([
                    {
                        "time": "上午",
                        "activity": f"{self.destination}最后游览",
                        "location": "景点",
                        "budget": round(daily_budget * 0.3, 2),
                        "category": "景点"
                    },
                    {
                        "time": "中午",
                        "activity": "退房，准备返程",
                        "location": "酒店",
                        "budget": round(food_budget * 0.5, 2),
                        "category": "餐饮"
                    },
                    {
                        "time": "下午",
                        "activity": f"离开{self.destination}",
                        "location": f"{self.destination}机场/火车站",
                        "budget": round(transport_budget * 0.6, 2),
                        "category": "交通"
                    }
                ])
            # 中间的日子安排景点游览
            else:
                day_plan.extend([
                    {
                        "time": "上午",
                        "activity": f"{self.destination}经典景点游览",
                        "location": "著名景点",
                        "budget": round(daily_budget * 0.4, 2),
                        "category": "景点"
                    },
                    {
                        "time": "中午",
                        "activity": "当地美食体验",
                        "location": "特色餐厅",
                        "budget": round(food_budget * 0.5, 2),
                        "category": "餐饮"
                    },
                    {
                        "time": "下午",
                        "activity": f"{self.destination}文化体验",
                        "location": "博物馆/文化区",
                        "budget": round(daily_budget * 0.3, 2),
                        "category": "景点"
                    },
                    {
                        "time": "晚上",
                        "activity": "自由活动/购物",
                        "location": "商业街/购物中心",
                        "budget": round(daily_budget * 0.3 + food_budget * 0.5, 2),
                        "category": "购物/餐饮"
                    }
                ])
            
            itinerary.append(day_plan)
        
        return itinerary
    
    def generate_markdown_report(self) -> str:
        """生成Markdown格式的行程报告"""
        dates = self.generate_dates()
        itinerary = self.generate_itinerary_template()
        
        markdown_content = f"# {self.destination} {self.days}天{self.days-1}晚行程规划\n\n"
        markdown_content += f"> 总预算：¥{self.budget} | 人数：{self.people}人 | 人均预算：¥{round(self.per_person_budget, 2)}\n\n"
        
        for day_idx, (date, day_plan) in enumerate(zip(dates, itinerary)):
            markdown_content += f"## Day {day_idx + 1} - {date}\n"
            markdown_content += "| 时间 | 活动 | 地点 | 预算 | 类别 |\n"
            markdown_content += "|------|------|------|------|------|\n"
            
            for item in day_plan:
                markdown_content += f"| {item['time']} | {item['activity']} | {item['location']} | ¥{item['budget']} | {item['category']} |\n"
            
            markdown_content += "\n"
        
        # 添加预算总结
        markdown_content += "## 预算总结\n"
        markdown_content += f"- 总预算：¥{self.budget}\n"
        markdown_content += f"- 人数：{self.people}人\n"
        markdown_content += f"- 人均预算：¥{round(self.per_person_budget, 2)}\n"
        markdown_content += f"- 每日预算（平均）：¥{round(self.budget / self.days, 2)}\n\n"
        
        # 添加建议
        markdown_content += "## 旅行小贴士\n"
        markdown_content += "- 出行前请确认天气情况，准备相应衣物\n"
        markdown_content += "- 提前预订热门景点门票以避免排队\n"
        markdown_content += "- 保管好个人财物，注意出行安全\n"
        markdown_content += "- 尝试当地特色美食，体验地道文化\n"
        
        return markdown_content
    
    def save_report(self, filepath: str):
        """保存行程报告到文件"""
        report = self.generate_markdown_report()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)


def main():
    """主函数 - 命令行入口"""
    parser = argparse.ArgumentParser(description='行程规划工具')
    parser.add_argument('destination', help='目的地')
    parser.add_argument('days', type=int, help='天数')
    parser.add_argument('people', type=int, help='人数')
    parser.add_argument('budget', type=float, help='总预算')
    parser.add_argument('-o', '--output', default=None, help='输出文件路径')
    
    args = parser.parse_args()
    
    # 创建行程规划器
    planner = TravelPlanner(args.destination, args.days, args.people, args.budget)
    
    # 生成报告
    report = planner.generate_markdown_report()
    
    # 确定输出文件路径
    if args.output:
        output_path = args.output
    else:
        output_path = f"{args.destination}_行程规划.md"
    
    # 保存报告
    planner.save_report(output_path)
    
    print(f"行程规划已生成并保存至：{output_path}")
    print("\n行程概览：")
    print(f"目的地：{args.destination}")
    print(f"天数：{args.days}")
    print(f"人数：{args.people}")
    print(f"总预算：¥{args.budget}")
    print(f"人均预算：¥{round(args.budget / args.people, 2)}")


if __name__ == "__main__":
    main()