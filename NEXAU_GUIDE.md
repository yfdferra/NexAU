# NexAU Framework: Comprehensive Guide to Utilization and Customization

## Introduction to NexAU

NexAU is a general-purpose agent framework for building intelligent agents with tool capabilities. It provides a modular tool system, flexible agent architecture, and seamless integration with various LLM providers. This guide will help you understand how to utilize NexAU effectively and customize it for your specific software development needs.

## Core Architecture

### Key Components

1. **Agent**: The main orchestrator that manages tool calls, LLM interactions, and workflow execution
2. **Tools**: Modular capabilities that agents can use (file operations, web search, bash commands, etc.)
3. **Skills**: Specialized knowledge packages that enhance agent capabilities for specific domains
4. **Middlewares**: Interceptors that modify agent behavior (logging, context compaction, etc.)
5. **Tracers**: Observability components for monitoring agent execution

### Directory Structure

```
nexau/
├── core/           # Core framework components
├── archs/          # Architectural patterns and implementations
├── cli/            # Command-line interface
└── examples/       # Example configurations and agents
```

## Getting Started with NexAU

### Installation Options

**From GitHub Release (Recommended):**
```bash
# Using pip
pip install git+ssh://git@github.com/nex-agi/NexAU.git@v0.3.5

# Using uv
uv pip install git+ssh://git@github.com/nex-agi/NexAU.git@v0.3.5
```

**From Source:**
```bash
git clone git@github.com:nex-agi/NexAU.git
cd NexAU
pip install uv
uv sync
```

### Environment Setup

Create a `.env` file with required configuration:
```env
LLM_MODEL="your-llm-model"
LLM_BASE_URL="your-llm-api-base-url"
LLM_API_KEY="your-llm-api-key"
SERPER_API_KEY="api key from serper.dev"  # Required for web search

# Optional: Langfuse for tracing
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_HOST="https://us.cloud.langfuse.com"
```

## Understanding the System Workflow

The `system-workflow.md` file (located at `examples/code_agent/system-workflow.md`) is the core instruction set that defines how your agent behaves. It contains approximately 284 lines of detailed specifications covering:

### Key Sections of system-workflow.md

1. **Agent Identity & Security Policies**: Defines the agent's role and security boundaries
2. **Communication Guidelines**: How the agent should format responses and interact
3. **Status Update Specifications**: Progress reporting and task management
4. **Tool Calling Protocols**: How to use tools efficiently and in parallel
5. **Code Style Guidelines**: Programming best practices and conventions
6. **Task Management (Todo System)**: Structured approach to breaking down work
7. **Error Handling & Linter Rules**: Quality assurance and error prevention

## Customizing Your Own Agent

### What to Keep from system-workflow.md

**Reusable Sections (Keep As-Is):**

1. **Core Communication Patterns** (`<communication>` section):
   - Markdown formatting rules
   - Code citation guidelines
   - File and function naming conventions

2. **Tool Calling Infrastructure** (`<tool_calling>` and `<maximize_parallel_tool_calls>`):
   - Parallel execution patterns
   - Tool discovery and usage protocols
   - Batch operation strategies

3. **Code Quality Standards** (`<code_style>` and `<linter_errors>`):
   - Naming conventions (Clean Code principles)
   - Control flow patterns
   - Error handling guidelines
   - Linter integration rules

4. **Task Management Framework** (`<todo_spec>` and `<flow>`):
   - Todo item creation and tracking
   - Workflow state management
   - Progress reporting structure

### What to Customize in system-workflow.md

**Agent-Specific Customizations:**

1. **Agent Identity** (Lines 1-13):
   - Update the agent's name and primary function
   - Modify security policies based on your use case
   - Adjust URL policies if needed

2. **Domain-Specific Instructions**:
   - Add specialized knowledge for your software development domain
   - Include project-specific conventions and patterns
   - Define your preferred development workflows

3. **Tool Preferences**:
   - Emphasize tools most relevant to your work
   - Add custom tool usage patterns
   - Define tool priority based on your tasks

