class Exercise:
    def __init__(self, user_id, date, exercise, duration):
        self.user_id = user_id
        self.date = date
        self.exercise = exercise
        self.duration = duration

    def save(self, db):
        """Save the exercise entry to the database."""
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO exercises (user_id, date, exercise, duration) VALUES (?, ?, ?, ?)",
                (self.user_id, self.date, self.exercise, self.duration),
            )
            conn.commit()


class Calorie:
    def __init__(self, user_id, date, calories):
        self.user_id = user_id
        self.date = date
        self.calories = calories

    def save(self, db):
        """Save the calorie entry to the database."""
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO calories (user_id, date, calories) VALUES (?, ?, ?)",
                (self.user_id, self.date, self.calories),
            )
            conn.commit()