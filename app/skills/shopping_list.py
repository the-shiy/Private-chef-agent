from app.db import recipes_db


_SHOPPING_CATEGORIES = {
    "Produce": ["lettuce", "spinach", "kale", "arugula", "tomato", "cucumber", "bell pepper",
                 "carrot", "broccoli", "cauliflower", "zucchini", "eggplant", "asparagus",
                 "celery", "onion", "garlic", "ginger", "avocado", "lemon", "lime",
                 "banana", "blueberries", "strawberries", "mango", "sweet potato", "daikon",
                 "cabbage", "bean sprouts", "mushroom", "shiitake", "enoki", "shimeji",
                 "cherry tomato", "red onion", "scallion"],
    "Protein": ["chicken breast", "chicken", "turkey", "ground turkey", "lean beef",
                "beef sirloin", "ground beef", "salmon", "cod", "shrimp", "tofu",
                "firm tofu", "soft tofu", "egg", "chickpea", "black bean", "lentil",
                "red lentil"],
    "Dairy & Alternatives": ["Greek yogurt", "yogurt", "halloumi", "mozzarella",
                              "Parmesan", "almond milk", "coconut milk", "cheese"],
    "Grains & Pasta": ["quinoa", "rice", "steamed rice", "rolled oats", "oats",
                        "whole wheat toast", "bread", "granola"],
    "Pantry": ["olive oil", "sesame oil", "soy sauce", "oyster sauce", "gochujang",
               "miso paste", "mirin", "vinegar", "red wine vinegar", "canned tomatoes",
               "sun-dried tomato", "corn kernel", "coconut flake", "honey",
               "mustard", "curry powder", "cumin", "paprika", "oregano", "thyme",
               "dill", "Italian herbs", "cooking wine", "cornstarch", "baking powder",
               "protein powder", "vanilla protein powder", "vegetable broth",
               "kombu dashi", "pickle", "black olive", "kalamata olive", "capers"],
    "Nuts & Seeds": ["pine nut", "almond", "sliced almond", "chia seed",
                      "walnut", "cashew", "peanut butter"],
    "Spices & Seasoning": ["salt", "black pepper", "red pepper flake", "gochujang sauce"],
}


def _categorize(ingredient: str) -> str:
    name = ingredient.strip().lower()
    for category, items in _SHOPPING_CATEGORIES.items():
        for item in items:
            if item in name or name in item:
                return category
    return "Other"


async def generate_shopping_list(input_text: str) -> str:
    """Generate a categorized shopping list from recipe names or ingredients.

    input_text: comma-separated recipe names or an ingredient list.
    Returns: categorized shopping list.
    """
    recipe_names = [r.strip() for r in input_text.split(",") if r.strip()]
    all_ingredients: dict[str, set[str]] = {}
    recipes_found = 0

    for name in recipe_names:
        recipes = recipes_db.list_all(search=name, limit=3)
        for recipe in recipes:
            if name.lower() in recipe["name"].lower():
                recipes_found += 1
                for ing in recipe["ingredients"].split(","):
                    ing = ing.strip()
                    cat = _categorize(ing)
                    all_ingredients.setdefault(cat, set()).add(ing)
                break

    if recipes_found == 0:
        # Treat input as ingredient list
        items = [i.strip() for i in input_text.split(",") if i.strip()]
        for item in items:
            cat = _categorize(item)
            all_ingredients.setdefault(cat, set()).add(item)
        header = f"Shopping List (from {len(items)} ingredients)"
    else:
        header = f"Shopping List (from {recipes_found} recipe(s))"

    lines = [header, "=" * 40]
    for category in ["Produce", "Protein", "Dairy & Alternatives",
                      "Grains & Pasta", "Pantry", "Nuts & Seeds",
                      "Spices & Seasoning", "Other"]:
        if category in all_ingredients:
            items = sorted(all_ingredients[category])
            lines.append(f"\n{category}:")
            for item in items:
                lines.append(f"  [ ] {item}")

    lines.append(f"\nTotal items: {sum(len(v) for v in all_ingredients.values())}")
    return "\n".join(lines)
