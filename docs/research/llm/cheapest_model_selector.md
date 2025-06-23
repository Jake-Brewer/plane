# Cheapest Model Selector - Pseudocode

This document provides pseudocode algorithms to determine the most cost-effective LLM model for a given project based on requirements and Cursor credit consumption.

## Algorithm: Find Cheapest Suitable Model

### Input Parameters
```pseudocode
PROJECT_REQUIREMENTS = {
    max_method_length: INTEGER,
    max_file_length: INTEGER,
    max_context_needed: INTEGER (tokens),
    concurrent_files_needed: INTEGER,
    imports_per_file: INTEGER,
    project_type: STRING,
    monthly_usage_estimate: INTEGER (requests/month),
    budget_constraint: FLOAT ($/month),
    mcp_tools_needed: INTEGER,
    special_requirements: LIST[STRING]
}

CURSOR_SUBSCRIPTION = {
    plan: "Hobby" | "Pro" | "Ultra",
    monthly_requests: INTEGER,
    monthly_cost: FLOAT
}
```

### Model Database (From Style Guide)
```pseudocode
MODELS = [
    {
        name: "Claude 4 Sonnet",
        max_method_length: 70,
        max_file_length: 1500,
        max_context: 200000,
        max_concurrent_files: 20,
        max_imports: 45,
        cursor_cost_normal: 1,  // requests per message
        cursor_cost_max: 450,   // requests per MTok (worst case)
        api_cost_input: 3.00,   // $ per MTok
        api_cost_output: 15.00, // $ per MTok
        mcp_tools: 100,
        project_types: ["Enterprise", "AAA Games"],
        user_sentiment: 5,
        subscription_required: "Pro"
    },
    {
        name: "GPT-4.1",
        max_method_length: 65,
        max_file_length: 1400,
        max_context: 1000000,
        max_concurrent_files: 30,
        max_imports: 40,
        cursor_cost_normal: 0,  // FREE
        cursor_cost_max: 300,   // requests per MTok
        api_cost_input: 2.50,
        api_cost_output: 10.00,
        mcp_tools: 90,
        project_types: ["Large Codebases", "Research"],
        user_sentiment: 5,
        subscription_required: "Hobby"
    },
    {
        name: "DeepSeek R1",
        max_method_length: 50,
        max_file_length: 900,
        max_context: 128000,
        max_concurrent_files: 15,
        max_imports: 25,
        cursor_cost_normal: 1,
        cursor_cost_max: 66,    // requests per MTok (best case)
        api_cost_input: 0.14,
        api_cost_output: 2.19,
        mcp_tools: 55,
        project_types: ["Budget Development"],
        user_sentiment: 4,
        subscription_required: "Pro"
    }
    // ... other models
]
```

### Main Algorithm
```pseudocode
FUNCTION find_cheapest_model(project_requirements, cursor_subscription):
    suitable_models = []
    
    // Step 1: Filter models by technical requirements
    FOR each model IN MODELS:
        IF meets_technical_requirements(model, project_requirements):
            suitable_models.append(model)
    
    // Step 2: Calculate costs for each suitable model
    cost_analysis = []
    FOR each model IN suitable_models:
        monthly_cost = calculate_monthly_cost(model, project_requirements, cursor_subscription)
        cost_analysis.append({
            model: model,
            monthly_cost: monthly_cost,
            cost_breakdown: get_cost_breakdown(model, project_requirements, cursor_subscription)
        })
    
    // Step 3: Sort by total monthly cost
    cost_analysis.sort(key=lambda x: x.monthly_cost)
    
    // Step 4: Return cheapest option with analysis
    RETURN {
        recommended_model: cost_analysis[0].model,
        monthly_cost: cost_analysis[0].monthly_cost,
        cost_breakdown: cost_analysis[0].cost_breakdown,
        alternatives: cost_analysis[1:3],  // Next 2 cheapest options
        savings_analysis: calculate_savings(cost_analysis)
    }

FUNCTION meets_technical_requirements(model, requirements):
    RETURN (
        model.max_method_length >= requirements.max_method_length AND
        model.max_file_length >= requirements.max_file_length AND
        model.max_context >= requirements.max_context_needed AND
        model.max_concurrent_files >= requirements.concurrent_files_needed AND
        model.max_imports >= requirements.imports_per_file AND
        model.mcp_tools >= requirements.mcp_tools_needed AND
        (requirements.project_type IN model.project_types OR 
         "General Development" IN model.project_types)
    )

FUNCTION calculate_monthly_cost(model, requirements, subscription):
    // Calculate Cursor subscription cost
    subscription_cost = get_subscription_cost(model.subscription_required)
    
    // Calculate request consumption
    normal_requests = requirements.monthly_usage_estimate
    max_requests = estimate_max_mode_usage(requirements)
    
    // Calculate if over limits
    total_requests = normal_requests * model.cursor_cost_normal + max_requests * model.cursor_cost_max
    
    IF total_requests <= subscription.monthly_requests:
        // Within subscription limits
        total_cost = subscription_cost
    ELSE:
        // Over limits - calculate overage
        overage_requests = total_requests - subscription.monthly_requests
        overage_cost = overage_requests * 0.04  // $0.04 per request
        total_cost = subscription_cost + overage_cost
    
    RETURN total_cost

FUNCTION get_subscription_cost(required_plan):
    SWITCH required_plan:
        CASE "Hobby": RETURN 0
        CASE "Pro": RETURN 20
        CASE "Ultra": RETURN 200
        DEFAULT: RETURN 20

FUNCTION estimate_max_mode_usage(requirements):
    // Estimate how often Max mode will be used based on project complexity
    complexity_factor = calculate_complexity(requirements)
    IF complexity_factor > 0.8:
        RETURN requirements.monthly_usage_estimate * 0.3  // 30% of requests in Max mode
    ELIF complexity_factor > 0.5:
        RETURN requirements.monthly_usage_estimate * 0.15 // 15% of requests in Max mode
    ELSE:
        RETURN requirements.monthly_usage_estimate * 0.05 // 5% of requests in Max mode

FUNCTION calculate_complexity(requirements):
    // Normalize complexity score 0-1
    method_complexity = requirements.max_method_length / 100.0
    file_complexity = requirements.max_file_length / 2000.0
    context_complexity = requirements.max_context_needed / 1000000.0
    concurrent_complexity = requirements.concurrent_files_needed / 50.0
    
    RETURN min(1.0, (method_complexity + file_complexity + context_complexity + concurrent_complexity) / 4.0)
```

