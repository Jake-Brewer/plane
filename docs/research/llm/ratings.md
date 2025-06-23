# LLM Ratings and Comparison for Cursor IDE

This document provides a comprehensive overview of the Large Language Models (LLMs) available out-of-the-box in Cursor IDE, along with their characteristics and performance ratings.


## Cost Analysis: Cursor vs Direct API

| Model | Cursor Cost (Normal) | Cursor Cost (Max) | Direct API Cost | Cursor Cost (API Key) | Notes |
|-------|---------------------|-------------------|----------------|---------------------|-------|
| **Claude 4 Sonnet** | 1 req/msg | 90/450 req/MTok | $3/$15 per MTok | Same as API | 20% markup in Cursor |
| **Claude 3.7 Sonnet** | 1 req/msg | 90/450 req/MTok | $3/$15 per MTok | Same as API | 20% markup in Cursor |
| **Claude 3.5 Sonnet** | 1 req/msg | 90/450 req/MTok | $3/$15 per MTok | Same as API | 20% markup in Cursor |
| **GPT-4.1** | 1 req/msg | 60/240 req/MTok | $2.50/$10 per MTok | Same as API | 20% markup in Cursor |
| **GPT-4o** | 1 req/msg | 75/300 req/MTok | $2.50/$10 per MTok | Same as API | 20% markup in Cursor |
| **o3** | 1 req/msg | 60/240 req/MTok | $15/$60 per MTok | Same as API | Premium reasoning model |
| **Gemini 2.5 Pro** | 1 req/msg | 37.5/300 req/MTok | $1.25/$5 per MTok | Same as API | Variable pricing |
| **Gemini 2.5 Flash** | Free | 4.5/105 req/MTok | $0.075/$0.30 per MTok | Same as API | Free in Cursor |
| **DeepSeek R1** | 1 req/msg | N/A | $0.14/$2.19 per MTok | Same as API | 85-90% cost savings |
| **Grok 3 Beta** | 1 req/msg | 90/450 req/MTok | $2/$10 per MTok | Same as API | Internet-aware AI |
| **Perplexity AI** | Via MCP | Via MCP | $1/$3 per MTok | Same as API | Research integration |

**Cost Definitions:**
- **Cursor Cost (Normal)**: Fixed requests per message in Normal mode
- **Cursor Cost (Max)**: Token-based pricing in Max mode (input/output per million tokens)
- **Direct API Cost**: Provider's official API pricing (input/output per million tokens)
- **Cursor Cost (API Key)**: Cost when using your own API key in Cursor (same as direct API)

## Built-in LLM Models

| Model | Provider | Cost Tier | Context Window | Performance Rating | Strengths | Limitations | Notes |
|-------|----------|-----------|----------------|-------------------|-----------|-------------|--------|
| **Claude 3.7 Sonnet** | Anthropic | Premium | 128K tokens | ⭐⭐⭐⭐⭐ | Superior code organization, excellent instruction following, production-grade output | Limited web search capability | Latest model (Feb 2025), best for code quality |
| **Claude 3.7 Sonnet Thinking** | Anthropic | Premium | 128K tokens | ⭐⭐⭐⭐⭐ | Deep reasoning, step-by-step analysis, complex problem solving | Slower responses, higher cost | Extended reasoning mode |
| **GPT-4.1** | OpenAI | Free/Premium | 1M tokens | ⭐⭐⭐⭐⭐ | Massive context window, strong coding performance, up-to-date knowledge | Newer model, less tested | Latest model (Apr 2025), free access |
| **GPT-4.5** | OpenAI | Usage-based | Large | ⭐⭐⭐⭐ | Very capable, handles complex tasks | Expensive ($2/request) | Premium model, high cost |
| **Claude 3.5 Sonnet** | Anthropic | Premium | 200K tokens | ⭐⭐⭐⭐ | Reliable performance, good code generation | Superseded by 3.7 | Previous generation | 
| **GPT-4o** | OpenAI | Premium | 128K tokens | ⭐⭐⭐⭐ | Fast responses, multimodal capabilities | Smaller context vs GPT-4.1 | Standard model |
| **GPT-4o mini** | OpenAI | Free/Low-cost | 128K tokens | ⭐⭐⭐ | Fast, cost-effective | Reduced capabilities | Good for simple tasks |
| **Gemini 2.5 Pro** | Google | Premium | Large | ⭐⭐⭐⭐ | Strong performance, good feature completion | Less code-focused | Well-rounded model |
| **DeepSeek V3.1** | DeepSeek | Premium | Large | ⭐⭐ | Cost-effective | Integration issues, bugs reported | Unstable integration |
| **Grok 3 Beta** | X (Twitter) | Premium | Large | ⭐⭐⭐ | Uses modern frameworks, lower code output | Multiple bugs, beta quality | Still in development |

## Performance Categories

### 🏆 **Top Tier (Best for Production)**
- **Claude 3.7 Sonnet** - Best overall for code quality and organization
- **GPT-4.1** - Best for large codebase analysis with massive context window
- **Claude 3.7 Sonnet Thinking** - Best for complex problem-solving

### 🥈 **High Performance**
- **GPT-4.5** - Excellent but expensive
- **Claude 3.5 Sonnet** - Reliable workhorse
- **GPT-4o** - Good all-around performance
- **Gemini 2.5 Pro** - Strong feature completion

### 🥉 **Standard/Budget**
- **GPT-4o mini** - Good for simple tasks, cost-effective
- **Grok 3 Beta** - Promising but buggy
- **DeepSeek V3.1** - Potential but unstable

## Cost Analysis

| Cost Tier | Models | Typical Use Case |
|-----------|--------|------------------|
| **Free** | GPT-4.1, GPT-4o mini | Learning, experimentation |
| **Premium Subscription** | Claude 3.7, GPT-4o, Gemini 2.5 Pro | Professional development |
| **Usage-based** | GPT-4.5 | Specialized/complex tasks |

## Recommendations

### For New Users
- Start with **GPT-4.1** (free access, large context)
- Upgrade to **Claude 3.7 Sonnet** for professional work

### For Professional Development
- **Claude 3.7 Sonnet** for code quality and organization
- **Claude 3.7 Sonnet Thinking** for complex architectural decisions
- **GPT-4.1** for large codebase analysis

### For Budget-Conscious Users
- **GPT-4o mini** for basic tasks
- **GPT-4.1** for advanced features without premium cost

## Model Selection Guide

**Choose Claude 3.7 Sonnet when:**
- Code quality and organization are critical
- Working on production applications
- Need clean, maintainable code output

**Choose GPT-4.1 when:**
- Working with large codebases
- Need extensive context understanding
- Budget is a concern (free tier available)

**Choose Claude 3.7 Sonnet Thinking when:**
- Solving complex architectural problems
- Need deep reasoning and analysis
- Time is less critical than quality

---

*Last Updated: January 2025*
*Based on Cursor IDE built-in model support* 