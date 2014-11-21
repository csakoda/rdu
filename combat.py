__author__ = 'ohell_000'


import globals as _
import random
import skills


def get_damage_string(damage, magical):
     if not magical:
        if damage < 1:
            return "clumsy ", "misses", "."
        elif damage < 5:
            return "clumsy ", "bruises", "."
        elif damage < 10:
            return "wobbly ", "scrapes", "."
        elif damage < 15:
            return "wobbly ", "scratches", "."
        elif damage < 20:
            return "amateur ", "lightly wounds", "."
        elif damage < 25:
            return "amateur ", "injures", "."
        elif damage < 30:
            return "competent ", "harms", ", creating a bruise."
        elif damage < 35:
            return "competent ", "thrashes", ", leaving marks!"
        elif damage < 40:
            return "cunning ", "decimates", ", the wound bleeds!"
        elif damage < 45:
            return "cunning ", "devastates", ", hitting organs!"
        elif damage < 50:
            return "calculated ", "mutilates", ", shredding flesh!"
        elif damage < 55:
            return "calculated ", "cripples", ", leaving GAPING holes!"
        elif damage < 60:
            return "calm ", "DISEMBOWELS", ", guts spill out!"
        elif damage < 65:
            return "calm ", "DISMEMBERS", ", blood sprays forth!"
        elif damage < 70:
            return "furious ", "ANNIHILATES!", ", revealing bones!"
        elif damage < 75:
            return "frenzied ", "OBLITERATES!", ", rending organs!"
        elif damage < 80:
            return "furious ", "DESTROYS!!", ", shattering bones!"
        elif damage < 85:
            return "barbaric ", "MASSACRES!!", ", gore splatters everywhere!"
        elif damage < 90:
            return "deadly ", "!DECAPITATES!", ", scrambling some brains!"
        elif damage < 95:
            return "legendary ", "!!SHATTERS!!", " into tiny pieces!"
        else:
            return "ultimate ", "inflicts UNSPEAKABLE damage to", "!!"
     else:  #  -Rework- to use spell damage
        if damage < 1:
            return "", "misses", "."
        elif damage < 5:
            return "", "bruises", "."
        elif damage < 10:
            return "", "scrapes", "."
        elif damage < 15:
            return "", "scratches", "."
        elif damage < 20:
            return "", "lightly wounds", "."
        elif damage < 25:
            return "", "injures", "."
        elif damage < 30:
            return "", "harms", ", creating a bruise."
        elif damage < 35:
            return "", "thrashes", ", leaving marks!"
        elif damage < 40:
            return "", "decimates", ", the wound bleeds!"
        elif damage < 45:
            return "", "devastates", ", hitting organs!"
        elif damage < 50:
            return "", "mutilates", ", shredding flesh!"
        elif damage < 55:
            return "", "cripples", ", leaving GAPING holes!"
        elif damage < 60:
            return "", "DISEMBOWELS", ", guts spill out!"
        elif damage < 65:
            return "", "DISMEMBERS", ", blood sprays forth!"
        elif damage < 70:
            return "", "ANNIHILATES!", ", revealing bones!"
        elif damage < 75:
            return "", "OBLITERATES!", ", rending organs!"
        elif damage < 80:
            return "", "DESTROYS!!", ", shattering bones!"
        elif damage < 85:
            return "", "MASSACRES!!", ", gore splatters everywhere!"
        elif damage < 90:
            return "", "!DECAPITATES!", ", scrambling some brains!"
        elif damage < 95:
            return "", "!!SHATTERS!!", " into tiny pieces!"
        else:
            return "", "inflicts UNSPEAKABLE damage to", "!!"


def do_elemental(hitter, victim, element):
    if not victim:
        return
    if random.randint(0,10) > 5:
        return
    if "flaming" in element:
        victim.send("You are burned by " + hitter.get_name() + "'s flames.\n\r")
        hitter.send(victim.get_name() + " is burned by your flames.\n\r")
        _.send_to_room_except(victim.get_name() + "is burned by " + hitter.get_name() + "'s flames.\n\r",hitter.get_room(),[victim.peer, hitter.peer])
        victim.damage(2)
        _.affect_list["blind"].apply_affect(victim,1)
    if "shocking" in element:
        hitter.send("You shock them with your weapon, but it doesn't seem to have any effect.\n\r")
    if "demon" in element:
        victim.send("You are stricken by the damnation of " + hitter.get_name() + ".\n\r")
        hitter.send(victim.get_name() + " is struck down by hellfire.\n\r")
        _.send_to_room_except(victim.get_name() + "is struck down by the damnation of " + hitter.get_name() +
                              ".\n\r",hitter.get_room(),[victim.peer, hitter.peer])
        victim.damage(2)
        _.affect_list["curse"].apply_affect(victim,1)

def start_combat(hitter, victim):
    try:
        victim.remove_affect("sap")
    except ValueError:
        pass
    if hitter == victim:
        return
    if hitter.fighting is None:
        hitter.fighting = victim
        hitter.set_position(_.POS_FIGHTING)
    if victim.fighting is None:
        victim.fighting = hitter
        victim.set_position(_.POS_FIGHTING)


def do_damage(hitter, victim, damage, noun, magical):
    dam_adjective, dam_verb, dam_tag = get_damage_string(damage, magical)
    hitter.send("Your %s%s %s %%s%s (%s)\n\r" % (dam_adjective, noun, dam_verb,
                                                 dam_tag, damage), True, False, [victim, ])
    try:
        hitter.fighting.send("%s's %s%s %s you%s (%s)\n\r" % (hitter.get_name(victim).capitalize(),
                                                                                    dam_adjective, noun, dam_verb,
                                                                                    dam_tag, damage))
    except AttributeError:
        pass
    _.send_to_room_except("%%s's %s%s %s %%s%s (%s)\n\r" % (dam_adjective, noun,
                                                           dam_verb, dam_tag, damage)
                        , hitter.get_room(), [hitter.peer, victim.peer], [hitter, victim])
    victim.damage(damage)  # -Debug- only, should be victim.damage(damage)
    if victim.is_dead():
        victim.handle_death(hitter)
        hitter.handle_kill(victim)


def do_one_hit(mob):
    victim = mob.fighting
    if mob.has_peer():
        mob.peer.nervous_count = _.NERVOUS_TIMER
    if victim.has_peer():
        victim.peer.nervous_count = _.NERVOUS_TIMER
    temp_damage, temp_noun, element = mob.get_damage()
    do_damage(mob, victim, temp_damage, temp_noun, False)
    do_elemental(mob, mob.fighting, element)


def do_one_round(mob):
    if mob.fighting is not None:
        do_one_hit(mob)
    if mob.fighting is not None:
        do_one_hit(mob)
    if "thirdattack" in mob.get_skills():  # Might need a try/except KeyError
        if mob.fighting is not None:
            do_one_hit(mob)


def do_full_round():
    start_combat_block()
    for m in _.mobiles:
        if m.fighting is not None:
            do_one_round(m)
    end_combat_block()


def start_combat_block():
    _.block_send = True
    for p in _.peers:
        p.send_buffer = ""


def end_combat_block():
    for m in _.peers:
        if m.account.player.fighting is not None:
            m.peer_send(m.account.player.fighting.get_condition())

    _.block_send = False

    for p in _.peers:
        if p.send_buffer != "":
            _.send_buf_to_char(p)
            p.send_buffer = ""