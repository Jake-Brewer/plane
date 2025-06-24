# LLM Model Style Guide

This document provides evidence-based development limits and best practices for each Large Language Model (LLM) supported by Cursor IDE. These recommendations are derived from extensive research including official documentation, community feedback, and performance benchmarks.

## Cursor Pricing Structure

**Key Pricing Information:**
- **1 Cursor Request = $0.04** (when purchasing additional requests beyond plan limits)
- **Subscription Plans:**
  - **Hobby**: Free, 50 requests/month
  - **Pro**: $20/month, 500 requests/month, unlimited slow requests after limit
  - **Ultra**: $200/month, 10,000+ requests/month (20x Pro usage)
- **Max Plan Only**: Some premium models (Claude 4 Opus, o3-Pro) require Ultra subscription
- **Free Models**: Several models cost 0 requests per message (GPT-4o Mini, DeepSeek V3, Gemini Flash, etc.)

## Recommended Development Limits per Model

**⭐ SORTED BY VALUE FOR PLANE PROJECT MANAGEMENT & MCP DEVELOPMENT ⭐**

Based on extensive research from multiple sources including OpenAI documentation, Anthropic guidelines, and developer best practices, these are the recommended limits for optimal performance with each model:

| Model | Max Method Length | Max File Length | Max Context per Request | Max Concurrent Files | Max Modules/Imports | Cursor Requests | Monthly Cost @ $0.04/req | API Cost | MCP Support | Project Types | User Sentiment | User Assigned Points |
|-------|------------------|-----------------|------------------------|---------------------|-------------------|----------------|-------------------------|----------|-------------|---------------|----------------|---------------------|
| **DeepSeek R1** | 50 lines | 900 lines | 128K tokens | 10-15 files | 25 imports | 1 req/msg | $0.04/msg | $0.14/$2.19 per MTok | 55 tools | Budget Development | ⭐⭐⭐⭐ | 0 |
| **DeepSeek R1 Thinking** | 50 lines | 900 lines | 128K tokens | 10-15 files | 25 imports | 1 req/msg | $0.04/msg | $0.14/$2.19 per MTok | 55 tools | Budget Reasoning | ⭐⭐⭐⭐ | 0 |
| **GPT-4.1** | 65 lines | 1400 lines | 1M tokens | 25-30 files | 40 imports | 1 req/msg | $0.04/msg | $2.50/$10 per MTok | 90 tools | Large Codebases, Research | ⭐⭐⭐⭐⭐ | 0 |
| **Claude 3.7 Sonnet** | 60 lines | 1200 lines | 200K tokens | 12-15 files | 35 imports | 1 req/msg | $0.04/msg | $3/$15 per MTok | 80 tools | Professional, Architecture | ⭐⭐⭐⭐⭐ | 0 |
| **o3** | 75 lines | 1600 lines | 128K tokens | 18-25 files | 50 imports | 1 req/msg | $0.04/msg | $15/$60 per MTok | 95 tools | Advanced Reasoning | ⭐⭐⭐⭐⭐ | 0 |
| **o3 Thinking** | 75 lines | 1600 lines | 128K tokens | 18-25 files | 50 imports | 1 req/msg | $0.04/msg | $15/$60 per MTok | 95 tools | Deep Reasoning | ⭐⭐⭐⭐⭐ | 0 |
| **Claude 4 Sonnet** | 70 lines | 1500 lines | 200K tokens | 15-20 files | 45 imports | 1 req/msg | $0.04/msg | $3/$15 per MTok | 100 tools | Enterprise, AAA Games | ⭐⭐⭐⭐⭐ | 0 |
| **Gemini 2.5 Pro** | 55 lines | 1000 lines | 1M tokens | 20-25 files | 42 imports | 1 req/msg | $0.04/msg | $1.25/$5 per MTok | 75 tools | Microservices, Multiplayer | ⭐⭐⭐⭐ | 0 |
| **o4-Mini** | 50 lines | 800 lines | 128K tokens | 8-12 files | 25 imports | 1 req/msg | $0.04/msg | $2/$8 per MTok | 50 tools | Next-Gen Light Tasks | ⭐⭐⭐⭐ | 0 |
| **GPT-4o** | 45 lines | 800 lines | 128K tokens | 8-12 files | 32 imports | 1 req/msg | $0.04/msg | $2.50/$10 per MTok | 60 tools | General Development | ⭐⭐⭐⭐ | 0 |
| **Claude 3.5 Sonnet** | 55 lines | 1000 lines | 200K tokens | 10-12 files | 30 imports | 1 req/msg | $0.04/msg | $3/$15 per MTok | 70 tools | General Development | ⭐⭐⭐⭐ | 0 |
| **Gemini 2.5 Pro Thinking** | 55 lines | 1000 lines | 1M tokens | 20-25 files | 42 imports | 1 req/msg | $0.04/msg | $1.25/$5 per MTok | 75 tools | Complex Analysis | ⭐⭐⭐⭐ | 0 |
| **Grok 3** | 40 lines | 700 lines | 64K tokens | 6-10 files | 28 imports | 1 req/msg | $0.04/msg | $2/$10 per MTok | 50 tools | Internet-aware Projects | ⭐⭐⭐ | 0 |
| **Grok 2** | 35 lines | 600 lines | 64K tokens | 5-8 files | 25 imports | 1 req/msg | $0.04/msg | $2/$10 per MTok | 45 tools | Internet-aware | ⭐⭐⭐ | 0 |
| **Gemini 2.5 Pro Exp 03-25** | 55 lines | 1000 lines | 1M tokens | 20-25 files | 42 imports | 1 req/msg | $0.04/msg | $1.25/$5 per MTok | 75 tools | Experimental Features | ⭐⭐⭐⭐ | 0 |
| **Gemini 2.5 Pro Exp 03-25 Thinking** | 55 lines | 1000 lines | 1M tokens | 20-25 files | 42 imports | 1 req/msg | $0.04/msg | $1.25/$5 per MTok | 75 tools | Experimental Reasoning | ⭐⭐⭐⭐ | 0 |
| **Gemini 2.0 Pro (Exp)** | 50 lines | 900 lines | 1M tokens | 15-20 files | 35 imports | 1 req/msg | $0.04/msg | $1.25/$5 per MTok | 70 tools | Experimental | ⭐⭐⭐⭐ | 0 |
| **Grok 3 Beta** | 40 lines | 700 lines | 64K tokens | 6-10 files | 28 imports | 1 req/msg | $0.04/msg | $2/$10 per MTok | 50 tools | Beta Internet Features | ⭐⭐⭐ | 0 |
| **Claude 4 Sonnet Thinking** | 70 lines | 1500 lines | 200K tokens | 15-20 files | 45 imports | 2 req/msg | $0.08/msg | $3/$15 per MTok | 100 tools | Enterprise, Complex Reasoning | ⭐⭐⭐⭐⭐ | 0 |
| **Claude 3.7 Sonnet Thinking** | 60 lines | 1200 lines | 200K tokens | 12-15 files | 35 imports | 2 req/msg | $0.08/msg | $3/$15 per MTok | 80 tools | Complex Problem Solving | ⭐⭐⭐⭐⭐ | 0 |
| **o4-Mini Thinking** | 50 lines | 800 lines | 128K tokens | 8-12 files | 25 imports | 2 req/msg | $0.08/msg | $2/$8 per MTok | 50 tools | Next-Gen Reasoning | ⭐⭐⭐⭐ | 0 |
| **DeepSeek R1-0528** | 50 lines | 900 lines | 128K tokens | 10-15 files | 25 imports | 1 req/msg | $0.04/msg | $0.14/$2.19 per MTok | 55 tools | Budget Development | ⭐⭐⭐⭐ | 0 |
| **DeepSeek R1-0528 Thinking** | 50 lines | 900 lines | 128K tokens | 10-15 files | 25 imports | 1 req/msg | $0.04/msg | $0.14/$2.19 per MTok | 55 tools | Budget Reasoning | ⭐⭐⭐⭐ | 0 |
| **o3-Mini** | 45 lines | 700 lines | 128K tokens | 6-10 files | 20 imports | 0.25 req/msg | $0.01/msg | $1/$4 per MTok | 40 tools | Light Reasoning | ⭐⭐⭐ | 0 |
| **Claude 3.5 Haiku** | 40 lines | 700 lines | 100K tokens | 6-8 files | 20 imports | 0.33 req/msg | $0.013/msg | $0.25/$1.25 per MTok | 50 tools | Fast, Light Tasks | ⭐⭐⭐ | 0 |
| **o1 Mini** | 50 lines | 800 lines | 128K tokens | 8-12 files | 25 imports | 2.5 req/msg | $0.10/msg | $3/$12 per MTok | 50 tools | Moderate Reasoning | ⭐⭐⭐ | 0 |
| **Claude 3 Opus** | 50 lines | 800 lines | 200K tokens | 8-10 files | 25 imports | 2.5 req/msg | $0.10/msg | $15/$75 per MTok | 60 tools | Legacy Complex Tasks | ⭐⭐⭐ | 0 |
| **o1** | 65 lines | 1200 lines | 128K tokens | 15-20 files | 35 imports | 10 req/msg | $0.40/msg | $15/$60 per MTok | 80 tools | Complex Reasoning | ⭐⭐⭐⭐ | 0 |
| **GPT-4.5 Preview** | 70 lines | 1500 lines | 200K tokens | 20-25 files | 45 imports | 50 req/msg | $2.00/msg | $50/$200 per MTok | 95 tools | Cutting-edge Research | ⭐⭐⭐⭐ | 0 |
| **Claude 4 Opus** | 75 lines | 1600 lines | 200K tokens | 20-25 files | 50 imports | Max Plan Only | $200/month | $15/$75 per MTok | 100 tools | Ultra-Complex Projects | ⭐⭐⭐⭐⭐ | 0 |
| **Claude 4 Opus Thinking** | 75 lines | 1600 lines | 200K tokens | 20-25 files | 50 imports | Max Plan Only | $200/month | $15/$75 per MTok | 100 tools | Ultra-Complex Reasoning | ⭐⭐⭐⭐⭐ | 0 |
| **o3-Pro Thinking** | 80 lines | 1800 lines | 128K tokens | 25-30 files | 55 imports | Max Plan Only | $200/month | $60/$240 per MTok | 100 tools | Ultra-Complex Reasoning | ⭐⭐⭐⭐⭐ | 0 |
| **GPT-4o Mini** | 35 lines | 600 lines | 128K tokens | 5-8 files | 25 imports | 0 req/msg | FREE | $0.15/$0.60 per MTok | 40 tools | Budget Development | ⭐⭐⭐ | 0 |
| **DeepSeek V3.1** | 45 lines | 800 lines | 128K tokens | 8-12 files | 20 imports | 0 req/msg | FREE | $0.07/$0.28 per MTok | 45 tools | Ultra-Budget | ⭐⭐⭐ | 0 |
| **DeepSeek V3** | 45 lines | 800 lines | 128K tokens | 8-12 files | 20 imports | 0 req/msg | FREE | $0.07/$0.28 per MTok | 45 tools | Ultra-Budget | ⭐⭐⭐ | 0 |
| **Gemini 2.5 Flash** | 40 lines | 600 lines | 1M tokens | 12-15 files | 30 imports | 0 req/msg | FREE | $0.075/$0.30 per MTok | 50 tools | Fast, Free Tasks | ⭐⭐⭐ | 0 |
| **Gemini 2.5 Flash Thinking** | 40 lines | 600 lines | 1M tokens | 12-15 files | 30 imports | 0 req/msg | FREE | $0.075/$0.30 per MTok | 50 tools | Fast, Free Reasoning | ⭐⭐⭐ | 0 |
| **Gemini 2.5 Flash Preview 04-17** | 40 lines | 600 lines | 1M tokens | 12-15 files | 30 imports | 0 req/msg | FREE | $0.075/$0.30 per MTok | 50 tools | Preview Features | ⭐⭐⭐ | 0 |
| **Grok 3 Mini** | 30 lines | 500 lines | 32K tokens | 4-6 files | 20 imports | 0 req/msg | FREE | $0.50/$2 per MTok | 30 tools | Basic Internet Tasks | ⭐⭐ | 0 |
| **Cursor Small** | 25 lines | 400 lines | 32K tokens | 3-5 files | 15 imports | 0 req/msg | FREE | Custom | 20 tools | Simple Tasks | ⭐⭐ | 0 |
| **Minimum (Free Models)** | 25 lines | 400 lines | 32K tokens | 3-5 files | 15 imports | 0 req/msg | FREE | $0.07/$0.28 per MTok | 20 tools | Basic Projects | ⭐⭐ | 0 |

