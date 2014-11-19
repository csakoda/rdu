__author__ = 'ohell_000'


import globals as _
import copy


def affect_apply_berserk(affect):
    affect.stats["hitroll"] = 10
    affect.stats["damroll"] = 10
    affect.target.heal(20)


class Affect():
    def __init__(self, name, desc, apply_string_self, apply_string_others, \
                 remove_string_self, remove_string_others, apply_function, wear_function, update_function):
        self.name = name
        self.desc = desc
        self.duration = 0
        self.apply_string_self = apply_string_self
        self.apply_string_others = apply_string_others
        self.remove_string_self = remove_string_self
        self.remove_string_others = remove_string_others
        self.apply_function = apply_function
        self.wear_function = wear_function
        self.update_function = update_function
        self.target = None
        self.stats = {
            "str": 0,
            "dex": 0,
            "int": 0,
            "con": 0,
            "wis": 0,
            "hitroll": 0,
            "damroll": 0
        }

    def apply_affect(self, target, duration):
        new_affect = copy.deepcopy(self)
        new_affect.target = target
        new_affect.duration = duration
        target.affects.append(new_affect)
        if self.apply_function is not None:
            self.apply_function(new_affect)
        target.peer.peer_send(self.apply_string_self)
        _.send_to_room_except(self.apply_string_others % target.get_name(), target.get_room(), [target.peer,])

    def remove_affect(self):
        if self.remove_string_self != "":
            self.target.peer.peer_send(self.remove_string_self)
        if self.remove_string_others != "":
            _.send_to_room_except(self.remove_string_others % self.target.get_name(), self.target.get_room(), \
                              [self.target.peer,])
        self.target.affects.remove(self)


def initialize_affects():
    _.affect_list["sanctuary"] = \
        Affect("sanctuary", "provides moderate damage reduction vs. mobs", \
               "You are surrounded by a white aura.\n\r", "%s is surrounded by a white aura.\n\r", \
               "The white aura surrounding you fades.\n\r", "The white aura surrounding %s fades.\n\r", \
               None, None, None)
    _.affect_list["shock"] = \
        Affect("shock", "causes moderate skill failure", \
               "You jerk and twitch from the shock!\n\r", "%s jerks and twitches from the shock!\n\r", \
               "", "", \
               None, None, None)
    _.affect_list["curse"] = \
        Affect("curse", "prevents recall", \
               "You feel unclean.\n\r", "%s looks very uncomfortable.\n\r", \
               "You feel better.\n\r", "%s looks more relaxed.\n\r", \
               None, None, None)
    _.affect_list["mirror"] = \
        Affect("mirror image", "blocks attacks before shattering", \
               "You create a mirror image of yourself.\n\r", "%s creates a mirror image.\n\r", \
               "Your mirror image shatters to pieces!\n\r", "%s's mirror image shatters to pieces!\n\r", \
               None, None, None)
    _.affect_list["berserk"] = \
        Affect("berserk", "+10 hitroll, +10 damroll", \
               "Your pulse races as you are consumed by rage!\n\r", "%s gets a wild look in their eyes.\n\r", \
               "You feel your pulse slow down.\n\r", "", \
               affect_apply_berserk, None, None)
    _.affect_list["sap"] = \
        Affect("sap", "you're temporarily unconscious and unable to wake", \
               "You slump to the ground, unconscious.\n\r", "%s slumps to the ground, unconscious.\n\r", \
               "You come to your senses.\n\r", "", \
               None, None, None)
    _.affect_list["dirtkick"] = \
        Affect("dirt kick", "you're temporarily blinded", \
               "You are blinded by the dirt in your eyes!\n\r", "%s is blinded by the dirt in their eyes!\n\r", \
               "You rub the dirt out of your eyes.\n\r", "%s rubs the dirt out of their eyes.\n\r", \
               None, None, None)
    _.affect_list["blind"] = \
        Affect("blind", "you're temporarily blinded", \
               "You are blinded!\n\r", "%s is blinded!\n\r", \
               "You are no longer blinded.\n\r", "%s is no longer blinded.\n\r", \
               None, None, None)

    _.affect_list_sorted = sorted(_.affect_list)