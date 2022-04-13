class Entry():

    # Class initializer. It has custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, concept, entry, mood_id, date):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.mood_id = mood_id
        self.date = date
