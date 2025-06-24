# LLM Model Selection Guide for Plane Development
# Last Updated: 2025-06-24T00:00:00Z

**PREREQUISITE**: Read `_llm_primer.md` first for core behavioral standards

## Quick Navigation
- **Core Behavioral Standards** → `_llm_primer.md`
- **Project Context** → `_llm_project_primer.md`
- **MCP Server Management** → `_llm_cursor_mcp_management.md`
- **Port Management** → `_llm_port_management.md`
- **Documentation Standards** → `_llm_documentation_management.md`
- **Detailed Model Comparison** → `docs/research/llm/model_style_guide.md`

---

## 🎯 Plane-Specific Model Recommendations

### **Top 3 Models for Plane Development** (Sorted by Value)

#### 1. **DeepSeek R1** - Best Overall Value ⭐⭐⭐⭐⭐
- **Cost**: $0.04/msg (90% cost savings vs premium models)
- **Strengths**: Excellent Python/TypeScript support, FastAPI expertise, Docker awareness
- **Perfect For**: MCP server development, Django REST API work, budget-conscious development
- **Plane Use Cases**: Building our Python MCP server, API endpoint proxying, metrics collection
- **Limits**: 50-line methods, 900-line files, 10-15 concurrent files

#### 2. **GPT-4.1** - Best for Large Codebases ⭐⭐⭐⭐⭐
- **Cost**: $0.04/msg (free tier available)
- **Strengths**: 1M token context, excellent for repository analysis, superior file handling
- **Perfect For**: Understanding the entire Plane codebase, complex refactoring, architectural decisions
- **Plane Use Cases**: Analyzing Plane's Django backend, Next.js frontend integration, database schema understanding
- **Limits**: 65-line methods, 1400-line files, 25-30 concurrent files

#### 3. **Claude 3.7 Sonnet** - Best for Architecture ⭐⭐⭐⭐⭐
- **Cost**: $0.04/msg
- **Strengths**: Superior architectural documentation (9.2/10 rating), professional-grade output
- **Perfect For**: System design, API architecture, production-ready code
- **Plane Use Cases**: Designing MCP server architecture, API endpoint organization, documentation generation
- **Limits**: 60-line methods, 1200-line files, 12-15 concurrent files

---

## 🔧 Task-Specific Model Selection

### **MCP Server Development** (Python FastAPI)
**Primary Choice**: **DeepSeek R1**
- Excellent Python understanding
- FastAPI framework expertise
- Docker container awareness
- Cost-effective for iterative development
- **Alternative**: GPT-4.1 for complex architectural decisions

### **Plane API Integration** (Django REST Framework)
**Primary Choice**: **GPT-4.1**
- Large context window for understanding Django codebase
- Excellent API design patterns
- Superior database schema comprehension
- **Alternative**: Claude 3.7 Sonnet for architectural documentation

### **Frontend Integration** (Next.js/React/TypeScript)
**Primary Choice**: **Claude 3.7 Sonnet**
- Superior TypeScript understanding
- React component architecture expertise
- Next.js routing and API routes
- **Alternative**: GPT-4.1 for large component refactoring

### **Docker & DevOps** (Container Management)
**Primary Choice**: **DeepSeek R1**
- Excellent Docker Compose understanding
- Port management and networking
- Environment configuration
- **Alternative**: GPT-4.1 for complex multi-container orchestration

### **Documentation & Guides** (Technical Writing)
**Primary Choice**: **Claude 3.7 Sonnet**
- Superior documentation generation (9.2/10 rating)
- Clear, professional writing style
- Comprehensive API documentation
- **Alternative**: GPT-4.1 for large-scale documentation projects

### **Database & Migrations** (PostgreSQL/Django)
**Primary Choice**: **GPT-4.1**
- Excellent database schema understanding
- Django migration expertise
- Large context for complex queries
- **Alternative**: Claude 3.7 Sonnet for migration documentation

