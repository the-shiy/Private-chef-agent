# Ingredient substitution reference data
_SUBSTITUTIONS: dict[str, list[dict[str, str]]] = {
    "dairy": [
        {"original": "milk", "sub": "almond milk / soy milk / oat milk"},
        {"original": "butter", "sub": "olive oil / coconut oil / avocado oil"},
        {"original": "cream", "sub": "coconut cream / cashew cream"},
        {"original": "yogurt", "sub": "coconut yogurt / soy yogurt"},
        {"original": "cheese", "sub": "nutritional yeast / cashew cheese / tofu"},
    ],
    "gluten": [
        {"original": "wheat flour", "sub": "almond flour / coconut flour / oat flour"},
        {"original": "pasta", "sub": "zucchini noodles / chickpea pasta / rice noodles"},
        {"original": "bread", "sub": "lettuce wraps / corn tortillas / rice cakes"},
        {"original": "soy sauce", "sub": "tamari / coconut aminos"},
        {"original": "breadcrumbs", "sub": "crushed almonds / ground oats / pork rinds"},
    ],
    "meat": [
        {"original": "chicken breast", "sub": "tofu / tempeh / seitan / jackfruit"},
        {"original": "ground beef", "sub": "lentils / textured vegetable protein / mushrooms"},
        {"original": "salmon", "sub": "marinated tofu steak / king oyster mushroom"},
        {"original": "shrimp", "sub": "king oyster mushroom slices / konjac shrimp"},
        {"original": "egg", "sub": "flax egg (1 tbsp flax + 3 tbsp water) / mashed banana"},
    ],
    "low_carb": [
        {"original": "rice", "sub": "cauliflower rice / shirataki rice"},
        {"original": "pasta", "sub": "zucchini noodles / shirataki noodles / spaghetti squash"},
        {"original": "potato", "sub": "cauliflower / turnip / celery root"},
        {"original": "bread", "sub": "lettuce wraps / cloud bread / almond flour bread"},
        {"original": "sugar", "sub": "stevia / monk fruit / erythritol"},
    ],
    "general": [
        {"original": "salt", "sub": "soy sauce (reduce salt) / herbs / spices / citrus juice"},
        {"original": "olive oil", "sub": "avocado oil / coconut oil / grapeseed oil"},
        {"original": "lemon juice", "sub": "lime juice / vinegar / white wine"},
        {"original": "honey", "sub": "maple syrup / agave / date syrup / stevia"},
        {"original": "rice vinegar", "sub": "apple cider vinegar / white wine vinegar / lemon juice"},
    ],
}


async def substitute_ingredient(input_text: str) -> str:
    """Find substitutions for ingredients based on dietary needs.

    input_text: ingredient name and any dietary restrictions.
    Example: "butter dairy-free" or "rice low carb"
    Returns: ranked substitution options.
    """
    text_lower = input_text.lower()

    # Determine which category to search
    category = "general"
    if any(w in text_lower for w in ["dairy", "milk", "butter", "cream", "cheese", "yogurt",
                                      "dairy-free", "lactose"]):
        category = "dairy"
    elif any(w in text_lower for w in ["gluten", "wheat", "bread", "pasta", "flour",
                                        "gluten-free", "celiac"]):
        category = "gluten"
    elif any(w in text_lower for w in ["meat", "chicken", "beef", "pork", "fish",
                                        "vegan", "vegetarian", "plant-based"]):
        category = "meat"
    elif any(w in text_lower for w in ["low carb", "low-carb", "keto", "rice", "sugar",
                                        "potato", "carb"]):
        category = "low_carb"

    # Find the specific ingredient being asked about
    results = []
    for entry in _SUBSTITUTIONS.get(category, []):
        if entry["original"] in text_lower:
            results.insert(0, entry)
        else:
            results.append(entry)

    if not results:
        results = _SUBSTITUTIONS["general"]

    lines = [f"Ingredient Substitution Guide", "=" * 35]
    lines.append(f"Category: {category.replace('_', ' ').title()}\n")

    for entry in results[:8]:
        lines.append(f"  {entry['original']} -> {entry['sub']}")

    lines.append(
        f"\nTip: Substitutions may affect taste and texture. "
        f"Adjust seasoning and cooking time accordingly."
    )
    return "\n".join(lines)
