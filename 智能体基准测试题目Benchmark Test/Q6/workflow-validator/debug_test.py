import sys
sys.path.append('.')

from workflow_validator import WorkflowNode, NodeType, OutgoingEdge

print("测试无效的if节点")
print("=" * 50)

try:
    # 创建无效的if节点（一个outgoing缺少conditional）
    node = WorkflowNode(
        resource_id="if1",
        node_type=NodeType.IF,
        outgoings=[
            OutgoingEdge(resource_id="task1"),  # 缺少conditional
            OutgoingEdge(resource_id="task2", conditional="condition == false")
        ]
    )
    print(f"✅ 节点创建成功（但应该失败）")
    print(f"   节点: {node}")
    print(f"   outgoings: {node.outgoings}")
    
    # 检查每个outgoing的conditional
    for i, outgoing in enumerate(node.outgoings):
        print(f"   outgoing {i}: resource_id={outgoing.resource_id}, conditional={outgoing.conditional}")
        
except ValueError as e:
    print(f"✅ 正确抛出异常: {e}")
except Exception as e:
    print(f"❌ 其他异常: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("\n测试有效的if节点")

try:
    # 创建有效的if节点
    node = WorkflowNode(
        resource_id="if1",
        node_type=NodeType.IF,
        outgoings=[
            OutgoingEdge(resource_id="task1", conditional="condition == true"),
            OutgoingEdge(resource_id="task2", conditional="condition == false")
        ]
    )
    print(f"✅ 节点创建成功")
    print(f"   节点: {node}")
    
except Exception as e:
    print(f"❌ 异常: {type(e).__name__}: {e}")