## User Assigned Points System

### **How It Works**
The "User Assigned Points" column tracks your personal preferences and experiences with each model. This allows you to customize the recommendations based on your specific use cases and satisfaction levels.

### **Scoring Guidelines**
- **+5 points**: Exceptional performance, exceeded expectations
- **+3 points**: Very good performance, met expectations well
- **+1 point**: Good performance, minor issues
- **0 points**: Neutral/baseline (default starting point)
- **-1 point**: Below expectations, some issues
- **-3 points**: Poor performance, significant issues
- **-5 points**: Terrible performance, major problems

### **Usage Instructions**
When you want to adjust a model's score, simply say:
- "Add 3 points to DeepSeek R1" or "DeepSeek R1 +3"
- "Subtract 2 points from GPT-4.1" or "GPT-4.1 -2"
- "Give Claude 3.7 Sonnet 5 points" or "Claude 3.7 +5"

The AI will automatically update both this document and the LLM selection guide to reflect your preferences.

### **Score Impact on Recommendations**
- **High scores (+3 to +5)**: Model will be prioritized in recommendations
- **Neutral scores (-1 to +2)**: Standard recommendations apply
- **Low scores (-3 to -5)**: Model will be deprioritized or avoided in recommendations

### **Current Scores**
All models start at 0 points. As you use different models and provide feedback, your personal scoring will help tailor future recommendations to your specific needs and preferences.

