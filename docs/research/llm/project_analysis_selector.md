# Project Analysis Model Selector - Pseudocode

This document provides pseudocode algorithms to determine the most cost-effective LLM model for analyzing a given project based on project attributes, technical requirements, and user sentiment weighting.

## Algorithm: Select Cheapest Analysis Model

### Input Parameters
```pseudocode
PROJECT_ATTRIBUTES = {
    // Technical Attributes - File Size Metrics
    largest_file_length: INTEGER,           // Critical: Must fit within model limits
    p95_file_length: INTEGER,              // 95th percentile: Handles most edge cases
    median_file_length: INTEGER,           // Typical file size for cost estimation
    average_file_length: INTEGER,          // For complexity calculations
    
    // Method Length Metrics
    largest_method_length: INTEGER,        // Critical: Must fit within model limits
    p95_method_length: INTEGER,           // 95th percentile: Handles most edge cases
    median_method_length: INTEGER,        // Typical method size
    
    // Project Scale
    total_files: INTEGER,
    max_concurrent_analysis: INTEGER,      // How many files analyzed simultaneously
    imports_per_file: INTEGER,             // Use median or average
    codebase_complexity: FLOAT (0.0-1.0),
    context_window_needed: INTEGER (tokens), // Based on largest expected analysis
    
    // Project Characteristics
    project_type: STRING,
    programming_languages: LIST[STRING],
    frameworks_used: LIST[STRING],
    architecture_pattern: STRING,
    
    // Analysis Requirements
    analysis_depth: "shallow" | "medium" | "deep",
    analysis_frequency: INTEGER (times per month),
    reasoning_required: BOOLEAN,
    internet_access_needed: BOOLEAN,
    mcp_tools_needed: INTEGER,
    
    // Constraints
    budget_limit: FLOAT ($/month),
    quality_threshold: INTEGER (1-5 stars),
    max_cost_per_analysis: FLOAT ($/analysis)
}

USER_PREFERENCES = {
    sentiment_weight: FLOAT (0.0-1.0),  // How much to weight user sentiment
    cost_weight: FLOAT (0.0-1.0),      // How much to weight cost
    performance_weight: FLOAT (0.0-1.0), // How much to weight performance
    prefer_free_models: BOOLEAN,
    risk_tolerance: "low" | "medium" | "high"
}
```

### Model Database (From Style Guide)
```pseudocode
ANALYSIS_MODELS = [
    // Free Models (0 requests/message)
    {
        name: "GPT-4o Mini",
        cursor_cost: 0.0,
        max_method_length: 35,
        max_file_length: 600,
        max_context: 128000,
        max_concurrent_files: 8,
        max_imports: 25,
        mcp_tools: 40,
        user_sentiment: 3,
        project_types: ["Budget Development"],
        reasoning_capability: 2,
        analysis_quality: 3
    },
    {
        name: "DeepSeek V3.1",
        cursor_cost: 0.0,
        max_method_length: 45,
        max_file_length: 800,
        max_context: 128000,
        max_concurrent_files: 12,
        max_imports: 20,
        mcp_tools: 45,
        user_sentiment: 3,
        project_types: ["Ultra-Budget"],
        reasoning_capability: 3,
        analysis_quality: 3
    },
    {
        name: "Gemini 2.5 Flash",
        cursor_cost: 0.0,
        max_method_length: 40,
        max_file_length: 600,
        max_context: 1000000,
        max_concurrent_files: 15,
        max_imports: 30,
        mcp_tools: 50,
        user_sentiment: 3,
        project_types: ["Fast, Free Tasks"],
        reasoning_capability: 2,
        analysis_quality: 3
    },
    
    // Low-Cost Models
    {
        name: "Claude 3.5 Haiku",
        cursor_cost: 0.013,
        max_method_length: 40,
        max_file_length: 700,
        max_context: 100000,
        max_concurrent_files: 8,
        max_imports: 20,
        mcp_tools: 50,
        user_sentiment: 3,
        project_types: ["Fast, Light Tasks"],
        reasoning_capability: 3,
        analysis_quality: 4
    },
    {
        name: "o3-Mini",
        cursor_cost: 0.01,
        max_method_length: 45,
        max_file_length: 700,
        max_context: 128000,
        max_concurrent_files: 10,
        max_imports: 20,
        mcp_tools: 40,
        user_sentiment: 3,
        project_types: ["Light Reasoning"],
        reasoning_capability: 4,
        analysis_quality: 4
    },
    
    // Standard Models
    {
        name: "Claude 4 Sonnet",
        cursor_cost: 0.04,
        max_method_length: 70,
        max_file_length: 1500,
        max_context: 200000,
        max_concurrent_files: 20,
        max_imports: 45,
        mcp_tools: 100,
        user_sentiment: 5,
        project_types: ["Enterprise", "AAA Games"],
        reasoning_capability: 5,
        analysis_quality: 5
    },
    {
        name: "GPT-4.1",
        cursor_cost: 0.04,
        max_method_length: 65,
        max_file_length: 1400,
        max_context: 1000000,
        max_concurrent_files: 30,
        max_imports: 40,
        mcp_tools: 90,
        user_sentiment: 5,
        project_types: ["Large Codebases", "Research"],
        reasoning_capability: 5,
        analysis_quality: 5
    },
    
    // High-Cost Models
    {
        name: "o1",
        cursor_cost: 0.40,
        max_method_length: 65,
        max_file_length: 1200,
        max_context: 128000,
        max_concurrent_files: 20,
        max_imports: 35,
        mcp_tools: 80,
        user_sentiment: 4,
        project_types: ["Complex Reasoning"],
        reasoning_capability: 5,
        analysis_quality: 5
    }
]
```

