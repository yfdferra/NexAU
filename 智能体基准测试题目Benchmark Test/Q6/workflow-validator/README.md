# 工作流验证器 (Workflow Validator)

一个用于验证流程配置的Python库，支持检测孤岛节点、死循环、输入输出问题等。

## 功能特性

- ✅ **节点类型支持**：开始节点、结束节点、任务节点、if判断节点
- ✅ **孤岛节点检测**：检测无法从开始节点到达的节点
- ✅ **死循环检测**：检测流程中的循环依赖（包括if节点的特殊处理）
- ✅ **输入输出验证**：验证节点的输入输出是否符合规则
- ✅ **if节点特殊验证**：验证if节点的conditional表达式和分支数量
- ✅ **可达路径分析**：找出所有从开始到结束的路径
- ✅ **图可视化**：生成工作流的文本表示

## 安装

将 `workflow_validator.py` 文件复制到您的项目中即可使用。

## 快速开始

### 基本使用

```python
from workflow_validator import validate_workflow

# 定义工作流节点
nodes = [
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

# 验证工作流
is_valid, errors = validate_workflow(nodes)

if is_valid:
    print("✅ 工作流有效")
else:
    print("❌ 工作流无效")
    for error in errors:
        print(f"  - {error}")
```

### 编程方式创建

```python
from workflow_validator import WorkflowNode, NodeType, OutgoingEdge, WorkflowValidator

# 创建节点对象
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
    # ... 更多节点
]

# 创建验证器并验证
validator = WorkflowValidator(nodes)
is_valid, errors = validator.validate()

# 获取更多信息
print(validator.visualize_graph())  # 可视化图结构
paths = validator.get_reachable_paths()  # 获取所有可达路径
```

## 节点类型

### 开始节点 (type: "start")
- 必须有且只有一个
- 不能有输入边
- 必须有输出边

### 结束节点 (type: "end")
- 必须有至少一个
- 不能有输出边
- 可以有输入边

### 任务节点 (type: "task")
- 必须有输入边
- 必须有输出边

### if判断节点 (type: "if")
- 必须有输入边
- 必须有至少两个输出边
- 每个输出边必须有conditional表达式
- conditional表达式必须有效（包含比较运算符）

## 验证规则

### 1. 基本结构验证
- 必须有且只有一个开始节点
- 必须有至少一个结束节点
- 节点ID必须唯一

### 2. 孤岛节点检测
检测无法从开始节点到达的节点。

### 3. 死循环检测
检测流程中的循环依赖，包括：
- 直接循环（A → A）
- 间接循环（A → B → C → A）
- if节点的自循环

### 4. 输入输出验证
- 开始节点：不能有输入，必须有输出
- 结束节点：不能有输出，可以有输入
- 其他节点：必须有输入和输出

### 5. if节点特殊验证
- 必须有至少两个输出边
- 每个输出边必须有conditional表达式
- conditional表达式必须包含比较运算符
- 括号必须匹配

## API参考

### 主要类

#### `WorkflowNode`
工作流节点类。

**属性：**
- `resource_id: str` - 节点唯一标识
- `node_type: NodeType` - 节点类型
- `outgoings: List[OutgoingEdge]` - 出边列表

#### `OutgoingEdge`
出边定义类。

**属性：**
- `resource_id: str` - 目标节点ID
- `conditional: Optional[str]` - 条件表达式（仅if节点使用）

#### `WorkflowValidator`
工作流验证器主类。

**方法：**
- `__init__(nodes: List[Union[WorkflowNode, Dict]])` - 初始化验证器
- `validate() -> Tuple[bool, List[str]]` - 验证工作流
- `get_reachable_paths() -> List[List[str]]` - 获取所有可达路径
- `visualize_graph() -> str` - 生成图的可视化文本

### 便捷函数

#### `validate_workflow(nodes: List[Union[WorkflowNode, Dict]]) -> Tuple[bool, List[str]]`
验证工作流的便捷函数。

## 示例

### 有效的工作流
```python
nodes = [
    {"resource_id": "start", "node_type": "start", "outgoings": [{"resource_id": "task1"}]},
    {"resource_id": "task1", "node_type": "task", "outgoings": [{"resource_id": "if1"}]},
    {"resource_id": "if1", "node_type": "if", "outgoings": [
        {"resource_id": "task2", "conditional": "condition == true"},
        {"resource_id": "task3", "conditional": "condition == false"}
    ]},
    {"resource_id": "task2", "node_type": "task", "outgoings": [{"resource_id": "end"}]},
    {"resource_id": "task3", "node_type": "task", "outgoings": [{"resource_id": "end"}]},
    {"resource_id": "end", "node_type": "end", "outgoings": []}
]
```

### 常见错误示例

1. **孤岛节点**：
   ```python
   nodes = [
       {"resource_id": "start", "node_type": "start", "outgoings": [{"resource_id": "task1"}]},
       {"resource_id": "task1", "node_type": "task", "outgoings": [{"resource_id": "end"}]},
       {"resource_id": "isolated", "node_type": "task", "outgoings": []},  # 孤岛节点
       {"resource_id": "end", "node_type": "end", "outgoings": []}
   ]
   ```
   **错误**：`存在孤岛节点（无法从开始节点到达）: isolated`

2. **死循环**：
   ```python
   nodes = [
       {"resource_id": "start", "node_type": "start", "outgoings": [{"resource_id": "task1"}]},
       {"resource_id": "task1", "node_type": "task", "outgoings": [{"resource_id": "task2"}]},
       {"resource_id": "task2", "node_type": "task", "outgoings": [{"resource_id": "task1"}]},  # 形成循环
       {"resource_id": "end", "node_type": "end", "outgoings": []}
   ]
   ```
   **错误**：`检测到死循环: task1 -> task2 -> task1`

3. **无效的if节点**：
   ```python
   nodes = [
       {"resource_id": "start", "node_type": "start", "outgoings": [{"resource_id": "if1"}]},
       {"resource_id": "if1", "node_type": "if", "outgoings": [
           {"resource_id": "task1"},  # 缺少conditional
           {"resource_id": "task2", "conditional": "condition == false"}
       ]},
       # ...
   ]
   ```
   **错误**：`if节点的outgoing必须包含conditional表达式`

## 运行测试

项目包含完整的测试套件：

```bash
# 运行所有测试
python test_validator.py

# 运行使用示例
python example_usage.py
```

## 集成到Web API

工作流验证器可以轻松集成到Web API中：

```python
from flask import Flask, request, jsonify
from workflow_validator import validate_workflow

app = Flask(__name__)

@app.route('/api/workflows/validate', methods=['POST'])
def validate_workflow_api():
    try:
        data = request.get_json()
        nodes = data.get('nodes', [])
        
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
```

## 项目结构

```
workflow-validator/
├── workflow_validator.py    # 主验证器模块
├── test_validator.py        # 测试套件
├── example_usage.py         # 使用示例
├── debug_test.py           # 调试脚本
└── README.md               # 本文档
```

## 许可证

MIT License