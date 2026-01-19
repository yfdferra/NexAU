"""
工作流验证器测试

测试各种工作流场景，包括：
1. 有效工作流
2. 孤岛节点
3. 死循环
4. 无效的输入输出
5. if节点特殊规则
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflow_validator import (
    WorkflowValidator, validate_workflow, WorkflowNode, NodeType, OutgoingEdge
)


def test_valid_workflow():
    """测试有效的工作流"""
    print("测试 1: 有效的工作流")
    print("-" * 40)
    
    nodes = [
        WorkflowNode(
            resource_id="start",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="task1")]
        ),
        WorkflowNode(
            resource_id="task1",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="if1")]
        ),
        WorkflowNode(
            resource_id="if1",
            node_type=NodeType.IF,
            outgoings=[
                OutgoingEdge(resource_id="task2", conditional="score > 60"),
                OutgoingEdge(resource_id="task3", conditional="score <= 60")
            ]
        ),
        WorkflowNode(
            resource_id="task2",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="task3",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="end",
            node_type=NodeType.END,
            outgoings=[]
        )
    ]
    
    validator = WorkflowValidator(nodes)
    is_valid, errors = validator.validate()
    
    print(f"验证结果: {'通过' if is_valid else '失败'}")
    if errors:
        print("错误信息:")
        for error in errors:
            print(f"  - {error}")
    
    print(f"图可视化:\n{validator.visualize_graph()}")
    
    paths = validator.get_reachable_paths()
    print(f"\n可达路径 ({len(paths)} 条):")
    for i, path in enumerate(paths, 1):
        print(f"  路径 {i}: {' -> '.join(path)}")
    
    print()
    return is_valid


def test_isolated_nodes():
    """测试孤岛节点"""
    print("测试 2: 孤岛节点检测")
    print("-" * 40)
    
    nodes = [
        WorkflowNode(
            resource_id="start",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="task1")]
        ),
        WorkflowNode(
            resource_id="task1",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="isolated_task",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="another_isolated")]
        ),
        WorkflowNode(
            resource_id="another_isolated",
            node_type=NodeType.TASK,
            outgoings=[]
        ),
        WorkflowNode(
            resource_id="end",
            node_type=NodeType.END,
            outgoings=[]
        )
    ]
    
    validator = WorkflowValidator(nodes)
    is_valid, errors = validator.validate()
    
    print(f"验证结果: {'通过' if is_valid else '失败'}")
    print("错误信息:")
    for error in errors:
        print(f"  - {error}")
    
    print(f"\n图可视化:\n{validator.visualize_graph()}")
    print()
    return not is_valid  # 应该失败


def test_cycle_detection():
    """测试死循环检测"""
    print("测试 3: 死循环检测")
    print("-" * 40)
    
    nodes = [
        WorkflowNode(
            resource_id="start",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="task1")]
        ),
        WorkflowNode(
            resource_id="task1",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="task2")]
        ),
        WorkflowNode(
            resource_id="task2",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="task3")]
        ),
        WorkflowNode(
            resource_id="task3",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="task1")]  # 形成循环
        ),
        WorkflowNode(
            resource_id="end",
            node_type=NodeType.END,
            outgoings=[]
        )
    ]
    
    validator = WorkflowValidator(nodes)
    is_valid, errors = validator.validate()
    
    print(f"验证结果: {'通过' if is_valid else '失败'}")
    print("错误信息:")
    for error in errors:
        print(f"  - {error}")
    
    print(f"\n图可视化:\n{validator.visualize_graph()}")
    print()
    return not is_valid  # 应该失败


def test_if_node_cycle():
    """测试if节点的死循环"""
    print("测试 4: if节点的死循环")
    print("-" * 40)
    
    nodes = [
        WorkflowNode(
            resource_id="start",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="if1")]
        ),
        WorkflowNode(
            resource_id="if1",
            node_type=NodeType.IF,
            outgoings=[
                OutgoingEdge(resource_id="task1", conditional="condition == true"),
                OutgoingEdge(resource_id="if1", conditional="condition == false")  # 指向自己
            ]
        ),
        WorkflowNode(
            resource_id="task1",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="end",
            node_type=NodeType.END,
            outgoings=[]
        )
    ]
    
    validator = WorkflowValidator(nodes)
    is_valid, errors = validator.validate()
    
    print(f"验证结果: {'通过' if is_valid else '失败'}")
    print("错误信息:")
    for error in errors:
        print(f"  - {error}")
    
    print(f"\n图可视化:\n{validator.visualize_graph()}")
    print()
    return not is_valid  # 应该失败


def test_invalid_if_node():
    """测试无效的if节点"""
    print("测试 5: 无效的if节点")
    print("-" * 40)
    
    try:
        nodes = [
            WorkflowNode(
                resource_id="start",
                node_type=NodeType.START,
                outgoings=[OutgoingEdge(resource_id="if1")]
            ),
            WorkflowNode(
                resource_id="if1",
                node_type=NodeType.IF,
                outgoings=[
                    OutgoingEdge(resource_id="task1"),  # 缺少conditional
                    OutgoingEdge(resource_id="task2", conditional="condition == false")
                ]
            ),
            WorkflowNode(
                resource_id="task1",
                node_type=NodeType.TASK,
                outgoings=[OutgoingEdge(resource_id="end")]
            ),
            WorkflowNode(
                resource_id="task2",
                node_type=NodeType.TASK,
                outgoings=[OutgoingEdge(resource_id="end")]
            ),
            WorkflowNode(
                resource_id="end",
                node_type=NodeType.END,
                outgoings=[]
            )
        ]
        
        validator = WorkflowValidator(nodes)
        is_valid, errors = validator.validate()
        
        print(f"验证结果: {'通过' if is_valid else '失败'}")
        print("错误信息:")
        for error in errors:
            print(f"  - {error}")
        
        print(f"\n图可视化:\n{validator.visualize_graph()}")
        print()
        return not is_valid  # 应该失败
        
    except ValueError as e:
        print(f"✅ 正确捕获到节点创建异常: {e}")
        print("（if节点缺少conditional表达式，在创建时就被验证捕获）")
        print()
        return True  # 测试通过，因为异常是预期的


def test_input_output_validation():
    """测试输入输出验证"""
    print("测试 6: 输入输出验证")
    print("-" * 40)
    
    nodes = [
        WorkflowNode(
            resource_id="start",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="task1")]
        ),
        WorkflowNode(
            resource_id="task1",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="task2"), OutgoingEdge(resource_id="task3")]
        ),
        WorkflowNode(
            resource_id="task2",
            node_type=NodeType.TASK,
            outgoings=[]  # 没有输出（应该错误）
        ),
        WorkflowNode(
            resource_id="task3",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="end",
            node_type=NodeType.END,
            outgoings=[OutgoingEdge(resource_id="task4")]  # 结束节点有输出（应该错误）
        ),
        WorkflowNode(
            resource_id="task4",
            node_type=NodeType.TASK,
            outgoings=[]
        )
    ]
    
    validator = WorkflowValidator(nodes)
    is_valid, errors = validator.validate()
    
    print(f"验证结果: {'通过' if is_valid else '失败'}")
    print("错误信息:")
    for error in errors:
        print(f"  - {error}")
    
    print(f"\n图可视化:\n{validator.visualize_graph()}")
    print()
    return not is_valid  # 应该失败


def test_multiple_start_nodes():
    """测试多个开始节点"""
    print("测试 7: 多个开始节点")
    print("-" * 40)
    
    nodes = [
        WorkflowNode(
            resource_id="start1",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="task1")]
        ),
        WorkflowNode(
            resource_id="start2",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="task2")]
        ),
        WorkflowNode(
            resource_id="task1",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="task2",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="end",
            node_type=NodeType.END,
            outgoings=[]
        )
    ]
    
    validator = WorkflowValidator(nodes)
    is_valid, errors = validator.validate()
    
    print(f"验证结果: {'通过' if is_valid else '失败'}")
    print("错误信息:")
    for error in errors:
        print(f"  - {error}")
    
    print(f"\n图可视化:\n{validator.visualize_graph()}")
    print()
    return not is_valid  # 应该失败


def test_no_end_nodes():
    """测试没有结束节点"""
    print("测试 8: 没有结束节点")
    print("-" * 40)
    
    nodes = [
        WorkflowNode(
            resource_id="start",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="task1")]
        ),
        WorkflowNode(
            resource_id="task1",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="task2")]
        ),
        WorkflowNode(
            resource_id="task2",
            node_type=NodeType.TASK,
            outgoings=[]
        )
    ]
    
    validator = WorkflowValidator(nodes)
    is_valid, errors = validator.validate()
    
    print(f"验证结果: {'通过' if is_valid else '失败'}")
    print("错误信息:")
    for error in errors:
        print(f"  - {error}")
    
    print(f"\n图可视化:\n{validator.visualize_graph()}")
    print()
    return not is_valid  # 应该失败


def test_complex_valid_workflow():
    """测试复杂的有效工作流"""
    print("测试 9: 复杂的有效工作流")
    print("-" * 40)
    
    nodes = [
        WorkflowNode(
            resource_id="start",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="init")]
        ),
        WorkflowNode(
            resource_id="init",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="check_condition")]
        ),
        WorkflowNode(
            resource_id="check_condition",
            node_type=NodeType.IF,
            outgoings=[
                OutgoingEdge(resource_id="process_a", conditional="type == 'A'"),
                OutgoingEdge(resource_id="process_b", conditional="type == 'B'"),
                OutgoingEdge(resource_id="process_default", conditional="type != 'A' && type != 'B'")
            ]
        ),
        WorkflowNode(
            resource_id="process_a",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="finalize")]
        ),
        WorkflowNode(
            resource_id="process_b",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="finalize")]
        ),
        WorkflowNode(
            resource_id="process_default",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="finalize")]
        ),
        WorkflowNode(
            resource_id="finalize",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="end",
            node_type=NodeType.END,
            outgoings=[]
        )
    ]
    
    validator = WorkflowValidator(nodes)
    is_valid, errors = validator.validate()
    
    print(f"验证结果: {'通过' if is_valid else '失败'}")
    if errors:
        print("错误信息:")
        for error in errors:
            print(f"  - {error}")
    
    print(f"\n图可视化:\n{validator.visualize_graph()}")
    
    paths = validator.get_reachable_paths()
    print(f"\n可达路径 ({len(paths)} 条):")
    for i, path in enumerate(paths, 1):
        print(f"  路径 {i}: {' -> '.join(path)}")
    
    print()
    return is_valid


def test_convenience_function():
    """测试便捷函数"""
    print("测试 10: 便捷函数测试")
    print("-" * 40)
    
    nodes_dict = [
        {
            "resource_id": "start",
            "node_type": "start",
            "outgoings": [{"resource_id": "task1"}]
        },
        {
            "resource_id": "task1",
            "node_type": "task",
            "outgoings": [{"resource_id": "end"}]
        },
        {
            "resource_id": "end",
            "node_type": "end",
            "outgoings": []
        }
    ]
    
    is_valid, errors = validate_workflow(nodes_dict)
    
    print(f"使用便捷函数验证结果: {'通过' if is_valid else '失败'}")
    if errors:
        print("错误信息:")
        for error in errors:
            print(f"  - {error}")
    
    print()
    return is_valid


def run_all_tests():
    """运行所有测试"""
    print("工作流验证器测试套件")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    tests = [
        ("有效工作流", test_valid_workflow),
        ("孤岛节点检测", test_isolated_nodes),
        ("死循环检测", test_cycle_detection),
        ("if节点死循环", test_if_node_cycle),
        ("无效if节点", test_invalid_if_node),
        ("输入输出验证", test_input_output_validation),
        ("多个开始节点", test_multiple_start_nodes),
        ("没有结束节点", test_no_end_nodes),
        ("复杂有效工作流", test_complex_valid_workflow),
        ("便捷函数", test_convenience_function),
    ]
    
    for test_name, test_func in tests:
        print(f"\n运行测试: {test_name}")
        try:
            result = test_func()
            test_results.append((test_name, result))
            print(f"✓ 测试完成")
        except Exception as e:
            print(f"✗ 测试失败: {e}")
            test_results.append((test_name, False))
    
    # 打印测试总结
    print("\n" + "=" * 60)
    print("测试总结:")
    print("-" * 60)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    print(f"通过: {passed}/{total}")
    print(f"失败: {total - passed}/{total}")
    
    if total - passed > 0:
        print("\n失败的测试:")
        for test_name, result in test_results:
            if not result:
                print(f"  - {test_name}")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🎉 所有测试通过！")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败！")
        sys.exit(1)