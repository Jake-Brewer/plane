# Cursor LLM Model Selector

A comprehensive Python application that automatically selects the most cost-effective LLM model for project analysis in Cursor IDE based on technical requirements, user preferences, and budget constraints.

## 🎯 Purpose

This tool helps developers and teams optimize their LLM usage costs in Cursor IDE by:
- **Analyzing project requirements** (file sizes, complexity, analysis frequency)
- **Filtering compatible models** based on technical limitations
- **Calculating real costs** using accurate Cursor pricing data
- **Recommending optimal models** with cost-benefit analysis
- **Suggesting optimizations** like hybrid approaches and frequency adjustments

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- No external dependencies (uses only standard library)

### Installation
```bash
git clone <this-repo>
cd cursor-llm-model-selector
```

### Usage

#### 1. Quick Test with Sample Project
```bash
python model_selector.py --sample
```

#### 2. Interactive Mode (Custom Input)
```bash
python model_selector.py --interactive
```

#### 3. Configuration File (Repeatable Analysis)
```bash
python model_selector.py --config sample_config.json
```

## 📊 Sample Output

```
🎯 LLM MODEL SELECTION ANALYSIS
================================================================================

📊 ANALYSIS SUMMARY
Total models evaluated: 10
Technically suitable: 5
Budget compatible: 5

🏆 RECOMMENDED MODEL: Claude 4 Sonnet
Monthly Cost: $0.10
Cost per Analysis: $0.01
Quality Rating: ⭐⭐⭐⭐⭐
Overall Score: 1.07/1.0
Budget Compatible: ✅

📋 TOP 5 ALTERNATIVES:
1. Claude 4 Sonnet      $  0.10/mo ⭐⭐⭐⭐⭐ Score: 1.07 ✅
2. Claude 3.7 Sonnet    $  0.10/mo ⭐⭐⭐⭐⭐ Score: 1.07 ✅
3. GPT-4.1              $  0.10/mo ⭐⭐⭐⭐⭐ Score: 1.07 ✅

💡 OPTIMIZATION OPPORTUNITIES:
Free Alternative: DeepSeek V3.1 (saves $0.10/mo, quality diff: -2)
Hybrid Approach: DeepSeek V3.1 + Claude 4 Sonnet ($0.08/mo, saves $0.02)

💾 Results automatically saved to model_selection_results.json
```

## 🔧 Configuration

### Project Attributes
Configure your project details in JSON format:

```json
{
  "project": {
    "largest_file_length": 800,
    "p95_file_length": 650,
    "median_file_length": 400,
    "largest_method_length": 50,
    "total_files": 100,
    "analysis_frequency": 10,
    "budget_limit": 10.0,
    "quality_threshold": 3
  }
}
```

### Key Metrics Explained

**File Size Metrics** (Critical for Understanding):
- **`largest_file_length`**: Maximum file size that MUST fit in model (hard limit)
- **`p95_file_length`**: 95th percentile size (handles edge cases)
- **`median_file_length`**: Typical file size (cost estimation)

**Why This Matters**: Models have different maximum file size limits. If your largest file is 1200 lines but a model only supports 800 lines, that model will fail completely.

## 🧠 Algorithm Overview

### 1. Technical Filtering
- Eliminates models that can't handle your largest files/methods
- Checks context window requirements
- Validates feature support (reasoning, MCP tools)
- Ensures minimum quality standards

### 2. Weighted Scoring
Each compatible model gets scored on:
- **Cost Efficiency** (40% weight) - Lower cost = higher score
- **Performance Quality** (30% weight) - Analysis capability + reasoning
- **User Sentiment** (30% weight) - Community ratings and reviews

### 3. Optimization Suggestions
- **Free Alternatives**: Zero-cost options with quality trade-offs
- **Hybrid Approaches**: 80% budget model + 20% premium model
- **Frequency Optimization**: Reduce analysis frequency to cut costs

