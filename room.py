import globals as _

def get_room(vnum):
    for a in _.areas:
        for r in a.rooms:
            if r.vnum == vnum:
                return r

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
            if a == self.stats["area"]:
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

    def display(self, char):
        
        #  Name and description
        buf = self.get_name() + "\n\r\n\r"\
        + self.get_desc() + "\n\r\n\rExits: [ "
        
        #  Exits
        noexit = True  # -Rework- (should do_peer see exits?)
        for d in [x for x in sorted(self.exits) if self.exits[x] is not None]:
            buf += _.get_dir_string(d) + " "
            noexit = False

        if noexit:
            buf += "none "

        buf += "]\n\r\n\r"

        #  Items

        for r in self.items:
            buf += "%s\n\r" % r.get_desc()
        if len(self.items) > 0:
            buf += "\n\r"

        #  Characters

        other_players = [c.player for c in _.peers if c is not char and c.player.get_room() == self
                                               and not c.linkdead and c.state == _.STATE_ONLINE]
        other_mobs = [m for m in _.mobiles if m.get_peer() is None and m.get_room() == self]
        others = other_mobs + other_players

        for c in others:
            pos_string = ""
            pos_tag = ""
            if c.get_position() == _.POS_FIGHTING:
                pos_tag = ", fighting %s" % c.fighting.get_name() if c.fighting is not None else "null"
            elif c.get_position() == _.POS_RESTING:
                pos_string = "resting "
            elif c.get_position() == _.POS_SLEEPING:
                pos_string = "sleeping "
            buf += "%s%s is %shere%s.\n\r" % ("<LINKDEAD> " if c.get_peer() is not None and c.get_peer().linkdead else "",
                                              c.stats["name"].capitalize(), pos_string, pos_tag)
        if len(others) > 0:
            buf += "\n\r"

        return buf

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