"""
流程配置验证器

该模块提供流程配置的验证功能，包括：
1. 孤岛节点检测
2. 死循环检测（包括if判断节点的特殊处理）
3. 输入输出验证
4. 流程完整性检查

支持以下节点类型：
- 开始节点 (type: "start")
- 结束节点 (type: "end")
- 任务节点 (type: "task")
- if判断节点 (type: "if")
"""

from typing import Dict, List, Optional, Set, Tuple, Union, Any
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict, deque


class NodeType(str, Enum):
    """节点类型枚举"""
    START = "start"
    END = "end"
    TASK = "task"
    IF = "if"


@dataclass
class OutgoingEdge:
    """出边定义"""
    resource_id: str
    conditional: Optional[str] = None  # 仅if节点使用


@dataclass
class WorkflowNode:
    """工作流节点定义"""
    resource_id: str
    node_type: NodeType
    outgoings: List[OutgoingEdge]
    
    def __post_init__(self):
        """验证节点数据"""
        if not self.resource_id:
            raise ValueError("节点必须包含resource_id")
        
        if not isinstance(self.node_type, NodeType):
            self.node_type = NodeType(self.node_type)
        
        # 验证outgoings
        if not isinstance(self.outgoings, list):
            raise ValueError("outgoings必须是列表")
        
        # 转换outgoings列表
        converted_outgoings = []
        for outgoing in self.outgoings:
            if isinstance(outgoing, OutgoingEdge):
                converted_outgoings.append(outgoing)
            elif isinstance(outgoing, dict):
                # 从字典创建OutgoingEdge，只提取需要的字段
                resource_id = outgoing.get("resource_id")
                conditional = outgoing.get("conditional")
                
                if not resource_id:
                    raise ValueError("outgoing必须包含resource_id")
                
                converted_outgoings.append(OutgoingEdge(
                    resource_id=resource_id,
                    conditional=conditional
                ))
            else:
                raise ValueError(f"无效的outgoing格式: {outgoing}")
        
        # 替换原始outgoings
        self.outgoings = converted_outgoings
        
        # 验证转换后的outgoings
        for outgoing in self.outgoings:
            # if节点必须有conditional表达式
            if self.node_type == NodeType.IF and outgoing.conditional is None:
                raise ValueError("if节点的outgoing必须包含conditional表达式")
            
            # 非if节点不能有conditional
            if self.node_type != NodeType.IF and outgoing.conditional is not None:
                raise ValueError("非if节点的outgoing不能包含conditional表达式")


