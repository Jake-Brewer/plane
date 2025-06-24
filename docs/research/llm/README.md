# LLM Model Selector

A Python script that automatically selects the most cost-effective LLM model for project analysis based on technical requirements, user preferences, and budget constraints.

## Features

- **Technical Compatibility Filtering**: Ensures models can handle your project's largest files and methods
- **Cost Optimization**: Finds the cheapest model that meets your requirements
- **Budget Management**: Respects monthly budget limits
- **Quality Assurance**: Maintains minimum quality thresholds
- **Optimization Suggestions**: Recommends hybrid approaches and cost-saving strategies
- **Multiple Input Methods**: Command line, interactive mode, or JSON configuration

## Quick Start

### 1. Run with Sample Project
```bash
python model_selector.py --sample
```

### 2. Interactive Mode
```bash
python model_selector.py --interactive
```

### 3. Configuration File
```bash
python model_selector.py --config sample_config.json
```

## Usage Examples

### Sample Output
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

💾 Results automatically saved to model_selection_results.json
```

## Configuration

### JSON Configuration Format
See `sample_config.json` for a complete example:

```json
{
  "project": {
    "largest_file_length": 1200,
    "p95_file_length": 950,
    "median_file_length": 600,
    "total_files": 150,
    "analysis_frequency": 15,
    "budget_limit": 10.0,
    "quality_threshold": 4
  },
  "preferences": {
    "cost_weight": 0.4,
    "performance_weight": 0.3,
    "sentiment_weight": 0.3
  }
}
```

### Key Parameters

#### File Size Metrics (Critical for Compatibility)
- **`largest_file_length`**: Maximum file size that must fit in model (hard limit)
- **`p95_file_length`**: 95th percentile file size (handles edge cases)
- **`median_file_length`**: Typical file size (cost estimation)

#### Method Length Metrics
- **`largest_method_length`**: Maximum method size that must fit in model
- **`p95_method_length`**: 95th percentile method size
- **`median_method_length`**: Typical method size

#### Budget & Quality
- **`budget_limit`**: Maximum monthly budget ($)
- **`analysis_frequency`**: How many analyses per month
- **`quality_threshold`**: Minimum quality rating (1-5 stars)

## Model Selection Algorithm

### 1. Technical Filtering
Models are filtered by hard requirements:
- Must handle largest file/method sizes
- Must support required context window
- Must meet quality threshold
- Must support required features (reasoning, MCP tools, etc.)

### 2. Weighted Scoring
Each compatible model gets scored based on:
- **Cost Efficiency** (40% weight by default)
- **Performance Quality** (30% weight)
- **User Sentiment** (30% weight)

### 3. Optimization Suggestions
The script suggests:
- **Free Alternatives**: Zero-cost options with quality trade-offs
- **Hybrid Approaches**: Mix of budget/premium models (80/20 split)
- **Frequency Optimization**: Reduce analysis frequency to save costs

## File Metrics Usage Guide

### Why Different Metrics Matter

**LARGEST values** - Critical for compatibility:
- Used for initial model filtering
- If largest file doesn't fit, model will fail completely
- Must ensure worst-case scenarios work

**95th PERCENTILE values** - For practical limits:
- Handles 95% of real-world cases
- Ignores extreme outliers
- Better for complexity assessment

**MEDIAN values** - For cost estimation:
- Represents typical usage patterns
- Most accurate for predicting costs
- Not skewed by outliers

## Supported Models

The script includes 10+ models across different cost tiers:

### Free Models ($0.00)
- GPT-4o Mini, DeepSeek V3.1, Gemini 2.5 Flash

### Low-Cost Models ($0.01-$0.02)
- Claude 3.5 Haiku, o3-Mini

### Standard Models ($0.04)
- Claude 4 Sonnet, Claude 3.7 Sonnet, GPT-4.1

### High-Cost Models ($0.10-$0.40)
- o1 Mini, o1

## Output Files

### Automatic JSON Export
Results are automatically saved to `model_selection_results.json` with:
- Complete project configuration
- Analysis summary
- Top 5 model recommendations
- Optimization suggestions

### Sample JSON Output
```json
{
  "analysis": {
    "total_models_evaluated": 10,
    "technically_suitable": 5,
    "budget_compatible": 5,
    "recommended_model": "Claude 4 Sonnet"
  },
  "recommendations": [
    {
      "model": "Claude 4 Sonnet",
      "monthly_cost": 0.10,
      "score": 1.07,
      "meets_budget": true
    }
  ],
  "optimizations": {
    "free_alternative": {
      "model": "DeepSeek V3.1",
      "monthly_savings": 0.10
    }
  }
}
```

## Advanced Usage

### Custom Model Database
Modify the `_load_model_database()` method to add new models or update pricing.

### Custom Scoring
Adjust weights in `UserPreferences`:
```python
preferences = UserPreferences(
    cost_weight=0.5,      # Prioritize cost
    performance_weight=0.3,
    sentiment_weight=0.2
)
```

### Batch Analysis
Process multiple projects by loading different config files:
```bash
for config in project_*.json; do
    python model_selector.py --config "$config"
done
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Related Files

- **`project_analysis_selector.md`**: Detailed pseudocode algorithm
- **`project_analysis_prompt.md`**: LLM prompt for manual analysis
- **`model_style_guide.md`**: Complete model database and specifications
- **`sample_config.json`**: Example configuration file

---

**Pro Tip**: Start with `--sample` to see how it works, then use `--interactive` to input your project details, and finally create a JSON config file for repeated analysis. 