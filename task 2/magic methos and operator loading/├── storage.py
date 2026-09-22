import json
import os


class Storage:

    @staticmethod
    def load_data(filename):

        if not os.path.exists(filename):
            return []

        with open(filename, "r") as file:
            return json.load(file)

    @staticmethod
    def save_data(filename, data):

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)