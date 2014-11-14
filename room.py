import globals as _


class Room():
    def __init__(self, vnum, area, name, desc):
        self.stats = {
            "area": area,
            "name": name,
            "desc": desc
        }
        self.exits = {
            _.DIR_NORTH: None,
            _.DIR_EAST: None,
            _.DIR_SOUTH: None,
            _.DIR_WEST: None,
            _.DIR_UP: None,
            _.DIR_DOWN: None
        }
        self.vnum = vnum
        self.items = []

    def __repr__(self):
        return ("%-7s: %s" % (self.vnum, self.get_name()))

    def get_exits(self):
        return self.exits

    def get_name(self):
        return self.stats["name"]

    def get_area(self):
        for a in _.areas:
            if a.name == self.stats["area"]:
                return a
        else:
            return None

    def random_exit(self):
        import random
        try:
            temp_exit = random.choice([e for e in self.exits if self.exits[e] is not None])
        except IndexError:
            return None
        return temp_exit

    def get_desc(self):
        return self.stats["desc"]

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        try:
            self.items.remove(item)
            return True
        except ValueError:
            return False