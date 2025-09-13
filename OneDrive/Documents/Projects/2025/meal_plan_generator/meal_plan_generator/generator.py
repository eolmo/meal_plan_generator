import json

# ----------------------------
# Sample Food Database (can expand later)
# ----------------------------
FOODS = {
    "oatmeal": {"calories": 150, "protein": 5, "carbs": 27, "fat": 3},
    "chicken_breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
    "brown_rice": {"calories": 215, "protein": 5, "carbs": 45, "fat": 1.8},
    "broccoli": {"calories": 55, "protein": 4, "carbs": 11, "fat": 0.6},
    "almonds": {"calories": 170, "protein": 6, "carbs": 6, "fat": 15},
    "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13},
    "eggs": {"calories": 70, "protein": 6, "carbs": 0.5, "fat": 5},
    "quinoa": {"calories": 120, "protein": 4, "carbs": 21, "fat": 1.9},
    "spinach": {"calories": 20, "protein": 2, "carbs": 3, "fat": 0.2},
    "greek_yogurt": {"calories": 100, "protein": 10, "carbs": 6, "fat": 0}
}

# ----------------------------
# User Input
# ----------------------------
print("Welcome to the Macro Meal Planner!\n")

age = int(input("Enter your age: "))
weight = float(input("Enter your weight (kg): "))
height = float(input("Enter your height (cm): "))
activity_level = input("Enter activity level (sedentary, light, moderate, active): ").lower()
calorie_target = int(input("Enter daily calorie target: "))
diet_type = input("Enter diet type (balanced, keto, mediterranean): ").lower()

# ----------------------------
# Sample Macro Ratios
# ----------------------------
def get_macro_ratios(diet_type):
    if diet_type == "keto":
        return {"protein": 0.25, "carbs": 0.05, "fat": 0.70}
    elif diet_type == "mediterranean":
        return {"protein": 0.20, "carbs": 0.50, "fat": 0.30}
    else:  # balanced
        return {"protein": 0.30, "carbs": 0.40, "fat": 0.30}

macro_ratios = get_macro_ratios(diet_type)

# ----------------------------
# Generate Meal Plan
# ----------------------------
def generate_meal_plan():
    plan = {}
    meals = ["Breakfast", "Lunch", "Dinner", "Snack"]
    
    # Simple approach: pick 2-3 foods per meal
    food_keys = list(FOODS.keys())
    
    for day in range(1, 8):
        day_plan = {}
        for meal in meals:
            meal_items = []
            # Pick 2 random foods (for prototype simplicity)
            import random
            choices = random.sample(food_keys, 2)
            for item in choices:
                meal_items.append({"food": item, **FOODS[item]})
            day_plan[meal] = meal_items
        plan[f"Day {day}"] = day_plan
    return plan

meal_plan = generate_meal_plan()

# ----------------------------
# Display Meal Plan with Macros
# ----------------------------
for day, meals in meal_plan.items():
    print(f"\n=== {day} ===")
    for meal_name, items in meals.items():
        print(f"\n{meal_name}:")
        total_cals = total_protein = total_carbs = total_fat = 0
        for item in items:
            print(f" - {item['food']} | {item['calories']} kcal, P:{item['protein']}g, C:{item['carbs']}g, F:{item['fat']}g")
            total_cals += item['calories']
            total_protein += item['protein']
            total_carbs += item['carbs']
            total_fat += item['fat']
        print(f"Total: {total_cals} kcal, P:{total_protein}g, C:{total_carbs}g, F:{total_fat}g")

# ----------------------------
# Save Plan to JSON
# ----------------------------
with open("meal_plan.json", "w") as f:
    json.dump(meal_plan, f, indent=4)

print("\nMeal plan saved to 'meal_plan.json'.")
