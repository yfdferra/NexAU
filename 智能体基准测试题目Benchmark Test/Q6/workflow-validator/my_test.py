from typing import Dict, List, Optional, Set, Tuple, Union, Any
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict, deque

# ==========================================
# 1. EDIT YOUR WORKFLOW HERE
# ==========================================
""" my_workflow = [
    {
        "resource_id": "start_node",
        "node_type": "start",
        "outgoings": [{"resource_id": "task_1"}]
    },
    {
        "resource_id": "task_1",
        "node_type": "task",
        "outgoings": [{"resource_id": "decision_node"}]
    },
    {
        "resource_id": "decision_node",
        "node_type": "if",
        "outgoings": [
            {"resource_id": "path_a", "conditional": "score > 50"},
            {"resource_id": "path_b", "conditional": "score <= 50"}
        ]
    },
    {
        "resource_id": "path_a",
        "node_type": "task",
        "outgoings": [{"resource_id": "end_node"}]
    },
    {
        "resource_id": "path_b",
        "node_type": "task",
        "outgoings": [{"resource_id": "end_node"}]
    },
    {
        "resource_id": "end_node",
        "node_type": "end",
        "outgoings": []
    }
] """

my_workflow = [
    {"resource_id": "start", "node_type": "start", "outgoings": [{"resource_id": "task_1"}]},
    {"resource_id": "task_1", "node_type": "task", "outgoings": [{"resource_id": "task_2"}]},
    {"resource_id": "task_2", "node_type": "task", "outgoings": [{"resource_id": "task_1"}]}, # Cycle here
    {"resource_id": "end", "node_type": "end", "outgoings": []}
]


""" my_workflow = [
    {"resource_id": "start", "node_type": "start", "outgoings": [{"resource_id": "decision"}]},
    {
        "resource_id": "decision",
        "node_type": "if",
        "outgoings": [
            {"resource_id": "path_a"}, # Error: Missing 'conditional' [cite: 35, 110]
            {"resource_id": "path_b", "conditional": "x < 0"}
        ]
    },
    {"resource_id": "path_a", "node_type": "task", "outgoings": [{"resource_id": "end"}]},
    {"resource_id": "path_b", "node_type": "task", "outgoings": [{"resource_id": "end"}]},
    {"resource_id": "end", "node_type": "end", "outgoings": []}
] """

# ==========================================
# 2. CORE VALIDATOR LOGIC
# ==========================================

class NodeType(str, Enum):
    START = "start"
    END = "end"
    TASK = "task"
    IF = "if"

@dataclass
class OutgoingEdge:
    resource_id: str
    conditional: Optional[str] = None

@dataclass
class WorkflowNode:
    resource_id: str
    node_type: NodeType
    outgoings: List[OutgoingEdge]
    
    def __post_init__(self):
        if not self.resource_id:
            raise ValueError("Node must contain resource_id")
        if not isinstance(self.node_type, NodeType):
            self.node_type = NodeType(self.node_type)
        
        converted_outgoings = []
        for outgoing in self.outgoings:
            if isinstance(outgoing, OutgoingEdge):
                converted_outgoings.append(outgoing)
            elif isinstance(outgoing, dict):
                res_id = outgoing.get("resource_id")
                cond = outgoing.get("conditional")
                if not res_id:
                    raise ValueError("Outgoing must contain resource_id")
                converted_outgoings.append(OutgoingEdge(resource_id=res_id, conditional=cond))
        
        self.outgoings = converted_outgoings
        for outgoing in self.outgoings:
            if self.node_type == NodeType.IF and outgoing.conditional is None:
                raise ValueError(f"IF node '{self.resource_id}' outgoing must have a conditional expression")
            if self.node_type != NodeType.IF and outgoing.conditional is not None:
                raise ValueError(f"Non-IF node '{self.resource_id}' outgoing cannot have a conditional")

