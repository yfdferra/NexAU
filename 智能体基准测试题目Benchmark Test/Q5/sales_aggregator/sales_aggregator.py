# Copyright (c) Nex-AGI. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
销售数据聚合模块
包含 aggregateSales 函数，用于清洗和聚合销售数据
"""

from typing import List, Dict, Union


def aggregateSales(salesData: List[Dict[str, Union[str, int, float]]]) -> Dict[str, float]:
    """
    清洗销售数据并计算每种商品的销售总额
    
    参数:
        salesData: 包含订单对象的数组
            对象结构: {"product": string, "quantity": number, "price": number}
    
    逻辑处理:
        1. 过滤无效数据：忽略 quantity（数量）或 price（单价）小于等于 0 的记录
        2. 计算总额：计算每个有效记录的销售额（quantity * price）
        3. 分组聚合：将相同 product（商品名）的销售额进行累加
    
    返回:
        一个字典，键为商品名称，值为该商品的总销售额（保留2位小数）
    
    示例:
        >>> sales_data = [
        ...     {"product": "Apple", "quantity": 10, "price": 2.5},
        ...     {"product": "Banana", "quantity": 5, "price": 1.5},
        ...     {"product": "Apple", "quantity": 3, "price": 2.5},
        ...     {"product": "Orange", "quantity": 0, "price": 3.0},  # 无效数据
        ...     {"product": "Banana", "quantity": 2, "price": 0},    # 无效数据
        ... ]
        >>> result = aggregateSales(sales_data)
        >>> print(result)
        {'Apple': 32.5, 'Banana': 7.5}
    """
    # 初始化结果字典
    aggregated_sales = {}
    
    # 遍历所有销售记录
    for record in salesData:
        # 提取数据
        product = record.get("product", "")
        quantity = record.get("quantity", 0)
        price = record.get("price", 0)
        
        # 验证数据有效性
        if not product or not isinstance(product, str):
            continue  # 跳过无效的商品名称
        
        # 检查数量和价格是否有效（大于0）
        if not isinstance(quantity, (int, float)) or not isinstance(price, (int, float)):
            continue  # 跳过非数值类型
        
        if quantity <= 0 or price <= 0:
            continue  # 跳过无效的数量或价格
        
        # 计算当前记录的销售额
        sales_amount = quantity * price
        
        # 累加到对应商品的总额中
        if product in aggregated_sales:
            aggregated_sales[product] += sales_amount
        else:
            aggregated_sales[product] = sales_amount
    
    # 格式化结果，保留2位小数
    formatted_result = {
        product: round(total_amount, 2)
        for product, total_amount in aggregated_sales.items()
    }
    
    return formatted_result


def aggregateSalesWithMap(salesData: List[Dict[str, Union[str, int, float]]]) -> Dict[str, float]:
    """
    使用字典推导式和 filter 实现的 aggregateSales 函数（替代版本）
    
    参数和返回值与 aggregateSales 函数相同，但实现方式更简洁
    """
    # 使用字典推导式进行聚合
    aggregated_sales = {}
    
    # 过滤有效记录并聚合
    for record in salesData:
        product = record.get("product", "")
        quantity = record.get("quantity", 0)
        price = record.get("price", 0)
        
        # 验证数据有效性
        if (isinstance(product, str) and product and 
            isinstance(quantity, (int, float)) and quantity > 0 and 
            isinstance(price, (int, float)) and price > 0):
            
            sales_amount = quantity * price
            
            if product in aggregated_sales:
                aggregated_sales[product] += sales_amount
            else:
                aggregated_sales[product] = sales_amount
    
    # 格式化结果，保留2位小数
    return {product: round(total, 2) for product, total in aggregated_sales.items()}


def printSalesSummary(salesData: List[Dict[str, Union[str, int, float]]]) -> None:
    """
    打印销售数据汇总报告
    
    参数:
        salesData: 销售数据数组
    """
    result = aggregateSales(salesData)
    
    print("=" * 50)
    print("销售数据汇总报告")
    print("=" * 50)
    
    if not result:
        print("没有有效的销售数据")
        return
    
    total_sales = sum(result.values())
    
    print(f"商品种类: {len(result)}")
    print(f"总销售额: ¥{total_sales:.2f}")
    print("-" * 50)
    
    # 按销售额降序排序
    sorted_items = sorted(result.items(), key=lambda x: x[1], reverse=True)
    
    for product, sales in sorted_items:
        percentage = (sales / total_sales * 100) if total_sales > 0 else 0
        print(f"{product:<15} ¥{sales:>10.2f} ({percentage:>5.1f}%)")
    
    print("=" * 50)


if __name__ == "__main__":
    # 示例数据
    sample_sales_data = [
        {"product": "Apple", "quantity": 10, "price": 2.5},
        {"product": "Banana", "quantity": 5, "price": 1.5},
        {"product": "Apple", "quantity": 3, "price": 2.5},
        {"product": "Orange", "quantity": 0, "price": 3.0},  # 无效数据：数量为0
        {"product": "Banana", "quantity": 2, "price": 0},    # 无效数据：价格为0
        {"product": "Grape", "quantity": -5, "price": 4.0},  # 无效数据：数量为负数
        {"product": "Mango", "quantity": 8, "price": 3.75},
        {"product": "Apple", "quantity": 2, "price": 2.8},
        {"product": "Mango", "quantity": 3, "price": 3.75},
        {"product": "", "quantity": 10, "price": 1.0},       # 无效数据：商品名称为空
        {"product": "Banana", "quantity": "invalid", "price": 1.5},  # 无效数据：数量非数值
    ]
    
    # 测试基本功能
    print("测试 aggregateSales 函数:")
    print("-" * 40)
    
    result = aggregateSales(sample_sales_data)
    print(f"聚合结果: {result}")
    
    # 验证结果
    expected_apple = (10 * 2.5) + (3 * 2.5) + (2 * 2.8)  # 25 + 7.5 + 5.6 = 38.1
    expected_banana = 5 * 1.5  # 7.5
    expected_mango = (8 * 3.75) + (3 * 3.75)  # 30 + 11.25 = 41.25
    
    print(f"\n验证计算:")
    print(f"Apple 总额: {result.get('Apple', 0):.2f} (期望: {expected_apple:.2f})")
    print(f"Banana 总额: {result.get('Banana', 0):.2f} (期望: {expected_banana:.2f})")
    print(f"Mango 总额: {result.get('Mango', 0):.2f} (期望: {expected_mango:.2f})")
    
    # 测试替代版本
    print(f"\n测试 aggregateSalesWithMap 函数:")
    print("-" * 40)
    
    result2 = aggregateSalesWithMap(sample_sales_data)
    print(f"聚合结果: {result2}")
    
    # 打印汇总报告
    print(f"\n打印销售汇总报告:")
    print("-" * 40)
    printSalesSummary(sample_sales_data)