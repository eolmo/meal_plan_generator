# meal_plan_generator_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import random
import json

# Absolute imports from your package
from meal_plan_generator.generator import MealPlanGenerator
from meal_plan_generator.foods import FOODS
from meal_plan_generator.macros import get_macro_ratios

# ----------------------------
# GUI Class
# ----------------------------
class MealPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x500")
        self.root.title("Macro Meal Planner")
        
        # ----------------------------
        # User input frame
        # ----------------------------
        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Age
        ttk.Label(self.frame, text="Age:").grid(row=0, column=0, sticky=tk.W)
        self.age_var = tk.IntVar()
        ttk.Entry(self.frame, textvariable=self.age_var).grid(row=0, column=1)

        # Weight
        ttk.Label(self.frame, text="Weight:").grid(row=1, column=0, sticky=tk.W)
        self.weight_var = tk.DoubleVar()
        ttk.Entry(self.frame, textvariable=self.weight_var).grid(row=1, column=1)

        # Weight unit
        self.weight_unit = tk.StringVar(value="kg")
        ttk.OptionMenu(self.frame, self.weight_unit, "kg", "kg", "lb").grid(row=1, column=2)

        # Height
        ttk.Label(self.frame, text="Height:").grid(row=2, column=0, sticky=tk.W)
        self.height_var = tk.DoubleVar()
        ttk.Entry(self.frame, textvariable=self.height_var).grid(row=2, column=1)

        # Height unit
        self.height_unit = tk.StringVar(value="cm")
        ttk.OptionMenu(self.frame, self.height_unit, "cm", "cm", "inches").grid(row=2, column=2)

        # Activity Level
        ttk.Label(self.frame, text="Activity Level:").grid(row=3, column=0, sticky=tk.W)
        self.activity_var = tk.StringVar()
        ttk.Combobox(self.frame, textvariable=self.activity_var, values=["sedentary", "light", "moderate", "active"]).grid(row=3, column=1)

        # Calorie Target
        ttk.Label(self.frame, text="Calorie Target:").grid(row=4, column=0, sticky=tk.W)
        self.calorie_var = tk.IntVar()
        ttk.Entry(self.frame, textvariable=self.calorie_var).grid(row=4, column=1)

        # Diet Type
        ttk.Label(self.frame, text="Diet Type:").grid(row=5, column=0, sticky=tk.W)
        self.diet_var = tk.StringVar()
        ttk.Combobox(self.frame, textvariable=self.diet_var, values=["balanced", "keto", "mediterranean"]).grid(row=5, column=1)

        # Generate Button
        ttk.Button(self.frame, text="Generate Meal Plan", command=self.generate_plan).grid(row=6, column=0, columnspan=3, pady=10)

        # Output text
        self.output = tk.Text(self.frame, wrap=tk.WORD, height=15)
        self.output.grid(row=7, column=0, columnspan=3, sticky=tk.NSEW)

        # Make rows and columns resize nicely
        self.frame.rowconfigure(7, weight=1)
        self.frame.columnconfigure(1, weight=1)

    # ----------------------------
    # Conversion helpers
    # ----------------------------
    def convert_weight_to_kg(self, weight, unit):
        if unit == "lb":
            return weight * 0.453592
        return weight

    def convert_height_to_cm(self, height, unit):
        if unit == "inches":
            return height * 2.54
        return height

    # ----------------------------
    # Generate meal plan
    # ----------------------------
    def generate_plan(self):
        try:
            age = self.age_var.get()
            weight = self.convert_weight_to_kg(self.weight_var.get(), self.weight_unit.get())
            height = self.convert_height_to_cm(self.height_var.get(), self.height_unit.get())
            activity_level = self.activity_var.get().lower()
            calorie_target = self.calorie_var.get()
            diet_type = self.diet_var.get().lower()

            # Use the generator class
            generator = MealPlanGenerator(age, weight, height, activity_level, calorie_target, diet_type)
            meal_plan = generator.generate_meal_plan()

            # Display in output box
            self.output.delete("1.0", tk.END)
            for day, meals in meal_plan.items():
                self.output.insert(tk.END, f"\n=== {day} ===\n")
                for meal_name, items in meals.items():
                    self.output.insert(tk.END, f"\n{meal_name}:\n")
                    total_cals = total_protein = total_carbs = total_fat = 0
                    for item in items:
                        self.output.insert(tk.END, f" - {item['food']} | {item['calories']} kcal, P:{item['protein']}g, C:{item['carbs']}g, F:{item['fat']}g\n")
                        total_cals += item['calories']
                        total_protein += item['protein']
                        total_carbs += item['carbs']
                        total_fat += item['fat']
                    self.output.insert(tk.END, f"Total: {total_cals} kcal, P:{total_protein}g, C:{total_carbs}g, F:{total_fat}g\n")
            
            # Optionally save to JSON
            with open("meal_plan.json", "w") as f:
                json.dump(meal_plan, f, indent=4)

            messagebox.showinfo("Success", "Meal plan generated and saved to 'meal_plan.json'.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate meal plan:\n{e}")