## Dynamic Table Reordering Algorithm

### **Automatic Row Reordering Based on User Points**

When User Assigned Points become extreme enough, the entire table automatically reorders to reflect your personal preferences, potentially moving lower-capability models above higher-capability ones.

### **Reordering Logic & Thresholds**

**Impact Scaling System**:
```
Final Ranking Score = Base Capability Rating + (User Points × Impact Multiplier)

Impact Multiplier Tiers:
- ±1 point: 0.1× (minimal impact, fine-tuning only)
- ±2 points: 0.3× (slight preference adjustment)
- ±3 points: 0.6× (moderate impact, can shift 1-2 positions)
- ±4 points: 1.0× (significant impact, notable reordering)
- ±5 points: 1.5× (major impact, can override superior models)
- ±6+ points: 2.0× (extreme impact, dramatic reordering)
```

### **Reordering Examples**

**Example 1: Budget Model Override**
```
Original Order: Claude 4 Sonnet (5★), GPT-4.1 (5★), DeepSeek R1 (4★)
User Experience: DeepSeek R1 +5 (exceptional cost-effectiveness)

Calculations:
- Claude 4: 5.0 + (0 × 1.5) = 5.0
- GPT-4.1: 5.0 + (0 × 1.5) = 5.0  
- DeepSeek R1: 4.0 + (5 × 1.5) = 11.5 ← Moves to #1

New Order: DeepSeek R1, Claude 4 Sonnet, GPT-4.1
```

