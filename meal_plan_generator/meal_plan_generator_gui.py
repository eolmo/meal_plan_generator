# meal_plan_generator_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
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
        self.root.geometry("700x550")
        self.root.title("Macro Meal Planner")

        # ----------------------------
        # Style & theme setup
        # ----------------------------
        self.root.configure(bg="#2E2E2E")  # Dark slate gray background
        style = ttk.Style()
        style.configure("TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Helvetica", 10, "bold"))
        style.configure("TEntry", foreground="#000000", font=("Helvetica", 10))
        style.configure("TButton", background="#009688", foreground="#FFFFFF", font=("Helvetica", 10, "bold"))
        style.map("TButton", background=[('active', '#00796B')])
        style.configure("TCombobox", foreground="#000000", font=("Helvetica", 10))

        # ----------------------------
        # User input frame
        # ----------------------------
        self.frame = ttk.Frame(root, padding=15)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # ----------------------------
        # Age
        # ----------------------------
        ttk.Label(self.frame, text="Age:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.age_var = tk.IntVar()
        ttk.Entry(self.frame, textvariable=self.age_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # ----------------------------
        # Weight & toggle
        # ----------------------------
        ttk.Label(self.frame, text="Weight:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.weight_var = tk.DoubleVar()
        ttk.Entry(self.frame, textvariable=self.weight_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Weight toggle button
        self.weight_unit = "kg"  # Default
        ttk.Label(self.frame, text="Unit:").grid(row=1, column=2, sticky=tk.W)
        self.weight_toggle_btn = tk.Button(self.frame, text="kg", width=5, bg="#009688", fg="white",
                                           command=self.toggle_weight_unit)
        self.weight_toggle_btn.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)

        # ----------------------------
        # Height & toggle
        # ----------------------------
        ttk.Label(self.frame, text="Height:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.height_var = tk.DoubleVar()
        ttk.Entry(self.frame, textvariable=self.height_var).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Height toggle button
        self.height_unit = "cm"  # Default
        ttk.Label(self.frame, text="Unit:").grid(row=2, column=2, sticky=tk.W)
        self.height_toggle_btn = tk.Button(self.frame, text="cm", width=5, bg="#009688", fg="white",
                                           command=self.toggle_height_unit)
        self.height_toggle_btn.grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)

        # ----------------------------
        # Activity Level
        # ----------------------------
        ttk.Label(self.frame, text="Activity Level:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.activity_var = tk.StringVar()
        ttk.Combobox(self.frame, textvariable=self.activity_var, values=["sedentary", "light", "moderate", "active"]).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # ----------------------------
        # Calorie Target
        # ----------------------------
        ttk.Label(self.frame, text="Calorie Target:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.calorie_var = tk.IntVar()
        ttk.Entry(self.frame, textvariable=self.calorie_var).grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        # ----------------------------
        # Diet Type
        # ----------------------------
        ttk.Label(self.frame, text="Diet Type:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.diet_var = tk.StringVar()
        ttk.Combobox(self.frame, textvariable=self.diet_var, values=["balanced", "keto", "mediterranean"]).grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

        # ----------------------------
        # Generate Button (brighter color)
        # ----------------------------
        self.generate_btn = tk.Button(
            self.frame,
            text="Generate Meal Plan",
            command=self.generate_plan,
            bg="#FFC107",   # Bright amber for visibility
            fg="black",
            font=("Helvetica", 10, "bold"),
            width=20
        )
        self.generate_btn.grid(row=6, column=0, columnspan=4, pady=15)

        # ----------------------------
        # Output text area
        # ----------------------------
        self.output = tk.Text(self.frame, wrap=tk.WORD, height=15, bg="#424242", fg="#FFFFFF", font=("Courier", 10), relief=tk.SUNKEN, bd=2)
        self.output.grid(row=7, column=0, columnspan=4, sticky=tk.NSEW, padx=5, pady=5)

        # Make rows and columns resize nicely
        self.frame.rowconfigure(7, weight=1)
        self.frame.columnconfigure(1, weight=1)

    # ----------------------------
    # Toggle helpers
    # ----------------------------
    def toggle_weight_unit(self):
        if self.weight_unit == "kg":
            self.weight_unit = "lb"
            self.weight_toggle_btn.configure(text="lb", bg="#FF9800")
        else:
            self.weight_unit = "kg"
            self.weight_toggle_btn.configure(text="kg", bg="#009688")

    def toggle_height_unit(self):
        if self.height_unit == "cm":
            self.height_unit = "inches"
            self.height_toggle_btn.configure(text="in", bg="#FF9800")
        else:
            self.height_unit = "cm"
            self.height_toggle_btn.configure(text="cm", bg="#009688")

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
            weight = self.convert_weight_to_kg(self.weight_var.get(), self.weight_unit)
            height = self.convert_height_to_cm(self.height_var.get(), self.height_unit)
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

            # Save plan to JSON
            with open("meal_plan.json", "w") as f:
                json.dump(meal_plan, f, indent=4)

            messagebox.showinfo("Success", "Meal plan generated and saved to 'meal_plan.json'.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate meal plan:\n{e}")
