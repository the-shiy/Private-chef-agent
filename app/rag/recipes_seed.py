"""Seed recipes for AI Personal Chef RAG knowledge base.

Each recipe dict:
    id: unique slug identifier
    name: recipe name
    ingredients: comma-separated ingredient list
    cuisine: Western / Chinese / Mediterranean / Japanese / Korean / Fusion
    difficulty: easy / medium / hard
    cooking_time: minutes
    nutrition: nutrition facts summary
    steps: numbered cooking steps
    tags: comma-separated attribute tags

To rebuild the vector index after editing this file, restart the server
or call RecipeVectorStore.rebuild(SEED_RECIPES).
"""

SEED_RECIPES: list[dict] = [
    # ==================== High Protein (5) ====================
    {
        "id": "recipe_hp_001",
        "name": "High-Protein Grilled Chicken Quinoa Bowl",
        "ingredients": "chicken breast, quinoa, avocado, cherry tomatoes, cucumber, lemon, olive oil, salt, black pepper",
        "cuisine": "Western",
        "difficulty": "easy",
        "cooking_time": 25,
        "nutrition": "Protein: 45g, Carbs: 38g, Fat: 18g, ~520 kcal. High protein, balanced macros.",
        "steps": "1. Season chicken with salt, pepper, and olive oil, marinate 10 min. 2. Grill 6-7 min per side until golden. 3. Cook quinoa per package instructions. 4. Dice avocado, halve tomatoes, slice cucumber. 5. Assemble bowl and drizzle with lemon juice.",
        "tags": "high-protein, meal-prep, gluten-free, dairy-free"
    },
    {
        "id": "recipe_hp_002",
        "name": "Pan-Seared Salmon with Asparagus",
        "ingredients": "salmon fillet, asparagus, garlic, lemon, olive oil, dill, salt, black pepper",
        "cuisine": "Mediterranean",
        "difficulty": "easy",
        "cooking_time": 20,
        "nutrition": "Protein: 38g, Carbs: 8g, Fat: 22g, ~420 kcal. Rich in Omega-3 fatty acids.",
        "steps": "1. Season salmon with salt, pepper, and dill. 2. Heat olive oil, sear skin-side down 4 min. 3. Flip and cook 3 more min. 4. Blanch asparagus 1 min, then pan-sear 2 min with salmon. 5. Finish with fresh lemon juice.",
        "tags": "high-protein, low-carb, omega-3, quick"
    },
    {
        "id": "recipe_hp_003",
        "name": "Korean Tofu Bibimbap Bowl",
        "ingredients": "firm tofu, spinach, carrot, bean sprouts, egg, gochujang sauce, sesame oil, steamed rice",
        "cuisine": "Korean",
        "difficulty": "medium",
        "cooking_time": 30,
        "nutrition": "Protein: 32g, Carbs: 52g, Fat: 15g, ~510 kcal. High plant protein, rich dietary fiber.",
        "steps": "1. Press tofu dry with paper towels, slice thick, pan-fry until golden. 2. Blanch spinach, squeeze dry, mix with garlic and sesame oil. 3. Julienne and saute carrot, blanch bean sprouts. 4. Fry a sunny-side-up egg. 5. Layer rice, all toppings in a bowl, add gochujang and mix well.",
        "tags": "high-protein, vegetarian-option, Korean, fiber-rich"
    },
    {
        "id": "recipe_hp_004",
        "name": "Lean Beef and Broccoli Stir-Fry",
        "ingredients": "lean beef sirloin, broccoli, bell peppers, onion, garlic, soy sauce, oyster sauce, cooking wine, cornstarch, olive oil",
        "cuisine": "Chinese",
        "difficulty": "easy",
        "cooking_time": 20,
        "nutrition": "Protein: 42g, Carbs: 18g, Fat: 12g, ~380 kcal. Rich in iron, high vitamin C.",
        "steps": "1. Slice beef against the grain, marinate with wine, soy sauce, cornstarch 10 min. 2. Blanch broccoli florets 1 min. 3. High-heat stir-fry beef until color changes, set aside. 4. Saute garlic and onion, add bell peppers and broccoli. 5. Return beef, add oyster sauce, toss well.",
        "tags": "high-protein, Chinese, low-carb, iron-rich"
    },
    {
        "id": "recipe_hp_005",
        "name": "Shrimp and Egg White Scramble",
        "ingredients": "shrimp, egg whites (4) + 1 whole egg, spinach, cherry tomatoes, onion, olive oil, salt",
        "cuisine": "Fusion",
        "difficulty": "easy",
        "cooking_time": 15,
        "nutrition": "Protein: 40g, Carbs: 10g, Fat: 14g, ~340 kcal. Low-fat high-protein, quick muscle-building meal.",
        "steps": "1. Marinate shrimp with salt and wine 5 min. 2. Whisk egg whites and whole egg with salt. 3. Pan-sear shrimp until pink, set aside. 4. Saute onion, add spinach and tomatoes. 5. Pour in eggs and shrimp, cook low heat stirring gently until set.",
        "tags": "high-protein, low-carb, quick, muscle-building"
    },

    # ==================== Low-Carb (4) ====================
    {
        "id": "recipe_lc_001",
        "name": "Cauliflower Chicken Fried Rice",
        "ingredients": "cauliflower, diced chicken breast, diced carrot, green peas, eggs, onion, soy sauce, olive oil",
        "cuisine": "Chinese",
        "difficulty": "easy",
        "cooking_time": 20,
        "nutrition": "Protein: 35g, Carbs: 15g (1/3 of regular fried rice), Fat: 16g, ~360 kcal.",
        "steps": "1. Pulse cauliflower in food processor to rice-sized grains. 2. Dice and marinate chicken. 3. Scramble eggs in pan, set aside. 4. Cook chicken until white, add onion, carrot, peas. 5. Add cauliflower rice, stir-fry 3 min, add soy sauce, fold in egg.",
        "tags": "low-carb, high-protein, gluten-free, creative"
    },
    {
        "id": "recipe_lc_002",
        "name": "Zucchini Noodles with Basil Pesto",
        "ingredients": "zucchini, fresh basil, pine nuts, Parmesan cheese, garlic, olive oil, cherry tomatoes, salt",
        "cuisine": "Mediterranean",
        "difficulty": "easy",
        "cooking_time": 15,
        "nutrition": "Protein: 12g, Carbs: 10g, Fat: 28g, ~350 kcal. Very low carb, rich in healthy fats.",
        "steps": "1. Spiralize zucchini into noodle shape. 2. Blend basil, pine nuts, garlic, olive oil, Parmesan into pesto. 3. Heat olive oil, toss zucchini noodles 1 min (do not overcook). 4. Mix in pesto, top with halved cherry tomatoes.",
        "tags": "low-carb, keto-friendly, Mediterranean, vegetarian-option"
    },
    {
        "id": "recipe_lc_003",
        "name": "Lettuce-Wrapped Turkey Burgers",
        "ingredients": "ground turkey, romaine lettuce leaves, tomato, onion, pickles, mustard, salt, black pepper",
        "cuisine": "Western",
        "difficulty": "easy",
        "cooking_time": 15,
        "nutrition": "Protein: 38g, Carbs: 8g, Fat: 10g, ~300 kcal. Bread-free, extremely low carb.",
        "steps": "1. Mix ground turkey with salt, pepper, minced onion, form into patties. 2. Cook 5 min per side over medium heat. 3. Wash and dry lettuce leaves as the bun. 4. Layer patty, tomato slices, pickles, drizzle mustard. 5. Wrap tightly with lettuce.",
        "tags": "low-carb, high-protein, gluten-free, keto-friendly"
    },
    {
        "id": "recipe_lc_004",
        "name": "Eggplant Lasagna Stack (No-Pasta)",
        "ingredients": "large eggplant, lean ground beef, canned tomatoes, onion, mozzarella, garlic, Italian herbs, olive oil",
        "cuisine": "Western",
        "difficulty": "medium",
        "cooking_time": 45,
        "nutrition": "Protein: 32g, Carbs: 18g, Fat: 22g, ~420 kcal. Eggplant replaces pasta sheets.",
        "steps": "1. Slice eggplant lengthwise 0.5cm thick, salt and rest 10 min to remove bitterness. 2. Pan-fry eggplant slices until lightly charred. 3. Saute garlic and onion, brown beef, add tomatoes and herbs, simmer 15 min. 4. Layer meat sauce, eggplant slices, and cheese in baking dish. 5. Top with mozzarella, bake at 180C for 20 min.",
        "tags": "low-carb, high-protein, Italian-style, keto-friendly"
    },

    # ==================== Mediterranean (3) ====================
    {
        "id": "recipe_med_001",
        "name": "Greek Salad with Grilled Halloumi",
        "ingredients": "halloumi cheese, tomatoes, cucumber, red onion, kalamata olives, olive oil, oregano, red wine vinegar, salt",
        "cuisine": "Mediterranean",
        "difficulty": "easy",
        "cooking_time": 10,
        "nutrition": "Protein: 22g, Carbs: 12g, Fat: 28g, ~420 kcal. Mediterranean diet, anti-inflammatory.",
        "steps": "1. Chop tomatoes, slice cucumber, thinly slice red onion, halve olives, mix. 2. Dress with olive oil, red wine vinegar, oregano, salt. 3. Slice halloumi 1cm thick, dry-grill 1 min each side until golden. 4. Place grilled halloumi on salad and serve immediately.",
        "tags": "Mediterranean, vegetarian-option, quick, anti-inflammatory"
    },
    {
        "id": "recipe_med_002",
        "name": "Mediterranean Baked Cod with Peppers",
        "ingredients": "cod fillet, bell peppers, cherry tomatoes, black olives, garlic, lemon, thyme, olive oil, salt",
        "cuisine": "Mediterranean",
        "difficulty": "easy",
        "cooking_time": 25,
        "nutrition": "Protein: 35g, Carbs: 10g, Fat: 12g, ~300 kcal. High protein, low fat, lean white fish.",
        "steps": "1. Preheat oven to 200C. 2. Pat cod dry, season with salt, olive oil, thyme. 3. Arrange pepper strips, tomatoes, olives, garlic on baking sheet. 4. Place cod on vegetables, drizzle lemon juice. 5. Bake 15-18 min at 200C until fish flakes easily.",
        "tags": "Mediterranean, high-protein, low-fat, baked"
    },
    {
        "id": "recipe_med_003",
        "name": "Chickpea and Spinach Stew",
        "ingredients": "canned chickpeas, spinach, onion, sun-dried tomatoes, garlic, cumin, paprika, olive oil, vegetable broth",
        "cuisine": "Mediterranean",
        "difficulty": "easy",
        "cooking_time": 25,
        "nutrition": "Protein: 18g, Carbs: 42g, Fat: 10g, ~350 kcal. Plant protein, high iron, vegetarian.",
        "steps": "1. Saute diced onion and minced garlic in olive oil. 2. Add cumin and paprika, cook 30 sec until fragrant. 3. Add drained chickpeas and chopped sun-dried tomatoes, stir. 4. Pour vegetable broth, simmer 15 min. 5. Fold in spinach until wilted, season with salt.",
        "tags": "Mediterranean, vegetarian, high-fiber, iron-rich"
    },

    # ==================== Vegetarian (3) ====================
    {
        "id": "recipe_veg_001",
        "name": "Red Lentil and Sweet Potato Coconut Curry",
        "ingredients": "red lentils, sweet potato, coconut milk, curry powder, onion, garlic, ginger, spinach, olive oil, salt",
        "cuisine": "Fusion",
        "difficulty": "easy",
        "cooking_time": 35,
        "nutrition": "Protein: 22g, Carbs: 48g, Fat: 14g, ~430 kcal. Plant protein with complex carbs.",
        "steps": "1. Peel and cube sweet potato. 2. Saute onion, garlic, and ginger. 3. Add curry powder, cook 30 sec, then add sweet potato, lentils, and coconut milk. 4. Add water, simmer 25 min until lentils are soft. 5. Stir in spinach until wilted, season with salt, serve with rice.",
        "tags": "vegetarian, high-protein, curry, fiber-rich"
    },
    {
        "id": "recipe_veg_002",
        "name": "Quinoa Stuffed Bell Peppers",
        "ingredients": "large bell peppers, quinoa, black beans, corn kernels, tomatoes, cumin, cilantro, lime, salt",
        "cuisine": "Fusion",
        "difficulty": "medium",
        "cooking_time": 30,
        "nutrition": "Protein: 18g, Carbs: 45g, Fat: 8g, ~340 kcal. Colorful, nutritionally complete.",
        "steps": "1. Cook quinoa per package instructions. 2. Cut tops off peppers and remove seeds. 3. Mix quinoa, black beans, corn, diced tomatoes, cumin, salt. 4. Stuff peppers firmly with mixture. 5. Bake at 180C for 15 min, garnish with cilantro and lime juice.",
        "tags": "vegetarian, high-fiber, colorful, meal-prep"
    },
    {
        "id": "recipe_veg_003",
        "name": "Japanese Mushroom and Tofu Hot Pot",
        "ingredients": "soft tofu, shiitake mushrooms, enoki mushrooms, shimeji mushrooms, napa cabbage, kombu dashi, mirin, soy sauce, scallion",
        "cuisine": "Japanese",
        "difficulty": "easy",
        "cooking_time": 20,
        "nutrition": "Protein: 20g, Carbs: 14g, Fat: 6g, ~180 kcal. Very low calorie, warm and comforting.",
        "steps": "1. Bring kombu dashi, mirin, and soy sauce to a boil. 2. Cut tofu into cubes, trim mushrooms, chop cabbage. 3. Arrange all ingredients in the pot. 4. Simmer 10 min until ingredients absorb the broth. 5. Garnish with scallions, serve with dipping sauce.",
        "tags": "vegetarian, low-calorie, Japanese, high-protein"
    },

    # ==================== Quick & Easy (3) ====================
    {
        "id": "recipe_qe_001",
        "name": "Avocado Poached Egg Toast",
        "ingredients": "whole wheat toast, avocado, egg, lemon juice, red pepper flakes, salt, black pepper",
        "cuisine": "Western",
        "difficulty": "easy",
        "cooking_time": 10,
        "nutrition": "Protein: 15g, Carbs: 28g, Fat: 20g, ~370 kcal. Balanced nutrition, perfect breakfast.",
        "steps": "1. Toast bread until lightly crisp. 2. Halve avocado, remove pit, mash with lemon juice and salt. 3. Poach egg: bring water to boil, turn off heat, create whirlpool, crack egg in, steep 3 min. 4. Spread avocado mash on toast, place poached egg, sprinkle pepper flakes and black pepper.",
        "tags": "quick, breakfast, high-fiber, healthy-fats"
    },
    {
        "id": "recipe_qe_002",
        "name": "Overnight Oats with Mixed Berries",
        "ingredients": "rolled oats, Greek yogurt, blueberries, strawberries, chia seeds, honey, sliced almonds",
        "cuisine": "Western",
        "difficulty": "easy",
        "cooking_time": 5,
        "nutrition": "Protein: 18g, Carbs: 45g, Fat: 10g, ~360 kcal. High fiber, rich in probiotics.",
        "steps": "1. In a mason jar, combine oats, Greek yogurt, and chia seeds. 2. Add water or milk to cover oats, stir. 3. Layer blueberries and sliced strawberries on top. 4. Drizzle honey, sprinkle almonds. 5. Refrigerate overnight (min 6 hours), grab and eat.",
        "tags": "quick, breakfast, meal-prep, high-fiber"
    },
    {
        "id": "recipe_qe_003",
        "name": "Miso Tofu Vegetable Soup",
        "ingredients": "white miso paste, soft tofu, dried wakame seaweed, daikon radish, carrot, kombu dashi, scallion",
        "cuisine": "Japanese",
        "difficulty": "easy",
        "cooking_time": 15,
        "nutrition": "Protein: 12g, Carbs: 16g, Fat: 5g, ~150 kcal. Low-calorie warming soup, probiotic-rich.",
        "steps": "1. Rehydrate wakame, dice tofu, thinly slice daikon and carrot. 2. Bring kombu dashi to boil, add daikon and carrot, cook 5 min. 3. Lower heat, add tofu cubes and wakame. 4. Dissolve miso in a ladle of broth first, then add to pot (do not boil). 5. Garnish with scallions and serve immediately.",
        "tags": "quick, low-calorie, Japanese, vegetarian-option"
    },

    # ==================== Breakfast (2) ====================
    {
        "id": "recipe_bf_001",
        "name": "High-Protein Banana Oat Pancakes",
        "ingredients": "banana, rolled oats, eggs, vanilla protein powder, baking powder, Greek yogurt, blueberries",
        "cuisine": "Western",
        "difficulty": "easy",
        "cooking_time": 15,
        "nutrition": "Protein: 30g, Carbs: 42g, Fat: 8g, ~370 kcal. Muscle-building breakfast, no flour.",
        "steps": "1. Mash banana until smooth. 2. Mix in oats, eggs, protein powder, baking powder to form batter. 3. Heat non-stick pan over medium, pour batter 1/4 cup per pancake. 4. Flip when bubbles appear on surface, cook until golden. 5. Serve with Greek yogurt and blueberries.",
        "tags": "breakfast, high-protein, gluten-free, muscle-building"
    },
    {
        "id": "recipe_bf_002",
        "name": "Green Power Smoothie Bowl",
        "ingredients": "spinach, frozen banana, mango, protein powder, unsweetened almond milk, granola, chia seeds, coconut flakes",
        "cuisine": "Fusion",
        "difficulty": "easy",
        "cooking_time": 5,
        "nutrition": "Protein: 28g, Carbs: 48g, Fat: 12g, ~400 kcal. Multivitamin boost, antioxidant-rich.",
        "steps": "1. Blend spinach, frozen banana, mango chunks, protein powder, almond milk. 2. Blend on high until thick and smooth (thicker than regular smoothie). 3. Pour into a bowl. 4. Top with granola, chia seeds, coconut flakes, and extra fruit slices.",
        "tags": "breakfast, high-protein, vegetarian-option, antioxidant"
    },
]
