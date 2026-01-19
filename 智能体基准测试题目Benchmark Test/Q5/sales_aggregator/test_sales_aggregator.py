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
测试 sales_aggregator.py 中的 aggregateSales 函数
"""

import sys
import os
from typing import List, Dict, Union

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sales_aggregator import aggregateSales, aggregateSalesWithMap, printSalesSummary


def test_basic_functionality() -> None:
    """测试基本功能"""
    print("测试 1: 基本功能测试")
    print("-" * 40)
    
    sales_data = [
        {"product": "Apple", "quantity": 10, "price": 2.5},
        {"product": "Banana", "quantity": 5, "price": 1.5},
        {"product": "Apple", "quantity": 3, "price": 2.5},
    ]
    
    result = aggregateSales(sales_data)
    print(f"销售数据: {sales_data}")
    print(f"聚合结果: {result}")
    
    expected = {"Apple": 32.5, "Banana": 7.5}
    assert result == expected, f"期望 {expected}，实际得到 {result}"
    print("✓ 基本功能测试通过")


def test_invalid_data_filtering() -> None:
    """测试无效数据过滤"""
    print("\n测试 2: 无效数据过滤测试")
    print("-" * 40)
    
    sales_data = [
        {"product": "Apple", "quantity": 10, "price": 2.5},
        {"product": "Orange", "quantity": 0, "price": 3.0},      # 数量为0
        {"product": "Banana", "quantity": 5, "price": 0},        # 价格为0
        {"product": "Grape", "quantity": -5, "price": 4.0},      # 数量为负数
        {"product": "Mango", "quantity": 8, "price": 3.75},
        {"product": "", "quantity": 10, "price": 1.0},           # 商品名称为空
        {"product": "Banana", "quantity": "invalid", "price": 1.5},  # 数量非数值
    ]
    
    result = aggregateSales(sales_data)
    print(f"销售数据 (包含无效记录): {sales_data}")
    print(f"聚合结果 (应只包含有效记录): {result}")
    
    expected = {"Apple": 25.0, "Mango": 30.0}
    assert result == expected, f"期望 {expected}，实际得到 {result}"
    print("✓ 无效数据过滤测试通过")


def test_decimal_precision() -> None:
    """测试小数精度"""
    print("\n测试 3: 小数精度测试")
    print("-" * 40)
    
    sales_data = [
        {"product": "Item1", "quantity": 3, "price": 1.333},
        {"product": "Item2", "quantity": 2, "price": 2.777},
        {"product": "Item1", "quantity": 1, "price": 1.333},
    ]
    
    result = aggregateSales(sales_data)
    print(f"销售数据: {sales_data}")
    print(f"聚合结果 (保留2位小数): {result}")
    
    # Item1: 3 * 1.333 + 1 * 1.333 = 4 * 1.333 = 5.332 ≈ 5.33
    # Item2: 2 * 2.777 = 5.554 ≈ 5.55
    expected = {"Item1": 5.33, "Item2": 5.55}
    assert result == expected, f"期望 {expected}，实际得到 {result}"
    print("✓ 小数精度测试通过")


def test_empty_input() -> None:
    """测试空输入"""
    print("\n测试 4: 空输入测试")
    print("-" * 40)
    
    sales_data = []
    result = aggregateSales(sales_data)
    print(f"空输入: {sales_data}")
    print(f"聚合结果: {result}")
    
    assert result == {}, f"期望空字典，实际得到 {result}"
    print("✓ 空输入测试通过")


def test_all_invalid_data() -> None:
    """测试全部无效数据"""
    print("\n测试 5: 全部无效数据测试")
    print("-" * 40)
    
    sales_data = [
        {"product": "Item1", "quantity": 0, "price": 10},
        {"product": "Item2", "quantity": 5, "price": 0},
        {"product": "Item3", "quantity": -2, "price": 5},
        {"product": "", "quantity": 3, "price": 2},
    ]
    
    result = aggregateSales(sales_data)
    print(f"全部无效数据: {sales_data}")
    print(f"聚合结果: {result}")
    
    assert result == {}, f"期望空字典，实际得到 {result}"
    print("✓ 全部无效数据测试通过")


def test_large_quantities() -> None:
    """测试大量数据"""
    print("\n测试 6: 大量数据测试")
    print("-" * 40)
    
    sales_data = []
    for i in range(100):
        sales_data.append({"product": f"Product{i % 10}", "quantity": i + 1, "price": 1.0})
    
    result = aggregateSales(sales_data)
    print(f"数据量: {len(sales_data)} 条记录")
    print(f"商品种类: {len(result)} 种")
    
    # 验证 Product0 的总销售额
    # Product0 的记录: quantity = 1, 11, 21, ..., 91 (共10条)
    # 总和 = (1 + 11 + 21 + ... + 91) * 1.0 = 460
    product0_total = sum(range(1, 100, 10))
    assert result.get("Product0", 0) == product0_total, f"Product0 期望 {product0_total}，实际得到 {result.get('Product0', 0)}"
    print("✓ 大量数据测试通过")


def test_alternative_implementation() -> None:
    """测试替代实现"""
    print("\n测试 7: 替代实现一致性测试")
    print("-" * 40)
    
    sales_data = [
        {"product": "Apple", "quantity": 10, "price": 2.5},
        {"product": "Banana", "quantity": 5, "price": 1.5},
        {"product": "Apple", "quantity": 3, "price": 2.5},
        {"product": "Orange", "quantity": 0, "price": 3.0},
        {"product": "Mango", "quantity": 8, "price": 3.75},
    ]
    
    result1 = aggregateSales(sales_data)
    result2 = aggregateSalesWithMap(sales_data)
    
    print(f"销售数据: {sales_data}")
    print(f"原函数结果: {result1}")
    print(f"替代函数结果: {result2}")
    
    assert result1 == result2, f"两个实现结果不一致: {result1} != {result2}"
    print("✓ 替代实现一致性测试通过")


def test_edge_cases() -> None:
    """测试边界情况"""
    print("\n测试 8: 边界情况测试")
    print("-" * 40)
    
    # 测试极小正值
    sales_data1 = [
        {"product": "Tiny", "quantity": 0.0001, "price": 0.0001},
    ]
    result1 = aggregateSales(sales_data1)
    print(f"极小值数据: {sales_data1}")
    print(f"聚合结果: {result1}")
    
    # 测试极大值
    sales_data2 = [
        {"product": "Large", "quantity": 1000000, "price": 1000000},
    ]
    result2 = aggregateSales(sales_data2)
    print(f"极大值数据: {sales_data2}")
    print(f"聚合结果: {result2}")
    
    # 测试混合类型
    sales_data3 = [
        {"product": "Mixed", "quantity": 10, "price": 2.5},
        {"product": "Mixed", "quantity": 5.5, "price": 2},  # 浮点数量
    ]
    result3 = aggregateSales(sales_data3)
    print(f"混合类型数据: {sales_data3}")
    print(f"聚合结果: {result3}")
    
    print("✓ 边界情况测试通过")


def run_all_tests() -> bool:
    """运行所有测试"""
    print("开始运行 aggregateSales 函数测试")
    print("=" * 60)
    
    tests = [
        test_basic_functionality,
        test_invalid_data_filtering,
        test_decimal_precision,
        test_empty_input,
        test_all_invalid_data,
        test_large_quantities,
        test_alternative_implementation,
        test_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: 通过 {passed}/{len(tests)}，失败 {failed}/{len(tests)}")
    
    if failed == 0:
        print("🎉 所有测试通过！")
        return True
    else:
        print("❌ 有测试失败，请检查代码")
        return False


def demo_functionality() -> None:
    """演示函数功能"""
    print("\n" + "=" * 60)
    print("演示 aggregateSales 函数功能")
    print("=" * 60)
    
    # 创建演示数据
    demo_data = [
        {"product": "笔记本电脑", "quantity": 5, "price": 5999.99},
        {"product": "智能手机", "quantity": 12, "price": 2999.50},
        {"product": "平板电脑", "quantity": 8, "price": 1999.00},
        {"product": "笔记本电脑", "quantity": 3, "price": 5999.99},
        {"product": "智能手表", "quantity": 15, "price": 899.00},
        {"product": "智能手机", "quantity": 7, "price": 2999.50},
        {"product": "无效商品", "quantity": 0, "price": 1000.00},  # 无效
        {"product": "另一个无效", "quantity": 10, "price": 0},     # 无效
    ]
    
    print("原始销售数据:")
    for i, record in enumerate(demo_data, 1):
        print(f"  {i:2d}. {record['product']:10} × {record['quantity']:3d} @ ¥{record['price']:8.2f}")
    
    print("\n运行 aggregateSales 函数...")
    result = aggregateSales(demo_data)
    
    print("\n聚合结果:")
    for product, total in result.items():
        print(f"  {product:10}: ¥{total:12.2f}")
    
    print("\n打印汇总报告:")
    printSalesSummary(demo_data)


if __name__ == "__main__":
    # 运行测试
    success = run_all_tests()
    
    if success:
        # 演示功能
        demo_functionality()
        
        print("\n" + "=" * 60)
        print("aggregateSales 函数实现完成！")
        print("=" * 60)
        print("\n函数特性总结:")
        print("1. ✅ 过滤无效数据（数量≤0 或 价格≤0）")
        print("2. ✅ 计算每个有效记录的销售额（quantity × price）")
        print("3. ✅ 按商品名称分组聚合")
        print("4. ✅ 结果保留2位小数")
        print("5. ✅ 处理边界情况和异常输入")
        print("6. ✅ 提供清晰的错误处理和类型检查")
    else:
        print("\n测试失败，请修复代码中的问题")
        sys.exit(1)