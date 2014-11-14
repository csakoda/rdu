__author__ = 'ohell_000'


import globals as _
import mobile


def get_player(target):
    for v in _.peers:
        if v.state is not _.STATE_ONLINE:
            continue
        if len(v.player.get_name()) >= len(target) \
                and v.player.get_name()[:len(target)].lower() == target.lower().strip():
            return v.player
    else:
        return None


class Player(mobile.Mobile):
    def __init__(self):
        mobile.Mobile.__init__(self)
        self.lag = 0
        self.prompt = "<%s/%shp>"
        self.equipment = {
            _.WEAR_ARMS: None,
            _.WEAR_BODY: None,
            _.WEAR_FEET: None,
            _.WEAR_FINGER: None,
            _.WEAR_FINGER2: None,
            _.WEAR_HAND: None,
            _.WEAR_HEAD: None,
            _.WEAR_LEGS: None,
            _.WEAR_NECK: None,
            _.WEAR_NECK2: None,
            _.WEAR_OFFHAND: None,
            _.WEAR_TORSO: None,
            _.WEAR_WAIST: None,
            _.WEAR_WRIST: None,
            _.WEAR_WRIST2: None,
            _.WEAR_FLOAT: None,
            _.WEAR_FLOAT2: None,
            _.WEAR_HELD: None,
            _.WEAR_LIGHT: None,
            _.WEAR_WEAPON: None
        }

    def get_damage(self):
        import random

        temp_weapon = self.equipment[_.WEAR_WEAPON]
        if temp_weapon is None:
            return random.randint(1,10), "punch"
        temp_damage = temp_weapon.get_damage()
        return temp_damage

    def get_prompt(self):
        return self.prompt % (self.get_hp(), self.get_max_hp())

    def get_keywords(self):
        return [self.get_name().lower(),]

    def get_skills(self):
        temp_skills = self.get_class().stats["skills"]
        return temp_skills

    def get_spells(self):
        temp_spells = self.get_class().stats["spells"]
        return temp_spells

    def get_hitroll(self):
        hitroll = 0
        for e in self.equipment:
            try:
                hitroll += self.equipment[e].stats["hitroll"]
            except (KeyError, AttributeError):
                continue
        for a in self.affects:
            try:
                hitroll += a.stats["hitroll"]
            except KeyError:
                continue
        return hitroll

    def get_damroll(self):
        damroll = 0
        for e in self.equipment:
            try:
                damroll += self.equipment[e].stats["damroll"]
            except (KeyError, AttributeError):
                continue
        for a in self.affects:
            try:
                damroll += a.stats["damroll"]
            except KeyError:
                continue
        return damroll

    def wield_weapon(self, weapon):  # -Rework- for brevity
        char = self.get_peer()
        if self.equipment[_.WEAR_WEAPON] is None:
                    #  Easy, just remove from inventory and equip to that slot
                    self.equipment[_.WEAR_WEAPON] = weapon
                    self.inventory.remove(weapon)
                    #  Eventually we will add messages better tailored to the slot being used
                    _.send_to_char(char, "You wield %s.\n\r" % weapon.get_name())
                    _.send_to_room_except("%s wields %s.\n\r" % (self.get_name(), weapon.get_name()), \
                                          self.get_room(), [char,])
            # No luck, so we just remove the item at the given slot and add the new item
        #  Easy, just remove from inventory and equip to that slot
        else:
            self.inventory.append(self.equipment[_.WEAR_WEAPON])
            _.send_to_char(char, "You stop using %s.\n\r" % self.equipment[_.WEAR_WEAPON].get_name())
            _.send_to_room_except("%s stops using %s.\n\r" % (self.get_name(), self.equipment[_.WEAR_WEAPON].get_name()), \
                                  self.get_room(), [char,])
            self.equipment[_.WEAR_WEAPON] = weapon
            self.inventory.remove(weapon)
            _.send_to_char(char, "You wield %s.\n\r" % weapon.get_name())
            _.send_to_room_except("%s wields %s.\n\r" % (self.get_name(), weapon.get_name()), \
                                  self.get_room(), [char,])

    def wear_armor(self, armor):  # -Rework- for brevity
        #  Presumes an item in your inventory
        char = self.get_peer()

        temp_loc = armor.wear_loc
        if temp_loc == _.WEAR_WEAPON:
            self.wield_weapon(armor)
            return
        #  Check if there's an open slot
        if self.equipment[temp_loc] is None:
            #  Easy, just remove from inventory and equip to that slot
            self.equipment[temp_loc] = armor
            self.inventory.remove(armor)
            #  Eventually we will add messages better tailored to the slot being used
            _.send_to_char(char, "You wear %s on your %s.\n\r" % (armor.get_name(), armor.wear_loc_string()))
            _.send_to_room_except("%s wears %s on their %s.\n\r" % (self.get_name(), armor.get_name(), armor.wear_loc_string()), \
                                  self.get_room(), [char,])
            return
        #  For a few items, check for a second open slot as well
        if temp_loc == _.WEAR_WRIST:
            if self.equipment[_.WEAR_WRIST2] is None:
                #  Easy, just remove from inventory and equip to that slot
                self.equipment[_.WEAR_WRIST2] = armor
                self.inventory.remove(armor)
                #  Eventually we will add messages better tailored to the slot being used
                _.send_to_char(char, "You wear %s on your %s.\n\r" % (armor.get_name(), armor.wear_loc_string()))
                _.send_to_room_except("%s wears %s on their %s.\n\r" % (self.get_name(), armor.get_name(), armor.wear_loc_string()), \
                                      self.get_room(), [char,])
                return
        if temp_loc == _.WEAR_FLOAT:
            if self.equipment[_.WEAR_FLOAT2] is None:
                #  Easy, just remove from inventory and equip to that slot
                self.equipment[_.WEAR_FLOAT2] = armor
                self.inventory.remove(armor)
                #  Eventually we will add messages better tailored to the slot being used
                _.send_to_char(char, "You wear %s on your %s.\n\r" % (armor.get_name(), armor.wear_loc_string()))
                _.send_to_room_except("%s wears %s on their %s.\n\r" % (self.get_name(), armor.get_name(), armor.wear_loc_string()), \
                                      self.get_room(), [char,])
                return
        if temp_loc == _.WEAR_FINGER:
            if self.equipment[_.WEAR_FINGER2] is None:
                #  Easy, just remove from inventory and equip to that slot
                self.equipment[_.WEAR_FINGER2] = armor
                self.inventory.remove(armor)
                #  Eventually we will add messages better tailored to the slot being used
                _.send_to_char(char, "You wear %s on your %s.\n\r" % (armor.get_name(), armor.wear_loc_string()))
                _.send_to_room_except("%s wears %s on their %s.\n\r" % (self.get_name(), armor.get_name(), armor.wear_loc_string()), \
                                      self.get_room(), [char,])
                return
        if temp_loc == _.WEAR_NECK:
            if self.equipment[_.WEAR_NECK2] is None:
                #  Easy, just remove from inventory and equip to that slot
                self.equipment[_.WEAR_NECK2] = armor
                self.inventory.remove(armor)
                #  Eventually we will add messages better tailored to the slot being used
                _.send_to_char(char, "You wear %s on your %s.\n\r" % (armor.get_name(), armor.wear_loc_string()))
                _.send_to_room_except("%s wears %s on their %s.\n\r" % (self.get_name(), armor.get_name(), armor.wear_loc_string()), \
                                      self.get_room(), [char,])
                return
        # No luck, so we just remove the item at the given slot and add the new item
        #  Easy, just remove from inventory and equip to that slot
        self.inventory.append(self.equipment[temp_loc])
        _.send_to_char(char, "You stop using %s.\n\r" % self.equipment[temp_loc].get_name())
        _.send_to_room_except("%s stops using %s.\n\r" % (self.get_name(), self.equipment[temp_loc].get_name()), \
                              self.get_room(), [char,])
        self.equipment[temp_loc] = armor
        self.inventory.remove(armor)
        #  Eventually we will add messages better tailored to the slot being used
        _.send_to_char(char, "You wear %s on your %s.\n\r" % (armor.get_name(), armor.wear_loc_string()))
        _.send_to_room_except("%s wears %s on their %s.\n\r" % (self.get_name(), armor.get_name(), armor.wear_loc_string()), \
                              self.get_room(), [char,])

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        try:
            self.inventory.remove(item)
            return True
        except ValueError:
            return False