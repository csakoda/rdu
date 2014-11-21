__author__ = 'ohell_000'


import globals as _
import room


class Area():
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.resets = []
        self.resetTimer = 0.0

    def reset(self):
        import copy
        print("Area reset: %s." % self.name)
        #first check that there are no players here...
        for i in range(len(self.rooms)):
            for mob in _.mobiles:
                #if mob is player, skip to next
                if mob.has_peer():
                    continue
                else:
                    if mob.get_room() is self.rooms[i]:
                        _.mobiles.remove(mob)
                        del(mob)
        last_mob = None
        for i in range(len(self.resets)):
            r_type = self.resets[i].split(':^:')[0]
            if r_type == "mobile":
                mob_data = self.resets[i].split(':^:')[1].strip('\n').split(' ')
                mob_vnum = mob_data[0]
                mob_room = mob_data[1]
                #print(mob_vnum,mob_room)
                available_mobs = [x for x in _.master_mobile_list if x.vnum == mob_vnum]
                if len(available_mobs) <= 0:
                    print("ERROR: Invalid mob created during reset.", mob_vnum)
                elif len(available_mobs) > 1:
                    print("ERROR: Reset attempted to create duplicate mob.")
                else:
                    new_mob = copy.deepcopy(available_mobs[0])
                    new_mob.stats["room"] = mob_room
                    _.mobiles.append(new_mob)
                    last_mob = new_mob
            elif r_type == "carry" or r_type == "wield":
                obj_vnum = self.resets[i].split(':^:')[1].strip('\n')
                available_objects = [x for x in _.items if x.vnum == obj_vnum]
                if len(available_objects) <= 0:
                    print("ERROR: Invalid object created during reset.", obj_vnum)
                elif len(available_objects) > 1:
                    print("ERROR: Reset attempted to create duplicate mob.")
                else:
                    new_obj = copy.deepcopy(available_objects[0])
                    last_mob.add_inventory(new_obj)

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
        for i in range(0,len(lines)):
            l = lines[i]
            #Read RESET information from the end of the area file.
            if l == "---START RESETS---\n":
                nextFile = False
                for j in range(i + 1, len(lines)):
                    if lines[j] == "--- END RESETS ---\n":
                        nextFile = True
                        break
                    temp_area.resets.append(lines[j])
                if nextFile:
                    break
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