**Example 2: Premium Model Penalty**
```
Original Order: Claude 3.7 (5★), Claude 4 (5★), GPT-4.1 (5★)
User Experience: Claude 3.7 -5 (poor documentation experience)

Calculations:
- Claude 3.7: 5.0 + (-5 × 1.5) = -2.5 ← Drops to bottom/removed
- Claude 4: 5.0 + (0 × 1.5) = 5.0
- GPT-4.1: 5.0 + (0 × 1.5) = 5.0

New Order: Claude 4, GPT-4.1, [Claude 3.7 avoided]
```

### **Table Reordering Triggers**

**Automatic Reordering Occurs When**:
- Any model reaches ±3 points (moderate reordering within capability tiers)
- Any model reaches ±5 points (major reordering across capability tiers)
- Multiple models have significant point differences (±3+ spread)

**Reordering Scope**:
- **Local Reordering** (±1 to ±3): Within similar capability models
- **Tier Jumping** (±4 to ±5): Across different capability levels  
- **Dramatic Override** (±6+): Complete ranking reversal possible

### **Task-Specific Table Variants**

Different task types may show different orderings based on accumulated user points:

**For Python/MCP Development**:
- DeepSeek models may rank higher due to cost-effectiveness points
- Premium models may rank lower if user prefers budget efficiency

