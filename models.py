class Exercise:
    def __init__(self, date, exercise, duration):
        self.date = date
        self.exercise = exercise
        self.duration = duration

    def save(self, db):
        """Save the exercise entry to the database."""
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO exercises (date, exercise, duration) VALUES (?, ?, ?)",
                (self.date, self.exercise, self.duration),
            )
            conn.commit()


class Calorie:
    def __init__(self, date, calories):
        self.date = date
        self.calories = calories

    def save(self, db):
        """Save the calorie entry to the database."""
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO calories (date, calories) VALUES (?, ?)",
                (self.date, self.calories),
            )
            conn.commit()