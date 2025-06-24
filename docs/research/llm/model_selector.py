#!/usr/bin/env python3
"""
LLM Model Selector for Project Analysis

This script implements the algorithm to select the most cost-effective LLM model
for analyzing a given project based on technical requirements, user preferences,
and budget constraints.

Usage:
    python model_selector.py --sample
    python model_selector.py --interactive
    python model_selector.py --config project_config.json
"""

import json
import argparse
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
from enum import Enum


class AnalysisDepth(Enum):
    SHALLOW = "shallow"
    MEDIUM = "medium"
    DEEP = "deep"


class RiskTolerance(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ProjectAttributes:
    """Project attributes for model selection"""
    # File Size Distribution
    largest_file_length: int
    p95_file_length: int
    median_file_length: int
    average_file_length: int
    
    # Method Length Distribution
    largest_method_length: int
    p95_method_length: int
    median_method_length: int
    
    # Project Scale
    total_files: int
    max_concurrent_analysis: int
    imports_per_file: int  # median
    codebase_complexity: float  # 0.0-1.0
    context_window_needed: int  # tokens, based on largest analysis
    
    # Project Characteristics
    project_type: str
    programming_languages: List[str]
    frameworks_used: List[str]
    architecture_pattern: str
    
    # Analysis Requirements
    analysis_depth: AnalysisDepth
    analysis_frequency: int  # times per month
    reasoning_required: bool
    internet_access_needed: bool
    mcp_tools_needed: int
    
    # Constraints
    budget_limit: float  # $/month
    quality_threshold: int  # 1-5 stars
    max_cost_per_analysis: float  # $/analysis


@dataclass
class UserPreferences:
    """User preferences for weighting selection criteria"""
    sentiment_weight: float = 0.3  # 0.0-1.0
    cost_weight: float = 0.4       # 0.0-1.0
    performance_weight: float = 0.3 # 0.0-1.0
    prefer_free_models: bool = False
    risk_tolerance: RiskTolerance = RiskTolerance.MEDIUM


@dataclass
class LLMModel:
    """LLM Model specifications"""
    name: str
    cursor_cost: float  # $ per request
    max_method_length: int
    max_file_length: int
    max_context: int  # tokens
    max_concurrent_files: int
    max_imports: int
    mcp_tools: int
    user_sentiment: int  # 1-5 stars
    project_types: List[str]
    reasoning_capability: int  # 1-5
    analysis_quality: int  # 1-5
    internet_access: bool = False


@dataclass
class ModelScore:
    """Scored model with analysis results"""
    model: LLMModel
    score: float
    monthly_cost: float
    cost_per_analysis: float
    meets_budget: bool
    compatibility_score: float
    performance_score: float
    cost_score: float


class ModelSelector:
    """Main class for LLM model selection"""
    
    def __init__(self):
        self.models = self._load_model_database()
    
    def _load_model_database(self) -> List[LLMModel]:
        """Load the complete model database"""
        return [
            # Free Models (0 requests/message)
            LLMModel(
                name="GPT-4o Mini",
                cursor_cost=0.0,
                max_method_length=35,
                max_file_length=600,
                max_context=128000,
                max_concurrent_files=8,
                max_imports=25,
                mcp_tools=40,
                user_sentiment=3,
                project_types=["Budget Development"],
                reasoning_capability=2,
                analysis_quality=3
            ),
            LLMModel(
                name="DeepSeek V3.1",
                cursor_cost=0.0,
                max_method_length=45,
                max_file_length=800,
                max_context=128000,
                max_concurrent_files=12,
                max_imports=20,
                mcp_tools=45,
                user_sentiment=3,
                project_types=["Ultra-Budget"],
                reasoning_capability=3,
                analysis_quality=3
            ),
            LLMModel(
                name="Gemini 2.5 Flash",
                cursor_cost=0.0,
                max_method_length=40,
                max_file_length=600,
                max_context=1000000,
                max_concurrent_files=15,
                max_imports=30,
                mcp_tools=50,
                user_sentiment=3,
                project_types=["Fast, Free Tasks"],
                reasoning_capability=2,
                analysis_quality=3
            ),
            
            # Low-Cost Models
            LLMModel(
                name="Claude 3.5 Haiku",
                cursor_cost=0.013,
                max_method_length=40,
                max_file_length=700,
                max_context=100000,
                max_concurrent_files=8,
                max_imports=20,
                mcp_tools=50,
                user_sentiment=3,
                project_types=["Fast, Light Tasks"],
                reasoning_capability=3,
                analysis_quality=4
            ),
            LLMModel(
                name="o3-Mini",
                cursor_cost=0.01,
                max_method_length=45,
                max_file_length=700,
                max_context=128000,
                max_concurrent_files=10,
                max_imports=20,
                mcp_tools=40,
                user_sentiment=3,
                project_types=["Light Reasoning"],
                reasoning_capability=4,
                analysis_quality=4
            ),
            
            # Standard Models
            LLMModel(
                name="Claude 4 Sonnet",
                cursor_cost=0.04,
                max_method_length=70,
                max_file_length=1500,
                max_context=200000,
                max_concurrent_files=20,
                max_imports=45,
                mcp_tools=100,
                user_sentiment=5,
                project_types=["Enterprise", "AAA Games"],
                reasoning_capability=5,
                analysis_quality=5
            ),
            LLMModel(
                name="Claude 3.7 Sonnet",
                cursor_cost=0.04,
                max_method_length=60,
                max_file_length=1200,
                max_context=200000,
                max_concurrent_files=15,
                max_imports=40,
                mcp_tools=80,
                user_sentiment=5,
                project_types=["Professional Development"],
                reasoning_capability=5,
                analysis_quality=5
            ),
            LLMModel(
                name="GPT-4.1",
                cursor_cost=0.04,
                max_method_length=65,
                max_file_length=1400,
                max_context=1000000,
                max_concurrent_files=30,
                max_imports=40,
                mcp_tools=90,
                user_sentiment=5,
                project_types=["Large Codebases", "Research"],
                reasoning_capability=5,
                analysis_quality=5
            ),
            
            # High-Cost Models
            LLMModel(
                name="o1",
                cursor_cost=0.40,
                max_method_length=65,
                max_file_length=1200,
                max_context=128000,
                max_concurrent_files=20,
                max_imports=35,
                mcp_tools=80,
                user_sentiment=4,
                project_types=["Complex Reasoning"],
                reasoning_capability=5,
                analysis_quality=5
            ),
            LLMModel(
                name="o1 Mini",
                cursor_cost=0.10,
                max_method_length=50,
                max_file_length=800,
                max_context=128000,
                max_concurrent_files=12,
                max_imports=25,
                mcp_tools=50,
                user_sentiment=3,
                project_types=["Moderate Reasoning"],
                reasoning_capability=4,
                analysis_quality=4
            ),
        ]
    
    def filter_by_technical_requirements(self, project: ProjectAttributes) -> List[LLMModel]:
        """Filter models by hard technical requirements"""
        suitable = []
        
        for model in self.models:
            # Use LARGEST values for hard limits (must handle worst case)
            if (model.max_method_length >= project.largest_method_length and
                model.max_file_length >= project.largest_file_length and
                model.max_context >= project.context_window_needed and
                model.max_concurrent_files >= project.max_concurrent_analysis and
                model.max_imports >= project.imports_per_file and
                model.mcp_tools >= project.mcp_tools_needed and
                model.user_sentiment >= project.quality_threshold):
                
                # Check reasoning requirement
                if project.reasoning_required and model.reasoning_capability < 3:
                    continue
                
                # Check internet access requirement
                if project.internet_access_needed and not model.internet_access:
                    continue
                
                suitable.append(model)
        
        return suitable
    
    def calculate_monthly_cost(self, model: LLMModel, project: ProjectAttributes) -> float:
        """Calculate monthly analysis cost using MEDIAN values for typical usage"""
        # Base cost per analysis (1 request = $0.04, so cost = cursor_cost * 0.04)
        cost_per_request = model.cursor_cost * 0.04
        
        # Estimate requests per analysis based on project complexity
        complexity_multiplier = 1.0 + project.codebase_complexity
        
        # Use median file length for typical cost estimation
        typical_requests_per_analysis = max(1, project.max_concurrent_analysis * complexity_multiplier)
        
        cost_per_analysis = cost_per_request * typical_requests_per_analysis
        monthly_cost = cost_per_analysis * project.analysis_frequency
        
        return monthly_cost
    
    def calculate_complexity_factor(self, project: ProjectAttributes) -> float:
        """Calculate complexity factor using different metrics appropriately"""
        # Use P95 for realistic complexity assessment
        method_complexity = min(1.0, project.p95_method_length / 100.0)
        file_complexity = min(1.0, project.p95_file_length / 2000.0)
        scale_complexity = min(1.0, project.total_files / 1000.0)
        
        # Add penalty for extreme outliers using LARGEST values
        worst_case_penalty = min(0.3, project.largest_file_length / 5000.0)
        
        return (method_complexity + file_complexity + scale_complexity + worst_case_penalty) / 4.0
    
    def calculate_weighted_score(self, model: LLMModel, project: ProjectAttributes, 
                               preferences: UserPreferences) -> float:
        """Calculate weighted score for model selection"""
        
        # Cost Score (higher is better, lower cost = higher score)
        monthly_cost = self.calculate_monthly_cost(model, project)
        max_reasonable_cost = 50.0  # Normalize against reasonable maximum
        cost_score = max(0.0, (max_reasonable_cost - monthly_cost) / max_reasonable_cost)
        
        # Performance Score
        performance_score = ((model.reasoning_capability + model.analysis_quality) / 10.0)
        
        # Compatibility Score
        complexity_factor = self.calculate_complexity_factor(project)
        
        # Bonus for project type specialization
        specialization_bonus = 0.0
        for project_type in model.project_types:
            if project_type.lower() in project.project_type.lower():
                specialization_bonus = 0.2
                break
        
        compatibility_score = min(1.0, (1.0 - complexity_factor) + specialization_bonus)
        
        # User Sentiment Score
        sentiment_score = model.user_sentiment / 5.0
        
        # Weighted final score
        final_score = (
            preferences.cost_weight * cost_score +
            preferences.performance_weight * performance_score +
            preferences.sentiment_weight * sentiment_score +
            0.1 * compatibility_score  # Small bonus for compatibility
        )
        
        # Apply free model preference
        if preferences.prefer_free_models and model.cursor_cost == 0.0:
            final_score *= 1.2
        
        return final_score
    
    def select_model(self, project: ProjectAttributes, 
                    preferences: UserPreferences) -> Tuple[List[ModelScore], Dict]:
        """Main selection algorithm"""
        
        # Step 1: Filter by technical requirements
        suitable_models = self.filter_by_technical_requirements(project)
        
        if not suitable_models:
            return [], {
                "error": "No models meet the technical requirements",
                "total_models_evaluated": len(self.models),
                "technically_suitable": 0,
                "budget_compatible": 0,
                "recommended_model": None,
                "monthly_cost_range": {"min": 0, "max": 0}
            }
        
        # Step 2: Calculate scores
        scored_models = []
        for model in suitable_models:
            monthly_cost = self.calculate_monthly_cost(model, project)
            cost_per_analysis = monthly_cost / project.analysis_frequency
            meets_budget = monthly_cost <= project.budget_limit
            
            score = self.calculate_weighted_score(model, project, preferences)
            
            scored_models.append(ModelScore(
                model=model,
                score=score,
                monthly_cost=monthly_cost,
                cost_per_analysis=cost_per_analysis,
                meets_budget=meets_budget,
                compatibility_score=self.calculate_complexity_factor(project),
                performance_score=(model.reasoning_capability + model.analysis_quality) / 10.0,
                cost_score=max(0.0, (50.0 - monthly_cost) / 50.0)
            ))
        
        # Step 3: Sort by score (highest first)
        scored_models.sort(key=lambda x: x.score, reverse=True)
        
        # Step 4: Filter by budget if needed
        budget_compatible = [m for m in scored_models if m.meets_budget]
        
        # Analysis summary
        analysis = {
            "total_models_evaluated": len(self.models),
            "technically_suitable": len(suitable_models),
            "budget_compatible": len(budget_compatible),
            "recommended_model": scored_models[0].model.name if scored_models else None,
            "monthly_cost_range": {
                "min": min(m.monthly_cost for m in scored_models) if scored_models else 0,
                "max": max(m.monthly_cost for m in scored_models) if scored_models else 0
            }
        }
        
        return scored_models, analysis
    
    def suggest_optimizations(self, project: ProjectAttributes, 
                            scored_models: List[ModelScore]) -> Dict:
        """Suggest cost optimization strategies"""
        if not scored_models:
            return {}
        
        optimizations = {}
        
        # Find free alternatives
        free_models = [m for m in scored_models if m.model.cursor_cost == 0.0]
        if free_models:
            optimizations["free_alternative"] = {
                "model": free_models[0].model.name,
                "monthly_savings": scored_models[0].monthly_cost,
                "quality_tradeoff": scored_models[0].model.analysis_quality - free_models[0].model.analysis_quality
            }
        
        # Hybrid approach suggestion
        if len(scored_models) >= 2:
            premium = scored_models[0]
            budget = scored_models[-1]
            
            # 80% budget model, 20% premium model
            hybrid_cost = (0.8 * budget.monthly_cost + 0.2 * premium.monthly_cost)
            savings = premium.monthly_cost - hybrid_cost
            
            if savings > 0:
                optimizations["hybrid_approach"] = {
                    "routine_model": budget.model.name,
                    "complex_model": premium.model.name,
                    "monthly_cost": hybrid_cost,
                    "monthly_savings": savings,
                    "split": "80% routine / 20% complex"
                }
        
        # Frequency optimization
        if project.analysis_frequency > 10:
            reduced_frequency = max(5, project.analysis_frequency // 2)
            savings = (scored_models[0].monthly_cost * 
                      (project.analysis_frequency - reduced_frequency) / project.analysis_frequency)
            
            optimizations["frequency_optimization"] = {
                "current_frequency": project.analysis_frequency,
                "suggested_frequency": reduced_frequency,
                "monthly_savings": savings
            }
        
        return optimizations


def create_sample_project() -> ProjectAttributes:
    """Create a sample project for testing"""
    return ProjectAttributes(
        # File Size Distribution
        largest_file_length=800,
        p95_file_length=650,
        median_file_length=400,
        average_file_length=450,
        
        # Method Length Distribution
        largest_method_length=50,
        p95_method_length=40,
        median_method_length=25,
        
        # Project Scale
        total_files=100,
        max_concurrent_analysis=5,
        imports_per_file=20,
        codebase_complexity=0.3,
        context_window_needed=100000,
        
        # Project Characteristics
        project_type="Web Development",
        programming_languages=["TypeScript", "JavaScript"],
        frameworks_used=["React", "Node.js", "Express"],
        architecture_pattern="MVC",
        
        # Analysis Requirements
        analysis_depth=AnalysisDepth.MEDIUM,
        analysis_frequency=10,
        reasoning_required=False,
        internet_access_needed=False,
        mcp_tools_needed=30,
        
        # Constraints
        budget_limit=10.0,
        quality_threshold=3,
        max_cost_per_analysis=1.0
    )


def print_analysis_results(scored_models: List[ModelScore], analysis: Dict, 
                          optimizations: Dict):
    """Print formatted analysis results"""
    print("\n" + "="*80)
    print("🎯 LLM MODEL SELECTION ANALYSIS")
    print("="*80)
    
    print(f"\n📊 ANALYSIS SUMMARY")
    print(f"Total models evaluated: {analysis['total_models_evaluated']}")
    print(f"Technically suitable: {analysis['technically_suitable']}")
    print(f"Budget compatible: {analysis['budget_compatible']}")
    
    if not scored_models:
        print("\n❌ No suitable models found!")
        return
    
    print(f"\n🏆 RECOMMENDED MODEL: {scored_models[0].model.name}")
    print(f"Monthly Cost: ${scored_models[0].monthly_cost:.2f}")
    print(f"Cost per Analysis: ${scored_models[0].cost_per_analysis:.2f}")
    print(f"Quality Rating: {'⭐' * scored_models[0].model.analysis_quality}")
    print(f"Overall Score: {scored_models[0].score:.2f}/1.0")
    print(f"Budget Compatible: {'✅' if scored_models[0].meets_budget else '❌'}")
    
    print(f"\n📋 TOP 5 ALTERNATIVES:")
    for i, model_score in enumerate(scored_models[:5], 1):
        budget_icon = "✅" if model_score.meets_budget else "❌"
        print(f"{i}. {model_score.model.name:<20} "
              f"${model_score.monthly_cost:>6.2f}/mo "
              f"{'⭐' * model_score.model.analysis_quality} "
              f"Score: {model_score.score:.2f} {budget_icon}")
    
    if optimizations:
        print(f"\n💡 OPTIMIZATION OPPORTUNITIES:")
        
        if "free_alternative" in optimizations:
            opt = optimizations["free_alternative"]
            print(f"Free Alternative: {opt['model']} "
                  f"(saves ${opt['monthly_savings']:.2f}/mo, "
                  f"quality diff: {opt['quality_tradeoff']})")
        
        if "hybrid_approach" in optimizations:
            opt = optimizations["hybrid_approach"]
            print(f"Hybrid Approach: {opt['routine_model']} + {opt['complex_model']} "
                  f"(${opt['monthly_cost']:.2f}/mo, saves ${opt['monthly_savings']:.2f})")
        
        if "frequency_optimization" in optimizations:
            opt = optimizations["frequency_optimization"]
            print(f"Reduce Frequency: {opt['current_frequency']} → {opt['suggested_frequency']} "
                  f"analyses/mo (saves ${opt['monthly_savings']:.2f})")


def interactive_mode():
    """Interactive mode for user input"""
    print("🤖 Interactive LLM Model Selector")
    print("Please provide your project details:")
    
    # Simplified interactive input for demo
    project_type = input("Project type (e.g., 'Web Development'): ") or "Web Development"
    total_files = int(input("Total files in project: ") or "100")
    largest_file = int(input("Largest file size (lines): ") or "800")
    analysis_freq = int(input("Analysis frequency (times/month): ") or "10")
    budget = float(input("Monthly budget ($): ") or "5.0")
    quality_min = int(input("Minimum quality (1-5 stars): ") or "3")
    
    # Create project with user inputs and reasonable defaults
    project = ProjectAttributes(
        largest_file_length=largest_file,
        p95_file_length=int(largest_file * 0.8),
        median_file_length=int(largest_file * 0.5),
        average_file_length=int(largest_file * 0.6),
        largest_method_length=min(80, largest_file // 10),
        p95_method_length=min(60, largest_file // 15),
        median_method_length=min(40, largest_file // 20),
        total_files=total_files,
        max_concurrent_analysis=min(8, total_files // 10),
        imports_per_file=20,
        codebase_complexity=0.3,
        context_window_needed=100000,
        project_type=project_type,
        programming_languages=["JavaScript"],
        frameworks_used=["React"],
        architecture_pattern="MVC",
        analysis_depth=AnalysisDepth.MEDIUM,
        analysis_frequency=analysis_freq,
        reasoning_required=True,
        internet_access_needed=False,
        mcp_tools_needed=30,
        budget_limit=budget,
        quality_threshold=quality_min,
        max_cost_per_analysis=budget / analysis_freq
    )
    
    return project


def main():
    parser = argparse.ArgumentParser(description="LLM Model Selector for Project Analysis")
    parser.add_argument("--config", help="JSON config file with project details")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--sample", action="store_true", help="Run with sample project")
    
    args = parser.parse_args()
    
    selector = ModelSelector()
    preferences = UserPreferences()
    
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
        project = ProjectAttributes(**config['project'])
        if 'preferences' in config:
            preferences = UserPreferences(**config['preferences'])
    elif args.interactive:
        project = interactive_mode()
    else:
        project = create_sample_project()
        print("🔬 Running analysis with sample project...")
    
    # Run analysis
    scored_models, analysis = selector.select_model(project, preferences)
    optimizations = selector.suggest_optimizations(project, scored_models)
    
    # Print results
    print_analysis_results(scored_models, analysis, optimizations)
    
    # Save results to JSON if desired
    save_results = input("\nSave results to JSON? (y/n): ").lower().strip()
    if save_results == 'y':
        results = {
            "project": asdict(project),
            "preferences": asdict(preferences),
            "analysis": analysis,
            "recommendations": [
                {
                    "model": model_score.model.name,
                    "monthly_cost": model_score.monthly_cost,
                    "score": model_score.score,
                    "meets_budget": model_score.meets_budget
                }
                for model_score in scored_models[:5]
            ],
            "optimizations": optimizations
        }
        
        with open("model_selection_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print("Results saved to model_selection_results.json")


if __name__ == "__main__":
    main() 