# run_gui.py
import sys
import os
import tkinter as tk

# ----------------------------
# Add project root to sys.path
# This ensures Python can find the 'meal_plan_generator' package
# ----------------------------
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ----------------------------
# Import the GUI class from the package
# ----------------------------
# Your GUI file is 'meal_plan_generator_gui.py' inside the package 'meal_plan_generator'
try:
    from meal_plan_generator.meal_plan_generator_gui import MealPlannerGUI
except ModuleNotFoundError as e:
    print("ERROR: Could not import MealPlannerGUI. Check your folder structure and __init__.py files.")
    print(e)
    sys.exit(1)

# ----------------------------
# Run the GUI application
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()                 # Create the main Tkinter window
    root.title("Macro Meal Planner")  # Optional: add window title
    app = MealPlannerGUI(root)      # Instantiate your GUI class
    root.mainloop()                 # Start the Tkinter event loop
