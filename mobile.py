__author__ = 'ohell_000'


import globals as _
import random
import re

def get_mobile_in_room(target, room):
    #check the number of the mob they are trying to target (if applicable) -> like, 2.bunnicula
    rx = re.compile("[0-9]+")
    n = 0
    if not rx.match(target) is None:
        n = int(rx.match(target).group()) - 1
        target = target.split('.')[1]
    for m in _.mobiles:
        for i in m.get_keywords():
            if len(i) >= len(target) and i[:len(target)] == target and m.get_room() == room:
                if n == 0:
                    return m
                else:
                    n -= 1
    else:
        return None


def get_mobile_in_room_except(target, room, exceptions):
    rx = re.compile("[0-9]+")
    n = 0
    if not rx.match(target) is None:
        n = int(rx.match(target).group()) - 1
        target = target.split('.')[1]
    for m in _.mobiles:
        for i in m.get_keywords():
            if len(i) >= len(target) and i[:len(target)] == target and m.get_room() == room and \
                    m not in exceptions:
                if n == 0:
                    return m
                else:
                    n -= 1
    else:
        return None


def get_mobile(target):
    rx = re.compile("[0-9]+")
    n = 0
    if not rx.match(target) is None:
        n = int(rx.match(target).group()) - 1
        target = target.split('.')[1]
    for m in _.mobiles:
        for i in m.get_keywords():
            if len(i) >= len(target) and i[:len(target)] == target:
                if n == 0:
                    return m
                else:
                    n -= 1
    else:
        return None


