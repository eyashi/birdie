# The database for the bird prediction engine. Start with a simple CSV situation?
# Upgrade to SQL later.

import os
import csv

DATABASE_FILE = "db.csv"


class Database:
    def __init__(self):
        if not os.path.isfile(DATABASE_FILE):
            self.initialize_db_csv()

    def initialize_db_csv(self):
        headers = ["filename", "bird_present", "bird_identity", "bird_mood"]
        with open(DATABASE_FILE, "w") as db:
            writer = csv.writer(db)
            writer.writerow(headers)

    def update(self, data):
        # Adds new prediction to the CSV

        # TODO: Validate the structure of the data coming in.
        with open(DATABASE_FILE, "a") as db:
            writer = csv.writer(db)
            writer.writerow(data)

    def return_counts(self):
        # TODO: Return the counts of clips with and without bird sounds
        pass

    def return_bird_clip_files(self):
        # TODO: Returns a list of file names that are positive for bird sounds.
        pass

    def return_no_bird_sounds(self):
        # TODO Returns a list of file names that are negative for bird sounds.
        pass
