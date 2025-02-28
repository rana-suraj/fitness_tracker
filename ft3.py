import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox


class FitnessTracker:
    def __init__(self):
        self.db_file = "fitness_tracker.db"
        self.initialize_database()

    def initialize_database(self):
        # Connect to the database (or create it if it doesn't exist)
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            # Create tables if they don't exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    exercise TEXT NOT NULL,
                    duration INTEGER NOT NULL
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS calories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    calories INTEGER NOT NULL
                )
            """
            )
            conn.commit()

    def add_exercise(self, date, exercise, duration):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO exercises (date, exercise, duration) VALUES (?, ?, ?)",
                (date, exercise, duration),
            )
            conn.commit()

    def add_calories(self, date, calories):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO calories (date, calories) VALUES (?, ?)", (date, calories)
            )
            conn.commit()

    def weekly_summary(self):
        today = datetime.now().strftime("%Y-%m-%d")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        summary = "Weekly Summary:\n"
        total_calories = 0
        total_exercises = []

        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()

            # Get exercises from the past week
            cursor.execute(
                "SELECT date, exercise, duration FROM exercises WHERE date BETWEEN ? AND ?",
                (week_ago, today),
            )
            exercises = cursor.fetchall()
            for exercise in exercises:
                total_exercises.append(
                    {"date": exercise[0], "exercise": exercise[1], "duration": exercise[2]}
                )

            # Get total calories from the past week
            cursor.execute(
                "SELECT SUM(calories) FROM calories WHERE date BETWEEN ? AND ?",
                (week_ago, today),
            )
            total_calories = cursor.fetchone()[0] or 0

        # Build the summary
        summary += f"Total Calories: {total_calories}\nExercises:\n"
        for exercise in total_exercises:
            summary += f"- {exercise['date']}: {exercise['exercise']} ({exercise['duration']} minutes)\n"

        return summary


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


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()