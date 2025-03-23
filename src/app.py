import tkinter as tk
from tkinter import ttk, messagebox
from services import FitnessTracker
from datetime import datetime

class FitnessTrackerApp:
    def __init__(self, root):
        self.tracker = FitnessTracker()
        self.root = root
        self.root.title("Fitness Tracker")

        # List of predefined exercises
        self.exercises = ["Running", "Cycling", "Swimming", "Weightlifting", "Yoga", "Walking"]

        # Show the login screen first
        self.show_login_screen()

    def show_login_screen(self):
        """Display the login screen."""
        self.clear_screen()

        # Username Label and Entry
        tk.Label(self.root, text="Username:").grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, pady=5)

        # Password Label and Entry
        tk.Label(self.root, text="Password:").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        # Login Button
        tk.Button(self.root, text="Login", command=self.login_user).grid(row=2, column=0, columnspan=2, pady=10)

        # Register Button
        tk.Button(self.root, text="Register", command=self.show_registration_screen).grid(row=3, column=0, columnspan=2, pady=10)

    def show_registration_screen(self):
        """Display the registration screen."""
        self.clear_screen()

        # Username Label and Entry
        tk.Label(self.root, text="Username:").grid(row=0, column=0, pady=5)
        self.reg_username_entry = tk.Entry(self.root)
        self.reg_username_entry.grid(row=0, column=1, pady=5)

        # Password Label and Entry
        tk.Label(self.root, text="Password:").grid(row=1, column=0, pady=5)
        self.reg_password_entry = tk.Entry(self.root, show="*")
        self.reg_password_entry.grid(row=1, column=1, pady=5)

        # Register Button
        tk.Button(self.root, text="Register", command=self.register_user).grid(row=2, column=0, columnspan=2, pady=10)

        # Back to Login Button
        tk.Button(self.root, text="Back to Login", command=self.show_login_screen).grid(row=3, column=0, columnspan=2, pady=10)

    def show_main_screen(self):
        """Display the main fitness tracking screen."""
        self.clear_screen()

        # Date Entry
        tk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, pady=5)

        # Exercise Dropdown
        tk.Label(self.root, text="Exercise:").grid(row=1, column=0, pady=5)
        self.exercise_combobox = ttk.Combobox(self.root, values=self.exercises)
        self.exercise_combobox.grid(row=1, column=1, pady=5)
        self.exercise_combobox.set("Select Exercise")  # Default placeholder text

        # Duration Entry
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

        # Logout Button
        tk.Button(self.root, text="Logout", command=self.show_login_screen).grid(
            row=7, column=0, columnspan=2, pady=10
        )

    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def validate_date(self, date_str):
        """Validate the date format."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def register_user(self):
        """Register a new user."""
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return
        try:
            self.tracker.register_user(username, password)
            messagebox.showinfo("Success", "User registered successfully!")
            self.show_login_screen()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def login_user(self):
        """Log in a user."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return
        if self.tracker.login_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.show_main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def add_exercise(self):
        """Add an exercise entry."""
        date = self.date_entry.get()
        if not self.validate_date(date):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        exercise = self.exercise_combobox.get()  # Get the selected exercise from the dropdown
        if exercise == "Select Exercise":
            messagebox.showerror("Error", "Please select an exercise.")
            return
        try:
            duration = int(self.duration_entry.get())
            self.tracker.add_exercise(date, exercise, duration)
            messagebox.showinfo("Success", "Exercise added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid duration.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_calories(self):
        """Add a calorie entry."""
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
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_summary(self):
        """Display the weekly summary."""
        try:
            summary = self.tracker.weekly_summary()
            messagebox.showinfo("Weekly Summary", summary)
        except Exception as e:
            messagebox.showerror("Error", str(e))