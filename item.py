__author__ = 'ohell_000'


import globals as _


def get_item_by_vnum(vnum):
    temp_item = None
    for i in _.items:
        if i.vnum == vnum:
            temp_item = i
            break
    return temp_item

def get_item_in_room(room, target):
    for e in room.items:
        for i in e.keywords:
            if len(i) >= len(target) and i[:len(target)] == target:
                return e
    else:
        return None

def get_item_in_inventory(char, target):
    for e in char.player.inventory:
        for i in e.keywords:
            if len(i) >= len(target) and i[:len(target)] == target:
                return e
    else:
        return None

def get_item_slot_in_equipment(char, target):
    for e in char.player.equipment:
        if char.player.equipment[e] is not None:
            for i in char.player.equipment[e].keywords:
                if len(i) >= len(target) and i[:len(target)] == target:
                    return e
    else:
        return None

class Item():
    def __init__(self, vnum, keywords, name, desc, wear_loc):
        self.carried = False
        self.vnum = vnum
        self.keywords = keywords
        self.wear_loc = wear_loc
        self.stats = {
            "name": name,
            "desc": desc,
            "weapon_type": None
        }

    def get_damage(self):
        return 0, "null"

    def get_desc(self):
        return self.stats["desc"]

    def get_name(self, looker=None):
        if looker is not None:
            if looker.can_see(self):
                return self.stats["name"]
            else:
                return "something"
        else:
            return self.stats["name"]

    def __repr__(self):
        return("%s: %s\n\r%s\n\r%s" % (self.vnum, self.get_name(), self.keywords, \
                                                         self.get_desc()))

    def check_keywords(self, string):
        if string in self.keywords:
            return True
        else:
            return False

    def wear_loc_string(self):
        if self.wear_loc == _.WEAR_WRIST:
            return "wrist"
        elif self.wear_loc == _.WEAR_ARMS:
            return "arms"
        elif self.wear_loc == _.WEAR_BODY:
            return "body"
        elif self.wear_loc == _.WEAR_FEET:
            return "feet"
        elif self.wear_loc == _.WEAR_FINGER:
            return "finger"
        elif self.wear_loc == _.WEAR_FLOAT:
            return "float"
        elif self.wear_loc == _.WEAR_HAND:
            return "hand"
        elif self.wear_loc == _.WEAR_HEAD:
            return "head"
        elif self.wear_loc == _.WEAR_HELD:
            return "held"
        elif self.wear_loc == _.WEAR_LEGS:
            return "legs"
        elif self.wear_loc == _.WEAR_LIGHT:
            return "light"
        elif self.wear_loc == _.WEAR_NECK:
            return "neck"
        elif self.wear_loc == _.WEAR_SHIELD:
            return "shield"
        elif self.wear_loc == _.WEAR_TORSO:
            return "torso"
        elif self.wear_loc == _.WEAR_WAIST:
            return "waist"
        elif self.wear_loc == _.WEAR_WRIST:
            return "wrist"
        else:
            return "unknown"

    def weapon_type_string(self):
        if self.weapon_type == _.WEAPON_AXE:
            return "axe"
        elif self.weapon_type == _.WEAPON_DAGGER:
            return "dagger"
        elif self.weapon_type == _.WEAPON_MACE:
            return "mace"
        elif self.weapon_type == _.WEAPON_SPEAR:
            return "spear"
        if self.weapon_type == _.WEAPON_SWORD:
            return "sword"

class Weapon(Item):
    def __init__(self, vnum, keywords, name, desc, weapon_type):
        Item.__init__(self, vnum, keywords, name, desc, _.WEAR_WEAPON)
        self.stats["weapon_type"] = weapon_type

    def __repr__(self):
        return Item.__repr__(self) + "\n\rType: %s" % self.weapon_type_string

    def get_damage(self):
        import random
        damage = 0
        for i in range(self.stats["dice_num"]):
            damage += random.randint(1, self.stats["dice_sides"])
        return damage, self.stats["noun"]

class Armor(Item):
    def __init__(self, vnum, keywords, name, desc, wear_loc):
        Item.__init__(self, vnum, keywords, name, desc, wear_loc)

    def __repr__(self):
        return Item.__repr__(self) + "\n\rLocation: %s" % self.wear_loc_string()

def initialize_items():
    f = open("data/items.dat","r")
    lines = f.readlines()
    for l in lines:
        if l == "--- START WEAPON ---\n":
            temp_item = Weapon("","","","","")
            continue
        if l == "--- START ARMOR ---\n":
            temp_item = Armor("","","","","")
            continue
        elif l == "--- END ITEM ---\n":
            _.items.append(temp_item)
            temp_item = None
            continue
        try:
            temp_key = l.split(":^:")[0].strip()
            temp_value = l.split(":^:")[1].strip()
            if "(*int)" in temp_value:
                temp_value = int(temp_value[6:])
            if temp_key == "vnum":
                temp_item.vnum = temp_value
            elif temp_key == "wear_loc":
                temp_item.wear_loc = temp_value
            elif temp_key == "keywords":
                temp_item.keywords = temp_value.split()
            else:
                temp_item.stats[temp_key] = temp_value
        except IndexError:
            print("Illegal item. Skipping.")