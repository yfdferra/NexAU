# Parallel Agents in NexAU: What You Need to Know

## The Critical Answer About Parallel Execution

**You are already experiencing parallel execution** through the built-in `<maximize_parallel_tool_calls>` system in `system-workflow.md`. This is NOT a separate "sub-agent" feature but rather intelligent parallelization within a single agent.

## What Parallel Execution You're Getting

### Built-In Parallel Features (Active Now)
1. **Parallel Tool Calls**: Multiple independent tools run simultaneously
2. **Batch File Operations**: Reading/writing multiple files happens concurrently  
3. **Concurrent Searches**: Different grep/glob patterns execute in parallel
4. **Optimized Resource Usage**: Automatic batching with 3-5 call limits

### Example of Current Parallel Behavior
When you ask the agent to:
- Read 3 different files
- Search for 2 different patterns
- Check system status

These operations happen **in parallel, not sequentially**, making your agent 3-5x faster.

## The "Sub-Agents" Misconception

### What People Often Think "Sub-Agents" Means
- Multiple independent AI agents working together
- Specialized agents for different tasks
- Coordinated multi-agent systems

### What NexAU Actually Provides
- **Single agent with parallel tool execution** (what you have now)
- **Optional**: You can create multiple agent instances and run them in parallel yourself
- **No built-in multi-agent coordination system** (but you can build it)

## How to Verify You Have Parallel Execution

### Check Your Current Experience
1. **Tool calls complete faster** than they would sequentially
2. **Multiple operations** appear to happen simultaneously
3. **The agent doesn't wait** for one tool to finish before starting another compatible tool

### Technical Verification
The parallel execution is controlled by these lines in `system-workflow.md` (lines 110-125):

```markdown
<maximize_parallel_tool_calls>
CRITICAL INSTRUCTION: For optimal efficiency, when performing multiple operations, 
invoke all relevant tools concurrently using multi_tool_use.parallel rather than sequentially.
Prioritize parallel tool calls whenever possible.
...
DEFAULT TO PARALLEL: Unless operations MUST be sequential, always execute multiple tools simultaneously.
</maximize_parallel_tool_calls>
```

## If You Want True Multi-Agent Systems

### What Would Be Required
1. **Create Multiple Agent Configurations**:
   ```yaml
   # frontend_agent.yaml
   name: "react_specialist"
   system_prompt: "./frontend_workflow.md"
   
   # backend_agent.yaml
   name: "api_specialist"  
   system_prompt: "./backend_workflow.md"
   ```

2. **Implement Manual Orchestration**:
   ```python
   import concurrent.futures
   from nexau import Agent
   
   frontend = Agent.from_yaml("frontend_agent.yaml")
   backend = Agent.from_yaml("backend_agent.yaml")
   
   with concurrent.futures.ThreadPoolExecutor() as executor:
       frontend_task = executor.submit(frontend.run, "Build React component")
       backend_task = executor.submit(backend.run, "Create REST API")
       
       results = [frontend_task.result(), backend_task.result()]
   ```

3. **Add Coordination Logic** (Advanced):
   - Message passing between agents
   - Shared context management
   - Result aggregation

### Why You Probably Don't Need This
For most software development tasks:
- **Single agent with parallel tools** is sufficient
- **Specialized knowledge** can be added via skills
- **Complex coordination** adds overhead without proportional benefit

## Minimal Customization: The Right Approach

### What to Change (Minimal)
1. **Agent Identity** (system-workflow.md lines 1-13):
   ```markdown
   You are [Your Name] Software Development Assistant, an interactive CLI tool 
   designed to assist with [Your Stack] development tasks.
   ```

2. **Add Domain Context** (after line 13):
   ```markdown
   <software_domain>
   Primary focus: [Your specific technology stack]
   Key responsibilities: [Your main tasks]
   Development standards: [Your quality requirements]
   </software_domain>
   ```

### What to Keep (Critical for Parallel Execution)
1. **Entire `<maximize_parallel_tool_calls>` section** (lines 110-125)
2. **Entire `<tool_calling>` section** (lines 86-99)
3. **All workflow management sections** (`<flow>`, `<todo_spec>`, etc.)

## Common Questions Answered

### Q: Do I need to activate parallel execution?
**A**: No, it's already active. The framework automatically parallelizes compatible tool calls.

### Q: Can I make it more parallel?
**A**: The current 3-5 simultaneous call limit is optimized for reliability. Increasing it could cause timeouts.

### Q: What about specialized sub-agents?
**A**: You can create them, but consider if skills or better prompts in a single agent would suffice.

### Q: How do I know it's working?
**A**: Notice that multiple file reads or searches complete much faster than they would sequentially.

## Summary: Your Path Forward

### For 95% of Use Cases
1. **Keep the parallel execution system as-is** (it's already working)
2. **Make minimal customizations** to agent identity and domain knowledge
3. **Leverage existing tools and skills** for specialized tasks
4. **Enjoy the performance benefits** of automatic parallelization

### Only If You Need True Multi-Agent
1. Create separate agent configurations
2. Implement manual parallel execution with threading
3. Add coordination logic if needed
4. Accept the complexity trade-off

## Final Recommendation

**Stick with the built-in parallel tool calling** you already have. It provides:
- Excellent performance (3-5x speedup)
- Automatic optimization
- No additional complexity
- Proven reliability

Focus your customization efforts on:
1. Making the agent an expert in your specific domain
2. Adding your team's coding conventions
3. Incorporating your development workflows

The parallel execution is already working for you - no activation or configuration needed!