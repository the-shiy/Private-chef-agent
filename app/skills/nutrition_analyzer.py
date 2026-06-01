from app.db import recipes_db


async def analyze_nutrition(input_text: str) -> str:
    """Analyze nutritional content of recipes or ingredient lists.

    input_text: recipe name, ingredient list, or meal description.
    Returns: structured nutritional breakdown.
    """
    # Try to look up a recipe by name first
    recipe = recipes_db.get_by_id(input_text)
    if not recipe:
        # Search by name match
        results = recipes_db.list_all(search=input_text, limit=5)
        if results:
            recipe = results[0]

    if recipe:
        return (
            f"Nutrition Analysis for: {recipe['name']}\n"
            f"Cuisine: {recipe['cuisine']} | Difficulty: {recipe['difficulty']} | "
            f"Time: {recipe['cooking_time']} min\n\n"
            f"Ingredients: {recipe['ingredients']}\n\n"
            f"Nutrition: {recipe['nutrition']}\n\n"
            f"Health Notes:\n"
            f"- This recipe uses {len(recipe['ingredients'].split(','))} main ingredients.\n"
            f"- {recipe['tags']}\n"
            f"- A balanced meal with protein, carbs, and fiber for sustained energy."
        )

    # Analyze from ingredient text
    items = [i.strip() for i in input_text.split(",") if i.strip()]
    if not items:
        return "Please provide a recipe name or ingredient list to analyze."

    return (
        f"Estimated Nutrition Analysis for: {', '.join(items)}\n"
        f"Number of ingredients: {len(items)}\n\n"
        f"For accurate macro calculations, please add this as a recipe in the database.\n"
        f"General guidance:\n"
        f"- Aim for 20-40g protein per meal\n"
        f"- Include 2-3 different colored vegetables\n"
        f"- Choose whole food carbs over refined carbs\n"
        f"- Use healthy fats (olive oil, avocado, nuts) in moderation"
    )