class Mobile():
    def __init__(self):
        self.stats = {
            "name": "",
            "desc": "",
            "longdesc": "",
            "class": "",
            "race": "",
            "version": _.VERSION,
            "room": _.START_ROOM,
            "hp": 100,
            "max_hp": 100,
            "mana": 100,
            "max_mana": 100,
            "moves": 100,
            "max_moves": 100,
            "position": _.POS_STANDING
        }
        self.keywords = []
        self.inventory = []
        self.affects = []
        self.fighting = None
        self.peer = None

    def get_position(self):
        return self.stats["position"]

    def is_sendable(self):
        return False

    def set_position(self, position):
        self.stats["position"] = position

    def get_damage(self):
        dmg = self.stats["damage"]
        #Damage string is in the form 5d6+3

        #TODO: Add code to check if MOB is wielding a weapon

        modifier = int(dmg.split('+')[1])
        dice = int(dmg.split('+')[0].split('d')[0])
        sides = int(dmg.split('+')[0].split('d')[1])
        dmg = modifier
        for i in range(dice):
            dmg += random.randint(0, sides)
        return (dmg, self.stats["noun"], "none")

    def affected_by(self, affect):
        for a in self.affects:
            if _.affect_list[affect].name == a.name:
                return True
        else:
            return False

    def remove_affect(self, affect):
        for a in self.affects:
            if a.name == affect:
                self.affects.remove(a)
                break

    def get_race(self):
        for r in _.races:
            if r.get_name() == self.stats["race"]:
                return r

    def get_class(self):
        for c in _.classes:
            if c.get_name() == self.stats["class"]:
                return c

    def get_hp(self):
        return self.stats["hp"]
        
    def get_mana(self):
        return self.stats["mana"]
        
    def get_moves(self):
        return self.stats["moves"]

    def get_skills(self):
        return []

    def get_hitroll(self):
        return 0

    def get_damroll(self):
        return 0

    def get_max_hp(self):
        return self.stats["max_hp"]
        
    def get_max_mana(self):
        return self.stats["max_mana"]
        
    def get_max_moves(self):
        return self.stats["max_moves"]

    def damage(self, amount):
        self.stats["hp"] -= amount

    def handle_death(self, villain):
        self.remove_from_combat()
        _.send_to_char(self.peer, "You have been KILLED!!\n\r", False)
        _.send_to_room_except("%s is DEAD!!\n\r" % self.get_name(), self.get_room(), [self.peer,])
        if villain.has_peer() and self.has_peer():
            _.send_to_all("%s suffers defeat at the hands of %s.\n\r" % (self.get_name(), villain.get_name()))
        if self.has_peer():
            self.set_position(_.POS_RESTING)
            self.stats["room"] = _.START_ROOM
            self.stats["hp"] = self.stats["max_hp"]
        else:
            _.mobiles.remove(self)

    def handle_kill(self, victim):
        pass

    def remove_from_combat(self):
        self.fighting = None
        self.set_position(_.POS_STANDING)
        for m in _.mobiles:
            if m.fighting == self:
                try:
                    m.fighting = random.choice([v for v in _.mobiles if v.fighting == m])
                except IndexError:
                    m.fighting = None
                    m.set_position(_.POS_STANDING)

    def heal(self, amount):
        self.stats["hp"] = min(self.stats["max_hp"], self.stats["hp"] + amount)

    def is_dead(self):
        if self.get_hp() <= 0:
            return True
        else:
            return False

    def get_keywords(self):
        return self.keywords

    def get_room(self):
        for a in _.areas:
            for r in a.rooms:
                if r.vnum == self.stats["room"]:
                    return r

    def get_area(self):
        return self.get_room().get_area()

    def add_lag(self, increment):
        self.lag += increment

    def get_name(self, looker=None):
        if looker is not None:
            if looker.can_see(self):
                return self.stats["name"]
            else:
                return "Someone"
        else:
            return self.stats["name"]

    def get_condition(self):
        percentage = self.get_hp() / self.get_max_hp()
        buf = ""
        if percentage >= 1:
            buf = "%s is in excellent condition.\n\r" % self.get_name().capitalize()
        elif percentage >= 0.9:
            buf = "%s has a few scratches.\n\r" % self.get_name().capitalize()
        elif percentage >= 0.75:
            buf = "%s has some small wounds and bruises.\n\r" % self.get_name().capitalize()
        elif percentage >= 0.55:
            buf = "%s has a few wounds.\n\r" % self.get_name().capitalize()
        elif percentage >= 0.35:
            buf = "%s has some big nasty wounds and scratches.\n\r" % self.get_name().capitalize()
        elif percentage >= 0.15:
            buf = "%s is pretty hurt.\n\r" % self.get_name().capitalize()
        elif percentage > 0:
            buf = "%s is in awful condition.\n\r" % self.get_name().capitalize()
        else:
            buf = "%s is mortally wounded and should be dead.\n\r" % self.get_name().capitalize()

        return buf

    def has_peer(self):
        if self.peer is None:
            return False
        else:
            return True

    def get_stat(self, stat):
        temp_stat = self.get_base_stat(stat)
        return temp_stat

    def get_base_stat(self, stat):
        temp_stat = self.get_race().stats["base_" + stat]
        if self.get_class().get_class_stat() == stat:
            temp_stat += 3
        return temp_stat

    def get_max_stat(self, stat):
        temp_stat = self.get_race().stats["max_" + stat]
        if self.get_class().get_class_stat() == stat:
            temp_stat = min(temp_stat + 2, 25)
        return temp_stat

    def affected_by(self, test_affect):
        if test_affect.name in [a.name for a in self.affects]:
            return True
        else:
            return False

    def can_see(self, target):
        if self.affected_by(_.affect_list["dirtkick"]):
            return False
        if self.affected_by(_.affect_list["blind"]):
            return False
        return True


def initialize_mobiles():
    f = open("data/mobiles.dat", "r")
    lines = f.readlines()
    for l in lines:
        if l == "--- START MOBILE ---\n":
            temp_mobile = Mobile()
            continue
        elif l == "--- END MOBILE ---\n":
            _.master_mobile_list.append(temp_mobile)
            temp_mobile = None
            continue
        try:
            temp_key = l.split(":^:")[0].strip()
            temp_value = l.split(":^:")[1].strip()
            if "(*int)" in temp_value:
                temp_value = int(temp_value[6:])
            elif temp_key == "vnum":
                temp_mobile.vnum = temp_value
            elif temp_key == "max_hp":
                #text stores as 5d6+200 or something similar: this code handles that
                t = temp_value.split("+")
                m = int(t[1])
                dice = int(t[0].split('d')[0])
                sides = int(t[0].split('d')[1])
                for i in range(0, dice):
                    m += random.randint(0, sides)
                temp_mobile.stats["max_hp"] = m
                #print (m)
            elif temp_key == "keywords":
                temp_mobile.keywords = temp_value.split()
            else:
                temp_mobile.stats[temp_key] = temp_value
        except IndexError:
            if ':^:' not in l:
                temp_mobile.stats["longdesc"] += l.strip() + '\n\r'
            else:
                print("Illegal mobile. Skipping.")