### Main Selection Algorithm
```pseudocode
FUNCTION select_cheapest_analysis_model(project_attributes, user_preferences):
    // Step 1: Filter models by technical requirements
    suitable_models = filter_by_technical_requirements(project_attributes)
    
    // Step 2: Calculate weighted scores for each suitable model
    scored_models = []
    FOR each model IN suitable_models:
        score = calculate_weighted_score(model, project_attributes, user_preferences)
        monthly_cost = calculate_monthly_analysis_cost(model, project_attributes)
        
        scored_models.append({
            model: model,
            score: score,
            monthly_cost: monthly_cost,
            cost_per_analysis: monthly_cost / project_attributes.analysis_frequency,
            meets_budget: monthly_cost <= project_attributes.budget_limit
        })
    
    // Step 3: Filter by budget constraints
    budget_suitable = filter(scored_models, lambda x: x.meets_budget)
    
    IF budget_suitable is empty:
        // No models meet budget - return cheapest option with warning
        cheapest = min(scored_models, key=lambda x: x.monthly_cost)
        RETURN {
            recommended_model: cheapest.model,
            warning: "Budget exceeded - cheapest option provided",
            monthly_cost: cheapest.monthly_cost,
            alternatives: []
        }
    
    // Step 4: Sort by weighted score (higher is better)
    budget_suitable.sort(key=lambda x: x.score, reverse=True)
    
    // Step 5: Return best option with alternatives
    RETURN {
        recommended_model: budget_suitable[0].model,
        monthly_cost: budget_suitable[0].monthly_cost,
        cost_per_analysis: budget_suitable[0].cost_per_analysis,
        confidence_score: budget_suitable[0].score,
        alternatives: budget_suitable[1:3],
        cost_savings: calculate_savings_analysis(budget_suitable)
    }

FUNCTION filter_by_technical_requirements(project_attributes):
    suitable = []
    FOR each model IN ANALYSIS_MODELS:
        IF (model.max_method_length >= project_attributes.average_method_length AND
            model.max_file_length >= project_attributes.average_file_length AND
            model.max_context >= project_attributes.context_window_needed AND
            model.max_concurrent_files >= project_attributes.max_concurrent_analysis AND
            model.max_imports >= project_attributes.imports_per_file AND
            model.mcp_tools >= project_attributes.mcp_tools_needed AND
            model.user_sentiment >= project_attributes.quality_threshold):
            
            suitable.append(model)
    
    RETURN suitable

FUNCTION calculate_weighted_score(model, project_attributes, user_preferences):
    // Cost score (lower cost = higher score)
    max_cost = 2.0  // GPT-4.5 Preview cost
    cost_score = (max_cost - model.cursor_cost) / max_cost
    
    // Performance score (based on analysis quality and reasoning)
    performance_score = (model.analysis_quality + model.reasoning_capability) / 10.0
    
    // Sentiment score (normalized)
    sentiment_score = model.user_sentiment / 5.0
    
    // Project type match bonus
    type_match_bonus = 0.0
    IF project_attributes.project_type IN model.project_types:
        type_match_bonus = 0.2
    
    // Analysis depth match
    depth_match_score = calculate_depth_match(model, project_attributes.analysis_depth)
    
    // Calculate weighted final score
    final_score = (
        cost_score * user_preferences.cost_weight +
        performance_score * user_preferences.performance_weight +
        sentiment_score * user_preferences.sentiment_weight +
        depth_match_score * 0.3 +
        type_match_bonus
    ) / (user_preferences.cost_weight + user_preferences.performance_weight + 
         user_preferences.sentiment_weight + 0.3 + (0.2 if type_match_bonus > 0 else 0))
    
    RETURN final_score

FUNCTION calculate_depth_match(model, required_depth):
    SWITCH required_depth:
        CASE "shallow":
            IF model.reasoning_capability >= 2: RETURN 1.0
            ELSE: RETURN 0.5
        CASE "medium":
            IF model.reasoning_capability >= 3: RETURN 1.0
            ELIF model.reasoning_capability >= 2: RETURN 0.7
            ELSE: RETURN 0.3
        CASE "deep":
            IF model.reasoning_capability >= 4: RETURN 1.0
            ELIF model.reasoning_capability >= 3: RETURN 0.6
            ELSE: RETURN 0.2
    RETURN 0.5

FUNCTION calculate_monthly_analysis_cost(model, project_attributes):
    cost_per_analysis = model.cursor_cost
    
    // Adjust for complexity multiplier
    complexity_multiplier = 1.0 + project_attributes.codebase_complexity
    adjusted_cost = cost_per_analysis * complexity_multiplier
    
    // Calculate monthly cost
    monthly_cost = adjusted_cost * project_attributes.analysis_frequency
    
    RETURN monthly_cost

FUNCTION calculate_complexity_factor(project_attributes):
    // Normalize complexity based on multiple factors
    method_complexity = min(1.0, project_attributes.average_method_length / 100.0)
    file_complexity = min(1.0, project_attributes.average_file_length / 2000.0)
    scale_complexity = min(1.0, project_attributes.total_files / 1000.0)
    
    RETURN (method_complexity + file_complexity + scale_complexity) / 3.0
```

