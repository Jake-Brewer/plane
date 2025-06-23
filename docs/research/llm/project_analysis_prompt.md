# Project Analysis Model Recommendation Prompt

**Recommended LLM for this prompt: Claude 4 Sonnet**  
*Reasoning: This task requires complex multi-variable analysis, cost optimization calculations, and detailed project assessment. Claude 4 Sonnet excels at structured reasoning, handles enterprise-level complexity well, and provides reliable recommendations with clear explanations. Its superior code organization understanding and architectural analysis capabilities make it ideal for project evaluation tasks.*

---

## The Prompt

You are an expert AI model selection consultant specializing in cost-optimized project analysis for Cursor IDE. Your task is to analyze a given project's characteristics and recommend the most cost-effective LLM model for conducting analysis on that project, considering technical requirements, budget constraints, and user sentiment preferences.

### Your Knowledge Base

**Available Analysis Models in Cursor IDE (2025):**

| Model | Cost/Message | Max Method | Max File | Context Window | Concurrent Files | MCP Tools | User Rating | Best For |
|-------|--------------|------------|----------|----------------|------------------|-----------|-------------|----------|
| **Free Models (0 requests/message)** |
| **GPT-4o Mini** | $0.00 | 35 lines | 600 lines | 128K tokens | 8 files | 40 tools | ⭐⭐⭐ | Budget development |
| **DeepSeek V3.1** | $0.00 | 45 lines | 800 lines | 128K tokens | 12 files | 45 tools | ⭐⭐⭐ | Ultra-budget projects |
| **DeepSeek V3** | $0.00 | 45 lines | 800 lines | 128K tokens | 12 files | 45 tools | ⭐⭐⭐ | Ultra-budget projects |
| **Gemini 2.5 Flash** | $0.00 | 40 lines | 600 lines | 1M tokens | 15 files | 50 tools | ⭐⭐⭐ | Fast, free analysis |
| **Gemini 2.5 Flash Thinking** | $0.00 | 40 lines | 600 lines | 1M tokens | 15 files | 50 tools | ⭐⭐⭐ | Free reasoning |
| **Grok 3 Mini** | $0.00 | 30 lines | 500 lines | 32K tokens | 6 files | 30 tools | ⭐⭐ | Basic internet tasks |
| **Cursor Small** | $0.00 | 25 lines | 400 lines | 32K tokens | 5 files | 20 tools | ⭐⭐ | Simple tasks |
| **Low-Cost Models** |
| **o3-Mini** | $0.01 | 45 lines | 700 lines | 128K tokens | 10 files | 40 tools | ⭐⭐⭐ | Light reasoning |
| **Claude 3.5 Haiku** | $0.013 | 40 lines | 700 lines | 100K tokens | 8 files | 50 tools | ⭐⭐⭐ | Fast, light tasks |
| **Standard Models** |
| **Claude 4 Sonnet** | $0.04 | 70 lines | 1500 lines | 200K tokens | 20 files | 100 tools | ⭐⭐⭐⭐⭐ | Enterprise, AAA games |
| **Claude 3.7 Sonnet** | $0.04 | 60 lines | 1200 lines | 200K tokens | 15 files | 80 tools | ⭐⭐⭐⭐⭐ | Professional development |
| **GPT-4.1** | $0.04 | 65 lines | 1400 lines | 1M tokens | 30 files | 90 tools | ⭐⭐⭐⭐⭐ | Large codebases |
| **o3** | $0.04 | 75 lines | 1600 lines | 128K tokens | 25 files | 95 tools | ⭐⭐⭐⭐⭐ | Advanced reasoning |
| **DeepSeek R1** | $0.04 | 50 lines | 900 lines | 128K tokens | 15 files | 55 tools | ⭐⭐⭐⭐ | Budget development |
| **High-Cost Models** |
| **o1 Mini** | $0.10 | 50 lines | 800 lines | 128K tokens | 12 files | 50 tools | ⭐⭐⭐ | Moderate reasoning |
| **o1** | $0.40 | 65 lines | 1200 lines | 128K tokens | 20 files | 80 tools | ⭐⭐⭐⭐ | Complex reasoning |

### Analysis Framework

When evaluating a project for model selection, consider these factors:

1. **Technical Requirements Assessment**
   - Average method length in the codebase
   - Average file length and largest files
   - Total number of files in project
   - Maximum concurrent files needed for analysis
   - Import complexity and dependencies
   - Required context window size

2. **Project Characteristics**
   - Project type (Web, Enterprise, Mobile, Game, etc.)
   - Programming languages and frameworks
   - Architecture patterns used
   - Codebase complexity level (0.0-1.0 scale)

3. **Analysis Requirements**
   - Analysis depth needed (shallow/medium/deep)
   - Frequency of analysis (times per month)
   - Reasoning requirements
   - Internet access needs
   - MCP tool requirements

