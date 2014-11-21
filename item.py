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

def get_item_in_inventory(peer, target):
    for e in peer.account.player.inventory:
        for i in e.keywords:
            if len(i) >= len(target) and i[:len(target)] == target:
                return e
    else:
        return None

def get_item_slot_in_equipment(peer, target):
    for e in peer.account.player.equipment:
        if peer.account.player.equipment[e] is not None:
            for i in peer.account.player.equipment[e].keywords:
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
        for w in self.wear_loc:
            if int(w) == _.WEAR_WRIST:
                return "wrist"
            elif int(w) == _.WEAR_ARMS:
                return "arms"
            elif int(w) == _.WEAR_BODY:
                return "body"
            elif int(w) == _.WEAR_FEET:
                return "feet"
            elif int(w) == _.WEAR_FINGER:
                return "finger"
            elif int(w) == _.WEAR_FLOAT:
                return "float"
            elif int(w) == _.WEAR_HAND:
                return "hand"
            elif int(w) == _.WEAR_HEAD:
                return "head"
            elif int(w) == _.WEAR_HELD:
                return "held"
            elif int(w) == _.WEAR_LEGS:
                return "legs"
            elif int(w) == _.WEAR_LIGHT:
                return "light"
            elif int(w) == _.WEAR_NECK:
                return "neck"
            elif int(w) == _.WEAR_OFFHAND:
                return "shield"
            elif int(w) == _.WEAR_TORSO:
                return "torso"
            elif int(w) == _.WEAR_WAIST:
                return "waist"
            elif int(w) == _.WEAR_WRIST:
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
        for i in range(int(self.stats["dice"])):
            damage += random.randint(1, int(self.stats["sides"]))
        try:
            return damage, self.stats["noun"], self.stats["flag"]
        except KeyError:
            return damage, self.stats["noun"], "none"

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
        elif l == "--- START ARMOR ---\n":
            temp_item = Armor("","","","","")
            continue
        elif l == "--- END ITEM ---\n":
            _.items.append(temp_item)
            temp_item = None
            continue
        elif l[:3] == "---":
            temp_item = Item("","","","","")
            continue
        try:
            temp_key = l.split(":^:")[0].strip()
            temp_value = l.split(":^:")[1].strip()
            if "(*int)" in temp_value:
                temp_value = int(temp_value[6:])
            if temp_key == "vnum":
                temp_item.vnum = temp_value
            elif temp_key == "wear_loc":
                temp_item.wear_loc = temp_value.split()
            elif temp_key == "keywords":
                temp_item.keywords = temp_value.split()
            else:
                temp_item.stats[temp_key] = temp_value
        except IndexError:
            print("Illegal item. Skipping.", l)