## 📈 Supported Models

### Free Tier ($0.00)
- **GPT-4o Mini**: Basic analysis, 600-line files
- **DeepSeek V3.1**: Advanced free option, 800-line files
- **Gemini 2.5 Flash**: Fast analysis, 1M token context

### Low-Cost ($0.01-$0.02)
- **Claude 3.5 Haiku**: Fast, light tasks
- **o3-Mini**: Light reasoning capabilities

### Standard ($0.04)
- **Claude 4 Sonnet**: Enterprise-grade, 1500-line files
- **Claude 3.7 Sonnet**: Professional development
- **GPT-4.1**: Large codebases, 1M token context

### Premium ($0.10-$0.40)
- **o1 Mini**: Moderate reasoning
- **o1**: Complex reasoning tasks

## 📁 Project Structure

```
cursor-llm-model-selector/
├── model_selector.py          # Main application
├── sample_config.json         # Example configuration
├── README.md                  # This file
└── docs/                      # Research and documentation
    ├── model_style_guide.md   # Complete model database
    ├── project_analysis_prompt.md    # LLM prompt version
    ├── project_analysis_selector.md  # Detailed algorithm
    ├── preparation.md          # Research methodology
    ├── ratings.md             # Model ratings and analysis
    └── strengths-and-weaknesses.md   # Detailed model comparison
```

## 🔬 Research Documentation

The `docs/` directory contains comprehensive research:

- **`model_style_guide.md`**: Complete database of 37+ models with accurate pricing
- **`strengths-and-weaknesses.md`**: Detailed analysis of each model's capabilities
- **`project_analysis_prompt.md`**: Ready-to-use LLM prompt for manual analysis
- **`ratings.md`**: Performance ratings across multiple criteria
- **`preparation.md`**: Research methodology and benchmarks

## 💡 Advanced Usage

### Custom Model Database
Add new models or update pricing in `model_selector.py`:

```python
LLMModel(
    name="New Model",
    cursor_cost=0.05,  # Cursor requests per message
    max_file_length=1000,
    max_method_length=100,
    # ... other attributes
)
```

### Batch Analysis
Process multiple projects:

```bash
for config in project_*.json; do
    python model_selector.py --config "$config"
done
```

### Custom Scoring Weights
Prioritize different factors:

```python
preferences = UserPreferences(
    cost_weight=0.6,      # Prioritize cost savings
    performance_weight=0.2,
    sentiment_weight=0.2
)
```

## 🎯 Use Cases

### Individual Developers
- **Budget Optimization**: Find cheapest model for personal projects
- **Quality Assurance**: Ensure model can handle your code complexity
- **Feature Matching**: Match models to specific project needs

### Development Teams
- **Cost Management**: Control team LLM expenses
- **Standardization**: Consistent model selection across projects
- **Hybrid Strategies**: Mix models for different use cases

### Enterprise
- **Budget Planning**: Predict and control LLM costs
- **Compliance**: Ensure models meet security/quality requirements
- **Optimization**: Maximize value from LLM investments

## 🔄 Integration

### CI/CD Pipeline
```bash
# Add to your build process
python model_selector.py --config project_config.json
# Use output to set Cursor model preferences
```

### Project Templates
Include `model_config.json` in project templates for automatic optimization.

### Team Workflows
Share configurations across team members for consistent model selection.

## 🤝 Contributing

This project was extracted from research on LLM optimization for development workflows. Contributions welcome for:
- New model additions
- Pricing updates
- Algorithm improvements
- Documentation enhancements

## 📄 License

MIT License - Feel free to use, modify, and distribute.

## 🆘 Support

For questions or issues:
1. Check the `docs/` directory for detailed documentation
2. Review `sample_config.json` for configuration examples
3. Run with `--sample` to see expected output format

---

**Pro Tip**: Start with `--sample` to understand the output, then use `--interactive` to input your project details, and finally create a JSON config file for repeated analysis.