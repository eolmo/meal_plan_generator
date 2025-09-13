# run_meal_plan.py
from meal_plan_generator.generator import MealPlanGenerator
from meal_plan_generator.foods import FOODS

def main():
    # Example setup
    calorie_target = 2200
    diet_type = "balanced"

    generator = MealPlanGenerator(calorie_target=calorie_target, diet_type=diet_type)
    meal_plan = generator.generate(foods=FOODS)

    print("\n--- 7-Day Meal Plan ---\n")
    for day, meals in meal_plan.items():
        print(f"{day}:")
        for meal_type, meal in meals.items():
            print(f"  {meal_type.capitalize()}: {meal}")
        print()

if __name__ == "__main__":
    main()