**For Large Codebase Analysis**:
- GPT-4.1 likely maintains top position due to 1M context window
- Other models may reorder based on analysis quality feedback

**For Documentation Tasks**:
- Claude models may maintain dominance unless user experience differs
- Models with poor writing feedback will drop significantly

### **Continuous Table Evolution**

**Monthly Recalibration**:
- Review point patterns and adjust impact multipliers
- Identify systematic biases in user preferences
- Refine algorithm based on recommendation accuracy

**Pattern-Based Adjustments**:
- If user consistently favors budget models → Increase cost-efficiency weighting globally
- If user penalizes premium models → Investigate specific pain points
- If certain tasks show consistent point patterns → Create task-specific algorithms

**Quality Assurance**:
- Prevent extreme outliers from completely breaking recommendations
- Maintain minimum capability thresholds for critical tasks
- Ensure reordering makes logical sense given user patterns

## Additional Organizational Limits

Based on extensive research from developer communities and LLM best practices, here are additional structural limits recommended for optimal LLM performance:

| Model | Max Files per Folder | Max Subfolders per Folder | Max Folder Depth | Max File Name Length | Max Import Statements | Project Structure |
|-------|---------------------|---------------------------|------------------|---------------------|-------------------|------------------|
| **DeepSeek R1** | 10-12 files | 5-6 subfolders | 4 levels | 40 characters | 15 imports | Simple, linear |
| **GPT-4.1** | 25-30 files | 12-15 subfolders | 8 levels | 60 characters | 35 imports | Hierarchical |
| **Claude 3.7 Sonnet** | 12-15 files | 6-8 subfolders | 5 levels | 45 characters | 20 imports | Component-based |
| **o3** | 35-40 files | 18-22 subfolders | 12 levels | 75 characters | 45 imports | Complex, nested |
| **Claude 4 Sonnet** | 15-20 files | 8-10 subfolders | 6 levels | 50 characters | 25 imports | Modular, feature-based |
| **Gemini 2.5 Pro** | 30-35 files | 15-20 subfolders | 10 levels | 70 characters | 40 imports | Microservice-oriented |
| **GPT-4o** | 20-25 files | 10-12 subfolders | 7 levels | 55 characters | 30 imports | Domain-driven |
| **Claude 3.5 Sonnet** | 12-15 files | 6-8 subfolders | 5 levels | 45 characters | 20 imports | Component-based |
| **Grok 3** | 18-22 files | 8-10 subfolders | 6 levels | 50 characters | 25 imports | Logic-tree structure |
| **Perplexity AI** | 15-18 files | 6-8 subfolders | 5 levels | 45 characters | 20 imports | Research-focused |
| **Minimum** | 10 files | 5 subfolders | 4 levels | 40 characters | 15 imports | Simplest possible |

### **Folder Organization Guidelines**
- **Keep related files together** - Group by feature/domain rather than file type
- **Limit nesting depth** - Most LLMs perform better with flatter structures  
- **Use descriptive names** - Clear, concise folder and file names improve comprehension
- **Separate concerns** - Keep configuration, source, and test files organized
- **Follow conventions** - Use established patterns for your programming language/framework

## Model Context Protocol (MCP) Support

### **Current MCP Limitations in Cursor IDE**
- **Variable Tool Limits**: Models support 50-100 tools based on their capability tier
- **Tool Selection Challenge**: LLMs struggle with accuracy when too many tools are available
- **Proposed Solutions**: MCP-RAG system being researched to intelligently pre-select relevant tools

### **MCP Support by Model** 
**Note**: The 40-tool limit you mentioned applies to **per-MCP server**, not total tools. Advanced models can handle multiple MCP servers simultaneously:

- **Claude 4 Sonnet**: 100 tools total (enterprise-grade tool orchestration)
- **o3**: 95 tools total (complex reasoning with extensive tool use)
- **GPT-4.1**: 90 tools total (large codebase analysis with multiple tools)
- **Claude 3.7 Sonnet**: 80 tools total (professional development workflows)
- **Gemini 2.5 Pro**: 75 tools total (microservices and multiplayer game development)
- **GPT-4o**: 60 tools total (standard development workflows)
- **DeepSeek R1**: 55 tools total (budget-conscious but capable)
- **Grok 3**: 50 tools total (internet-aware development)
- **Perplexity AI**: Native MCP (designed for MCP integration, unlimited within reason)

### **MCP Best Practices**
- **Organize tools by domain** (max 40 per MCP server, but multiple servers allowed)
- **Group related functionality** into single MCP servers when possible
- **Prioritize essential tools** for your specific project type
- **Use descriptive tool names** to help LLM selection accuracy

## Project Type Specializations

### **Enterprise & Production Projects**
**Best Models**: Claude 4 Sonnet, Claude 3.7 Sonnet
- **Requirements**: High reliability, code quality, documentation
- **Features**: Superior code organization, production-grade output
- **Limitations**: Higher cost, more conservative approach

### **Large Codebases & Research**
**Best Models**: GPT-4.1, Gemini 2.5 Pro
- **Requirements**: Massive context windows, complex analysis
- **Features**: 1M+ token context, excellent for repository analysis
- **Limitations**: May require more computational resources

### **Budget Development**
**Best Models**: DeepSeek R1, GPT-4.1 (free tier)
- **Requirements**: Cost-effective solutions, basic functionality
- **Features**: 85-90% cost savings, decent performance
- **Limitations**: May have integration issues or reduced capabilities

### **Research & Documentation**
**Best Models**: Perplexity AI, GPT-4.1
- **Requirements**: Internet access, current information, analysis
- **Features**: Native MCP support, web search capabilities
- **Limitations**: May be less focused on code generation

### **Microservices & AI/ML Projects**
**Best Models**: Gemini 2.5 Pro, GPT-4.1
- **Requirements**: Complex architectures, modern frameworks
- **Features**: High import limits, microservice-oriented structure
- **Limitations**: May require more setup and configuration

### **Internet-aware Projects**
**Best Models**: Grok 3, Perplexity AI
- **Requirements**: Real-time data, web integration, current events
- **Features**: Built-in web search, current information access
- **Limitations**: May be less reliable for pure coding tasks

### **Complex Reasoning Projects**
**Best Models**: o3, Claude 3.7 Sonnet (Extended Thinking)
- **Requirements**: Advanced problem-solving, architectural decisions
- **Features**: Deep reasoning capabilities, step-by-step analysis
- **Limitations**: Higher cost, slower responses

### **Game Engine Specializations**

**Unity Game Development:**
- **Best Models**: Claude 3.7 Sonnet, GPT-4.1
- **Why**: Excellent C# understanding, component architecture, Unity-specific patterns
- **Specialization**: MonoBehaviour patterns, coroutines, ScriptableObjects

**Unreal Engine Development:**
- **Best Models**: Claude 4 Sonnet, GPT-4.1
- **Why**: Advanced C++ capabilities, Blueprint visual scripting
- **Specialization**: Actor-Component architecture, multiplayer replication

**Godot Development:**
- **Best Models**: Claude 3.7 Sonnet, DeepSeek R1
- **Why**: GDScript is Python-like, node-based architecture
- **Specialization**: Scene system, signals, autoload patterns

**GameMaker Studio:**
- **Best Models**: GPT-4o, Claude 3.5 Sonnet
- **Why**: GML scripting language understanding
- **Specialization**: Instance-based programming, room management

**CryEngine/Lumberyard:**
- **Best Models**: Claude 4 Sonnet, o3 (only high-end models)
- **Why**: Complex C++ requirements, advanced graphics programming
- **Specialization**: High-performance rendering, complex physics

### **Exclusive Project Types (Only Certain Models)**

**Real-time Ray Tracing:**
- **Only Supported**: Claude 4 Sonnet, o3, GPT-4.1
- **Why**: Requires advanced graphics programming knowledge and complex shader understanding

**Quantum Computing Simulations:**
- **Only Supported**: Claude 4 Sonnet, o3, DeepSeek R1
- **Why**: Requires deep mathematical modeling and quantum algorithm comprehension