### **Performance & Optimization** (System Tuning)
**Primary Choice**: **o3**
- Advanced reasoning for performance analysis
- Complex optimization strategies
- **Alternative**: GPT-4.1 for large-scale performance analysis

---

## 💰 Budget-Based Recommendations

### **Free/Ultra-Budget** ($0/month)
1. **DeepSeek V3.1** (FREE) - Ultra-budget option with decent Python support
2. **GPT-4o Mini** (FREE) - General development, limited capabilities
3. **Gemini 2.5 Flash** (FREE) - Fast tasks with 1M context window

**Best For**: Learning, experimentation, simple scripting
**Limitations**: Reduced capabilities, smaller context windows, fewer MCP tools

### **Standard Budget** ($20/month - Cursor Pro)
1. **DeepSeek R1** ($0.04/msg) - Best value for professional development
2. **GPT-4.1** ($0.04/msg) - Premium capabilities at standard pricing
3. **Claude 3.7 Sonnet** ($0.04/msg) - Professional architecture work

**Best For**: Professional Plane development, MCP server work, production systems
**Sweet Spot**: Optimal balance of capability and cost

### **Premium Budget** ($200/month - Cursor Ultra)
1. **Claude 4 Opus** (Max Plan Only) - Ultra-complex projects
2. **o3-Pro Thinking** (Max Plan Only) - Advanced reasoning
3. **All standard models** with higher request limits

**Best For**: Enterprise development, complex architectural decisions, unlimited usage

---

## 🎯 Decision Tree

### Start Here: What's Your Primary Goal?

#### **Building the Plane MCP Server** (Python FastAPI)
```
Budget Matters? 
├─ YES → DeepSeek R1 (90% cost savings, excellent Python)
└─ NO → Claude 3.7 Sonnet (superior architecture, professional grade)
```

#### **Understanding Plane Codebase** (Analysis & Research)
```
Codebase Size?
├─ Large (100K+ lines) → GPT-4.1 (1M context window)
├─ Medium (10K-100K) → Claude 3.7 Sonnet (architectural understanding)
└─ Small (<10K) → DeepSeek R1 (cost-effective)
```

#### **API Development** (REST endpoints, integration)
```
Complexity Level?
├─ High (Complex business logic) → Claude 3.7 Sonnet
├─ Medium (Standard CRUD) → GPT-4.1 or DeepSeek R1
└─ Low (Simple endpoints) → DeepSeek R1
```

#### **Documentation & Guides** (Technical writing)
```
Documentation Type?
├─ Architectural (System design) → Claude 3.7 Sonnet (9.2/10 rating)
├─ API Reference (Endpoints) → GPT-4.1 (comprehensive coverage)
└─ User Guides (How-to) → DeepSeek R1 (clear, concise)
```

#### **DevOps & Infrastructure** (Docker, deployment)
```
Infrastructure Complexity?
├─ Complex (Multi-container, orchestration) → GPT-4.1
├─ Medium (Docker Compose, networking) → DeepSeek R1
└─ Simple (Single container) → DeepSeek R1
```

---

## 📊 Model Comparison Matrix

### **For Plane Development Tasks**

