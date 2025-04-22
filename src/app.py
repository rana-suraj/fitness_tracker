import tkinter as tk
from tkinter import ttk, messagebox
from services import FitnessTracker
from datetime import datetime

class FitnessTrackerApp:
    def __init__(self, root):
        self.tracker = FitnessTracker()
        self.root = root
        self.root.title("Fitness Tracker")
        self.root.geometry("500x650")
        
        # Predefined exercises
        self.exercises = ["Running", "Cycling", "Swimming", "Weightlifting", "Yoga", "Walking"]
        
        # Configure styles
        self.configure_styles()
        
        # Show initial screen
        self.show_login_screen()

    def configure_styles(self):
        """Configure custom widget styles"""
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('Accent.TButton', foreground='white', background='#4285F4')
        
        self.root.option_add('*TCombobox*Listbox.font', ('Arial', 10))
        self.root.option_add('*TCombobox*Listbox.selectBackground', '#4285F4')

    def clear_screen(self):
        """Remove all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # Screens
    def show_login_screen(self):
        """Display the login screen"""
        self.clear_screen()
        
        # Widgets
        ttk.Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Login", command=self.login_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Register", command=self.show_registration_screen).pack(side=tk.LEFT, padx=5)
        
        # Center widgets
        self.root.grid_columnconfigure(1, weight=1)

    def show_main_screen(self):
        """Display the main tracking interface"""
        self.clear_screen()
        
        # Date
        ttk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        # Exercise
        ttk.Label(self.root, text="Exercise:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.exercise_var = tk.StringVar()
        self.exercise_dropdown = ttk.Combobox(
            self.root, 
            textvariable=self.exercise_var,
            values=self.exercises,
            state="readonly"
        )
        self.exercise_dropdown.current(0)
        self.exercise_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        # Duration
        ttk.Label(self.root, text="Duration (mins):").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.duration_entry = ttk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        # Calories
        ttk.Label(self.root, text="Calories:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.calories_entry = ttk.Entry(self.root)
        self.calories_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        
        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Add Exercise", command=self.add_exercise).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Calories", command=self.add_calories).pack(side=tk.LEFT, padx=5)
        
        # Visualization Button
        ttk.Button(
            self.root, 
            text="📊 View Weekly Report", 
            style='Accent.TButton',
            command=self.show_visualization
        ).grid(row=5, column=0, columnspan=2, pady=15, padx=10, sticky='ew')
        
        # Logout
        ttk.Button(
            self.root, 
            text="Logout", 
            command=self.show_login_screen
        ).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)

    def show_visualization(self):
        """Display the visualization window"""
        try:
            vis_window = tk.Toplevel(self.root)
            vis_window.title("Weekly Fitness Report")
            vis_window.geometry("900x700")
            
            # Generate and pack charts
            canvas = self.tracker.generate_visualization(vis_window)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Close button
            ttk.Button(
                vis_window,
                text="Close",
                command=vis_window.destroy
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")

    # Core Functions
    def validate_date(self, date_str):
        """Check if date has YYYY-MM-DD format"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def register_user(self):
        """Handle user registration"""
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password required")
            return
            
        try:
            self.tracker.register_user(username, password)
            messagebox.showinfo("Success", "Registration successful!")
            self.show_login_screen()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def login_user(self):
        """Handle user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password required")
            return
            
        if self.tracker.login_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.show_main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def add_exercise(self):
        """Add exercise record"""
        date = self.date_entry.get()
        exercise = self.exercise_var.get()
        duration = self.duration_entry.get()
        
        if not self.validate_date(date):
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
            
        try:
            self.tracker.add_exercise(date, exercise, int(duration))
            messagebox.showinfo("Success", "Exercise logged!")
            self.duration_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_calories(self):
        """Add calorie record"""
        date = self.date_entry.get()
        calories = self.calories_entry.get()
        
        if not self.validate_date(date):
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
            
        try:
            self.tracker.add_calories(date, int(calories))
            messagebox.showinfo("Success", "Calories logged!")
            self.calories_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Calories must be a number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_registration_screen(self):
        """Show registration form"""
        self.clear_screen()
        
        ttk.Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.reg_username_entry = ttk.Entry(self.root)
        self.reg_username_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.reg_password_entry = ttk.Entry(self.root, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Register", command=self.register_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back to Login", command=self.show_login_screen).pack(side=tk.LEFT, padx=5)
        
        self.root.grid_columnconfigure(1, weight=1)