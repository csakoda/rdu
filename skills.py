__author__ = 'ohell_000'


import globals as _
import random
import combat
import mobile


def do_sap(char, args, target, success):
    if success:  # Success
        target.remove_from_combat()
        target.set_position(_.POS_SLEEPING)
        _.affect_list["sap"].apply_affect(target, 12)
    else:
        combat.start_combat_block()
        combat.start_combat(char.player, target)
        combat.do_damage(char.player, target, 0, "sap", False)
        combat.end_combat_block()


def do_bash(char, args, target, success):
    combat.start_combat_block()
    if success:
        _.send_to_char(char, "You send %s flying with a powerful bash!\n\r" % target.get_name(char.player))
        _.send_to_char(target.get_peer(), "%s sends you flying with a powerful bash!\n\r" % char.player.get_name())
        _.send_to_room_except("%s sends %s flying with a powerful bash!\n\r" %
                              (char.player.get_name(), target.get_name()), char.player.get_room(),
                              [char, target.get_peer()])
        temp_damage = random.randint(2,12)
        combat.do_damage(char.player, target, temp_damage, "bash", False)
        combat.start_combat(char.player, target)
    else:
        _.send_to_char(char, "You fall flat on your face!\n\r")
        _.send_to_char(target.get_peer(), "%s falls flat on their face!\n\r" % char.player.get_name())
        _.send_to_room_except("%s falls flat on their face!\n\r" %
                              char.player.get_name(), char.player.get_room(),
                              [char, target.get_peer()])
    combat.end_combat_block()


def do_dirtkick(char, args, target, success):
    combat.start_combat_block()
    if success:
        _.affect_list["dirtkick"].apply_affect(target, 24)
    else:
        combat.do_damage(char.player, target, 0, "kicked dirt", False)
    combat.end_combat_block()


def get_room_by_vnum(v):
    for a in _.areas:
        for r in a.rooms:
            if r.vnum == v:
                return r

def do_hunt(char, rgs, target, success):
    _.send_to_room_except(char.player.get_name() + " sniffs the air.",char.player.get_room(),[char])
    myroom = char.player.get_room()
    destroom = target.get_room()
    if myroom == destroom:
        _.send_to_char(char, target.get_name() + " is HERE!")
        return
    fringe = []
    for i,j in myroom.exits.items():
        if not j is None:
            fringe.append((get_room_by_vnum(j),i))
    visited = [myroom]

    for room in fringe:
        if room[0] is None:
            #print("NONE")
            pass
        elif room[0] in visited:
            #print("VISITED")
            pass
        elif room[0] is destroom:
            #print("DESTINATION FOUND: ", _.get_dir_string(room[1]))
            _.send_to_char(char, target.get_name() + " is " + _.get_dir_string(room[1]) + " of you.")
            return
        else:
            for i,j in room[0].exits.items():
                if not j is None and not get_room_by_vnum(j) in visited:
                    fringe.append((get_room_by_vnum(j),room[1]))
        visited.append(room[0])


def do_berserk(char, args, target, success):
    if success:  # Success
        _.affect_list["berserk"].apply_affect(char.player, 12)
    else:
        _.send_to_char(char, "Your pulse speeds up, but nothing happens.\n\r")


def check_bash(base_chance, hero, target):
    return base_chance


def check_dirtkick(base_chance, hero, target):
    return base_chance


def check_berserk(base_chance, hero, target):
    return base_chance


def check_sneak(base_chance, hero, target):
    return base_chance


def check_sap(base_chance, hero, target):
    return 50