## Example Usage

### Example 1: Budget Web Development Project
```pseudocode
project = {
    max_method_length: 40,
    max_file_length: 600,
    max_context_needed: 64000,
    concurrent_files_needed: 8,
    imports_per_file: 20,
    project_type: "Web Development",
    monthly_usage_estimate: 200,
    budget_constraint: 25.00,
    mcp_tools_needed: 30,
    special_requirements: ["Cost-effective"]
}

subscription = {
    plan: "Pro",
    monthly_requests: 500,
    monthly_cost: 20.00
}

result = find_cheapest_model(project, subscription)
// Expected: DeepSeek R1 or GPT-4.1 (free tier)
```

### Example 2: Enterprise Application
```pseudocode
project = {
    max_method_length: 60,
    max_file_length: 1200,
    max_context_needed: 150000,
    concurrent_files_needed: 15,
    imports_per_file: 35,
    project_type: "Enterprise",
    monthly_usage_estimate: 800,
    budget_constraint: 100.00,
    mcp_tools_needed: 80,
    special_requirements: ["High Quality", "Production Grade"]
}

subscription = {
    plan: "Pro",
    monthly_requests: 500,
    monthly_cost: 20.00
}

result = find_cheapest_model(project, subscription)
// Expected: Claude 3.7 Sonnet with overage costs calculated
```

## Cost Optimization Strategies

### Strategy 1: Hybrid Model Usage
```pseudocode
FUNCTION optimize_with_hybrid_approach(project_requirements):
    // Use cheaper model for routine tasks, premium for complex ones
    routine_model = find_cheapest_model(reduce_requirements(project_requirements))
    complex_model = find_best_model(project_requirements)
    
    estimated_savings = calculate_hybrid_savings(routine_model, complex_model, project_requirements)
    RETURN {
        routine_model: routine_model,
        complex_model: complex_model,
        estimated_monthly_savings: estimated_savings
    }
```

### Strategy 2: Direct API Comparison
```pseudocode
FUNCTION compare_cursor_vs_api(model, monthly_usage):
    cursor_cost = calculate_cursor_cost(model, monthly_usage)
    api_cost = calculate_direct_api_cost(model, monthly_usage)
    
    IF api_cost < cursor_cost:
        savings = cursor_cost - api_cost
        RETURN {
            recommendation: "Use Direct API",
            monthly_savings: savings,
            breakeven_usage: calculate_breakeven_point(model)
        }
    ELSE:
        RETURN {
            recommendation: "Use Cursor Subscription",
            monthly_savings: 0,
            reason: "Subscription is more cost-effective"
        }
```

## Implementation Notes

1. **Real-time Pricing**: Model costs change frequently - implement API calls to get current pricing
2. **Usage Tracking**: Monitor actual usage vs estimates to refine calculations
3. **Context Optimization**: Implement context window optimization to reduce Max mode usage
4. **Batch Processing**: Group similar requests to minimize per-request overhead
5. **Caching**: Cache model responses for repeated queries to reduce costs

## Validation Checklist

- [ ] Technical requirements are met by selected model
- [ ] Monthly cost is within budget constraint
- [ ] Model supports required project type
- [ ] MCP tool limits are sufficient
- [ ] User sentiment rating is acceptable (≥3 stars)
- [ ] Subscription plan requirements are feasible
- [ ] Overage costs are calculated accurately
- [ ] Alternative models are provided for comparison 