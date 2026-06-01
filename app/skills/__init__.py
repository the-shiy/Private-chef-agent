from app.skills.registry import Skill, skill_registry
from app.skills.nutrition_analyzer import analyze_nutrition
from app.skills.shopping_list import generate_shopping_list
from app.skills.meal_planner import plan_meals
from app.skills.ingredient_substitutor import substitute_ingredient


def register_all_skills():
    skills = [
        Skill(
            name="nutrition_analyzer",
            display_name="Nutrition Analyzer",
            description="Analyze nutritional content of recipes. Provides calorie "
                        "counts, macro breakdown, and health assessments from "
                        "ingredient lists or recipe names.",
            handler=analyze_nutrition,
            enabled=True,
            requires_recipe_db=True,
        ),
        Skill(
            name="shopping_list",
            display_name="Shopping List Generator",
            description="Generate categorized grocery shopping lists from "
                        "recipes. Organizes ingredients by store section "
                        "(produce, protein, dairy, pantry, etc.) for easy shopping.",
            handler=generate_shopping_list,
            enabled=True,
            requires_recipe_db=True,
        ),
        Skill(
            name="meal_planner",
            display_name="Meal Planner",
            description="Create balanced multi-day meal plans based on dietary "
                        "preferences. Supports high-protein, low-carb, vegetarian, "
                        "and cuisine-specific plans for up to 7 days.",
            handler=plan_meals,
            enabled=True,
            requires_recipe_db=True,
        ),
        Skill(
            name="ingredient_substitutor",
            display_name="Ingredient Substitutor",
            description="Find healthy ingredient substitutions for dietary "
                        "restrictions (dairy-free, gluten-free, vegan, low-carb). "
                        "Includes cooking tips for each substitute.",
            handler=substitute_ingredient,
            enabled=True,
            requires_recipe_db=False,
        ),
    ]
    for skill in skills:
        skill_registry.register(skill)