class WorkflowValidator:
    def __init__(self, nodes: List[Union[WorkflowNode, Dict[str, Any]]]):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.graph: Dict[str, List[str]] = defaultdict(list)
        self.reverse_graph: Dict[str, List[str]] = defaultdict(list)
        self.node_types: Dict[str, NodeType] = {}
        
        for node_data in nodes:
            node = WorkflowNode(**node_data) if isinstance(node_data, dict) else node_data
            self.nodes[node.resource_id] = node
            self.node_types[node.resource_id] = node.node_type
            for outgoing in node.outgoings:
                self.graph[node.resource_id].append(outgoing.resource_id)
                self.reverse_graph[outgoing.resource_id].append(node.resource_id)

    def validate(self) -> Tuple[bool, List[str]]:
        errors = []
        errors.extend(self._validate_basic_structure())
        errors.extend(self._find_isolated_nodes())
        errors.extend(self._find_cycles())
        errors.extend(self._validate_input_output())
        errors.extend(self._validate_if_nodes())
        return len(errors) == 0, errors

    def _validate_basic_structure(self) -> List[str]:
        errors = []
        if not self.nodes: return ["Workflow cannot be empty"]
        starts = [n for n, t in self.node_types.items() if t == NodeType.START]
        if len(starts) != 1: errors.append(f"Workflow must have exactly one START node, found {len(starts)}")
        ends = [n for n, t in self.node_types.items() if t == NodeType.END]
        if not ends: errors.append("Workflow must have at least one END node")
        return errors

    def _find_isolated_nodes(self) -> List[str]:
        starts = [n for n, t in self.node_types.items() if t == NodeType.START]
        if not starts: return []
        visited, queue = {starts[0]}, deque([starts[0]])
        while queue:
            curr = queue.popleft()
            for neighbor in self.graph.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        unreachable = set(self.nodes.keys()) - visited
        return [f"Isolated nodes detected: {', '.join(unreachable)}"] if unreachable else []

    def _find_cycles(self) -> List[str]:
        errors, visited, stack = [], set(), set()
        def dfs(node_id, path):
            if node_id in stack:
                cycle = path[path.index(node_id):] + [node_id]
                errors.append(f"Cycle detected: {' -> '.join(cycle)}")
                return True
            if node_id in visited: return False
            visited.add(node_id); stack.add(node_id); path.append(node_id)
            for neighbor in self.graph.get(node_id, []):
                dfs(neighbor, path.copy())
            stack.remove(node_id); path.pop(); return False
        for node_id in self.nodes:
            if node_id not in visited: dfs(node_id, [])
        return errors

    def _validate_input_output(self) -> List[str]:
        errors = []
        for nid, node in self.nodes.items():
            if node.node_type == NodeType.START and nid in self.reverse_graph and self.reverse_graph[nid]:
                errors.append(f"START node '{nid}' cannot have input edges")
            if node.node_type == NodeType.END and nid in self.graph and self.graph[nid]:
                errors.append(f"END node '{nid}' cannot have output edges")
            if node.node_type in [NodeType.TASK, NodeType.IF]:
                if nid not in self.reverse_graph or not self.reverse_graph[nid]:
                    errors.append(f"Node '{nid}' is missing an input edge")
                if nid not in self.graph or not self.graph[nid]:
                    errors.append(f"Node '{nid}' is missing an output edge")
        return errors

    def _validate_if_nodes(self) -> List[str]:
        errors = []
        for nid, node in self.nodes.items():
            if node.node_type == NodeType.IF:
                if len(node.outgoings) < 2:
                    errors.append(f"IF node '{nid}' must have at least two branches")
                for out in node.outgoings:
                    if not out.conditional or not any(op in out.conditional for op in ['==', '!=', '>', '<', '>=', '<=', '&&', '||']):
                        errors.append(f"IF node '{nid}' has an invalid conditional: {out.conditional}")
        return errors

    def visualize_graph(self) -> str:
        lines = ["\nWorkflow Structure:", "=" * 50]
        for nid, node in self.nodes.items():
            out_str = ", ".join([f"{e.resource_id}" + (f" [{e.conditional}]" if e.conditional else "") for e in node.outgoings])
            lines.append(f"{nid} ({node.node_type.value}) -> [{out_str}]")
        lines.append("=" * 50)
        return "\n".join(lines)

    def get_reachable_paths(self) -> List[List[str]]:
        paths, starts, ends = [], [n for n, t in self.node_types.items() if t == NodeType.START], [n for n, t in self.node_types.items() if t == NodeType.END]
        if not starts or not ends: return []
        def dfs(curr, path, visited):
            if curr in visited: return
            new_path = path + [curr]
            if curr in ends: paths.append(new_path)
            else:
                visited.add(curr)
                for neighbor in self.graph.get(curr, []):
                    dfs(neighbor, new_path, visited.copy())
        dfs(starts[0], [], set())
        return paths

# ==========================================
# 3. EXECUTION BLOCK
# ==========================================

if __name__ == "__main__":
    try:
        validator = WorkflowValidator(my_workflow)
        is_valid, errors = validator.validate()
        
        if is_valid:
            print("✅ Success: The workflow is valid!")
            print(validator.visualize_graph())
            
            paths = validator.get_reachable_paths()
            print(f"Found {len(paths)} unique paths:")
            for i, path in enumerate(paths, 1):
                print(f"  Path {i}: {' -> '.join(path)}")
        else:
            print("❌ Validation Failed!")
            for error in errors:
                print(f"  - {error}")
                
    except Exception as e:
        print(f"❌ System Error: {e}")