4. **Communication Style**:
   - Adjust verbosity level based on your preferences
   - Modify progress reporting frequency
   - Customize summary formats

### Minimal Customization Approach

For minimal changes while creating a software development agent:

1. **Update the agent identity** (Line 1):
   ```
   You are [Your Agent Name], an interactive CLI tool designed to assist with [Your Specific Domain] software engineering tasks.
   ```

2. **Add domain-specific context** after the core instructions:
   ```
   <domain_specific>
   - Focus on [Your Technology Stack] development
   - Follow [Your Company/Team] coding conventions
   - Prioritize [Your Specific Development Workflows]
   </domain_specific>
   ```

3. **Adjust tool emphasis** in the `<tool_calling>` section if needed

## Parallel Sub-Agents System

### Understanding Parallel Execution

**Current Implementation:**
The parallel execution you're experiencing is **already built into the framework** through the `<maximize_parallel_tool_calls>` specification. This is not a separate sub-agent system but rather intelligent parallelization of tool calls within a single agent.

**Key Parallelization Features:**

1. **Automatic Batch Processing**: The agent automatically groups independent tool calls
2. **Concurrent File Operations**: Multiple file reads/writes happen simultaneously
3. **Parallel Searches**: Different search patterns execute concurrently
4. **Optimized Resource Usage**: Limits to 3-5 simultaneous calls to prevent timeouts

### How Parallel Tool Calls Work

```python
# Example of parallel tool call pattern (handled automatically by the framework)
# When you need to read multiple files:
file1_content = read_file("/path/to/file1.py")
file2_content = read_file("/path/to/file2.py")
file3_content = read_file("/path/to/file3.py")

# The framework executes these 3 calls in parallel, not sequentially
```

### Activating Advanced Parallel Features

**For true sub-agent parallelism** (multiple independent agents working together), you would need to:

1. **Create Multiple Agent Configurations**:
   ```yaml
   # agent1.yaml
   name: "frontend_specialist"
   system_prompt: "./frontend-workflow.md"
   
   # agent2.yaml  
   name: "backend_specialist"
   system_prompt: "./backend-workflow.md"
   ```

2. **Implement Orchestration Logic**:
   ```python
   from nexau import Agent
   
   frontend_agent = Agent.from_yaml("agent1.yaml")
   backend_agent = Agent.from_yaml("agent2.yaml")
   
   # Run agents in parallel using threading or asyncio
   import concurrent.futures
   
   with concurrent.futures.ThreadPoolExecutor() as executor:
       frontend_future = executor.submit(frontend_agent.run, "Build React component")
       backend_future = executor.submit(backend_agent.run, "Create API endpoint")
       
       results = [frontend_future.result(), backend_future.result()]
   ```

3. **Use Middleware for Coordination** (Advanced):
   - Implement custom middleware for inter-agent communication
   - Use shared context or message buses
   - Implement result aggregation patterns

## Creating Your Custom Software Development Agent

### Step-by-Step Minimal Customization

**1. Copy the Base Configuration:**
```bash
cp examples/code_agent/code_agent.yaml my_software_agent.yaml
cp examples/code_agent/system-workflow.md my_software_workflow.md
```

**2. Make Minimal Edits to system-workflow.md:**
- Change line 1 to reflect your agent's purpose
- Add 2-3 lines of domain-specific context after the core instructions
- Keep all other sections intact

**3. Configure Your Agent YAML:**
```yaml
# my_software_agent.yaml
name: "my_software_dev_agent"
system_prompt: "./my_software_workflow.md"
# Keep all tools, skills, and middlewares as-is
```

**4. Run Your Custom Agent:**
```bash
./run-agent my_software_agent.yaml
```

### Recommended Tool Set for Software Development

The default tool set in `code_agent.yaml` is already comprehensive for software development:

- **File Operations**: `file_read`, `file_write`, `file_edit`, `multiedit`
- **Code Search**: `grep`, `glob`
- **System Operations**: `bash`, `ls`, `run_code`
- **Web Resources**: `web_search`, `web_read`
- **Task Management**: `todo_write`

### Adding Custom Tools (Optional)

If you need specialized tools:

1. **Create Tool Definition** (`my_tool.tool.yaml`):
   ```yaml
   name: my_custom_tool
   description: Tool for [specific purpose]
   parameters:
     # Define parameters
   ```

2. **Implement Tool Binding** (`my_tool.py`):
   ```python
   def my_custom_tool_function(param1, param2):
       # Implementation
       return result
   ```

3. **Add to Agent Configuration**:
   ```yaml
   tools:
     - name: my_custom_tool
       yaml_path: "./tools/my_tool.tool.yaml"
       binding: "my_tool_module:my_custom_tool_function"
   ```

## Best Practices for Agent Customization

### Do's and Don'ts

**✅ DO:**
- Keep the core workflow patterns intact
- Add domain-specific context clearly
- Test your customizations incrementally
- Use the existing todo system for task management
- Leverage parallel tool calling automatically

**❌ DON'T:**
- Remove essential security policies
- Override parallel execution optimizations
- Change core communication protocols
- Eliminate error handling guidelines
- Modify the tool calling infrastructure

### Testing Your Custom Agent

1. **Start Simple**:
   ```bash
   ./run-agent my_software_agent.yaml
   Enter your task: "Create a simple Python function that adds two numbers"
   ```

2. **Verify Core Functions**:
   - Tool calling works correctly
   - Parallel execution is happening
   - Todo system functions properly
   - Code quality guidelines are followed

3. **Test Domain-Specific Tasks**:
   - Try tasks specific to your software domain
   - Verify custom instructions are being followed
   - Check that specialized knowledge is applied

## Troubleshooting Common Issues

### Parallel Execution Not Working
- Ensure you're using the latest version of NexAU
- Check that `<maximize_parallel_tool_calls>` section is intact
- Verify tool definitions support parallel execution

### Agent Not Following Custom Instructions
- Check system prompt path in YAML configuration
- Verify custom workflow file is properly formatted
- Ensure domain-specific sections are clearly marked

### Tool Binding Errors
- Confirm tool function signatures match YAML definitions
- Check import paths in agent configuration
- Verify required dependencies are installed

## Advanced Customization Paths

### When You Need More Than Minimal Changes

**Scenario 1: Specialized Development Workflow**
- Create custom skills for your technology stack
- Implement domain-specific middlewares
- Add custom tool integrations

**Scenario 2: Team-Specific Conventions**
- Extend code style guidelines
- Add team-specific patterns and anti-patterns
- Implement custom quality gates

**Scenario 3: Complex Multi-Agent Systems**
- Build orchestrator agents
- Implement inter-agent communication
- Create specialized agent roles

## Conclusion

NexAU provides a powerful, flexible framework for building intelligent software development assistants. By understanding which parts of `system-workflow.md` to keep and which to customize, you can create effective agents with minimal changes.

**Key Takeaways:**
1. The parallel execution you experience is built into the framework's tool calling system
2. Most of `system-workflow.md` should remain unchanged for optimal agent behavior
3. Focus customization on agent identity and domain-specific knowledge
4. The existing tool set is comprehensive for general software development
5. Start with minimal changes and expand only as needed

For most software development use cases, simply updating the agent's identity and adding a few lines of domain context will create an effective, parallel-enabled assistant that follows best practices while adapting to your specific needs.

## Resources

- **Official Documentation**: `docs/` directory in the NexAU repository
- **Example Agents**: `examples/code_agent/` for reference implementations
- **Tool Definitions**: `examples/code_agent/tools/` for tool patterns
- **Skill Examples**: `examples/code_agent/skills/` for specialized knowledge packages

Remember: The power of NexAU lies in its balanced approach—providing strong defaults while allowing targeted customization where it matters most for your specific software development workflow.