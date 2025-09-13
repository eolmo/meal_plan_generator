import random
import json
from meal_plan_generator.foods import FOODS
from meal_plan_generator.macros import get_macro_ratios

class MealPlanGenerator:
    def __init__(self, age, weight, height, activity_level, calorie_target, diet_type, foods_data=None):
        """
        Initialize the generator with user inputs.
        foods_data: list or dict of foods (default FOODS + user-added foods)
        diet_type: "balanced", "keto", "mediterranean"
        """
        self.age = age
        self.weight = weight          # kg
        self.height = height          # cm
        self.activity_level = activity_level
        self.calorie_target = calorie_target
        self.diet_type = diet_type
        self.macro_ratios = get_macro_ratios(diet_type)

        # Use default FOODS if no foods_data is provided
        if foods_data is None:
            self.foods_data = FOODS
        else:
            # Convert list of user foods to dict if necessary
            if isinstance(foods_data, list):
                # Each food item must have 'food' key
                self.foods_data = {f['food']: {k: v for k, v in f.items() if k != 'food'} for f in foods_data}
            else:
                self.foods_data = foods_data

    def filter_foods_by_diet(self):
        """
        Returns a dict of foods filtered by the current diet_type.
        If a food has a 'diet_type' key, it must match; else include it by default.
        """
        filtered = {}
        for food_name, info in self.foods_data.items():
            if 'diet_type' in info:
                # food can have multiple diet types as list
                allowed_diets = info['diet_type']
                if isinstance(allowed_diets, str):
                    allowed_diets = [allowed_diets.lower()]
                if self.diet_type.lower() in allowed_diets:
                    filtered[food_name] = info
            else:
                # include food without diet_type
                filtered[food_name] = info
        return filtered

    def generate_meal_plan(self):
        """
        Generate a simple 7-day meal plan.
        Each meal gets 2 random foods for prototype simplicity.
        """
        plan = {}
        meals = ["Breakfast", "Lunch", "Dinner", "Snack"]

        # Filter foods by diet type
        filtered_foods = self.filter_foods_by_diet()
        food_keys = list(filtered_foods.keys())

        for day in range(1, 8):
            day_plan = {}
            for meal in meals:
                meal_items = []
                if food_keys:
                    choices = random.sample(food_keys, min(2, len(food_keys)))
                    for item in choices:
                        meal_items.append({"food": item, **filtered_foods[item]})
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