| Task | DeepSeek R1 | GPT-4.1 | Claude 3.7 | Claude 4 | o3 | User Assigned Points |
|------|-------------|---------|-------------|----------|-----|---------------------|
| **Python MCP Server** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | DeepSeek R1: +1, GPT-4.1: +1, Claude 3.7: +1, Claude 4: +1, o3: +1 |
| **Django API Work** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | DeepSeek R1: +1, GPT-4.1: +1, Claude 3.7: +1, Claude 4: +1, o3: +1 |
| **Next.js Frontend** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | DeepSeek R1: +1, GPT-4.1: +1, Claude 3.7: +1, Claude 4: +1, o3: +1 |
| **Docker/DevOps** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | DeepSeek R1: +1, GPT-4.1: +1, Claude 3.7: +1, Claude 4: +1, o3: +1 |
| **Documentation** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | DeepSeek R1: +1, GPT-4.1: +1, Claude 3.7: +1, Claude 4: +1, o3: +1 |
| **Cost Efficiency** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | DeepSeek R1: +1, GPT-4.1: +1, Claude 3.7: +1, Claude 4: +1, o3: +1 |
| **Large Codebase** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | DeepSeek R1: +1, GPT-4.1: +1, Claude 3.7: +1, Claude 4: +1, o3: +1 |
| **MCP Tools** | ⭐⭐⭐ (55) | ⭐⭐⭐⭐ (90) | ⭐⭐⭐⭐ (80) | ⭐⭐⭐⭐⭐ (100) | ⭐⭐⭐⭐ (95) | DeepSeek R1: +1, GPT-4.1: +1, Claude 3.7: +1, Claude 4: +1, o3: +1 |

### **User Assigned Points System**

**Purpose**: Track your personal preferences and experiences with each model for Plane development tasks.

**How to Use**:
- Say "Add 3 points to DeepSeek R1" or "DeepSeek R1 +3"
- Say "Subtract 2 points from GPT-4.1" or "GPT-4.1 -2" 
- The AI will update both this guide and the main model style guide

**Scoring Impact on Plane Recommendations**:
- **+5 to +3**: Model becomes top priority for that task type
- **+2 to -1**: Standard recommendations apply
- **-2 to -5**: Model avoided or deprioritized for that task type

**Example Scenarios**:
- If DeepSeek R1 performs exceptionally well for your MCP server development: "DeepSeek R1 +5"
- If Claude 3.7 Sonnet's documentation quality disappoints: "Claude 3.7 -2"
- If GPT-4.1 handles your large Plane codebase perfectly: "GPT-4.1 +4"

---

## 🧮 Dynamic Model Reordering Algorithm

### **How User Points Override Base Capabilities**

The recommendation system uses a sophisticated algorithm that balances objective model capabilities with your personal experience scores. As User Assigned Points become more extreme, they increasingly override the base capability rankings.

### **Impact Scaling Formula**

```
Final Score = Base Capability Score + (User Points × Impact Multiplier)

Impact Multiplier Calculation:
- Points 0 to ±1: Multiplier = 0.1 (minimal impact)
- Points ±2: Multiplier = 0.3 (slight impact)
- Points ±3: Multiplier = 0.6 (moderate impact)
- Points ±4: Multiplier = 1.0 (significant impact)
- Points ±5: Multiplier = 1.5 (major impact)
- Points ±6+: Multiplier = 2.0 (extreme impact, can override superior models)
```

### **Reordering Thresholds**

**Minor Adjustments** (±1 to ±2 points):
- Slight preference adjustments within same capability tier
- Won't move a 3-star model above a 5-star model
- Fine-tunes recommendations between similar models

**Moderate Impact** (±3 to ±4 points):
- Can move models up/down 1-2 positions in recommendations
- May prioritize a 4-star model over a 5-star model
- Significantly affects task-specific recommendations

**Major Override** (±5+ points):
- Can move lower-capability models above higher-capability ones
- Example: DeepSeek R1 (+5) could be recommended over Claude 4 Sonnet (0) for Python tasks
- Extreme negative scores (-5) will avoid otherwise excellent models

### **Task-Specific Point Tracking**

The system monitors which tasks trigger point adjustments to refine the algorithm:

**MCP Server Development**:
- Track: Python expertise, FastAPI knowledge, Docker integration
- Common adjustments: DeepSeek R1 often gets +points for cost-effectiveness

**Django API Work**:
- Track: Database schema understanding, REST API patterns, migration handling
- Common adjustments: GPT-4.1 often gets +points for large codebase analysis

**Documentation Writing**:
- Track: Technical writing quality, API documentation, architectural explanations
- Common adjustments: Claude 3.7 often gets +points for professional output

