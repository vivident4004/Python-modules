def validate_ingredients(ingredients: str) -> str:
    ing = set(ingredients.strip().split(" "))
    valid_ingredients = {"air", "earth", "fire", "water"}
    if all(i in valid_ingredients for i in ing) and ingredients:
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
