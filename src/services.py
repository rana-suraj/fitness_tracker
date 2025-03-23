from datetime import datetime, timedelta
from database import Database
from models import Exercise, Calorie

class FitnessTracker:
    def __init__(self):
        self.db = Database()
        self.current_user_id = None  # Track the logged-in user

    def register_user(self, username, password):
        """Register a new user."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            conn.commit()

    def login_user(self, username, password):
        """Log in a user."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and user[1] == password:  # Compare plain-text passwords
                self.current_user_id = user[0]  # Set the current user ID
                return True
            return False

    def add_exercise(self, date, exercise, duration):
        """Add an exercise entry for the current user."""
        if not self.current_user_id:
            raise Exception("User not logged in")
        exercise_entry = Exercise(self.current_user_id, date, exercise, duration)
        exercise_entry.save(self.db)

    def add_calories(self, date, calories):
        """Add a calorie entry for the current user."""
        if not self.current_user_id:
            raise Exception("User not logged in")
        calorie_entry = Calorie(self.current_user_id, date, calories)
        calorie_entry.save(self.db)

    def weekly_summary(self):
        """Generate a summary of the past week's data for the current user."""
        if not self.current_user_id:
            raise Exception("User not logged in")
        today = datetime.now().strftime("%Y-%m-%d")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        summary = "Weekly Summary:\n"
        total_calories = 0
        total_exercises = []

        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            # Get exercises from the past week
            cursor.execute(
                "SELECT date, exercise, duration FROM exercises WHERE user_id = ? AND date BETWEEN ? AND ?",
                (self.current_user_id, week_ago, today),
            )
            exercises = cursor.fetchall()
            for exercise in exercises:
                total_exercises.append(
                    {"date": exercise[0], "exercise": exercise[1], "duration": exercise[2]}
                )

            # Get total calories from the past week
            cursor.execute(
                "SELECT SUM(calories) FROM calories WHERE user_id = ? AND date BETWEEN ? AND ?",
                (self.current_user_id, week_ago, today),
            )
            total_calories = cursor.fetchone()[0] or 0

        # Build the summary
        summary += f"Total Calories: {total_calories}\nExercises:\n"
        for exercise in total_exercises:
            summary += f"- {exercise['date']}: {exercise['exercise']} ({exercise['duration']} minutes)\n"

        return summary