import tkinter as tk
from tkinter import messagebox
from services import FitnessTracker

class FitnessTrackerApp:
    def __init__(self, root):
        self.tracker = FitnessTracker()
        self.root = root
        self.root.title("Fitness Tracker")

        self.create_widgets()

    def create_widgets(self):
        # Date Entry
        tk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, pady=5)

        # Exercise Entry
        tk.Label(self.root, text="Exercise:").grid(row=1, column=0, pady=5)
        self.exercise_entry = tk.Entry(self.root)
        self.exercise_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.root, text="Duration (minutes):").grid(row=2, column=0, pady=5)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, pady=5)

        # Add Exercise Button
        tk.Button(self.root, text="Add Exercise", command=self.add_exercise).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Calorie Entry
        tk.Label(self.root, text="Calories:").grid(row=4, column=0, pady=5)
        self.calories_entry = tk.Entry(self.root)
        self.calories_entry.grid(row=4, column=1, pady=5)

        # Add Calorie Button
        tk.Button(self.root, text="Add Calories", command=self.add_calories).grid(
            row=5, column=0, columnspan=2, pady=10
        )

        # Weekly Summary Button
        tk.Button(self.root, text="View Weekly Summary", command=self.show_summary).grid(
            row=6, column=0, columnspan=2, pady=10
        )

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_exercise(self):
        date = self.date_entry.get()
        if not self.validate_date(date):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        exercise = self.exercise_entry.get()
        try:
            duration = int(self.duration_entry.get())
            self.tracker.add_exercise(date, exercise, duration)
            messagebox.showinfo("Success", "Exercise added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid duration.")

    def add_calories(self):
        date = self.date_entry.get()
        if not self.validate_date(date):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        try:
            calories = int(self.calories_entry.get())
            self.tracker.add_calories(date, calories)
            messagebox.showinfo("Success", "Calories added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid calorie amount.")

    def show_summary(self):
        summary = self.tracker.weekly_summary()
        messagebox.showinfo("Weekly Summary", summary)