__author__ = 'ohell_000'


import globals as _
import random
import combat
import mobile


def do_sap(peer, args, target, success):
    if success:  # Success
        target.remove_from_combat()
        target.set_position(_.POS_SLEEPING)
        _.affect_list["sap"].apply_affect(target, 12)
    else:
        combat.start_combat_block()
        combat.start_combat(peer.account.player, target)
        combat.do_damage(peer.account.player, target, 0, "sap", False)
        combat.end_combat_block()


def do_bash(peer, args, target, success):
    combat.start_combat_block()
    if success:
        peer.account.player.send("You send %s flying with a powerful bash!?!?!?\n\r" % target.get_name(peer.account.player))
        target.send("%s sends you flying with a powerful bash!\n\r" % peer.account.player.get_name())
        _.send_to_room_except("%s sends %s flying with a powerful bash!\n\r" %
                              (peer.account.player.get_name(), target.get_name()), peer.account.player.get_room(),
                              [peer, target.peer])
        temp_damage = random.randint(2,12)
        combat.do_damage(peer.account.player, target, temp_damage, "bash", False)
        combat.start_combat(peer.account.player, target)
    else:
        peer.account.player.send("You fall flat on your face!\n\r")
        target.send("%s falls flat on their face!\n\r" % peer.account.player.get_name())
        _.send_to_room_except("%s falls flat on their face!\n\r" %
                              peer.account.player.get_name(), peer.account.player.get_room(),
                              [peer, target.peer])
    combat.end_combat_block()


def do_dirtkick(peer, args, target, success):
    combat.start_combat_block()
    if success:
        _.affect_list["dirtkick"].apply_affect(target, 24)
    else:
        combat.do_damage(peer.account.player, target, 0, "kicked dirt", False)
    combat.end_combat_block()


def get_room_by_vnum(v):
    for a in _.areas:
        for r in a.rooms:
            if r.vnum == v:
                return r

def do_hunt(peer, rgs, target, success):
    _.send_to_room_except(peer.account.player.get_name() + " sniffs the air.",peer.account.player.get_room(),[peer])
    myroom = peer.account.player.get_room()
    destroom = target.get_room()
    if myroom == destroom:
        peer.account.player.send(target.get_name() + " is HERE!")
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
            peer.account.player.send(target.get_name() + " is " + _.get_dir_string(room[1]) + " of you.")
            return
        else:
            for i,j in room[0].exits.items():
                if not j is None and not get_room_by_vnum(j) in visited:
                    fringe.append((get_room_by_vnum(j),room[1]))
        visited.append(room[0])


def do_berserk(peer, args, target, success):
    if success:  # Success
        _.affect_list["berserk"].apply_affect(peer.account.player, 12)
    else:
        peer.account.player.send("Your pulse speeds up, but nothing happens.\n\r")


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

    def check_function(self, base_chance, peer, target):
        return self.base_chance

    def execute_skill(self, peer, args):
        #  Check in_combat
        if self.function is None:
            peer.account.player.send("This is a passive skill.\n\r")
            return
        if peer.account.player.fighting is not None and not self.in_combat:
            peer.account.player.send("You can't use that in combat.\n\r")
            return

        #  Find target
        if self.target_state == _.TARGET_SELF_ONLY:
            target = peer.account.player
        elif self.target_state == _.TARGET_PREFER_SELF:
            try:
                target = mobile.get_mobile_in_room(args.split()[0], peer.account.player.get_room())
                if target == None:
                    peer.account.player.send("They aren't here.\n\r")
                    return
            except IndexError:
                target = peer.account.player
        elif self.target_state == _.TARGET_PREFER_FIGHTING:
            try:
                target = mobile.get_mobile_in_room(args.split()[0], peer.account.player.get_room())
                if target == None:
                    peer.account.player.send("They aren't here.\n\r")
                    return
            except IndexError:
                if peer.account.player.fighting is None:
                    peer.account.player.send("You aren't fighting anyone.\n\r")
                    return
                else:
                    target = peer.account.player.fighting
        elif self.target_state == _.TARGET_TARGET_ONLY:
            try:
                target = mobile.get_mobile_in_room(args.split()[0], peer.account.player.get_room())
                if target == None:
                    peer.account.player.send("They aren't here.\n\r")
                    return
            except IndexError:
                    peer.account.player.send("You must provide a target.\n\r")
                    return
        elif self.target_state == _.TARGET_TARGET_ANYWHERE:
            try:
                target = mobile.get_mobile(args.split()[0])
                if target == None:
                    peer.account.player.send("You can't find them.\n\r")
                    return
            except IndexError:
                peer.account.player.send("You must provide a target.\n\r")
                return
        else:
            target = None

        if target == peer.account.player and not self.self_targetable:
            peer.account.player.send("You can't use that on yourself.\n\r")
            return

        if peer.account.player.get_position() < self.position:
            if peer.account.player.get_position() == _.POS_SLEEPING:
                peer.account.player.send("You can't do that, you're sleeping!\n\r")
            elif peer.account.player.get_position() == _.POS_RESTING:
                peer.account.player.send("Nah...you're too relaxed.\n\r")
            elif peer.account.player.get_position() == _.POS_STANDING:
                peer.peer_send("You aren't fighting anyone.\n\r")
            return
        chance = self.check_function(self.base_chance, peer.account.player, target)

        # Modify chance for global things: e.g., being shocked

        if peer.account.player.affected_by(_.affect_list["shock"]):
            chance -= 10

        success = random.randint(1,100) <= chance
        self.function(peer, args, target, success)

        if self.aggro:
            combat.start_combat(peer.account.player, target)

        if success:
            peer.account.player.add_lag(self.success_lag)
        else:
            peer.account.player.add_lag(self.fail_lag)

def initialize_skills():
    _.skill_list["bash"] = Skill(do_bash, _.POS_STANDING, 6, 6, True, _.TARGET_PREFER_FIGHTING, True, False, check_bash)
    _.skill_list["dirtkick"] = Skill(do_dirtkick, _.POS_STANDING, 6, 6, True, _.TARGET_PREFER_FIGHTING, True, False,
                                     check_dirtkick)
    _.skill_list["berserk"] = Skill(do_berserk, _.POS_STANDING, 3, 3, False, _.TARGET_SELF_ONLY, True, True, check_berserk)
    _.skill_list["sap"] = Skill(do_sap, _.POS_STANDING, 3, 3, False, _.TARGET_TARGET_ONLY, False, False, check_sap)
    _.skill_list["sneak"] = Skill(None, _.POS_STANDING, 3, 3, True, _.TARGET_TARGET_ONLY, False, False, check_sneak)
    _.skill_list["hunt"] = Skill(do_hunt, _.POS_STANDING, 1, 1, False, _.TARGET_TARGET_ANYWHERE, False, False, check_bash)

    _.skill_list_sorted = sorted(_.skill_list)