__author__ = 'ohell_000'


import globals as _
import random
import mobile
import combat


def spell_sanctuary(peer, args, target):
    _.affect_list["sanctuary"].apply_affect(target, 6)


def spell_gate(peer, args, target):
    import commands

    try:
        target = mobile.get_mobile(args.split()[0])
    except IndexError:
        peer.account.player.send("You must provide a target for that spell.\n\r")
        return
    if target is None:
        peer.account.player.send("You can't find them.\n\r")
        return
    if target == peer.account.player:
        peer.account.player.send("You can't gate to yourself.\n\r")
        return
    peer.account.player.remove_from_combat()
    _.send_to_room_except("%s steps through a gate and vanishes.\n\r" % peer.account.player.get_name(), peer.account.player.get_room(),
                          [peer,])
    peer.account.player.send("You step through a gate and vanish.\n\r")
    peer.account.player.stats["room"] = target.get_room().vnum
    _.send_to_room_except("%s has arrived through a gate.\n\r" % peer.account.player.get_name(), peer.account.player.get_room(),
                          [peer,])
    commands.do_look(peer, "")


def spell_mirror(peer, args, target):
    _.affect_list["mirror"].apply_affect(peer.account.player, 12)


def spell_lightning(peer, args, target):
    combat.do_damage(peer.account.player, target, random.randint(10,15), "lightning bolt", True)


def spell_heal(peer, args, target):
    target.heal(random.randint(1,50))
    peer.account.player.send("You heal %s.\n\r" % target.get_name())
    target.send("A warm feeling fills your body.\n\r")


def spell_curse(peer, args, target):
    if random.randint(0,1) == 0:
        _.affect_list["curse"].apply_affect(target, 6)
    else:
        peer.account.player.send("%s resisted your curse.\n\r" % target.get_name())


def spell_blind(peer, args, target):
    if random.randint(0,1) == 0:
        _.affect_list["blind"].apply_affect(target, 6)
    else:
        peer.account.player.send("%s resisted your blind.\n\r" % target.get_name())


def spell_phantom(peer, args, target):
    combat.do_damage(peer.account.player, target, random.randint(5,10), "ghoulish grasp", True)
    if random.randint(0,1) == 0:
        _.affect_list["shock"].apply_affect(target, 6)


class Spell():
    def __init__(self, function, lag, words, aggro, target_state, in_combat):
        self.function = function
        self.words = words
        self.lag = lag
        self.aggro = aggro
        self.target_state = target_state
        self.in_combat = in_combat

    def execute_spell(self, peer, args):

        #  Check in_combat
        if peer.account.player.fighting is not None and not self.in_combat:
            peer.account.player.send("You can't cast that spell in combat.\n\r")
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
        else:
            target = None

        combat.start_combat_block()
        if self.aggro:
            combat.start_combat(peer.account.player, target)
        if random.randint(0,1) == 5:  # -Rework- right now there's no chance of losing concentration
            self.lost_concentration(peer)
            return
        _.send_to_room_except("%s utters the words, '%s'.\n\r" % (peer.account.player.get_name(), self.words), \
                              peer.account.player.get_room(), [peer,])
        self.function(peer, args, target)
        combat.end_combat_block()
        peer.account.player.add_lag(self.lag)

    def lost_concentration(self, peer):
        import combat
        peer.account.player.add_lag(self.lag)
        peer.account.player.send("You lost your concentration.\n\r")
        _.send_to_room_except("%s utters the words, '%s'.\n\r" % (peer.account.player.get_name(), self.words), \
                              peer.account.player.get_room(), [peer,])
        combat.end_combat_block()

def initialize_spells():
    _.spell_list["sanctuary"] = Spell(spell_sanctuary, 3, "gaiqhjabral", False, _.TARGET_PREFER_SELF, False)
    _.spell_list["lightning"] = Spell(spell_lightning, 3, "diesilla barh", True, _.TARGET_PREFER_FIGHTING, True)
    _.spell_list["phantom"] = Spell(spell_phantom, 3, "spaihaw yafqz", True, _.TARGET_PREFER_FIGHTING, True)
    _.spell_list["heal"] = Spell(spell_heal, 3, "heal", False, _.TARGET_PREFER_SELF, True)
    _.spell_list["curse"] = Spell(spell_curse, 3, "curse", True, _.TARGET_PREFER_FIGHTING, True)
    _.spell_list["blind"] = Spell(spell_blind, 3, "blind", True, _.TARGET_PREFER_FIGHTING, True)
    _.spell_list["mirror"] = Spell(spell_mirror, 3, "wuffaf uwaoz", False, _.TARGET_SELF_ONLY, False)
    _.spell_list["gate"] = Spell(spell_gate, 3, "oahz", False, _.TARGET_IGNORE, True)

    _.spell_list_sorted = sorted(_.spell_list)