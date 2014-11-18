__author__ = 'ohell_000'


import globals as _
import room


class Area():
    def __init__(self, name):
        self.name = name
        self.rooms = []


def initialize_area():
    import copy
    import os

    areaFiles = []
    for file in os.listdir("./data/areas"):
        if file.endswith(".are"):
            areaFiles.append(file)
    for fn in areaFiles:
        f = open("./data/areas/" + fn)
        temp_area = Area(fn[:1].capitalize() + fn[1:len(fn) - 4])
        _.areas.append(temp_area)
        lines = f.readlines()
        temp_room = None
        for l in lines:
            if l == "--- START ROOM ---\n":
                temp_room = room.Room("", temp_area, "", "")
                temp_mobiles = []
                continue
            elif l == "---  END ROOM  ---\n":
                for m in temp_mobiles:
                    m.stats["room"] = temp_room.vnum
                    _.mobiles.append(m)
                _.rooms.append(temp_room)
                temp_area.rooms.append(temp_room)
                temp_room = None
                continue
            try:
                temp_key = l.split(":^:")[0].strip()
                temp_value = l.split(":^:")[1].strip()
                if temp_key == "vnum":
                    temp_room.vnum = temp_value
                elif temp_key == "exit":
                    try:
                        temp_exit_data = l.split(":^:")[2].strip().split(',')
                        temp_vnum = temp_exit_data[0]
                        temp_room.exits[int(temp_value)] = temp_vnum
                    except IndexError:
                        print("Illegal exit found.")
                elif temp_key == "mobiles":
                    for m in temp_value.split():
                        available_mobs = [x for x in _.master_mobile_list if x.vnum == m]
                        if len(available_mobs) < 1:
                            print("Room reset contains unknown vnum \"%s\"." % m)
                        elif len(available_mobs) > 1:
                            print("Room reset contains duplicated vnum \"%s\"." % m)
                        else:
                            temp_mobiles.append(copy.deepcopy(available_mobs[0]))
                else:
                    if temp_key == "desc":
                        temp_value += "\n\r"
                    temp_room.stats[temp_key] = temp_value
            except IndexError:
                if ":^:" not in l: # This is a multi-line which for now can only be a description
                    temp_room.stats["desc"] += l.strip() + "\n\r"
                else:
                    temp_value = ""
                    temp_room.stats[temp_key] = temp_value