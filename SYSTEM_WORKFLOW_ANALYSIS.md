# System-Workflow.md: Detailed Analysis for Customization

## Complete Section Breakdown

### Section 1: Agent Identity & Core Policies (Lines 1-13)
**Content**: Agent introduction, security policies, URL policies
**Customization Level**: **HIGH** - This defines who your agent is
**Recommendation**: Update agent name and primary function. Keep security policies unless you have specific reasons to change them.

### Section 2: Communication Guidelines (<communication>) (Lines 14-25)
**Content**: Markdown formatting, code citation, file naming conventions
**Customization Level**: **LOW** - These are universal best practices
**Recommendation**: Keep as-is for consistent, professional communication

### Section 3: Status Update Specifications (<status_update_spec>) (Lines 27-56)
**Content**: Progress reporting patterns, tense usage, todo integration
**Customization Level**: **MEDIUM** - Can adjust frequency/style
**Recommendation**: Keep core structure, adjust verbosity if needed

### Section 4: Summary Specifications (<summary_spec>) (Lines 58-68)
**Content**: End-of-turn summaries, change documentation
**Customization Level**: **LOW** - Standard reporting format
**Recommendation**: Keep as-is for clear progress tracking

### Section 5: Completion Specifications (<completion_spec>) (Lines 70-76)
**Content**: Task completion verification, todo list reconciliation
**Customization Level**: **LOW** - Essential workflow completion
**Recommendation**: Keep as-is for proper task management

### Section 6: Workflow Flow (<flow>) (Lines 78-84)
**Content**: Step-by-step execution pattern, discovery passes
**Customization Level**: **LOW** - Core execution engine
**Recommendation**: Keep as-is for reliable agent behavior

### Section 7: Tool Calling Protocols (<tool_calling>) (Lines 86-99)
**Content**: Tool usage patterns, parallel execution, todo integration
**Customization Level**: **LOW** - Critical for performance
**Recommendation**: Keep as-is - this enables parallel tool execution

### Section 8: Context Understanding (<context_understanding>) (Lines 101-108)
**Content**: Search strategies, information gathering patterns
**Customization Level**: **MEDIUM** - Can add domain-specific search patterns
**Recommendation**: Keep core, add domain-specific queries if needed

### Section 9: Parallel Tool Calls (<maximize_parallel_tool_calls>) (Lines 110-125)
**Content**: Parallel execution rules, batch processing, optimization
**Customization Level**: **LOW** - Performance-critical section
**Recommendation**: **DO NOT MODIFY** - This enables the parallel execution you're experiencing

### Section 10: Grep Specifications (<grep_spec>) (Lines 127-130)
**Content**: Search tool preferences, pattern matching guidelines
**Customization Level**: **LOW** - Tool optimization
**Recommendation**: Keep as-is for efficient code exploration

### Section 11: Code Change Guidelines (<making_code_changes>) (Lines 132-142)
**Content**: Code editing patterns, dependency management, UI guidelines
**Customization Level**: **MEDIUM** - Can add project-specific patterns
**Recommendation**: Keep core, add technology-specific guidelines

### Section 12: Code Style Guidelines (<code_style>) (Lines 144-183)
**Content**: Naming conventions, control flow, comments, formatting
**Customization Level**: **HIGH** - Should match your team's style
**Recommendation**: Review and align with your coding standards

### Section 13: Linter Error Handling (<linter_errors>) (Lines 185-189)
**Content**: Error prevention, quality assurance, fix limits
**Customization Level**: **LOW** - Quality control essential
**Recommendation**: Keep as-is for code quality

### Section 14: Non-Compliance Rules (<non_compliance>) (Lines 191-197)
**Content**: Self-correction patterns, error recovery
**Customization Level**: **LOW** - Reliability mechanisms
**Recommendation**: Keep as-is for robust operation

### Section 15: Code Citation Methods (<citing_code>) (Lines 199-236)
**Content**: Code display formats, line number handling
**Customization Level**: **LOW** - Consistent presentation
**Recommendation**: Keep as-is for clear code communication

### Section 16: Inline Line Numbers (<inline_line_numbers>) (Lines 238-240)
**Content**: Metadata handling in code chunks
**Customization Level**: **LOW** - Technical implementation detail
**Recommendation**: Keep as-is

