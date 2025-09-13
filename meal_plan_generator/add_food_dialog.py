import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class AddFoodDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add New Food")
        self.geometry("400x350")
        self.configure(bg="#2E2E2E")

        # ----------------------------
        # Food Name
        # ----------------------------
        ttk.Label(self, text="Food Name:", background="#2E2E2E", foreground="white").pack(pady=5)
        self.food_name_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.food_name_var).pack(fill=tk.X, padx=20)

        # ----------------------------
        # Calories
        # ----------------------------
        ttk.Label(self, text="Calories:", background="#2E2E2E", foreground="white").pack(pady=5)
        self.calories_var = tk.DoubleVar()
        ttk.Entry(self, textvariable=self.calories_var).pack(fill=tk.X, padx=20)

        # ----------------------------
        # Protein
        # ----------------------------
        ttk.Label(self, text="Protein (g):", background="#2E2E2E", foreground="white").pack(pady=5)
        self.protein_var = tk.DoubleVar()
        ttk.Entry(self, textvariable=self.protein_var).pack(fill=tk.X, padx=20)

        # ----------------------------
        # Carbs
        # ----------------------------
        ttk.Label(self, text="Carbs (g):", background="#2E2E2E", foreground="white").pack(pady=5)
        self.carbs_var = tk.DoubleVar()
        ttk.Entry(self, textvariable=self.carbs_var).pack(fill=tk.X, padx=20)

        # ----------------------------
        # Fat
        # ----------------------------
        ttk.Label(self, text="Fat (g):", background="#2E2E2E", foreground="white").pack(pady=5)
        self.fat_var = tk.DoubleVar()
        ttk.Entry(self, textvariable=self.fat_var).pack(fill=tk.X, padx=20)

        # ----------------------------
        # Diet Type (dropdown)
        # ----------------------------
        ttk.Label(self, text="Diet Type:", background="#2E2E2E", foreground="white").pack(pady=5)
        self.diet_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.diet_var,
                     values=["balanced", "keto", "mediterranean"]).pack(fill=tk.X, padx=20)

        # ----------------------------
        # Save Button
        # ----------------------------
        ttk.Button(self, text="Save Food", command=self.save_food).pack(pady=20)

    # ----------------------------
    # Save food to JSON
    # ----------------------------
    def save_food(self):
        food = {
            "food": self.food_name_var.get().strip(),
            "calories": self.calories_var.get(),
            "protein": self.protein_var.get(),
            "carbs": self.carbs_var.get(),
            "fat": self.fat_var.get(),
            "diet_type": self.diet_var.get().lower() if self.diet_var.get() else "balanced"
        }

        if not food["food"]:
            messagebox.showerror("Error", "Food name is required")
            return

        # Load existing user foods
        user_foods_file = "user_foods.json"
        if os.path.exists(user_foods_file):
            with open(user_foods_file, "r") as f:
                user_foods = json.load(f)
        else:
            user_foods = []

        # Remove duplicates by food name
        user_foods = [f for f in user_foods if f.get("food").lower() != food["food"].lower()]
        user_foods.append(food)

        # Save updated list
        with open(user_foods_file, "w") as f:
            json.dump(user_foods, f, indent=4)

        messagebox.showinfo("Success", f"{food['food']} saved successfully!")
        self.destroy()
