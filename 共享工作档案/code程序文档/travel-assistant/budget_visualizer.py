#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预算可视化工具 - Budget Visualizer
用于智能旅行助手项目，支持读取预算数据并生成可视化图表

功能：
1. 读取JSON/CSV格式的预算数据
2. 生成费用分类饼图（住宿、餐饮、交通、门票、其他）
3. 生成每日支出柱状图
4. 保存图表为图片文件

作者: OpenClaw Coder Agent
日期: 2026-03-11
"""

import json
import csv
import os
import sys
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

# 导入matplotlib用于绘图
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
matplotlib.rcParams['axes.unicode_minus'] = False


@dataclass
class BudgetData:
    """预算数据类，存储分类费用和每日支出"""
    categories: Dict[str, float]  # 费用分类: 住宿、餐饮、交通、门票、其他
    daily: Dict[str, float]       # 每日支出: Day1, Day2, Day3...


class BudgetVisualizer:
    """
    预算可视化器类
    
    主要功能：
    - 从文件读取预算数据（JSON/CSV）
    - 生成费用分类饼图
    - 生成每日支出柱状图
    - 保存图表为图片
    """
    
    # 分类名称的中文映射
    CATEGORY_NAMES = {
        'accommodation': '住宿',
        'food': '餐饮',
        'transport': '交通',
        'tickets': '门票',
        'others': '其他'
    }
    
    # 分类颜色映射
    CATEGORY_COLORS = {
        'accommodation': '#FF6B6B',  # 红色
        'food': '#4ECDC4',           # 青色
        'transport': '#45B7D1',      # 蓝色
        'tickets': '#96CEB4',        # 绿色
        'others': '#FFEAA7'          # 黄色
    }
    
    def __init__(self):
        """初始化预算可视化器"""
        self.data: Optional[BudgetData] = None
        self.fig_size = (14, 6)  # 图表尺寸
        self.dpi = 150  # 图片分辨率
    
    def load_from_json(self, filepath: str) -> bool:
        """
        从JSON文件加载预算数据
        
        Args:
            filepath: JSON文件路径
            
        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # 验证数据结构
            if 'categories' not in raw_data or 'daily' not in raw_data:
                print(f"错误: JSON文件格式不正确，缺少'categories'或'daily'字段")
                return False
            
            self.data = BudgetData(
                categories=raw_data['categories'],
                daily=raw_data['daily']
            )
            print(f"成功从JSON文件加载数据: {filepath}")
            return True
            
        except FileNotFoundError:
            print(f"错误: 文件不存在 - {filepath}")
            return False
        except json.JSONDecodeError as e:
            print(f"错误: JSON解析失败 - {e}")
            return False
        except Exception as e:
            print(f"错误: 加载JSON文件时发生异常 - {e}")
            return False
    
    def load_from_csv(self, filepath: str) -> bool:
        """
        从CSV文件加载预算数据
        
        CSV格式要求：
        - 第一列为类型（category/daily）
        - 第二列为项目名称
        - 第三列为金额
        
        Args:
            filepath: CSV文件路径
            
        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            categories = {}
            daily = {}
            
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)  # 跳过表头
                
                for row in reader:
                    if len(row) < 3:
                        continue
                    
                    data_type, name, value = row[0].strip(), row[1].strip(), row[2].strip()
                    
                    try:
                        amount = float(value)
                        if data_type.lower() == 'category':
                            categories[name] = amount
                        elif data_type.lower() == 'daily':
                            daily[name] = amount
                    except ValueError:
                        print(f"警告: 跳过无效数值 - {value}")
                        continue
            
            if not categories and not daily:
                print(f"错误: CSV文件中没有有效数据")
                return False
            
            self.data = BudgetData(categories=categories, daily=daily)
            print(f"成功从CSV文件加载数据: {filepath}")
            return True
            
        except FileNotFoundError:
            print(f"错误: 文件不存在 - {filepath}")
            return False
        except Exception as e:
            print(f"错误: 加载CSV文件时发生异常 - {e}")
            return False
    
    def load_data(self, filepath: str) -> bool:
        """
        自动根据文件扩展名加载数据
        
        Args:
            filepath: 数据文件路径（支持.json和.csv）
            
        Returns:
            bool: 加载成功返回True，否则返回False
        """
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.json':
            return self.load_from_json(filepath)
        elif ext == '.csv':
            return self.load_from_csv(filepath)
        else:
            print(f"错误: 不支持的文件格式 - {ext}")
            print("支持的格式: .json, .csv")
            return False
    
    def set_data(self, categories: Dict[str, float], daily: Dict[str, float]) -> None:
        """
        直接设置预算数据
        
        Args:
            categories: 费用分类字典
            daily: 每日支出字典
        """
        self.data = BudgetData(categories=categories, daily=daily)
    
    def _get_category_labels(self) -> List[str]:
        """获取分类的中文标签"""
        return [self.CATEGORY_NAMES.get(k, k) for k in self.data.categories.keys()]
    
    def _get_category_colors(self) -> List[str]:
        """获取分类的颜色"""
        return [self.CATEGORY_COLORS.get(k, '#CCCCCC') for k in self.data.categories.keys()]
    
    def create_pie_chart(self, ax=None) -> Optional[plt.Axes]:
        """
        创建费用分类饼图
        
        Args:
            ax: matplotlib的Axes对象，如果为None则创建新的
            
        Returns:
            plt.Axes: 图表的Axes对象
        """
        if self.data is None:
            print("错误: 请先加载数据")
            return None
        
        if not self.data.categories:
            print("错误: 没有分类数据")
            return None
        
        # 创建新的axes如果未提供
        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 6))
        
        # 准备数据
        values = list(self.data.categories.values())
        labels = self._get_category_labels()
        colors = self._get_category_colors()
        
        # 计算百分比
        total = sum(values)
        
        # 创建饼图
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            colors=colors,
            autopct=lambda pct: f'{pct:.1f}%\n({pct/100*total:.0f})',
            startangle=90,
            explode=[0.02] * len(values),  # 轻微分离
            shadow=True,
            textprops={'fontsize': 10}
        )
        
        # 设置标题
        ax.set_title('费用分类占比', fontsize=14, fontweight='bold', pad=20)
        
        # 添加总计信息
        ax.text(0, -1.3, f'总计: {total:.0f} 元', 
                ha='center', fontsize=12, fontweight='bold')
        
        return ax
    
    def create_bar_chart(self, ax=None) -> Optional[plt.Axes]:
        """
        创建每日支出柱状图
        
        Args:
            ax: matplotlib的Axes对象，如果为None则创建新的
            
        Returns:
            plt.Axes: 图表的Axes对象
        """
        if self.data is None:
            print("错误: 请先加载数据")
            return None
        
        if not self.data.daily:
            print("错误: 没有每日支出数据")
            return None
        
        # 创建新的axes如果未提供
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        
        # 准备数据
        days = list(self.data.daily.keys())
        values = list(self.data.daily.values())
        
        # 创建渐变色
        colors = plt.cm.Blues([0.4 + 0.15 * i for i in range(len(days))])
        
        # 创建柱状图
        bars = ax.bar(days, values, color=colors, edgecolor='black', linewidth=1.2)
        
        # 在柱子上添加数值标签
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.0f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 设置标题和标签
        ax.set_title('每日支出对比', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('金额 (元)', fontsize=12)
        
        # 设置网格线
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # 添加总计信息
        total = sum(values)
        avg = total / len(values) if values else 0
        ax.text(0.95, 0.95, f'总计: {total:.0f} 元\n平均: {avg:.0f} 元/天',
                transform=ax.transAxes, ha='right', va='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontsize=10)
        
        return ax
    
    def create_combined_chart(self) -> Optional[plt.Figure]:
        """
        创建组合图表（饼图+柱状图）
        
        Returns:
            plt.Figure: 组合图表的Figure对象
        """
        if self.data is None:
            print("错误: 请先加载数据")
            return None
        
        # 创建图形和子图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.fig_size)
        fig.suptitle('旅行预算可视化分析', fontsize=16, fontweight='bold', y=1.02)
        
        # 创建饼图
        if self.data.categories:
            self.create_pie_chart(ax1)
        else:
            ax1.text(0.5, 0.5, '无分类数据', ha='center', va='center', transform=ax1.transAxes)
            ax1.set_title('费用分类占比')
        
        # 创建柱状图
        if self.data.daily:
            self.create_bar_chart(ax2)
        else:
            ax2.text(0.5, 0.5, '无每日数据', ha='center', va='center', transform=ax2.transAxes)
            ax2.set_title('每日支出对比')
        
        # 调整布局
        plt.tight_layout()
        
        return fig
    
    def save_chart(self, output_path: str, fig: Optional[plt.Figure] = None) -> bool:
        """
        保存图表为图片
        
        Args:
            output_path: 输出图片路径（支持.png, .jpg, .pdf等格式）
            fig: 要保存的Figure对象，如果为None则创建新的组合图表
            
        Returns:
            bool: 保存成功返回True，否则返回False
        """
        try:
            # 如果没有提供fig，创建新的组合图表
            if fig is None:
                fig = self.create_combined_chart()
                if fig is None:
                    return False
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # 保存图片
            fig.savefig(output_path, dpi=self.dpi, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"图表已保存至: {output_path}")
            
            # 关闭图形释放内存
            plt.close(fig)
            
            return True
            
        except Exception as e:
            print(f"错误: 保存图表失败 - {e}")
            return False
    
    def generate_report(self) -> str:
        """
        生成预算报告文本
        
        Returns:
            str: 格式化的预算报告
        """
        if self.data is None:
            return "错误: 请先加载数据"
        
        report = []
        report.append("=" * 40)
        report.append("旅行预算报告")
        report.append("=" * 40)
        
        # 分类费用
        if self.data.categories:
            report.append("\n【费用分类】")
            cat_total = sum(self.data.categories.values())
            for key, value in self.data.categories.items():
                name = self.CATEGORY_NAMES.get(key, key)
                pct = (value / cat_total * 100) if cat_total > 0 else 0
                report.append(f"  {name}: {value:.0f} 元 ({pct:.1f}%)")
            report.append(f"  分类总计: {cat_total:.0f} 元")
        
        # 每日支出
        if self.data.daily:
            report.append("\n【每日支出】")
            daily_total = sum(self.data.daily.values())
            for day, value in self.data.daily.items():
                report.append(f"  {day}: {value:.0f} 元")
            avg = daily_total / len(self.data.daily) if self.data.daily else 0
            report.append(f"  每日平均: {avg:.0f} 元")
            report.append(f"  支出总计: {daily_total:.0f} 元")
        
        report.append("\n" + "=" * 40)
        
        return "\n".join(report)


def create_sample_data() -> Dict:
    """
    创建示例预算数据
    
    Returns:
        Dict: 示例数据字典
    """
    return {
        "categories": {
            "accommodation": 800,
            "food": 600,
            "transport": 1000,
            "tickets": 300,
            "others": 200
        },
        "daily": {
            "Day1": 1200,
            "Day2": 1500,
            "Day3": 900
        }
    }


def save_sample_data(output_dir: str = ".") -> str:
    """
    保存示例数据到文件
    
    Args:
        output_dir: 输出目录
        
    Returns:
        str: 保存的文件路径
    """
    sample_data = create_sample_data()
    
    # 保存JSON格式
    json_path = os.path.join(output_dir, "sample_budget.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    print(f"示例JSON数据已保存: {json_path}")
    
    # 保存CSV格式
    csv_path = os.path.join(output_dir, "sample_budget.csv")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'name', 'amount'])
        
        # 写入分类数据
        for key, value in sample_data['categories'].items():
            writer.writerow(['category', key, value])
        
        # 写入每日数据
        for key, value in sample_data['daily'].items():
            writer.writerow(['daily', key, value])
    print(f"示例CSV数据已保存: {csv_path}")
    
    return json_path


def main():
    """
    主函数 - 演示预算可视化工具的使用
    """
    print("=" * 50)
    print("预算可视化工具 - Budget Visualizer")
    print("=" * 50)
    
    # 创建示例数据
    print("\n[1] 创建示例数据...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_json = save_sample_data(script_dir)
    
    # 初始化可视化器
    print("\n[2] 初始化预算可视化器...")
    visualizer = BudgetVisualizer()
    
    # 从JSON加载数据
    print("\n[3] 从JSON文件加载数据...")
    if visualizer.load_from_json(sample_json):
        # 生成报告
        print("\n[4] 生成预算报告...")
        print(visualizer.generate_report())
        
        # 创建并保存图表
        print("\n[5] 创建并保存可视化图表...")
        output_path = os.path.join(script_dir, "budget_chart.png")
        if visualizer.save_chart(output_path):
            print(f"\n✓ 可视化图表已成功生成!")
            print(f"  图表文件: {output_path}")
        
        # 演示直接设置数据
        print("\n[6] 演示直接设置数据...")
        visualizer.set_data(
            categories={
                "accommodation": 1200,
                "food": 800,
                "transport": 1500,
                "tickets": 500,
                "others": 300
            },
            daily={
                "Day1": 1500,
                "Day2": 1800,
                "Day3": 1200,
                "Day4": 1000
            }
        )
        print("已设置新的预算数据（4天行程）")
        print(visualizer.generate_report())
    
    print("\n" + "=" * 50)
    print("演示完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
