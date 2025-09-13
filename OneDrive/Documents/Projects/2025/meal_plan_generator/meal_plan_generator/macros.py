# meal_plan_generator/macros.py

def get_macro_ratios(diet_type: str):
    diet_type = diet_type.lower()
    if diet_type == "keto":
        return {"protein": 0.25, "carbs": 0.05, "fat": 0.70}
    elif diet_type == "mediterranean":
        return {"protein": 0.20, "carbs": 0.50, "fat": 0.30}
    else:  # balanced
        return {"protein": 0.30, "carbs": 0.40, "fat": 0.30}
