import json
import sqlite3
from models import Entry, Mood, mood

ENTRIES = [
    {
        "concept": "Javascript",
        "entry": "I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.",
        "moodId": 1,
        "date": "Wed Sep 15 2021 10:10:47 ",
        "id": 1
    },
    {
        "concept": "Python",
        "entry": "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake",
        "moodId": 4,
        "date": "Wed Sep 15 2021 10:11:33 ",
        "id": 2
    },
    {
        "concept": "Python",
        "entry": "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks",
        "moodId": 3,
        "date": "Wed Sep 15 2021 10:13:11 ",
        "id": 3
    },
    {
        "concept": "Javascript",
        "entry": "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.",
        "moodId": 3,
        "date": "Wed Sep 15 2021 10:14:05 ",
        "id": 4
    }
]

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        """)

        # Initialize an empty list to hold all animal representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])

            # Create a mood instance from the current row
            mood = Mood(row['mood_id'], row['mood_label'])
            
            # Add the dictionary representation of the mood to the entry
            entry.mood = mood.__dict__

            # Add the dictionary representation of the entry to the list
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

# Function with a single parameter
def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'],
                            data['mood_id'], data['date'])
        
        # Create a mood instance from the current row
        mood = Mood(data['mood_id'], data['mood_label'])
            
        # Add the dictionary representation of the mood to the entry
        entry.mood = mood.__dict__

        return json.dumps(entry.__dict__)

def create_entry(entry):
    # Get the id value of the last entry in the list
    max_id = ENTRIES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the entry dictionary
    entry["id"] = new_id

    # Add the entry dictionary to the list
    ENTRIES.append(entry)

    # Return the dictionary with `id` property added
    return entry

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entries
        WHERE id = ?
        """, (id, ))
        
def update_entry(id, new_entry):
    # Iterate the ENTRIES list, but use enumerate() so that
    # you can access the index value of each item.
    for index, entry in enumerate(ENTRIES):
        if entry["id"] == id:
            # Found the entry. Update the value.
            ENTRIES[index] = new_entry
            break
        
def search_entry( search_term ):
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        WHERE e.entry LIKE ? OR e.concept LIKE ?
        """,
        ("%"+search_term+"%", "%"+search_term+"%", ))
        
        # Load the single result into memory
        dataset = db_cursor.fetchall()
        
        entries = []
        
        for row in dataset:

            # Create an animal instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])

            # Create a mood instance from the current row
            mood = Mood(row['mood_id'], row['mood_label'])
            
            # Add the dictionary representation of the mood to the entry
            entry.mood = mood.__dict__

            # Add the dictionary representation of the entry to the list
            entries.append(entry.__dict__)

        return json.dumps(entries)