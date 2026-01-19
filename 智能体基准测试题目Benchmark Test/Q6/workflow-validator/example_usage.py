"""
工作流验证器使用示例

展示如何在项目中使用工作流验证器来验证流程配置。
"""

import json
from workflow_validator import (
    WorkflowValidator, validate_workflow, WorkflowNode, NodeType, OutgoingEdge
)


def example_from_json_config():
    """示例1: 从JSON配置验证工作流"""
    print("示例1: 从JSON配置验证工作流")
    print("=" * 60)
    
    # JSON格式的工作流配置
    workflow_json = """
    {
        "nodes": [
            {
                "resource_id": "start",
                "node_type": "start",
                "outgoings": [
                    {"resource_id": "validate_input"}
                ]
            },
            {
                "resource_id": "validate_input",
                "node_type": "task",
                "outgoings": [
                    {"resource_id": "check_eligibility"}
                ]
            },
            {
                "resource_id": "check_eligibility",
                "node_type": "if",
                "outgoings": [
                    {
                        "resource_id": "process_approved",
                        "conditional": "age >= 18 && has_id == true"
                    },
                    {
                        "resource_id": "process_rejected",
                        "conditional": "age < 18 || has_id == false"
                    }
                ]
            },
            {
                "resource_id": "process_approved",
                "node_type": "task",
                "outgoings": [
                    {"resource_id": "send_approval_notification"}
                ]
            },
            {
                "resource_id": "process_rejected",
                "node_type": "task",
                "outgoings": [
                    {"resource_id": "send_rejection_notification"}
                ]
            },
            {
                "resource_id": "send_approval_notification",
                "node_type": "task",
                "outgoings": [
                    {"resource_id": "end"}
                ]
            },
            {
                "resource_id": "send_rejection_notification",
                "node_type": "task",
                "outgoings": [
                    {"resource_id": "end"}
                ]
            },
            {
                "resource_id": "end",
                "node_type": "end",
                "outgoings": []
            }
        ]
    }
    """
    
    # 解析JSON
    config = json.loads(workflow_json)
    nodes_data = config["nodes"]
    
    # 使用便捷函数验证
    is_valid, errors = validate_workflow(nodes_data)
    
    if is_valid:
        print("✅ 工作流配置有效！")
        
        # 创建验证器获取更多信息
        validator = WorkflowValidator(nodes_data)
        
        # 显示图结构
        print("\n工作流结构:")
        print(validator.visualize_graph())
        
        # 显示可达路径
        paths = validator.get_reachable_paths()
        print(f"\n从开始到结束的可达路径 ({len(paths)} 条):")
        for i, path in enumerate(paths, 1):
            print(f"  路径 {i}: {' -> '.join(path)}")
    else:
        print("❌ 工作流配置无效！")
        print("\n错误信息:")
        for error in errors:
            print(f"  - {error}")
    
    print()


def example_programmatic_creation():
    """示例2: 编程方式创建和验证工作流"""
    print("示例2: 编程方式创建和验证工作流")
    print("=" * 60)
    
    # 编程方式创建工作流节点
    nodes = [
        WorkflowNode(
            resource_id="start",
            node_type=NodeType.START,
            outgoings=[OutgoingEdge(resource_id="load_data")]
        ),
        WorkflowNode(
            resource_id="load_data",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="transform_data")]
        ),
        WorkflowNode(
            resource_id="transform_data",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="analyze_data")]
        ),
        WorkflowNode(
            resource_id="analyze_data",
            node_type=NodeType.IF,
            outgoings=[
                OutgoingEdge(
                    resource_id="generate_report",
                    conditional="data_quality >= 0.8"
                ),
                OutgoingEdge(
                    resource_id="flag_for_review",
                    conditional="data_quality < 0.8"
                )
            ]
        ),
        WorkflowNode(
            resource_id="generate_report",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="archive_results")]
        ),
        WorkflowNode(
            resource_id="flag_for_review",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="notify_team")]
        ),
        WorkflowNode(
            resource_id="archive_results",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="notify_team",
            node_type=NodeType.TASK,
            outgoings=[OutgoingEdge(resource_id="end")]
        ),
        WorkflowNode(
            resource_id="end",
            node_type=NodeType.END,
            outgoings=[]
        )
    ]
    
    # 创建验证器
    validator = WorkflowValidator(nodes)
    
    # 验证工作流
    is_valid, errors = validator.validate()
    
    if is_valid:
        print("✅ 数据处理工作流有效！")
        
        # 显示工作流信息
        print("\n工作流统计:")
        print(f"  总节点数: {len(nodes)}")
        
        node_type_count = {}
        for node in nodes:
            node_type = node.node_type.value
            node_type_count[node_type] = node_type_count.get(node_type, 0) + 1
        
        for node_type, count in node_type_count.items():
            print(f"  {node_type}节点: {count}个")
        
        print("\n工作流结构:")
        print(validator.visualize_graph())
        
    else:
        print("❌ 数据处理工作流无效！")
        print("\n错误信息:")
        for error in errors:
            print(f"  - {error}")
    
    print()


