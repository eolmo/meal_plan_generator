# generator.py
import random
import json
from meal_plan_generator.foods import FOODS
from meal_plan_generator.macros import get_macro_ratios

class MealPlanGenerator:
    def __init__(self, age, weight, height, activity_level, calorie_target, diet_type):
        """
        Initialize the generator with user inputs
        """
        self.age = age
        self.weight = weight          # kg
        self.height = height          # cm
        self.activity_level = activity_level
        self.calorie_target = calorie_target
        self.diet_type = diet_type
        self.macro_ratios = get_macro_ratios(diet_type)

    def generate_meal_plan(self):
        """
        Generate a simple 7-day meal plan using FOODS.
        Each meal gets 2 random foods for prototype simplicity.
        """
        plan = {}
        meals = ["Breakfast", "Lunch", "Dinner", "Snack"]
        food_keys = list(FOODS.keys())

        for day in range(1, 8):
            day_plan = {}
            for meal in meals:
                meal_items = []
                choices = random.sample(food_keys, 2)
                for item in choices:
                    meal_items.append({"food": item, **FOODS[item]})
                day_plan[meal] = meal_items
            plan[f"Day {day}"] = day_plan

        return plan

    def save_plan_to_json(self, filename="meal_plan.json"):
        """
        Generate the meal plan and save it to a JSON file.
        """
        meal_plan = self.generate_meal_plan()
        with open(filename, "w") as f:
            json.dump(meal_plan, f, indent=4)
        return meal_plan
