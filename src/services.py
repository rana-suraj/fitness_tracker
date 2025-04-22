import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import Database
from models import Exercise, Calorie

class FitnessTracker:
    def __init__(self):
        self.db = Database()
        self.current_user_id = None

    # User Management
    def register_user(self, username, password):
        """Register a new user with plain-text password (for compatibility)"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            conn.commit()

    def login_user(self, username, password):
        """Authenticate user with plain-text password check"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and user[1] == password:
                self.current_user_id = user[0]
                return True
            return False

    # Fitness Data
    def add_exercise(self, date, exercise, duration):
        """Add exercise record for current user"""
        if not self.current_user_id:
            raise Exception("User not logged in")
        Exercise(self.current_user_id, date, exercise, duration).save(self.db)

    def add_calories(self, date, calories):
        """Add calorie record for current user"""
        if not self.current_user_id:
            raise Exception("User not logged in")
        Calorie(self.current_user_id, date, calories).save(self.db)

    # Visualization
    def get_weekly_summary(self):
        """Aggregate weekly data for visualization"""
        if not self.current_user_id:
            raise Exception("User not logged in")

        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")

        with self.db.get_connection() as conn:
            # Get exercise totals per day
            exercises = conn.execute("""
                SELECT date, SUM(duration) as minutes 
                FROM exercises 
                WHERE user_id=? AND date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date
            """, (self.current_user_id, week_ago, today)).fetchall()

            # Get calorie totals per day
            calories = conn.execute("""
                SELECT date, SUM(calories) as calories
                FROM calories
                WHERE user_id=? AND date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date
            """, (self.current_user_id, week_ago, today)).fetchall()

        return {
            'exercise_dates': [e[0] for e in exercises],
            'exercise_mins': [e[1] for e in exercises],
            'calorie_dates': [c[0] for c in calories],
            'calorie_totals': [c[1] for c in calories]
        }

    def generate_visualization(self, master_window):
        """Create matplotlib charts embedded in Tkinter"""
        data = self.get_weekly_summary()
        
        fig = plt.Figure(figsize=(10, 8), dpi=100)
        fig.suptitle("Weekly Fitness Summary", fontweight='bold')
        
        # Exercise Chart (Bar)
        ax1 = fig.add_subplot(211)
        bars = ax1.bar(data['exercise_dates'], data['exercise_mins'], color='#4285F4')
        ax1.set_title('Exercise Minutes', pad=10)
        ax1.set_ylabel('Minutes')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        # Calorie Chart (Line)
        ax2 = fig.add_subplot(212)
        line = ax2.plot(data['calorie_dates'], data['calorie_totals'], 
                       marker='o', color='#EA4335', linewidth=2.5)
        ax2.set_title('Calorie Intake', pad=10)
        ax2.set_ylabel('Calories')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on points
        for x, y in zip(data['calorie_dates'], data['calorie_totals']):
            ax2.text(x, y, f'{int(y)}', 
                    ha='center', va='bottom', 
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)
        
        canvas = FigureCanvasTkAgg(fig, master=master_window)
        canvas.draw()
        return canvas