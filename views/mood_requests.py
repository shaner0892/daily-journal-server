# MOODS = [
#     {
#         "id": 1,
#         "label": "Happy"
#     },
#     {
#         "id": 2,
#         "label": "Sad"
#     },
#     {
#         "id": 3,
#         "label": "Angry"
#     },
#     {
#         "id": 4,
#         "label": "Ok"
#     }
# ]

# def get_all_moods():
#     return MOODS

import json
import sqlite3

from models.mood import Mood


def get_all_moods():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        # sqlite3 allows python and sql to be translated and interact
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # cursor is "give me sql and i will speak to the database"
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        """)

        # Initialize an empty list to hold all animal representations
        moods = []

        # Convert rows of data into a Python list (list of dictionaries)
        # fetchall is get all data and uses the factory defined at top (sqliterow) and return dictionaries (python)
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        # using python code to loop through sql data
        for row in dataset:

            # Create an entry instance from the current row
            mood = Mood(row['id'], row['label'])
            
            moods.append(mood.__dict__)

    # Use `json` package to properly serialize list as JSON
    # takes the entire thing and turns it into a string
    return json.dumps(moods)