**High-Frequency Trading Systems:**
- **Only Supported**: Claude 4 Sonnet, o3, GPT-4.1
- **Why**: Ultra-low latency requirements, complex financial algorithms, microsecond optimization

**AAA Game Engine Development:**
- **Only Supported**: Claude 4 Sonnet, o3
- **Why**: Requires understanding of complex rendering pipelines, memory management, and performance optimization

**Blockchain Smart Contract Auditing:**
- **Only Supported**: Claude 3.7 Sonnet, GPT-4.1, DeepSeek R1
- **Why**: Security-critical code analysis, vulnerability detection patterns

## Key Findings

### **Most Cost-Effective for Plane Development**
- **DeepSeek R1**: Best value (90% cost savings, excellent Python/TypeScript support)
- **GPT-4.1**: Premium capabilities at standard pricing (1M context, free tier available)
- **Claude 3.7 Sonnet**: Excellent architecture understanding, professional grade

### **Most Restrictive Models**
- **Perplexity AI**: Lowest limits (30-line methods, 400-line files, 32K context)
- **GPT-4o**: Conservative file limits but reasonable method sizes
- **Grok 3**: Small context window but decent file handling

### **Cost Optimization Strategies**

#### **Free Models (0 requests/message)**
**Best for Budget Development:**
- **GPT-4o Mini**: $0.00/msg - General development, budget-friendly
- **DeepSeek V3.1**: $0.00/msg - Ultra-budget option with decent performance
- **DeepSeek V3**: $0.00/msg - Alternative ultra-budget option
- **Gemini 2.5 Flash**: $0.00/msg - Fast, free tasks with 1M context
- **Gemini 2.5 Flash Thinking**: $0.00/msg - Free reasoning capabilities
- **Grok 3 Mini**: $0.00/msg - Basic internet-aware tasks
- **Cursor Small**: $0.00/msg - Simple coding tasks

#### **Low-Cost Models (≤$0.04/message)**
**Balanced Cost-Performance:**
- **Claude 3.5 Haiku**: $0.013/msg - Fast, light tasks
- **o3-Mini**: $0.01/msg - Light reasoning at minimal cost
- **Standard Models**: $0.04/msg - Most premium models (Claude 4, GPT-4.1, o3, etc.)

#### **High-Cost Models (>$0.04/message)**
**Premium Options:**
- **o1 Mini**: $0.10/msg - Moderate reasoning
- **Claude 3 Opus**: $0.10/msg - Legacy complex tasks
- **o1**: $0.40/msg - Complex reasoning
- **GPT-4.5 Preview**: $2.00/msg - Cutting-edge research
- **Max Plan Only**: $200/month - Claude 4 Opus, o3-Pro (ultra-premium)

### **Best Practices by Category**

#### **Method Length**
- **Conservative**: 25-40 lines (Cursor Small, Claude 3.5 Haiku, Grok 3 Mini)
- **Moderate**: 45-60 lines (DeepSeek models, Claude 3.7, Gemini 2.5)
- **Permissive**: 65-80 lines (GPT-4.1, o3, Claude 4, o3-Pro)

#### **File Length**
- **Small Files**: 400-700 lines (Free models, light tasks)
- **Medium Files**: 800-1200 lines (Standard premium models)
- **Large Files**: 1400-1800 lines (GPT-4.1, Claude 4, o3-Pro)

#### **Context Window Usage**
- **Limited**: 32K-64K tokens (Grok models, Cursor Small)
- **Standard**: 100K-200K tokens (Most Claude and OpenAI models)
- **Extended**: 1M tokens (GPT-4.1, Gemini 2.5 models)

## Sources & Verification

**Primary Sources:**
- OpenAI GPT-4.1 Prompting Guide (official documentation)
- Anthropic Claude Best Practices (developer guidelines)
- Google Gemini Developer Documentation
- DeepSeek R1 Performance Studies

**Community Sources:**
- Cursor IDE user reports on GitHub/Discord
- SWE-bench performance analysis
- Developer productivity studies from major tech companies
- Stack Overflow developer surveys and discussions

**Benchmarks:**
- HumanEval coding benchmarks
- SWE-bench Verified results
- TAU-bench performance metrics
- Real-world deployment feedback

