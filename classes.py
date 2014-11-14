__author__ = 'ohell_000'


import globals as _


class Class ():
    def __init__(self):
        self.stats = {
            "name": "",
            "class_stat": ""
        }

    def get_name(self):
        return self.stats["name"]

    def get_class_stat(self):
        return self.stats["class_stat"]

def initialize_classes():
    f = open("data/classes.dat", "r")
    lines = f.readlines()
    for l in lines:
        if l == "--- START CLASS ---\n":
            temp_class = Class()
            continue
        elif l == "--- END CLASS ---\n":
            _.classes.append(temp_class)
            temp_class = None
            continue
        try:
            temp_key = l.split(":^:")[0].strip()
            temp_value = l.split(":^:")[1].strip()
            if "(*int)" in temp_value:
                temp_value = int(temp_value[6:])
            if temp_key == "skills" or temp_key == "spells":
                temp_value = temp_value.split()
            temp_class.stats[temp_key] = temp_value
        except IndexError:
            print("Illegal class. Skipping.")
    f.close()