**Frontend Development**:
- Track: TypeScript understanding, React patterns, Next.js expertise
- Common adjustments: Models may get -points for poor component architecture

### **Algorithm Examples**

**Scenario 1: Moderate Positive Experience**
```
Task: Python MCP Server Development
Base Rankings: Claude 4 (5★), DeepSeek R1 (4★), GPT-4o (3★)
User Points: DeepSeek R1 +3

Calculation:
- Claude 4: 5.0 + (0 × 0.6) = 5.0
- DeepSeek R1: 4.0 + (3 × 0.6) = 5.8 ← New top choice
- GPT-4o: 3.0 + (0 × 0.6) = 3.0

Result: DeepSeek R1 moves to #1 recommendation
```

**Scenario 2: Extreme Negative Experience**
```
Task: Documentation Writing
Base Rankings: Claude 3.7 (5★), Claude 4 (5★), GPT-4.1 (4★)
User Points: Claude 3.7 -5

Calculation:
- Claude 3.7: 5.0 + (-5 × 1.5) = -2.5 ← Avoided
- Claude 4: 5.0 + (0 × 1.5) = 5.0 ← New top choice
- GPT-4.1: 4.0 + (0 × 1.5) = 4.0

Result: Claude 3.7 dropped from recommendations despite high base rating
```

### **Feedback Loop**:
- Track recommendation accuracy vs. user satisfaction
- Adjust thresholds based on real-world performance
- Incorporate new model capabilities as they're released

---

## 🔧 Implementation Logic for AI Assistant

### **Model Reordering Function**

When providing model recommendations, the AI assistant should apply this logic:

```python
def calculate_final_score(base_rating, user_points):
    """Calculate final score with impact multiplier"""
    if abs(user_points) <= 1:
        multiplier = 0.1
    elif abs(user_points) == 2:
        multiplier = 0.3
    elif abs(user_points) == 3:
        multiplier = 0.6
    elif abs(user_points) == 4:
        multiplier = 1.0
    elif abs(user_points) == 5:
        multiplier = 1.5
    else:  # 6+
        multiplier = 2.0
    
    return base_rating + (user_points * multiplier)

def should_reorder_recommendations(user_points_dict):
    """Determine if recommendations should be reordered"""
    max_abs_points = max(abs(points) for points in user_points_dict.values())
    return max_abs_points >= 3  # Reorder threshold

def generate_personalized_recommendations(task_type, user_points):
    """Generate recommendations considering user points"""
    # Apply scoring algorithm and reorder if necessary
    # Prioritize models with high final scores
    # Avoid models with negative final scores
    pass
```

### **Recommendation Override Rules**

**When to Override Standard Recommendations**:
1. **Any model has ±5+ points**: Major reordering likely
2. **Multiple models have ±3+ points**: Comparative reordering needed
3. **Negative scores below -2**: Avoid recommending that model
4. **Positive scores above +3**: Prioritize in recommendations

**Task-Specific Considerations**:
- **MCP Server Development**: Weight cost-efficiency and Python expertise higher
- **Large Codebase Analysis**: Maintain preference for high-context models unless severely penalized
- **Documentation**: Prioritize writing quality unless user experience suggests otherwise
- **Emergency/Critical Tasks**: Consider overriding user points for mission-critical capabilities

### **Pattern Recognition Triggers**

**Monitor for These Patterns**:
- **Budget Preference**: Consistent +points to DeepSeek, GPT-4o Mini, free models
- **Premium Aversion**: Consistent -points to Claude 4, o3, expensive models  
- **Task-Specific Bias**: Points consistently applied to same models for same tasks
- **Quality Issues**: Negative points for specific capabilities (documentation, reasoning, etc.)

**Adjustment Actions**:
- **Budget Pattern** → Increase cost-efficiency weighting in base recommendations
- **Premium Issues** → Investigate specific pain points with expensive models
- **Task Bias** → Create task-specific recommendation variants
- **Quality Problems** → Flag for algorithm refinement or model capability updates