## Example Usage Scenarios

### Scenario 1: Budget Web Development Analysis
```pseudocode
project = {
    average_method_length: 35,
    average_file_length: 500,
    total_files: 50,
    max_concurrent_analysis: 8,
    imports_per_file: 15,
    codebase_complexity: 0.3,
    context_window_needed: 50000,
    project_type: "Web Development",
    analysis_depth: "medium",
    analysis_frequency: 10,  // 10 times per month
    budget_limit: 5.00,
    quality_threshold: 3
}

preferences = {
    sentiment_weight: 0.2,
    cost_weight: 0.6,
    performance_weight: 0.2,
    prefer_free_models: true
}

result = select_cheapest_analysis_model(project, preferences)
// Expected: Gemini 2.5 Flash (free, 1M context) or DeepSeek V3.1
```

### Scenario 2: Enterprise Application Analysis
```pseudocode
project = {
    average_method_length: 60,
    average_file_length: 1200,
    total_files: 200,
    max_concurrent_analysis: 15,
    imports_per_file: 35,
    codebase_complexity: 0.8,
    context_window_needed: 180000,
    project_type: "Enterprise",
    analysis_depth: "deep",
    analysis_frequency: 20,
    budget_limit: 25.00,
    quality_threshold: 4
}

preferences = {
    sentiment_weight: 0.4,
    cost_weight: 0.3,
    performance_weight: 0.3,
    prefer_free_models: false
}

result = select_cheapest_analysis_model(project, preferences)
// Expected: Claude 4 Sonnet or GPT-4.1 (high quality, within budget)
```

