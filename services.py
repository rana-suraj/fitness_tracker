from datetime import datetime, timedelta
from database import Database
from models import Exercise, Calorie

class FitnessTracker:
    def __init__(self):
        self.db = Database()

    def add_exercise(self, date, exercise, duration):
        """Add an exercise entry."""
        exercise_entry = Exercise(date, exercise, duration)
        exercise_entry.save(self.db)

    def add_calories(self, date, calories):
        """Add a calorie entry."""
        calorie_entry = Calorie(date, calories)
        calorie_entry.save(self.db)

    def weekly_summary(self):
        """Generate a summary of the past week's data."""
        today = datetime.now().strftime("%Y-%m-%d")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        summary = "Weekly Summary:\n"
        total_calories = 0
        total_exercises = []

        with self.db.get_connection() as conn:
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