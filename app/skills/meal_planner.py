from app.db import recipes_db
from app.rag.vector_store import RecipeVectorStore
import os


def _get_vector_store() -> RecipeVectorStore:
    db_path = os.path.join(os.path.dirname(__file__), "..", "db", "personal_chief.db")
    return RecipeVectorStore(
        db_path=db_path,
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )


async def plan_meals(input_text: str) -> str:
    """Plan meals based on dietary preferences and goals.

    input_text: dietary goals, preferences, number of days, meals per day.
    Example: "high protein 3 days 2 meals per day"
    Returns: day-by-day meal plan with recipes.
    """
    text_lower = input_text.lower()

    # Parse simple preferences from input
    prefer_cuisine = None
    for cuisine in ["chinese", "western", "japanese", "mediterranean", "korean", "fusion"]:
        if cuisine in text_lower:
            prefer_cuisine = cuisine.capitalize()
            break

    prefer_difficulty = None
    if "easy" in text_lower or "quick" in text_lower or "simple" in text_lower:
        prefer_difficulty = "easy"
    elif "medium" in text_lower:
        prefer_difficulty = "medium"

    high_protein = "high protein" in text_lower or "protein" in text_lower
    low_carb = "low carb" in text_lower or "low-carb" in text_lower
    vegetarian = "vegetarian" in text_lower or "vegan" in text_lower

    # Determine how many meals to plan
    days = 3
    meals_per_day = 2
    for word in text_lower.split():
        if word.isdigit():
            days = min(int(word), 7)

    total_meals = days * meals_per_day

    # Get all recipes and filter
    all_recipes = recipes_db.get_all_as_dicts()
    filtered = all_recipes

    if prefer_cuisine:
        filtered = [r for r in filtered if r["cuisine"] == prefer_cuisine]
    if prefer_difficulty:
        filtered = [r for r in filtered if r["difficulty"] == prefer_difficulty]
    if high_protein:
        filtered = [r for r in filtered if "high protein" in r["tags"].lower()
                    or "high-protein" in r["tags"].lower()]
    if low_carb:
        filtered = [r for r in filtered if "low-carb" in r["tags"].lower()
                    or "keto" in r["tags"].lower()]
    if vegetarian:
        filtered = [r for r in filtered if "vegetarian" in r["tags"].lower()]

    if len(filtered) < total_meals:
        filtered = all_recipes

    # Pick meals (cycle through filtered list)
    selected = (filtered * (total_meals // len(filtered) + 1))[:total_meals]

    lines = [f"Meal Plan: {days} days x {meals_per_day} meals/day", "=" * 45]
    for day in range(days):
        lines.append(f"\nDay {day + 1}:")
        for meal_idx in range(meals_per_day):
            idx = day * meals_per_day + meal_idx
            if idx < len(selected):
                r = selected[idx]
                meal_type = "Lunch" if meal_idx == 0 else "Dinner"
                lines.append(
                    f"  {meal_type}: {r['name']} "
                    f"[{r['cuisine']}, {r['difficulty']}, {r['cooking_time']}min]"
                )
                lines.append(f"    {r['nutrition']}")

    lines.append(f"\nTip: Use /api/v1/skills/shopping_list to generate a shopping list!")
    return "\n".join(lines)
