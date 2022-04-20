import json
import sqlite3
import datetime
from models import Entry, Mood, EntryTag
from models.tag import Tag

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
        # sqlite3 allows python and sql to be translated and interact
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # cursor is "give me sql and i will speak to the database"
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

        # Convert rows of data into a Python list (list of dictionaries)
        # fetchall is get all data and uses the factory defined at top (sqliterow) and return dictionaries (python)
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        # using python code to loop through sql data
        for row in dataset:

            # Create an entry instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])

            # Create a mood instance from the current row
            mood = Mood(row['mood_id'], row['mood_label'])
            
            # Add the dictionary representation of the mood to the entry
            # the value of mood is an object and now we are turning it into a dictionary (built in value) (dunderscore)
            entry.mood = mood.__dict__
            
            # Now when you get all entries you need to check for tags and add them to the entry
            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT
                t.id,
                t.name
            FROM Entries e
            JOIN EntryTags et
                ON e.id = et.entry_id
            JOIN Tags t
                ON t.id = et.tag_id
            WHERE e.id = ?
                """, (entry.id, ))
            
            #fetch all of the tags (in a python list)
            tagList = db_cursor.fetchall()
            
            for row in tagList:
                tag = Tag(row['id'], row['name'])
                
                entry.tags.append(tag.__dict__)
                
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    # takes the entire thing and turns it into a string
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

def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entries 
            (concept, entry, mood_id, date) 
        VALUES 
            (?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'], new_entry['moodId'], datetime.date.today()))
        
        id = db_cursor.lastrowid
        
        new_entry['id'] = id
        
        # Modify the create_entry method to loop through a list of tags after adding the entry 
        # to the database. Inside the loop, you'll execute another sql command to add a row 
        # to the entrytag table.
        
        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO EntryTags 
                (entry_id, tag_id) 
            VALUES 
                (?, ?);
            """, (id, tag))
        
    return json.dumps(new_entry)
    
def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entries
        WHERE id = ?
        """, (id, ))
        
def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        # 150-156 is a query
        db_cursor.execute("""
        UPDATE Entries
            SET
                concept = ?,
                entry = ?,
                mood_id = ?, 
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], 
              new_entry['mood_id'], new_entry['date'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
        
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