def example_error_scenarios():
    """示例3: 错误场景处理"""
    print("示例3: 错误场景处理")
    print("=" * 60)
    
    print("场景1: 包含死循环的工作流")
    print("-" * 40)
    
    cyclic_nodes = [
        {
            "resource_id": "start",
            "node_type": "start",
            "outgoings": [{"resource_id": "process"}]
        },
        {
            "resource_id": "process",
            "node_type": "task",
            "outgoings": [{"resource_id": "validate"}]
        },
        {
            "resource_id": "validate",
            "node_type": "task",
            "outgoings": [{"resource_id": "process"}]  # 指向process，形成循环
        },
        {
            "resource_id": "end",
            "node_type": "end",
            "outgoings": []
        }
    ]
    
    is_valid, errors = validate_workflow(cyclic_nodes)
    print(f"验证结果: {'有效' if is_valid else '无效'}")
    if errors:
        print("检测到的问题:")
        for error in errors:
            print(f"  - {error}")
    
    print("\n场景2: 包含孤岛节点的工作流")
    print("-" * 40)
    
    isolated_nodes = [
        {
            "resource_id": "start",
            "node_type": "start",
            "outgoings": [{"resource_id": "main_task"}]
        },
        {
            "resource_id": "main_task",
            "node_type": "task",
            "outgoings": [{"resource_id": "end"}]
        },
        {
            "resource_id": "isolated_task",
            "node_type": "task",
            "outgoings": [{"resource_id": "another_isolated"}]
        },
        {
            "resource_id": "another_isolated",
            "node_type": "task",
            "outgoings": []
        },
        {
            "resource_id": "end",
            "node_type": "end",
            "outgoings": []
        }
    ]
    
    is_valid, errors = validate_workflow(isolated_nodes)
    print(f"验证结果: {'有效' if is_valid else '无效'}")
    if errors:
        print("检测到的问题:")
        for error in errors:
            print(f"  - {error}")
    
    print("\n场景3: if节点缺少conditional表达式")
    print("-" * 40)
    
    invalid_if_nodes = [
        {
            "resource_id": "start",
            "node_type": "start",
            "outgoings": [{"resource_id": "decision"}]
        },
        {
            "resource_id": "decision",
            "node_type": "if",
            "outgoings": [
                {"resource_id": "path_a"},  # 缺少conditional
                {"resource_id": "path_b", "conditional": "value == false"}
            ]
        },
        {
            "resource_id": "path_a",
            "node_type": "task",
            "outgoings": [{"resource_id": "end"}]
        },
        {
            "resource_id": "path_b",
            "node_type": "task",
            "outgoings": [{"resource_id": "end"}]
        },
        {
            "resource_id": "end",
            "node_type": "end",
            "outgoings": []
        }
    ]
    
    try:
        is_valid, errors = validate_workflow(invalid_if_nodes)
        print(f"验证结果: {'有效' if is_valid else '无效'}")
        if errors:
            print("检测到的问题:")
            for error in errors:
                print(f"  - {error}")
    except ValueError as e:
        print(f"✅ 正确捕获到配置错误: {e}")
        print("（if节点必须在创建时就包含conditional表达式）")
    
    print()


def example_integration_with_web_api():
    """示例4: 与Web API集成"""
    print("示例4: 与Web API集成示例")
    print("=" * 60)
    
    print("假设的Web API请求/响应流程:")
    print()
    print("1. 客户端发送工作流配置到API:")
    print("   POST /api/workflows/validate")
    print("   Content-Type: application/json")
    print("   Body: { \"nodes\": [...] }")
    print()
    
    print("2. 服务器端验证代码示例:")
    print("""
    from workflow_validator import validate_workflow
    
    @app.route('/api/workflows/validate', methods=['POST'])
    def validate_workflow_api():
        try:
            data = request.get_json()
            nodes = data.get('nodes', [])
            
            # 验证工作流
            is_valid, errors = validate_workflow(nodes)
            
            if is_valid:
                return jsonify({
                    'valid': True,
                    'message': '工作流配置有效'
                }), 200
            else:
                return jsonify({
                    'valid': False,
                    'errors': errors
                }), 400
                
        except ValueError as e:
            return jsonify({
                'valid': False,
                'errors': [str(e)]
            }), 400
        except Exception as e:
            return jsonify({
                'valid': False,
                'errors': [f'服务器错误: {str(e)}']
            }), 500
    """)
    
    print()
    print("3. 客户端收到响应:")
    print("   - 如果有效: {'valid': true, 'message': '工作流配置有效'}")
    print("   - 如果无效: {'valid': false, 'errors': ['错误描述1', '错误描述2']}")
    print()


def main():
    """主函数：运行所有示例"""
    print("工作流验证器使用示例")
    print("=" * 60)
    print()
    
    # 运行所有示例
    example_from_json_config()
    example_programmatic_creation()
    example_error_scenarios()
    example_integration_with_web_api()
    
    print("=" * 60)
    print("示例运行完成！")
    print()
    print("总结:")
    print("- 工作流验证器可以验证JSON配置或编程创建的流程")
    print("- 支持检测孤岛节点、死循环、输入输出问题")
    print("- 对if节点有特殊验证规则")
    print("- 可以集成到Web API或任何Python应用中")


if __name__ == "__main__":
    main()