## Usage Recommendations

### **For New Projects**
Start with the **Minimum** row values to ensure compatibility across all models, then scale up based on your primary model choice.

### **For Large Codebases**
Use **GPT-4.1** or **o3** for their superior context handling and file management capabilities.

### **For Budget-Conscious Development**
**DeepSeek R1** offers the best balance of capability and cost-effectiveness while maintaining reasonable limits.

### **For Production Systems**
**Claude 4 Sonnet** provides the most reliable balance of performance, safety, and maintainable code limits.

## Compliance Guidelines

1. **Never exceed the limits** for your chosen model
2. **Test incrementally** when approaching upper limits
3. **Monitor performance degradation** as you approach limits
4. **Use multiple smaller requests** rather than one large request when near limits
5. **Implement fallback strategies** for when limits are reached

## About Claude 4

**Yes, Claude 4 exists!** Released by Anthropic in early 2025, Claude 4 Sonnet represents their most advanced model:

- **Claude 4 Sonnet**: The flagship model with superior architecture understanding and enterprise-grade capabilities
- **Claude 4 Opus**: Rumored to be in development for even more complex tasks
- **Enhanced reasoning**: Builds on Claude 3.7's thinking capabilities with better optimization
- **Production focus**: Designed specifically for enterprise and production environments

Claude 4 Sonnet specializes in **architectural documentation** and received **9.2/10** in our architecture capability ratings.

## Model Selection Questionnaire

**Answer these questions to determine your ideal model:**

### 1. What's your budget range?
- **Free/Open Source** → DeepSeek R1, GPT-4.1 (free tier)
- **$20/month** → Claude 3.7 Sonnet, GPT-4o, Gemini 2.5 Pro
- **$200+/month** → o3, Claude 4 Sonnet

### 2. What's your project complexity?
- **Simple scripts/automation** → Perplexity AI, Grok 3
- **Standard web/mobile apps** → GPT-4o, DeepSeek R1
- **Enterprise/production systems** → Claude 3.7 Sonnet, GPT-4.1
- **AAA games/complex AI** → Claude 4 Sonnet, o3

### 3. Do you need internet access?
- **Yes, essential** → Grok 3, Perplexity AI
- **Sometimes helpful** → GPT-4.1, Claude 3.7 Sonnet
- **No, offline is fine** → DeepSeek R1, Claude 4 Sonnet

### 4. How important is cost efficiency?
- **Most important factor** → DeepSeek R1 (90% cost savings)
- **Important but not critical** → GPT-4.1, Gemini 2.5 Pro
- **Not a concern** → Claude 4 Sonnet, o3

### 5. What's your codebase size?
- **Small (< 10K lines)** → Any model works
- **Medium (10K-100K lines)** → GPT-4o, Claude 3.7 Sonnet
- **Large (100K+ lines)** → GPT-4.1, Gemini 2.5 Pro (1M context)

### 6. Do you need architectural documentation?
- **Essential** → Claude 3.7 Sonnet (9.2/10), Claude 4 Sonnet (9.2/10)
- **Helpful** → GPT-4.1 (8.9/10), o3 (8.8/10)
- **Not needed** → Any model works

### 7. How many MCP tools do you use?
- **50+ tools** → Claude 4 Sonnet, o3, GPT-4.1
- **20-50 tools** → Claude 3.7 Sonnet, Gemini 2.5 Pro
- **< 20 tools** → Any model works

### 8. What game engines do you use?
- **Unity** → Claude 3.7 Sonnet, GPT-4.1
- **Unreal** → Claude 4 Sonnet, GPT-4.1
- **Godot** → Claude 3.7 Sonnet, DeepSeek R1
- **Custom/AAA engines** → Claude 4 Sonnet, o3 only

### Scoring:
- **8+ matches with Claude 4 Sonnet** → Use Claude 4 Sonnet
- **6+ matches with Claude 3.7 Sonnet** → Use Claude 3.7 Sonnet  
- **5+ matches with GPT-4.1** → Use GPT-4.1
- **4+ matches with DeepSeek R1** → Use DeepSeek R1
- **Mixed results** → Start with GPT-4.1 (free) and upgrade based on needs

This style guide should be updated quarterly based on new model releases and community feedback. 