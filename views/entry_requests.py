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
    return ENTRIES

# Function with a single parameter
def get_single_entry(id):
    # Variable to hold the found entry, if it exists
    requested_entry = None

    # Iterate the ENTRIES list above. Very similar to the
    # for..of loops you used in JavaScript.
    for entry in ENTRIES:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if entry["id"] == id:
            requested_entry = entry

    return requested_entry

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
    # Initial -1 value for entry index, in case one isn't found
    entry_index = -1

    # Iterate the ENTRIES list, but use enumerate() so that you
    # can access the index value of each item
    for index, entry in enumerate(ENTRIES):
        if entry["id"] == id:
            # Found the entry. Store the current index.
            entry_index = index

    # If the entry was found, use pop(int) to remove it from list
    if entry_index >= 0:
        ENTRIES.pop(entry_index)
        
def update_entry(id, new_entry):
    # Iterate the ENTRIES list, but use enumerate() so that
    # you can access the index value of each item.
    for index, entry in enumerate(ENTRIES):
        if entry["id"] == id:
            # Found the entry. Update the value.
            ENTRIES[index] = new_entry
            break