4. **Budget & Quality Constraints**
   - Monthly budget limit
   - Minimum quality threshold (1-5 stars)
   - Maximum cost per analysis
   - User preference for free vs. paid models

5. **Scoring Methodology**
   - Cost efficiency (lower cost = higher score)
   - Performance capability (analysis quality + reasoning)
   - User sentiment rating
   - Project type specialization match
   - Technical requirement compatibility

### Output Format

Provide your analysis in this structured format:

```markdown
# Project Analysis & Model Recommendation

## Project Assessment Summary
**Project Type:** [Identified project type]
**Complexity Level:** [Low/Medium/High] (0.0-1.0 scale)
**Technical Requirements:**
- Average method length: X lines
- Average file length: X lines  
- Total files: X
- Context window needed: X tokens
- Concurrent analysis files: X
- MCP tools needed: X

## Model Compatibility Analysis

### ✅ Suitable Models
[List models that meet technical requirements with brief reasoning]

### ❌ Eliminated Models  
[List models that don't meet requirements and why]

## Cost-Benefit Analysis

### 🏆 RECOMMENDED MODEL: [MODEL NAME]
**Monthly Cost:** $X.XX (based on Y analyses/month)
**Cost per Analysis:** $X.XX
**Quality Rating:** ⭐⭐⭐⭐⭐
**Confidence Score:** X/10

**Why This Model:**
- [Primary reason 1]
- [Primary reason 2]  
- [Primary reason 3]

### Alternative Options:
1. **[Second Choice]** - $X.XX/month - [Brief reasoning]
2. **[Third Choice]** - $X.XX/month - [Brief reasoning]

## Optimization Opportunities

### Cost Savings Strategies:
- [Strategy 1 with potential savings]
- [Strategy 2 with potential savings]

### Hybrid Approach (if applicable):
- **Routine Analysis:** [Cheaper model] for 80% of tasks
- **Complex Analysis:** [Premium model] for 20% of tasks
- **Estimated Savings:** $X.XX/month

## Risk Assessment & Considerations
- [Any limitations or concerns]
- [Scalability considerations]
- [Alternative scenarios to consider]

## Final Recommendation Summary
**Model:** [Recommended model]
**Monthly Budget:** $X.XX
**Expected Quality:** [Quality level]
**Confidence Level:** [High/Medium/Low]
**Next Steps:** [Actionable recommendations]
```

### Example Analysis

**Sample Project Input:**
```
Project Details:
- React/TypeScript web application
- Node.js backend with Express
- 150 total files
- Average method length: 45 lines
- Average file length: 800 lines
- Need to analyze 5-8 files simultaneously
- 25 imports per file on average
- Analysis frequency: 15 times per month
- Budget limit: $10/month
- Quality threshold: 4+ stars
- Analysis depth: Medium to deep
- Project type: Professional web development
```

Now analyze this project and provide your structured recommendation.

---

## How to Use This Prompt

### Step 1: Prepare Project Information
Gather these details about your project:
- **Codebase metrics** (file counts, line counts, complexity)
- **Technical requirements** (context needs, concurrent analysis)
- **Budget constraints** (monthly limit, cost per analysis)
- **Quality requirements** (minimum rating, analysis depth)
- **Usage patterns** (frequency, project type)

### Step 2: Submit to Claude 4 Sonnet
1. Copy the entire prompt above
2. Add your specific project details at the end
3. Submit to Claude 4 Sonnet for analysis
4. Review the structured recommendation

### Step 3: Implement Recommendation
- Set up the recommended model in Cursor
- Monitor actual costs vs. estimates
- Adjust analysis frequency if needed
- Consider hybrid approaches for optimization

### Why Claude 4 Sonnet for This Task?

**Claude 4 Sonnet excels at:**
- **Complex multi-variable analysis** across 30+ models and 15+ criteria
- **Structured decision-making** with clear reasoning chains
- **Enterprise-level project assessment** and architectural understanding
- **Cost optimization calculations** with accurate trade-off analysis
- **Risk assessment** and scenario planning
- **Clear, actionable recommendations** with confidence scoring

**Alternative Model Options:**
- **GPT-4.1**: Better for very large codebases (1M+ token context needs)
- **Claude 3.7 Sonnet**: Good alternative if Claude 4 unavailable
- **o3**: Best for projects requiring deep reasoning analysis

### Pro Tips for Better Results

1. **Be Specific with Metrics**: Provide exact numbers for file sizes, method lengths, etc.
2. **Include Context**: Mention team size, experience level, and project timeline
3. **Budget Clarity**: Specify both hard limits and preferred spending ranges
4. **Quality Standards**: Be clear about minimum acceptable quality levels
5. **Usage Patterns**: Estimate realistic analysis frequency and complexity
6. **Future Planning**: Consider how requirements might change as project grows

This prompt will help you make data-driven, cost-optimized decisions about which LLM model to use for analyzing your specific project while balancing cost, quality, and technical requirements. 