---

## 🚀 Getting Started Recommendations

### **New to Plane Development**
1. **Start with DeepSeek R1** - Cost-effective, excellent Python support
2. **Use GPT-4.1 free tier** - For understanding the codebase
3. **Upgrade to Claude 3.7 Sonnet** - When you need professional documentation

### **Experienced Developer**
1. **Primary**: **Claude 3.7 Sonnet** - Professional architecture work
2. **Secondary**: **GPT-4.1** - Large codebase analysis
3. **Budget**: **DeepSeek R1** - Cost-effective iteration

### **Enterprise/Production**
1. **Primary**: **Claude 4 Sonnet** - Enterprise-grade capabilities
2. **Architecture**: **Claude 3.7 Sonnet** - Superior documentation
3. **Analysis**: **GPT-4.1** - Large-scale repository analysis

---

## 🔄 Model Switching Strategy

### **Development Workflow**
```
Planning Phase → Claude 3.7 Sonnet (architecture)
    ↓
Implementation → DeepSeek R1 (cost-effective coding)
    ↓
Code Review → GPT-4.1 (large context analysis)
    ↓
Documentation → Claude 3.7 Sonnet (professional docs)
    ↓
Optimization → o3 (advanced reasoning)
```

### **Budget Management**
- **Use free models** for experimentation and learning
- **Switch to DeepSeek R1** for production development (90% cost savings)
- **Upgrade to premium models** only for complex architectural decisions
- **Monitor request usage** and adjust model selection accordingly

---

## 📋 Integration with Other LLM Guides

### **Cross-References**
- **Port Management**: Use DeepSeek R1 for Docker port configuration → `_llm_port_management.md`
- **MCP Server Setup**: Follow Claude 3.7 Sonnet for architecture → `_llm_cursor_mcp_management.md`
- **Documentation**: Use Claude 3.7 Sonnet for all docs → `_llm_documentation_management.md`
- **Project Context**: Refer to current Plane status → `_llm_project_primer.md`

### **Workflow Integration**
1. **Read** `_llm_primer.md` (core standards)
2. **Check** `_llm_project_primer.md` (current context)
3. **Select model** using this guide
4. **Follow specific guidance** from relevant `_llm_*.md` files
5. **Update documentation** per `_llm_documentation_management.md`

---

## 🎯 Success Metrics

### **Model Performance Indicators**
- **Code Quality**: Professional, maintainable, well-documented
- **Cost Efficiency**: Staying within budget while meeting requirements
- **Development Speed**: Faster iteration with appropriate model selection
- **Error Rate**: Fewer bugs and issues with proper model matching

### **When to Switch Models**
- **DeepSeek R1 → GPT-4.1**: When you need larger context windows
- **GPT-4.1 → Claude 3.7**: When you need superior documentation
- **Any → o3**: When you need advanced reasoning for complex problems
- **Premium → Free**: When experimenting or learning new concepts

---

## 📞 Quick Reference

### **Emergency Model Selection**
- **Urgent bug fix**: DeepSeek R1 (fast, cost-effective)
- **Production issue**: Claude 3.7 Sonnet (professional, reliable)
- **Complex architectural decision**: o3 or Claude 4 Sonnet
- **Large codebase analysis**: GPT-4.1 (1M context window)

### **Daily Development**
- **Morning planning**: Claude 3.7 Sonnet (architecture)
- **Active coding**: DeepSeek R1 (cost-effective)
- **Code review**: GPT-4.1 (comprehensive analysis)
- **Documentation**: Claude 3.7 Sonnet (professional quality)

---

**Remember**: This guide is specifically tailored for Plane project management development and MCP server work. Always consider your specific use case, budget constraints, and project requirements when selecting a model. Refer to `docs/research/llm/model_style_guide.md` for detailed technical specifications and limits. 