## Cost Optimization Strategies

### Strategy 1: Hybrid Analysis Approach
```pseudocode
FUNCTION optimize_with_hybrid_analysis(project_attributes):
    // Use free models for routine analysis, premium for complex analysis
    routine_requirements = reduce_analysis_requirements(project_attributes)
    complex_requirements = enhance_analysis_requirements(project_attributes)
    
    routine_model = select_cheapest_analysis_model(routine_requirements, {cost_weight: 1.0})
    complex_model = select_cheapest_analysis_model(complex_requirements, {performance_weight: 0.7, sentiment_weight: 0.3})
    
    // Calculate split usage (80% routine, 20% complex)
    routine_cost = routine_model.monthly_cost * 0.8
    complex_cost = complex_model.monthly_cost * 0.2
    
    RETURN {
        routine_model: routine_model,
        complex_model: complex_model,
        total_monthly_cost: routine_cost + complex_cost,
        savings_vs_single_model: calculate_hybrid_savings(routine_model, complex_model, project_attributes)
    }
```

### Strategy 2: Analysis Batching
```pseudocode
FUNCTION optimize_with_batching(project_attributes, batch_size):
    // Batch multiple analyses to reduce per-analysis overhead
    original_frequency = project_attributes.analysis_frequency
    batched_frequency = ceil(original_frequency / batch_size)
    
    batched_attributes = project_attributes.copy()
    batched_attributes.analysis_frequency = batched_frequency
    batched_attributes.max_concurrent_analysis *= batch_size
    
    result = select_cheapest_analysis_model(batched_attributes, user_preferences)
    
    RETURN {
        recommended_approach: "Batched Analysis",
        batch_size: batch_size,
        model: result.recommended_model,
        monthly_cost: result.monthly_cost,
        cost_per_analysis: result.monthly_cost / original_frequency,
        savings: calculate_batching_savings(result, original_frequency, batch_size)
    }
```

## Decision Tree Shortcuts

### Quick Decision Logic
```pseudocode
FUNCTION quick_model_selection(project_attributes):
    // Fast decision tree for common scenarios
    
    IF project_attributes.budget_limit <= 0:
        RETURN select_best_free_model(project_attributes)
    
    IF project_attributes.analysis_depth == "shallow" AND project_attributes.prefer_free_models:
        RETURN "Gemini 2.5 Flash"  // Best free option with 1M context
    
    IF project_attributes.project_type == "Enterprise" AND project_attributes.budget_limit >= 20:
        RETURN "Claude 4 Sonnet"  // Premium quality for enterprise
    
    IF project_attributes.context_window_needed > 500000:
        RETURN "GPT-4.1"  // Only model with 1M+ context at reasonable cost
    
    IF project_attributes.analysis_depth == "deep" AND project_attributes.budget_limit >= 10:
        RETURN "o3-Mini"  // Best reasoning at low cost
    
    // Default to cost-optimized selection
    RETURN select_cheapest_analysis_model(project_attributes, {cost_weight: 0.8, performance_weight: 0.2})
```

## Validation & Testing

### Test Cases
```pseudocode
TEST_CASES = [
    {
        name: "Micro Project",
        attributes: {budget_limit: 0, total_files: 5, analysis_depth: "shallow"},
        expected_models: ["GPT-4o Mini", "DeepSeek V3.1", "Gemini 2.5 Flash"]
    },
    {
        name: "Large Codebase",
        attributes: {total_files: 1000, context_window_needed: 800000, budget_limit: 50},
        expected_models: ["GPT-4.1"]  // Only model with sufficient context
    },
    {
        name: "Budget Constraint",
        attributes: {budget_limit: 2.00, analysis_frequency: 50},
        expected_models: ["Free models only"]
    }
]

FUNCTION run_validation_tests():
    FOR each test_case IN TEST_CASES:
        result = select_cheapest_analysis_model(test_case.attributes, default_preferences)
        ASSERT result.recommended_model.name IN test_case.expected_models
```

This pseudocode provides a comprehensive framework for selecting the most cost-effective model for project analysis while considering user sentiment, technical requirements, and budget constraints. 