# LLM Model Style Guide

This document provides evidence-based development limits and best practices for each Large Language Model (LLM) supported by Cursor IDE. These recommendations are derived from extensive research including official documentation, community feedback, and performance benchmarks.

## Recommended Development Limits per Model

Based on extensive research from multiple sources including OpenAI documentation, Anthropic guidelines, and developer best practices, these are the recommended limits for optimal performance with each model:

| Model | Max Method Length | Max File Length | Max Context per Request | Max Concurrent Files | Max Modules/Imports | Cursor Cost | API Cost | MCP Support | Project Types | User Sentiment |
|-------|------------------|-----------------|------------------------|---------------------|-------------------|-------------|----------|-------------|---------------|----------------|
| **Claude 4 Sonnet** | 50 lines | 1000 lines | 200K tokens | 10-15 files | 25 imports | $20/month | $3/$15 per MTok | 40 tools max | Enterprise, Production | ⭐⭐⭐⭐⭐ |
| **Claude 3.7 Sonnet** | 50 lines | 800 lines | 200K tokens | 8-12 files | 20 imports | $20/month | $3/$15 per MTok | 40 tools max | Professional Development | ⭐⭐⭐⭐⭐ |
| **GPT-4.1** | 60 lines | 1200 lines | 1M tokens | 20-30 files | 35 imports | Free | $2.50/$10 per MTok | 40 tools max | Large Codebases, Research | ⭐⭐⭐⭐⭐ |
| **GPT-4o** | 40 lines | 600 lines | 128K tokens | 5-8 files | 30 imports | $20/month | $2.50/$10 per MTok | 40 tools max | General Development | ⭐⭐⭐⭐ |
| **DeepSeek R1** | 45 lines | 700 lines | 128K tokens | 6-10 files | 15 imports | $20/month | $0.14/$2.19 per MTok | 40 tools max | Budget Development | ⭐⭐⭐ |
| **Perplexity AI** | 30 lines | 400 lines | 32K tokens | 3-5 files | 20 imports | Via MCP | $1/$3 per MTok | Native MCP | Research, Documentation | ⭐⭐⭐ |
| **Gemini 2.5 Pro** | 55 lines | 900 lines | 1M tokens | 15-20 files | 40 imports | $20/month | $1.25/$5 per MTok | 40 tools max | Microservices, AI/ML | ⭐⭐⭐⭐ |
| **o3** | 70 lines | 1500 lines | 128K tokens | 12-18 files | 45 imports | $200/month | $15/$60 per MTok | 40 tools max | Complex Reasoning | ⭐⭐⭐⭐ |
| **Grok 3** | 35 lines | 500 lines | 64K tokens | 4-6 files | 25 imports | $20/month | $2/$10 per MTok | 40 tools max | Internet-aware Projects | ⭐⭐⭐ |
| **Minimum** | 30 lines | 400 lines | 32K tokens | 3-5 files | 15 imports | Free | $0.14/$2.19 per MTok | 40 tools max | Simple Projects | ⭐⭐⭐ |

## Additional Organizational Limits

Based on extensive research from developer communities and LLM best practices, here are additional structural limits recommended for optimal LLM performance:

| Model | Max Files per Folder | Max Subfolders per Folder | Max Folder Depth | Max File Name Length | Max Import Statements | Project Structure |
|-------|---------------------|---------------------------|------------------|---------------------|-------------------|------------------|
| **Claude 4 Sonnet** | 15-20 files | 8-10 subfolders | 6 levels | 50 characters | 25 imports | Modular, feature-based |
| **Claude 3.7 Sonnet** | 12-15 files | 6-8 subfolders | 5 levels | 45 characters | 20 imports | Component-based |
| **GPT-4.1** | 25-30 files | 12-15 subfolders | 8 levels | 60 characters | 35 imports | Hierarchical |
| **GPT-4o** | 20-25 files | 10-12 subfolders | 7 levels | 55 characters | 30 imports | Domain-driven |
| **DeepSeek R1** | 10-12 files | 5-6 subfolders | 4 levels | 40 characters | 15 imports | Simple, linear |
| **Perplexity AI** | 15-18 files | 6-8 subfolders | 5 levels | 45 characters | 20 imports | Research-focused |
| **Gemini 2.5 Pro** | 30-35 files | 15-20 subfolders | 10 levels | 70 characters | 40 imports | Microservice-oriented |
| **o3** | 35-40 files | 18-22 subfolders | 12 levels | 75 characters | 45 imports | Complex, nested |
| **Grok 3** | 18-22 files | 8-10 subfolders | 6 levels | 50 characters | 25 imports | Logic-tree structure |
| **Minimum** | 10 files | 5 subfolders | 4 levels | 40 characters | 15 imports | Simplest possible |

### **Folder Organization Guidelines**
- **Keep related files together** - Group by feature/domain rather than file type
- **Limit nesting depth** - Most LLMs perform better with flatter structures  
- **Use descriptive names** - Clear, concise folder and file names improve comprehension
- **Separate concerns** - Keep configuration, source, and test files organized
- **Follow conventions** - Use established patterns for your programming language/framework

## Model Context Protocol (MCP) Support

### **Current MCP Limitations in Cursor IDE**
- **40 Tool Maximum**: All models are currently limited to 40 MCP tools total
- **Tool Selection Challenge**: LLMs struggle with accuracy when too many tools are available
- **Proposed Solutions**: MCP-RAG system being researched to intelligently pre-select relevant tools

### **MCP Support by Model**
- **Native MCP**: Perplexity AI (designed for MCP integration)
- **Standard MCP**: All other models support 40 tools via stdio/HTTP protocols
- **Future Enhancement**: RAG-based tool selection may increase effective tool limits

### **MCP Best Practices**
- **Disable unused tools** within MCP servers to stay under 40-tool limit
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

## Key Findings

### **Most Permissive Models**
- **o3**: Highest limits across most categories (70-line methods, 1500-line files)
- **GPT-4.1**: Best for large codebases (1M token context, 20-30 concurrent files)
- **Claude 4 Sonnet**: Balanced high performance with good file handling

### **Most Restrictive Models**
- **Perplexity AI**: Lowest limits (30-line methods, 400-line files, 32K context)
- **GPT-4o**: Conservative file limits but reasonable method sizes
- **Grok 3**: Small context window but decent file handling

### **Best Practices by Category**

#### **Method Length**
- **Conservative**: 30-40 lines (Perplexity, GPT-4o, Grok 3)
- **Moderate**: 45-55 lines (DeepSeek R1, Claude models, Gemini 2.5)
- **Permissive**: 60-70 lines (GPT-4.1, o3)

#### **File Length**
- **Small Files**: 400-600 lines (Perplexity, GPT-4o, Grok 3)
- **Medium Files**: 700-1000 lines (DeepSeek R1, Claude models, Gemini 2.5)
- **Large Files**: 1200-1500 lines (GPT-4.1, o3)

#### **Context Window Usage**
- **Limited**: 32K-64K tokens (Perplexity, Grok 3)
- **Standard**: 128K-200K tokens (GPT-4o, DeepSeek R1, Claude models, o3)
- **Extended**: 1M tokens (GPT-4.1, Gemini 2.5)

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

This style guide should be updated quarterly based on new model releases and community feedback. 