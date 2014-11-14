__author__ = 'ohell_000'


import globals as _


class Race():
    def __init__(self):
        self.stats = {
            "base_str": 10,
            "base_dex": 10,
            "base_int": 10,
            "base_con": 10,
            "base_wis": 10,
            "max_str": 20,
            "max_dex": 20,
            "max_int": 20,
            "max_con": 20,
            "max_wis": 20,
            "name": ""
        }

    def get_name(self):
        return self.stats["name"]


def initialize_races():
    f = open("data/races.dat", "r")
    lines = f.readlines()
    for l in lines:
        if l == "--- START RACE ---\n":
            temp_race = Race()
            continue
        elif l == "--- END RACE ---\n":
            _.races.append(temp_race)
            temp_race = None
            continue
        try:
            temp_key = l.split(":^:")[0].strip()
            temp_value = l.split(":^:")[1].strip()
            if "(*int)" in temp_value:
                temp_value = int(temp_value[6:])
            temp_race.stats[temp_key] = temp_value
        except IndexError:
            print("Illegal race. Skipping.")
    f.close()