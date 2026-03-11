#!/usr/bin/env python3
"""
价格监控脚本 (Price Monitor)
功能：模拟监控酒店/机票价格变化，记录历史，价格低于阈值时提醒，生成趋势图
"""

import json
import random
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# 尝试导入matplotlib，如果失败则使用纯文本模式
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("[WARNING] matplotlib 未安装，将使用纯文本模式输出")


class PriceMonitor:
    """
    价格监控类，用于监控酒店或机票价格变化
    
    Attributes:
        item_type (str): 监控类型 ('hotel' 或 'flight')
        item_name (str): 项目名称
        threshold (float): 价格阈值，低于此值会触发提醒
        history_file (str): 价格历史数据存储文件路径
        price_history (List[Dict]): 价格历史记录列表
    """
    
    def __init__(self, item_type: str, item_name: str, threshold: float, 
                 history_file: Optional[str] = None):
        """
        初始化价格监控器
        
        Args:
            item_type: 监控类型 ('hotel' 或 'flight')
            item_name: 项目名称
            threshold: 价格阈值
            history_file: 历史数据文件路径，默认为 None (自动生成)
        """
        self.item_type = item_type
        self.item_name = item_name
        self.threshold = threshold
        self.history_file = history_file or f"{item_type}_{item_name.replace(' ', '_')}_history.json"
        self.price_history: List[Dict] = []
        self._load_history()
    
    def _load_history(self) -> None:
        """从文件加载价格历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.price_history = json.load(f)
                print(f"[INFO] 已加载 {len(self.price_history)} 条历史记录")
            except (json.JSONDecodeError, IOError) as e:
                print(f"[WARNING] 加载历史数据失败: {e}")
                self.price_history = []
    
    def _save_history(self) -> None:
        """保存价格历史到文件"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.price_history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"[ERROR] 保存历史数据失败: {e}")
    
    def simulate_current_price(self) -> float:
        """
        模拟获取当前价格（使用随机数据）
        
        Returns:
            float: 模拟的当前价格
        """
        # 基础价格根据类型设定
        base_price = 800 if self.item_type == 'hotel' else 1200
        
        # 根据历史记录调整基础价格
        if self.price_history:
            last_price = self.price_history[-1]['price']
            # 价格在上一价格的基础上波动 -10% 到 +10%
            change_percent = random.uniform(-0.1, 0.1)
            current_price = last_price * (1 + change_percent)
        else:
            # 首次记录，在基础价格附近波动
            current_price = base_price * random.uniform(0.8, 1.3)
        
        return round(current_price, 2)
    
    def check_price(self) -> Tuple[float, bool]:
        """
        检查当前价格并记录
        
        Returns:
            Tuple[float, bool]: (当前价格, 是否低于阈值)
        """
        current_price = self.simulate_current_price()
        is_low = current_price < self.threshold
        
        record = {
            'timestamp': datetime.now().isoformat(),
            'price': current_price,
            'threshold': self.threshold,
            'alert': is_low
        }
        
        self.price_history.append(record)
        self._save_history()
        
        return current_price, is_low
    
    def generate_alert(self, current_price: float) -> str:
        """
        生成价格提醒消息
        
        Args:
            current_price: 当前价格
            
        Returns:
            str: 提醒消息
        """
        savings = self.threshold - current_price
        savings_percent = (savings / self.threshold) * 100
        
        alert_msg = f"""
🎉 价格提醒！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
项目: {self.item_name} ({self.item_type.upper()})
当前价格: ¥{current_price:.2f}
设定阈值: ¥{self.threshold:.2f}
节省金额: ¥{savings:.2f} ({savings_percent:.1f}%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
建议立即预订！
"""
        return alert_msg
    
    def generate_trend_chart(self, output_file: Optional[str] = None) -> str:
        """
        生成价格趋势图
        
        Args:
            output_file: 输出图片路径，默认为 None (自动生成)
            
        Returns:
            str: 生成的图片文件路径（或空字符串如果matplotlib不可用）
        """
        if not MATPLOTLIB_AVAILABLE:
            print("[WARNING] matplotlib 未安装，无法生成图表")
            self._print_text_chart()
            return ""
        
        if len(self.price_history) < 2:
            print("[WARNING] 历史数据不足，无法生成趋势图")
            return ""
        
        # 准备数据
        dates = [datetime.fromisoformat(record['timestamp']) for record in self.price_history]
        prices = [record['price'] for record in self.price_history]
        
        # 创建图表
        plt.figure(figsize=(12, 6))
        plt.plot(dates, prices, 'b-', linewidth=2, marker='o', markersize=4, label='价格走势')
        
        # 添加阈值线
        plt.axhline(y=self.threshold, color='r', linestyle='--', linewidth=2, 
                   label=f'阈值 (¥{self.threshold:.2f})')
        
        # 标记低于阈值的点
        low_prices = [(d, p) for d, p in zip(dates, prices) if p < self.threshold]
        if low_prices:
            low_dates, low_vals = zip(*low_prices)
            plt.scatter(low_dates, low_vals, color='green', s=100, zorder=5, 
                       label='低价机会', marker='*')
        
        # 设置图表样式
        plt.title(f'{self.item_name} 价格趋势图', fontsize=16, fontweight='bold')
        plt.xlabel('时间', fontsize=12)
        plt.ylabel('价格 (¥)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='best', fontsize=10)
        
        # 格式化x轴日期
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # 保存图片
        output_file = output_file or f"{self.item_type}_{self.item_name.replace(' ', '_')}_trend.png"
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"[INFO] 趋势图已保存: {output_file}")
        return output_file
    
    def _print_text_chart(self) -> None:
        """打印文本格式的趋势图（当matplotlib不可用时）"""
        if len(self.price_history) < 2:
            return
        
        print("\n📈 价格趋势（文本模式）")
        print("-" * 50)
        
        prices = [record['price'] for record in self.price_history[-20:]]  # 最近20条
        max_price = max(prices)
        min_price = min(prices)
        price_range = max_price - min_price if max_price != min_price else 1
        
        for i, (record, price) in enumerate(zip(self.price_history[-20:], prices)):
            timestamp = datetime.fromisoformat(record['timestamp']).strftime('%m-%d %H:%M')
            bar_len = int((price - min_price) / price_range * 30)
            bar = '█' * bar_len + '░' * (30 - bar_len)
            marker = "🟢" if price < self.threshold else " "
            print(f"{timestamp} {marker} ¥{price:>7.2f} |{bar}")
        
        print(f"\n阈值线: ¥{self.threshold:.2f} {'🟢=低于阈值'}")
        print("-" * 50)
    
    def get_statistics(self) -> Dict:
        """
        获取价格统计信息
        
        Returns:
            Dict: 统计信息字典
        """
        if not self.price_history:
            return {}
        
        prices = [record['price'] for record in self.price_history]
        return {
            'count': len(prices),
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'current_price': prices[-1],
            'threshold': self.threshold
        }
    
    def print_statistics(self) -> None:
        """打印统计信息"""
        stats = self.get_statistics()
        if not stats:
            print("[INFO] 暂无价格数据")
            return
        
        print(f"""
📊 价格统计 ({self.item_name})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
记录次数: {stats['count']}
最低价格: ¥{stats['min_price']:.2f}
最高价格: ¥{stats['max_price']:.2f}
平均价格: ¥{stats['avg_price']:.2f}
当前价格: ¥{stats['current_price']:.2f}
设定阈值: ¥{stats['threshold']:.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


def simulate_historical_data(monitor: PriceMonitor, days: int = 7) -> None:
    """
    模拟生成历史数据（用于演示）
    
    Args:
        monitor: PriceMonitor 实例
        days: 模拟天数
    """
    print(f"[INFO] 正在生成 {days} 天的模拟历史数据...")
    
    base_price = 800 if monitor.item_type == 'hotel' else 1200
    now = datetime.now()
    
    for i in range(days * 4):  # 每6小时一个数据点
        timestamp = now - timedelta(hours=i*6)
        # 添加一些随机波动和趋势
        trend = -0.02 * i  # 轻微下降趋势
        noise = random.uniform(-0.1, 0.1)
        price = base_price * (1 + trend + noise)
        
        record = {
            'timestamp': timestamp.isoformat(),
            'price': round(price, 2),
            'threshold': monitor.threshold,
            'alert': price < monitor.threshold
        }
        monitor.price_history.insert(0, record)
    
    monitor._save_history()
    print(f"[INFO] 已生成 {len(monitor.price_history)} 条历史记录")


def main():
    """
    主函数 - 演示价格监控功能
    """
    print("=" * 50)
    print("🚀 价格监控系统演示")
    print("=" * 50)
    
    # 示例1: 监控酒店价格
    print("\n【示例1】酒店价格监控")
    print("-" * 50)
    
    hotel_monitor = PriceMonitor(
        item_type='hotel',
        item_name='昆明翠湖宾馆',
        threshold=700.0
    )
    
    # 生成模拟历史数据
    simulate_historical_data(hotel_monitor, days=5)
    
    # 检查当前价格
    current_price, is_low = hotel_monitor.check_price()
    print(f"当前价格: ¥{current_price:.2f}")
    
    if is_low:
        print(hotel_monitor.generate_alert(current_price))
    else:
        print(f"[INFO] 当前价格高于阈值 (¥{hotel_monitor.threshold:.2f})")
    
    # 打印统计信息
    hotel_monitor.print_statistics()
    
    # 生成趋势图
    chart_file = hotel_monitor.generate_trend_chart()
    
    # 示例2: 监控机票价格
    print("\n【示例2】机票价格监控")
    print("-" * 50)
    
    flight_monitor = PriceMonitor(
        item_type='flight',
        item_name='北京-昆明航班',
        threshold=1000.0
    )
    
    simulate_historical_data(flight_monitor, days=3)
    
    current_price, is_low = flight_monitor.check_price()
    print(f"当前价格: ¥{current_price:.2f}")
    
    if is_low:
        print(flight_monitor.generate_alert(current_price))
    
    flight_monitor.print_statistics()
    flight_chart = flight_monitor.generate_trend_chart()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print(f"📁 生成的文件:")
    print(f"   - 酒店历史数据: {hotel_monitor.history_file}")
    print(f"   - 酒店趋势图: {chart_file}")
    print(f"   - 机票历史数据: {flight_monitor.history_file}")
    print(f"   - 机票趋势图: {flight_chart}")
    print("=" * 50)


if __name__ == '__main__':
    main()