class Skill():

    def __init__(self, function, position, success_lag, fail_lag, aggro, target_state, in_combat, self_targetable,
                 check_function=None, base_chance=80):
        self.function = function
        self.position = position
        self.success_lag = success_lag
        self.fail_lag = fail_lag
        self.aggro = aggro
        self.target_state = target_state
        self.in_combat = in_combat
        self.self_targetable = self_targetable
        self.base_chance = base_chance
        if check_function is not None:
            self.check_function = check_function

    def check_function(self, base_chance, char, target):
        return self.base_chance

    def execute_skill(self, char, args):
        #  Check in_combat
        if self.function is None:
            _.send_to_char(char, "This is a passive skill.\n\r")
            return
        if char.player.fighting is not None and not self.in_combat:
            _.send_to_char(char, "You can't use that in combat.\n\r")
            return

        #  Find target
        if self.target_state == _.TARGET_SELF_ONLY:
            target = char.player
        elif self.target_state == _.TARGET_PREFER_SELF:
            try:
                target = mobile.get_mobile_in_room(args.split()[0], char.player.get_room())
                if target == None:
                    _.send_to_char(char, "They aren't here.\n\r")
                    return
            except IndexError:
                target = char.player
        elif self.target_state == _.TARGET_PREFER_FIGHTING:
            try:
                target = mobile.get_mobile_in_room(args.split()[0], char.player.get_room())
                if target == None:
                    _.send_to_char(char, "They aren't here.\n\r")
                    return
            except IndexError:
                if char.player.fighting is None:
                    _.send_to_char(char, "You aren't fighting anyone.\n\r")
                    return
                else:
                    target = char.player.fighting
        elif self.target_state == _.TARGET_TARGET_ONLY:
            try:
                target = mobile.get_mobile_in_room(args.split()[0], char.player.get_room())
                if target == None:
                    _.send_to_char(char, "They aren't here.\n\r")
                    return
            except IndexError:
                    _.send_to_char(char, "You must provide a target.\n\r")
                    return
        elif self.target_state == _.TARGET_TARGET_ANYWHERE:
            try:
                target = mobile.get_mobile(args.split()[0])
                if target == None:
                    _.send_to_char(char, "You can't find them.\n\r")
                    return
            except IndexError:
                _.send_to_char(char, "You must provide a target.\n\r")
                return
        else:
            target = None

        if target == char.player and not self.self_targetable:
            _.send_to_char(char, "You can't use that on yourself.\n\r")
            return

        if char.player.get_position() < self.position:
            if char.player.get_position() == _.POS_SLEEPING:
                _.send_to_char(char, "You can't do that, you're sleeping!\n\r")
            elif char.player.get_position() == _.POS_RESTING:
                _.send_to_char(char, "Nah...you're too relaxed.\n\r")
            elif char.player.get_position() == _.POS_STANDING:
                _.send_to_char((char, "You aren't fighting anyone.\n\r"))
            return
        chance = self.check_function(self.base_chance, char.player, target)

        # Modify chance for global things: e.g., being shocked

        if char.player.affected_by(_.affect_list["shock"]):
            chance -= 10

        success = random.randint(1,100) <= chance
        self.function(char, args, target, success)

        if self.aggro:
            combat.start_combat(char.player, target)

        if success:
            char.player.add_lag(self.success_lag)
        else:
            char.player.add_lag(self.fail_lag)

def initialize_skills():
    _.skill_list["bash"] = Skill(do_bash, _.POS_STANDING, 6, 6, True, _.TARGET_PREFER_FIGHTING, True, False, check_bash)
    _.skill_list["dirtkick"] = Skill(do_dirtkick, _.POS_STANDING, 6, 6, True, _.TARGET_PREFER_FIGHTING, True, False,
                                     check_dirtkick)
    _.skill_list["berserk"] = Skill(do_berserk, _.POS_STANDING, 3, 3, False, _.TARGET_SELF_ONLY, True, True, check_berserk)
    _.skill_list["sap"] = Skill(do_sap, _.POS_STANDING, 3, 3, False, _.TARGET_TARGET_ONLY, False, False, check_sap)
    _.skill_list["sneak"] = Skill(None, _.POS_STANDING, 3, 3, True, _.TARGET_TARGET_ONLY, False, False, check_sneak)
    _.skill_list["hunt"] = Skill(do_hunt, _.POS_STANDING, 1, 1, False, _.TARGET_TARGET_ANYWHERE, False, False, check_bash)

    _.skill_list_sorted = sorted(_.skill_list)