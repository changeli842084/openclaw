#!/usr/bin/env python3
"""
汇率转换工具 (Currency Converter)
功能：支持人民币、美元、欧元、日元、韩元之间的汇率转换
作者：Coder Agent
版本：1.0.0
"""

import sys
import argparse
from typing import Optional


class CurrencyConverter:
    """
    汇率转换器类
    提供多种货币之间的汇率转换功能
    """
    
    # 模拟汇率数据（以USD为基准）
    # 汇率更新时间：2026-03-11（模拟数据）
    EXCHANGE_RATES = {
        'USD': 1.0,      # 美元 - 基准货币
        'CNY': 0.142,    # 人民币 1 CNY = 0.142 USD
        'EUR': 1.08,     # 欧元
        'JPY': 0.0067,   # 日元
        'KRW': 0.00074,  # 韩元
    }
    
    # 货币中文名称映射
    CURRENCY_NAMES = {
        'USD': '美元',
        'CNY': '人民币',
        'EUR': '欧元',
        'JPY': '日元',
        'KRW': '韩元',
    }
    
    # 支持的货币代码
    SUPPORTED_CURRENCIES = list(EXCHANGE_RATES.keys())
    
    def __init__(self):
        """初始化汇率转换器"""
        pass
    
    def validate_currency(self, currency_code: str) -> bool:
        """
        验证货币代码是否有效
        
        Args:
            currency_code: 货币代码（如 CNY, USD）
            
        Returns:
            bool: 货币代码是否有效
        """
        return currency_code.upper() in self.SUPPORTED_CURRENCIES
    
    def validate_amount(self, amount: str) -> Optional[float]:
        """
        验证金额是否有效
        
        Args:
            amount: 金额字符串
            
        Returns:
            float: 转换后的浮点数金额，如果无效则返回 None
        """
        try:
            value = float(amount)
            if value < 0:
                return None
            return value
        except ValueError:
            return None
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        执行汇率转换
        
        Args:
            amount: 要转换的金额
            from_currency: 源货币代码
            to_currency: 目标货币代码
            
        Returns:
            float: 转换后的金额
            
        Raises:
            ValueError: 如果货币代码无效
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # 验证货币代码
        if not self.validate_currency(from_currency):
            raise ValueError(f"不支持的源货币代码: {from_currency}")
        if not self.validate_currency(to_currency):
            raise ValueError(f"不支持的目标货币代码: {to_currency}")
        
        # 获取汇率
        from_rate = self.EXCHANGE_RATES[from_currency]
        to_rate = self.EXCHANGE_RATES[to_currency]
        
        # 转换逻辑：先转为USD，再转为目标货币
        # amount * from_rate = USD金额
        # USD金额 / to_rate = 目标货币金额
        result = (amount * from_rate) / to_rate
        
        return result
    
    def get_currency_info(self, currency_code: str) -> str:
        """
        获取货币信息
        
        Args:
            currency_code: 货币代码
            
        Returns:
            str: 货币名称和代码
        """
        code = currency_code.upper()
        name = self.CURRENCY_NAMES.get(code, '未知货币')
        return f"{name}({code})"
    
    def list_supported_currencies(self) -> str:
        """
        获取支持的货币列表
        
        Returns:
            str: 格式化的货币列表字符串
        """
        currencies = []
        for code in self.SUPPORTED_CURRENCIES:
            name = self.CURRENCY_NAMES.get(code, '未知')
            rate = self.EXCHANGE_RATES[code]
            currencies.append(f"  {code}: {name} (汇率: {rate})")
        return "\n".join(currencies)


def parse_arguments():
    """
    解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(
        description='汇率转换工具 - 支持 CNY, USD, EUR, JPY, KRW',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python currency_converter.py 100 CNY USD    # 100人民币转美元
  python currency_converter.py 50 USD EUR     # 50美元转欧元
  python currency_converter.py --list         # 显示支持的货币列表
        '''
    )
    
    parser.add_argument(
        'amount',
        nargs='?',
        help='要转换的金额'
    )
    
    parser.add_argument(
        'from_currency',
        nargs='?',
        help='源货币代码 (如: CNY, USD, EUR, JPY, KRW)'
    )
    
    parser.add_argument(
        'to_currency',
        nargs='?',
        help='目标货币代码 (如: CNY, USD, EUR, JPY, KRW)'
    )
    
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='显示支持的货币列表'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    
    return parser.parse_args()


def main():
    """
    主函数 - 程序入口
    """
    # 创建转换器实例
    converter = CurrencyConverter()
    
    # 解析命令行参数
    args = parse_arguments()
    
    # 如果请求显示货币列表
    if args.list:
        print("支持的货币列表：")
        print(converter.list_supported_currencies())
        print("\n注：汇率为模拟数据，以USD为基准")
        return 0
    
    # 检查必需参数
    if not args.amount or not args.from_currency or not args.to_currency:
        print("错误：缺少必需参数")
        print("用法: python currency_converter.py <金额> <源货币> <目标货币>")
        print("      python currency_converter.py --list  # 查看支持的货币")
        return 1
    
    # 验证金额
    amount = converter.validate_amount(args.amount)
    if amount is None:
        print(f"错误：无效金额 '{args.amount}'。请输入一个非负数。")
        return 1
    
    # 验证货币代码
    from_currency = args.from_currency.upper()
    to_currency = args.to_currency.upper()
    
    if not converter.validate_currency(from_currency):
        print(f"错误：不支持的源货币代码 '{from_currency}'")
        print(f"支持的货币: {', '.join(converter.SUPPORTED_CURRENCIES)}")
        return 1
    
    if not converter.validate_currency(to_currency):
        print(f"错误：不支持的目标货币代码 '{to_currency}'")
        print(f"支持的货币: {', '.join(converter.SUPPORTED_CURRENCIES)}")
        return 1
    
    # 执行转换
    try:
        result = converter.convert(amount, from_currency, to_currency)
        
        # 格式化输出
        if args.verbose:
            print(f"汇率转换详情：")
            print(f"  源货币: {converter.get_currency_info(from_currency)}")
            print(f"  目标货币: {converter.get_currency_info(to_currency)}")
            print(f"  转换金额: {amount}")
            print(f"  转换结果: {result:.2f}")
            print(f"\n{amount} {from_currency} = {result:.2f} {to_currency}")
        else:
            print(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        
        return 0
        
    except ValueError as e:
        print(f"转换错误: {e}")
        return 1
    except Exception as e:
        print(f"未知错误: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
