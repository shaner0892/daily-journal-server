import json
import sqlite3

from models.tag import Tag


def get_all_tags():
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
            t.id,
            t.name
        FROM Tags t
        """)

        # Initialize an empty list to hold all animal representations
        tags = []

        # Convert rows of data into a Python list (list of dictionaries)
        # fetchall is get all data and uses the factory defined at top (sqliterow) and return dictionaries (python)
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        # using python code to loop through sql data
        for row in dataset:

            # Create an entry instance from the current row
            tag = Tag(row['id'], row['name'])
            
            tags.append(tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    # takes the entire thing and turns it into a string
    return json.dumps(tags)