#!/usr/bin/env python3
"""
行程优化器 (Route Optimizer)
功能：输入景点列表和位置，根据距离优化游览顺序，输出最优路线，计算总路程
"""

import json
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from itertools import permutations


@dataclass
class Attraction:
    """
    景点数据类
    
    Attributes:
        name (str): 景点名称
        latitude (float): 纬度
        longitude (float): 经度
        visit_duration (int): 建议游览时长（分钟）
        rating (float): 评分（1-5）
        category (str): 类别
    """
    name: str
    latitude: float
    longitude: float
    visit_duration: int = 60  # 默认游览60分钟
    rating: float = 4.0
    category: str = "景点"
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category}, 评分: {self.rating})"


class RouteOptimizer:
    """
    路线优化器类
    
    使用贪心算法或穷举法（小规模）来优化游览路线
    
    Attributes:
        attractions (List[Attraction]): 景点列表
        start_point (Attraction): 起始点
        end_point (Optional[Attraction]): 终点（可选）
    """
    
    def __init__(self, start_point: Optional[Attraction] = None):
        """
        初始化路线优化器
        
        Args:
            start_point: 起始点，默认为 None（使用第一个景点作为起点）
        """
        self.attractions: List[Attraction] = []
        self.start_point = start_point
        self.end_point: Optional[Attraction] = None
    
    def add_attraction(self, attraction: Attraction) -> None:
        """
        添加景点
        
        Args:
            attraction: 景点对象
        """
        self.attractions.append(attraction)
    
    def add_attractions(self, attractions: List[Attraction]) -> None:
        """
        批量添加景点
        
        Args:
            attractions: 景点列表
        """
        self.attractions.extend(attractions)
    
    def set_start_point(self, start_point: Attraction) -> None:
        """
        设置起始点
        
        Args:
            start_point: 起始景点
        """
        self.start_point = start_point
    
    def set_end_point(self, end_point: Attraction) -> None:
        """
        设置终点
        
        Args:
            end_point: 终点景点
        """
        self.end_point = end_point
    
    @staticmethod
    def calculate_distance(attr1: Attraction, attr2: Attraction) -> float:
        """
        计算两个景点之间的直线距离（使用Haversine公式）
        
        Args:
            attr1: 第一个景点
            attr2: 第二个景点
            
        Returns:
            float: 距离（公里）
        """
        R = 6371  # 地球半径（公里）
        
        lat1, lon1 = math.radians(attr1.latitude), math.radians(attr1.longitude)
        lat2, lon2 = math.radians(attr2.latitude), math.radians(attr2.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def calculate_total_distance(self, route: List[Attraction]) -> float:
        """
        计算路线的总距离
        
        Args:
            route: 景点顺序列表
            
        Returns:
            float: 总距离（公里）
        """
        if len(route) < 2:
            return 0.0
        
        total = 0.0
        for i in range(len(route) - 1):
            total += self.calculate_distance(route[i], route[i+1])
        return total
    
    def optimize_greedy(self) -> List[Attraction]:
        """
        使用贪心算法优化路线（最近邻算法）
        
        Returns:
            List[Attraction]: 优化后的路线
        """
        if not self.attractions:
            return []
        
        # 确定起点
        if self.start_point:
            current = self.start_point
            remaining = [a for a in self.attractions if a != self.start_point]
        else:
            current = self.attractions[0]
            remaining = self.attractions[1:]
        
        route = [current]
        
        while remaining:
            # 找到最近的下一个景点
            nearest = min(remaining, 
                         key=lambda a: self.calculate_distance(current, a))
            route.append(nearest)
            remaining.remove(nearest)
            current = nearest
        
        # 如果有指定终点，确保路线包含终点
        if self.end_point and self.end_point not in route:
            route.append(self.end_point)
        
        return route
    
    def optimize_brute_force(self) -> List[Attraction]:
        """
        使用穷举法找到最优路线（适用于少量景点，<=8个）
        
        Returns:
            List[Attraction]: 最优路线
        """
        if len(self.attractions) > 8:
            print("[WARNING] 景点数量过多，使用贪心算法代替")
            return self.optimize_greedy()
        
        if not self.attractions:
            return []
        
        # 确定起点和需要排列的景点
        if self.start_point:
            fixed_start = [self.start_point]
            to_permute = [a for a in self.attractions if a != self.start_point]
        else:
            fixed_start = []
            to_permute = self.attractions
        
        # 确定终点
        if self.end_point:
            fixed_end = [self.end_point]
            if self.end_point in to_permute:
                to_permute.remove(self.end_point)
        else:
            fixed_end = []
        
        best_route = None
        best_distance = float('inf')
        
        # 穷举所有排列
        for perm in permutations(to_permute):
            route = fixed_start + list(perm) + fixed_end
            distance = self.calculate_total_distance(route)
            if distance < best_distance:
                best_distance = distance
                best_route = route
        
        return list(best_route) if best_route else []
    
    def optimize(self, method: str = 'auto') -> List[Attraction]:
        """
        优化路线（自动选择算法）
        
        Args:
            method: 优化方法 ('greedy', 'brute_force', 或 'auto')
            
        Returns:
            List[Attraction]: 优化后的路线
        """
        if method == 'auto':
            if len(self.attractions) <= 8:
                return self.optimize_brute_force()
            else:
                return self.optimize_greedy()
        elif method == 'greedy':
            return self.optimize_greedy()
        elif method == 'brute_force':
            return self.optimize_brute_force()
        else:
            raise ValueError(f"未知的优化方法: {method}")
    
    def generate_route_report(self, route: List[Attraction]) -> str:
        """
        生成路线报告
        
        Args:
            route: 优化后的路线
            
        Returns:
            str: 格式化报告
        """
        if not route:
            return "[ERROR] 没有可显示的路线"
        
        total_distance = self.calculate_total_distance(route)
        total_duration = sum(a.visit_duration for a in route)
        
        report = []
        report.append("=" * 60)
        report.append("🗺️  优化后的游览路线")
        report.append("=" * 60)
        report.append("")
        
        for i, attraction in enumerate(route, 1):
            report.append(f"📍 第{i}站: {attraction.name}")
            report.append(f"   类别: {attraction.category}")
            report.append(f"   评分: {'⭐' * int(attraction.rating)} ({attraction.rating}/5)")
            report.append(f"   建议游览: {attraction.visit_duration} 分钟")
            report.append(f"   坐标: ({attraction.latitude:.4f}, {attraction.longitude:.4f})")
            
            if i < len(route):
                dist = self.calculate_distance(attraction, route[i])
                report.append(f"   ➡️  到下一站: {dist:.2f} 公里")
            report.append("")
        
        report.append("-" * 60)
        report.append(f"📊 路线统计")
        report.append(f"   总路程: {total_distance:.2f} 公里")
        report.append(f"   总游览时间: {total_duration} 分钟 ({total_duration//60}小时{total_duration%60}分钟)")
        report.append(f"   景点数量: {len(route)}")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def export_route(self, route: List[Attraction], filename: str) -> None:
        """
        导出路线到JSON文件
        
        Args:
            route: 优化后的路线
            filename: 输出文件名
        """
        route_data = {
            'route': [asdict(a) for a in route],
            'total_distance': self.calculate_total_distance(route),
            'total_duration': sum(a.visit_duration for a in route),
            'attraction_count': len(route)
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(route_data, f, ensure_ascii=False, indent=2)
            print(f"[INFO] 路线已导出到: {filename}")
        except IOError as e:
            print(f"[ERROR] 导出失败: {e}")
    
    @staticmethod
    def load_attractions_from_json(filename: str) -> List[Attraction]:
        """
        从JSON文件加载景点
        
        Args:
            filename: JSON文件路径
            
        Returns:
            List[Attraction]: 景点列表
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            attractions = []
            for item in data:
                attraction = Attraction(
                    name=item['name'],
                    latitude=item['latitude'],
                    longitude=item['longitude'],
                    visit_duration=item.get('visit_duration', 60),
                    rating=item.get('rating', 4.0),
                    category=item.get('category', '景点')
                )
                attractions.append(attraction)
            
            print(f"[INFO] 从 {filename} 加载了 {len(attractions)} 个景点")
            return attractions
        except (IOError, json.JSONDecodeError, KeyError) as e:
            print(f"[ERROR] 加载景点失败: {e}")
            return []


def create_sample_attractions() -> List[Attraction]:
    """
    创建示例景点数据（昆明）
    
    Returns:
        List[Attraction]: 示例景点列表
    """
    return [
        Attraction("翠湖公园", 25.0596, 102.7041, 90, 4.5, "自然景观"),
        Attraction("云南大学", 25.0604, 102.7029, 60, 4.3, "文化景点"),
        Attraction("金马碧鸡坊", 25.0389, 102.7183, 30, 4.0, "历史建筑"),
        Attraction("滇池", 24.8252, 102.6906, 120, 4.6, "自然景观"),
        Attraction("西山森林公园", 24.9567, 102.6294, 180, 4.4, "自然景观"),
        Attraction("云南省博物馆", 25.0375, 102.7628, 120, 4.5, "博物馆"),
        Attraction("官渡古镇", 25.0156, 102.7603, 90, 4.2, "历史古镇"),
        Attraction("石林风景区", 24.8189, 103.3248, 240, 4.7, "自然景观"),
    ]


def main():
    """
    主函数 - 演示路线优化功能
    """
    print("=" * 70)
    print("🚀 行程优化器演示")
    print("=" * 70)
    
    # 创建优化器
    optimizer = RouteOptimizer()
    
    # 添加示例景点
    print("\n[INFO] 加载示例景点数据（昆明）...")
    attractions = create_sample_attractions()
    optimizer.add_attractions(attractions)
    
    print(f"[INFO] 已添加 {len(attractions)} 个景点:")
    for i, a in enumerate(attractions, 1):
        print(f"   {i}. {a}")
    
    # 示例1: 使用贪心算法优化
    print("\n" + "=" * 70)
    print("【示例1】贪心算法优化（最近邻算法）")
    print("=" * 70)
    
    route_greedy = optimizer.optimize(method='greedy')
    print(optimizer.generate_route_report(route_greedy))
    
    # 示例2: 使用穷举法优化（景点数量少时）
    print("\n" + "=" * 70)
    print("【示例2】穷举法优化（全局最优）")
    print("=" * 70)
    
    # 只选择5个景点进行穷举演示
    optimizer_small = RouteOptimizer()
    optimizer_small.add_attractions(attractions[:5])
    
    route_brute = optimizer_small.optimize(method='brute_force')
    print(optimizer_small.generate_route_report(route_brute))
    
    # 示例3: 指定起点和终点
    print("\n" + "=" * 70)
    print("【示例3】指定起点和终点")
    print("=" * 70)
    
    optimizer_custom = RouteOptimizer()
    optimizer_custom.add_attractions(attractions)
    optimizer_custom.set_start_point(attractions[0])  # 翠湖公园作为起点
    optimizer_custom.set_end_point(attractions[3])     # 滇池作为终点
    
    route_custom = optimizer_custom.optimize()
    print(optimizer_custom.generate_route_report(route_custom))
    
    # 导出路线
    print("\n" + "=" * 70)
    print("【导出功能演示】")
    print("=" * 70)
    
    optimizer.export_route(route_greedy, "kunming_route.json")
    
    # 显示距离矩阵（用于调试/分析）
    print("\n" + "=" * 70)
    print("【景点间距离矩阵】（单位：公里）")
    print("=" * 70)
    
    print(f"{'景点':<15}", end="")
    for a in attractions[:5]:
        print(f"{a.name[:6]:<10}", end="")
    print()
    
    for i, a1 in enumerate(attractions[:5]):
        print(f"{a1.name[:6]:<10}", end="")
        for j, a2 in enumerate(attractions[:5]):
            if i == j:
                print(f"{'-':<10}", end="")
            else:
                dist = RouteOptimizer.calculate_distance(a1, a2)
                print(f"{dist:<10.1f}", end="")
        print()
    
    print("\n" + "=" * 70)
    print("✅ 演示完成！")
    print("=" * 70)


if __name__ == '__main__':
    main()