### Section 17: Markdown Specifications (<markdown_spec>) (Lines 242-250)
**Content**: Heading usage, emphasis, bullet formatting, URL handling
**Customization Level**: **LOW** - Presentation standards
**Recommendation**: Keep as-is for professional formatting

### Section 18: Todo Specifications (<todo_spec>) (Lines 252-267)
**Content**: Task definition, management, prioritization
**Customization Level**: **LOW** - Core task management system
**Recommendation**: Keep as-is for effective work breakdown

### Section 19: Critical Rules (Lines 269-273)
**Content**: Security reminders, tool usage mandates
**Customization Level**: **LOW** - Essential safeguards
**Recommendation**: Keep as-is for security and compliance

### Section 20: Code References (Lines 275-282)
**Content**: File path patterns for navigation
**Customization Level**: **LOW** - Developer experience
**Recommendation**: Keep as-is for easy code navigation

## Customization Priority Matrix

### Keep As-Is (Do Not Modify)
1. **Parallel execution system** (<maximize_parallel_tool_calls>)
2. **Tool calling infrastructure** (<tool_calling>)
3. **Core workflow patterns** (<flow>, <completion_spec>)
4. **Security policies** (Lines 3-4, 269-273)
5. **Task management system** (<todo_spec>)

### Review and Align (Minor Adjustments)
1. **Code style guidelines** - Match your team's conventions
2. **Communication style** - Adjust verbosity if needed
3. **Domain-specific searches** - Add your technology stack

### Customize Fully (Required Changes)
1. **Agent identity** - Define who your agent is
2. **Primary function** - Specify your software development focus
3. **Domain context** - Add your specific knowledge areas

## Minimal Customization Template

```markdown
# Replace Lines 1-13 with:

You are [Your Agent Name], an interactive CLI tool designed to assist with [Your Specific Domain] software engineering tasks. Follow the instructions below and leverage available tools to help the user effectively.

CRITICAL SECURITY POLICY: Only assist with defensive security tasks. Decline to create, modify, or enhance any code that could be used maliciously. Permitted activities include security analysis, detection rules, vulnerability explanations, defensive tools, and security documentation.

CRITICAL URL POLICY: Never generate or speculate about URLs unless you're certain they're for programming assistance. Only utilize URLs provided by the user in their messages or from local files.

You function as an AI coding assistant used as an example of NexAU, a universal agent framework.

# Add after Line 13 (before <communication>):

<domain_context>
## Specialized Knowledge for [Your Domain]
- Primary focus: [Your Technology Stack, e.g., "Full-stack web development with React and Node.js"]
- Key frameworks: [List your main frameworks]
- Development workflow: [Describe your typical workflow]
- Quality standards: [Your specific quality requirements]
</domain_context>

# Keep everything else exactly as-is
```

## Parallel Execution: What You're Already Getting

**Important Clarification**: The parallel execution you're experiencing comes from the `<maximize_parallel_tool_calls>` section (lines 110-125). This is **NOT** a separate sub-agent system but rather intelligent parallelization within a single agent.

**How it works**:
- When you make multiple independent tool calls, they execute simultaneously
- File reads, searches, and other operations happen in parallel
- The agent automatically batches compatible operations
- Limits to 3-5 simultaneous calls prevent system overload

**What you don't need to do**:
- No special activation required - it's built-in
- No configuration changes needed
- No separate sub-agent setup

**What you could add** (advanced):
- True multi-agent systems require custom orchestration
- Specialized agent roles need separate configurations
- Complex workflows may benefit from agent specialization

## Summary: Your Customization Path

### For Minimal Changes (Recommended)
1. Update agent identity (lines 1-13)
2. Add domain context section
3. Review code style for alignment
4. **Keep everything else unchanged**

### Files to Modify
1. `system-workflow.md` - Only lines 1-13 + domain context
2. Agent YAML - Update name and system prompt path

### Files to Leave Alone
1. All tool definitions
2. All skill definitions  
3. All middleware configurations
4. Core framework files

This approach gives you a customized agent that leverages all NexAU's powerful features (including parallel execution) while adapting to your specific software development needs.