class WorkflowValidator:
    """工作流验证器"""
    
    def __init__(self, nodes: List[Union[WorkflowNode, Dict[str, Any]]]):
        """
        初始化验证器
        
        Args:
            nodes: 节点列表，可以是WorkflowNode对象或字典
        """
        self.nodes: Dict[str, WorkflowNode] = {}
        self.graph: Dict[str, List[str]] = defaultdict(list)  # 邻接表
        self.reverse_graph: Dict[str, List[str]] = defaultdict(list)  # 反向邻接表
        self.node_types: Dict[str, NodeType] = {}
        
        # 转换节点为WorkflowNode对象
        for node_data in nodes:
            if isinstance(node_data, dict):
                node = WorkflowNode(**node_data)
            else:
                node = node_data
            
            self.nodes[node.resource_id] = node
            self.node_types[node.resource_id] = node.node_type
            
            # 构建图
            for outgoing in node.outgoings:
                self.graph[node.resource_id].append(outgoing.resource_id)
                self.reverse_graph[outgoing.resource_id].append(node.resource_id)
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        验证整个工作流
        
        Returns:
            Tuple[bool, List[str]]: (是否有效, 错误消息列表)
        """
        errors = []
        
        # 1. 检查基本结构
        errors.extend(self._validate_basic_structure())
        
        # 2. 检查孤岛节点
        errors.extend(self._find_isolated_nodes())
        
        # 3. 检查死循环
        errors.extend(self._find_cycles())
        
        # 4. 检查输入输出
        errors.extend(self._validate_input_output())
        
        # 5. 检查if节点特殊规则
        errors.extend(self._validate_if_nodes())
        
        return len(errors) == 0, errors
    
    def _validate_basic_structure(self) -> List[str]:
        """验证基本结构"""
        errors = []
        
        # 检查是否有节点
        if not self.nodes:
            errors.append("工作流不能为空")
            return errors
        
        # 检查是否有开始节点
        start_nodes = [node_id for node_id, node_type in self.node_types.items() 
                      if node_type == NodeType.START]
        if not start_nodes:
            errors.append("工作流必须包含至少一个开始节点")
        elif len(start_nodes) > 1:
            errors.append(f"工作流只能有一个开始节点，找到 {len(start_nodes)} 个")
        
        # 检查是否有结束节点
        end_nodes = [node_id for node_id, node_type in self.node_types.items() 
                    if node_type == NodeType.END]
        if not end_nodes:
            errors.append("工作流必须包含至少一个结束节点")
        
        # 检查节点ID唯一性
        if len(self.nodes) != len(set(self.nodes.keys())):
            errors.append("节点ID必须唯一")
        
        return errors
    
    def _find_isolated_nodes(self) -> List[str]:
        """查找孤岛节点（无法从开始节点到达或无法到达结束节点）"""
        errors = []
        
        # 找到开始节点
        start_nodes = [node_id for node_id, node_type in self.node_types.items() 
                      if node_type == NodeType.START]
        if not start_nodes:
            return errors  # 基本结构验证会处理这个错误
        
        start_node = start_nodes[0]
        
        # BFS遍历从开始节点可达的所有节点
        visited = set()
        queue = deque([start_node])
        
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            
            visited.add(current)
            
            # 添加所有出边节点
            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)
        
        # 找到不可达的节点
        unreachable_nodes = set(self.nodes.keys()) - visited
        if unreachable_nodes:
            errors.append(f"存在孤岛节点（无法从开始节点到达）: {', '.join(unreachable_nodes)}")
        
        return errors
    
    def _find_cycles(self) -> List[str]:
        """查找死循环（使用DFS检测环）"""
        errors = []
        
        # 使用DFS检测环
        visited = set()
        recursion_stack = set()
        
        def dfs(node_id: str, path: List[str]) -> bool:
            """深度优先搜索检测环"""
            if node_id in recursion_stack:
                # 找到环
                cycle_start = path.index(node_id)
                cycle = path[cycle_start:] + [node_id]
                errors.append(f"检测到死循环: {' -> '.join(cycle)}")
                return True
            
            if node_id in visited:
                return False
            
            visited.add(node_id)
            recursion_stack.add(node_id)
            path.append(node_id)
            
            has_cycle = False
            for neighbor in self.graph.get(node_id, []):
                if dfs(neighbor, path.copy()):
                    has_cycle = True
            
            recursion_stack.remove(node_id)
            path.pop()
            return has_cycle
        
        # 从每个未访问的节点开始DFS
        for node_id in self.nodes.keys():
            if node_id not in visited:
                dfs(node_id, [])
        
        return errors
    
    def _validate_input_output(self) -> List[str]:
        """验证节点的输入输出"""
        errors = []
        
        for node_id, node in self.nodes.items():
            # 开始节点不能有输入
            if node.node_type == NodeType.START:
                if node_id in self.reverse_graph and self.reverse_graph[node_id]:
                    errors.append(f"开始节点 '{node_id}' 不能有输入边")
            
            # 结束节点不能有输出
            if node.node_type == NodeType.END:
                if node_id in self.graph and self.graph[node_id]:
                    errors.append(f"结束节点 '{node_id}' 不能有输出边")
            
            # 普通节点和if节点必须有输入（除了开始节点）
            if node.node_type in [NodeType.TASK, NodeType.IF]:
                if node_id not in self.reverse_graph or not self.reverse_graph[node_id]:
                    errors.append(f"节点 '{node_id}' 没有输入边")
            
            # 所有节点（除了结束节点）必须有输出
            if node.node_type != NodeType.END:
                if node_id not in self.graph or not self.graph[node_id]:
                    errors.append(f"节点 '{node_id}' 没有输出边")
        
        return errors
    
    def _validate_if_nodes(self) -> List[str]:
        """验证if节点的特殊规则"""
        errors = []
        
        for node_id, node in self.nodes.items():
            if node.node_type == NodeType.IF:
                # if节点必须有至少两个出边
                if len(node.outgoings) < 2:
                    errors.append(f"if节点 '{node_id}' 必须有至少两个出边（true/false分支）")
                
                # 检查conditional表达式
                conditionals = [outgoing.conditional for outgoing in node.outgoings 
                              if outgoing.conditional is not None]
                
                # 应该至少有一个true和一个false条件
                if len(conditionals) != len(node.outgoings):
                    errors.append(f"if节点 '{node_id}' 的所有出边都必须有conditional表达式")
                
                # 检查条件表达式是否有效（简单检查）
                for outgoing in node.outgoings:
                    if outgoing.conditional and not self._is_valid_conditional(outgoing.conditional):
                        errors.append(f"if节点 '{node_id}' 的conditional表达式无效: {outgoing.conditional}")
        
        return errors
    
    def _is_valid_conditional(self, expression: str) -> bool:
        """
        简单验证conditional表达式
        
        Args:
            expression: 条件表达式
            
        Returns:
            bool: 表达式是否有效
        """
        # 这里实现一个简单的表达式验证
        # 实际应用中可能需要更复杂的解析器
        if not expression:
            return False
        
        # 检查基本语法
        try:
            # 简单检查：是否包含常见的比较运算符
            operators = ['==', '!=', '>', '<', '>=', '<=', '&&', '||']
            has_operator = any(op in expression for op in operators)
            
            # 检查括号匹配
            stack = []
            for char in expression:
                if char == '(':
                    stack.append(char)
                elif char == ')':
                    if not stack:
                        return False
                    stack.pop()
            
            return has_operator and len(stack) == 0
        except:
            return False
    
    def get_reachable_paths(self) -> List[List[str]]:
        """
        获取所有从开始节点到结束节点的可达路径
        
        Returns:
            List[List[str]]: 所有可达路径
        """
        paths = []
        
        # 找到开始和结束节点
        start_nodes = [node_id for node_id, node_type in self.node_types.items() 
                      if node_type == NodeType.START]
        end_nodes = [node_id for node_id, node_type in self.node_types.items() 
                    if node_type == NodeType.END]
        
        if not start_nodes or not end_nodes:
            return paths
        
        start_node = start_nodes[0]
        
        def dfs(current: str, path: List[str], visited: Set[str]):
            """深度优先搜索所有路径"""
            if current in visited:
                return
            
            new_path = path + [current]
            visited.add(current)
            
            if current in end_nodes:
                paths.append(new_path.copy())
            else:
                for neighbor in self.graph.get(current, []):
                    dfs(neighbor, new_path, visited.copy())
        
        dfs(start_node, [], set())
        return paths
    
    def visualize_graph(self) -> str:
        """
        生成图的文本可视化
        
        Returns:
            str: 图的文本表示
        """
        lines = []
        lines.append("工作流图结构:")
        lines.append("=" * 50)
        
        for node_id, node in self.nodes.items():
            node_type_str = node.node_type.value
            outgoing_str = ", ".join([
                f"{edge.resource_id}" + 
                (f" [{edge.conditional}]" if edge.conditional else "")
                for edge in node.outgoings
            ])
            lines.append(f"{node_id} ({node_type_str}) -> [{outgoing_str}]")
        
        lines.append("=" * 50)
        return "\n".join(lines)


# 便捷函数
def validate_workflow(nodes: List[Union[WorkflowNode, Dict[str, Any]]]) -> Tuple[bool, List[str]]:
    """
    验证工作流的便捷函数
    
    Args:
        nodes: 节点列表
        
    Returns:
        Tuple[bool, List[str]]: (是否有效, 错误消息列表)
    """
    validator = WorkflowValidator(nodes)
    return validator.validate()


def create_example_workflow() -> List[Dict[str, Any]]:
    """创建示例工作流"""
    return [
        {
            "resource_id": "start",
            "node_type": "start",
            "outgoings": [{"resource_id": "task1"}]
        },
        {
            "resource_id": "task1",
            "node_type": "task",
            "outgoings": [{"resource_id": "if1"}]
        },
        {
            "resource_id": "if1",
            "node_type": "if",
            "outgoings": [
                {"resource_id": "task2", "conditional": "condition == true"},
                {"resource_id": "task3", "conditional": "condition == false"}
            ]
        },
        {
            "resource_id": "task2",
            "node_type": "task",
            "outgoings": [{"resource_id": "end"}]
        },
        {
            "resource_id": "task3",
            "node_type": "task",
            "outgoings": [{"resource_id": "end"}]
        },
        {
            "resource_id": "end",
            "node_type": "end",
            "outgoings": []
        }
    ]


if __name__ == "__main__":
    # 示例用法
    print("工作流验证器示例")
    print("=" * 50)
    
    # 创建示例工作流
    example_nodes = create_example_workflow()
    
    # 创建验证器
    validator = WorkflowValidator(example_nodes)
    
    # 可视化图
    print(validator.visualize_graph())
    print()
    
    # 验证工作流
    is_valid, errors = validator.validate()
    
    if is_valid:
        print("✅ 工作流验证通过！")
        
        # 显示可达路径
        paths = validator.get_reachable_paths()
        print(f"\n找到 {len(paths)} 条从开始到结束的路径:")
        for i, path in enumerate(paths, 1):
            print(f"  路径 {i}: {' -> '.join(path)}")
    else:
        print("❌ 工作流验证失败！")
        print("\n错误信息:")
        for error in errors:
            print(f"  - {error}")