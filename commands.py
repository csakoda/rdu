__author__ = 'ohell_000'


import globals as _
import random


def do_move(peer, direction):
    temp_new_room_vnum = peer.account.player.get_room().exits[direction]
    if temp_new_room_vnum is None:
        peer.account.player.send("You can't go that way.\n\r")
        return
    elif temp_new_room_vnum not in [x.vnum for x in _.rooms]:
        peer.account.player.send("Illegal room. Contact an immortal.\n\r")
        return

    dir_string = _.get_dir_string(direction)

    if "sneak" not in peer.account.player.get_skills():
        _.send_to_room_except("%s leaves %s.\n\r" % (peer.account.player.stats["name"], dir_string), peer.account.player.get_room(), [peer,])
    peer.account.player.stats["room"] = temp_new_room_vnum
    do_look(peer, "")
    if "sneak" not in peer.account.player.get_skills():
        _.send_to_room_except("%s has arrived.\n\r" % peer.account.player.stats["name"], peer.account.player.get_room(), [peer,])
    return


def do_north(peer, args):
    do_move(peer, _.DIR_NORTH)


def do_east(peer, args):
    do_move(peer, _.DIR_EAST)


def do_south(peer, args):
    do_move(peer, _.DIR_SOUTH)


def do_west(peer, args):
    do_move(peer, _.DIR_WEST)


def do_up(peer, args):
    do_move(peer, _.DIR_UP)


def do_down(peer, args):
    do_move(peer, _.DIR_DOWN)


def do_cgossip(peer, args):
    if args == "":
        peer.account.player.send("What do you want to cgossip?\n\r")
        return
    peer.account.player.send("{gYou cgossip '%s'{g\n\r" % args)
    _.send_to_all_except("{g%s cgossips '%s'{g\n\r" % (peer.account.player.stats["name"], args), [peer,])


def do_yell(peer, args):
    if args == "":
        peer.account.player.send("Yell what?\n\r")
        return
    peer.account.player.send("{RYou yell '%s'{x\n\r" % args)
    _.send_to_area_except("{R%s yells '%s'{x\n\r" % (peer.account.player.stats["name"], args), peer.account.player.get_area(), [peer,])


def do_say(peer, args):
    if args == "":
        peer.account.player.send("What do you want to say?\n\r")
        return
    peer.account.player.send("{yYou say '%s'{x\n\r" % args)
    _.send_to_room_except("{y%s says '%s'{x\n\r" % (peer.account.player.stats["name"], args), peer.account.player.get_room(),[peer,])


def do_tell(peer, args):
    import player

    try:
        target = args.split()[0]
    except IndexError:
        peer.account.player.send("Who do you want to tell?\n\r")
        return
    target_player = player.get_player(target)
    if target_player is None:
        peer.account.player.send("You can't find them.\n\r")
        return
    try:
        message = args.split()[1]
    except IndexError:
        peer.account.player.send("What do you want to tell them?\n\r")
        return
    peer.account.player.send("{mYou tell %s '{y%s{m'{x\n\r" % (target_player.get_name(), message))
    target_player.send("{m%s tells you '{y%s'{m\n\r" % (peer.account.player.get_name(), message))


def do_emote(peer, args):
    _.send_to_room("%s %s\n\r" % (peer.account.player.stats["name"], args), peer.account.player.get_room())


def do_who(peer, args):
    buf = ""
    for c in _.peers:
        if c.game_state == _.STATE_ONLINE:
            buf += "[51 %-7s %7s] [  Loner ] %s%s %s\n\r" % ( c.account.player.stats["race"].capitalize(), \
                c.account.player.stats["class"].capitalize(), "<LINKDEAD> " if c.linkdead else "", \
                c.account.player.stats["name"], c)
    peer.account.player.send(buf)


def do_where(peer, args):
    found = False
    myarea = peer.account.player.get_area()
    buf = "Area: " + myarea.name + "\n\rPlayers near you:\n\r"
    for c in _.peers:
        buf += "%s  %s\n\r" % (c.account.player.stats["name"], c.account.player.get_room().get_name())
        found = True
    if not found:
        buf += "None\n\r"
    peer.account.player.send(buf)


def do_score(peer, args):
    buf = ""
    temp_player = peer.account.player

    buf += temp_player.get_name() + "\n\r"
    buf += "---------------------------------- Info ---------------------------------\n\r"
    buf += "Race: %-15s Class: %-15s\n\r" % (temp_player.stats["race"], temp_player.stats["class"])
    buf += "---------------------------------- Stats --------------------------------\n\r"
    buf += "Hp: %s of %s\n\r" % (temp_player.get_hp(), temp_player.get_max_hp())
    buf += "Str: %2s of %2s     Con: %2s of %2s\n\r" % (temp_player.get_stat("str"), temp_player.get_max_stat("str"),
                                                        temp_player.get_stat("con"), temp_player.get_max_stat("con"))
    buf += "Int: %2s of %2s     Wis: %2s of %2s\n\r" % (temp_player.get_stat("int"), temp_player.get_max_stat("int"),
                                                        temp_player.get_stat("wis"), temp_player.get_max_stat("wis"))
    buf += "Dex: %2s of %2s\n\r" % (temp_player.get_stat("dex"), temp_player.get_max_stat("dex"))
    buf += "Hitroll: %s Damroll: %s\n\r" % (temp_player.get_hitroll(), temp_player.get_damroll())
    buf += "Gold: " + str(int(temp_player.get_wealth() / 100)) + " Silver: " + str(temp_player.get_wealth() % 100) + "\n\r"

    peer.account.player.send(buf)


def do_commands(peer, args):
    peer.account.player.send(str(_.command_list_sorted) + "\n\r")


def do_skills(peer, args):
    buf = str(peer.account.player.get_skills()) + "\n\r"
    peer.account.player.send(buf)


def do_spells(peer, args):
    buf = str(peer.account.player.get_spells()) + "\n\r"
    peer.account.player.send(buf)

def do_prompt(peer, args):
    if len(args) < 1:
        buf = "\n\rPrompt options:\n\r\n\r"
        buf += " %h     current hp\n\r"
        buf += " %H     maximum hp\n\r"
        buf += " %m     current mana\n\r"
        buf += " %M     maximum mana\n\r"
        buf += " %v     current moves\n\r"
        buf += " %V     maximum moves\n\r"
        buf += " %a     current area\n\r"
        buf += " %r     current room\n\r"
        buf += " %n     newline\n\r"
        
        temp_prompt = peer.account.player.get_raw_prompt()
        temp_prompt = temp_prompt.replace("%%", "%")
        temp_prompt = temp_prompt.replace("{", "{{")
        buf += "\n\rCurrent prompt is:\n\r" + temp_prompt +"\n\r"
        peer.account.player.send(buf)
        return
    peer.account.player.stats["prompt"] = args.replace("%", "%%")
    peer.account.player.send("Prompt set.\n\r")

def do_look(peer, args):
    temp_room = peer.account.player.get_room()

    if not peer.account.player.can_see(None):
        peer.account.player.send("You can't see anything!\n\r")
        return

    #TODO: Look NORTH

    #Look AT something or someone
    if not args is None and not args is "":
        import mobile
        target = args.split()[0]

        #check mobiles
        temp_target = mobile.get_mobile_in_room(target, temp_room)

        if temp_target:
            peer.account.player.send(temp_target.stats['desc'] + "\n\r")

        else:
            import item
            temp_target = item.get_item_in_room(temp_room, target)

            if temp_target:
                peer.account.player.send(temp_target.stats['desc'] + "\n\r")
            elif item.get_item_in_inventory(peer, target):
                peer.account.player.send(item.get_item_in_inventory(peer, target).stats['desc'] + "\n\r")
            else:
                peer.account.player.send("They aren't here.\n\r")

    else:
        peer.account.player.send(temp_room.display(peer))


def do_peer(peer, args):
    import room
    if len(args) < 1:
        peer.account.player.send("Peer in which direction?")
        return
    direction = _.get_dir_constant(args.split()[0])
    
    temp_room = peer.account.player.get_room()
    temp_new_room_vnum = temp_room.exits[direction]
    if temp_new_room_vnum is None:
        peer.account.player.send("There's nothing in that direction.")
        return
    elif temp_new_room_vnum not in [x.vnum for x in _.rooms]:
        peer.account.player.send("Illegal room. Contact an immortal.\n\r")
        return
    peer.account.player.send("You peer intensely and see...\n\r\n\r" + room.get_room(temp_new_room_vnum).display(peer));
    

def do_color(peer, args):
    temp_color = 1 - peer.account.player.get_color()
    peer.account.player.stats["color"] = temp_color
    if temp_color == 1:
        peer.account.player.send("Color is {rON{x now, cool!\n\r")
    else:
        peer.account.player.send("Color is off now. Sigh.")

def do_quit(peer, args):  # -Rework- to avoid quitting while nervous
    if peer.nervous_count > 0:
        peer.account.player.send("You are too excited to quit!\n\r")
        return
    peer.account.player.save()
    peer.account.player.send("Alas, all good things must come to an end.\n\r")
    peer.quit()
    peer.game_state = _.STATE_QUIT


def do_qui(peer, args):
    peer.account.player.send("If you want to QUIT, you'll have to spell it out.\n\r")


def do_shutdown(peer, args):
    peer.account.player.send("whyudoah\n\r")
    
    
def do_shutdow(peer, args):
    peer.account.player.send("If you want to SHUTDOWN, you'll have to spell it out.\n\r")

def do_get(peer, args):
    import item

    temp_room = peer.account.player.get_room()
    try:
        target = args.split()[0]
    except IndexError:
        peer.account.player.send("Get what?\n\r")
        return
    if len(peer.account.player.inventory) >= _.MAX_CARRY:
        peer.account.player.send("You can't carry any more.\n\r")
        return
    temp_item = item.get_item_in_room(temp_room, target)
    if temp_item is None:
        peer.account.player.send("You don't see that here.\n\r")
        return
    peer.account.player.send("You get %s.\n\r" % temp_item.get_name())
    _.send_to_room_except("%s gets %s.\n\r" % (peer.account.player.get_name(), temp_item.get_name()), peer.account.player.get_room(), [peer,])
    temp_room.remove_item(temp_item)
    peer.account.player.add_item(temp_item)


def do_wear(peer, args):
    import item

    try:
        target = args.split()[0]
    except IndexError:
        peer.account.player.send("Wear what?\n\r")
        return
    if len(peer.account.player.inventory) == 0:
        peer.account.player.send("You're not carrying that.\n\r")
        return
    temp_item = item.get_item_in_inventory(peer, target)
    if temp_item is None:
        peer.account.player.send("You're not carrying that.\n\r")
        return
    peer.account.player.wear_armor(temp_item)


def do_inventory(peer, args):
    buf = "You are carrying:\n\r"
    if len(peer.account.player.inventory) == 0:
        peer.account.player.send(buf + "Nothing.\n\r")
        return
    for i in peer.account.player.inventory:
        buf += "   " + i.get_name() + "\n\r"
    buf += "\n\r"
    peer.account.player.send(buf)


def do_equipment(peer, args):
    buf = "You are using:\n\r"
    buf += "<used as light> %s\n\r" % (peer.account.player.equipment[_.WEAR_LIGHT].get_name() \
       if peer.account.player.equipment[_.WEAR_LIGHT] is not None else "Nothing")
    buf += "<worn on finger> %s\n\r" % (peer.account.player.equipment[_.WEAR_FINGER].get_name() \
       if peer.account.player.equipment[_.WEAR_FINGER] is not None else "Nothing")
    buf += "<worn on finger> %s\n\r" % (peer.account.player.equipment[_.WEAR_FINGER2].get_name() \
       if peer.account.player.equipment[_.WEAR_FINGER2] is not None else "Nothing")
    buf += "<worn around neck> %s\n\r" % (peer.account.player.equipment[_.WEAR_NECK].get_name() \
       if peer.account.player.equipment[_.WEAR_NECK] is not None else "Nothing")
    buf += "<worn around neck> %s\n\r" % (peer.account.player.equipment[_.WEAR_NECK2].get_name() \
       if peer.account.player.equipment[_.WEAR_NECK2] is not None else "Nothing")
    buf += "<worn on torso> %s\n\r" % (peer.account.player.equipment[_.WEAR_TORSO].get_name() \
       if peer.account.player.equipment[_.WEAR_TORSO] is not None else "Nothing")
    buf += "<worn on head> %s\n\r" % (peer.account.player.equipment[_.WEAR_HEAD].get_name() \
       if peer.account.player.equipment[_.WEAR_HEAD] is not None else "Nothing")
    buf += "<worn on legs> %s\n\r" % (peer.account.player.equipment[_.WEAR_LEGS].get_name() \
       if peer.account.player.equipment[_.WEAR_LEGS] is not None else "Nothing")
    buf += "<worn on feet> %s\n\r" % (peer.account.player.equipment[_.WEAR_FEET].get_name() \
       if peer.account.player.equipment[_.WEAR_FEET] is not None else "Nothing")
    buf += "<worn on hands> %s\n\r" % (peer.account.player.equipment[_.WEAR_HAND].get_name() \
       if peer.account.player.equipment[_.WEAR_HAND] is not None else "Nothing")
    buf += "<worn on arms> %s\n\r" % (peer.account.player.equipment[_.WEAR_ARMS].get_name() \
       if peer.account.player.equipment[_.WEAR_ARMS] is not None else "Nothing")
    buf += "<worn as shield> %s\n\r" % (peer.account.player.equipment[_.WEAR_OFFHAND].get_name() \
       if peer.account.player.equipment[_.WEAR_OFFHAND] is not None else "Nothing")
    buf += "<worn about body> %s\n\r" % (peer.account.player.equipment[_.WEAR_BODY].get_name() \
       if peer.account.player.equipment[_.WEAR_BODY] is not None else "Nothing")
    buf += "<worn about waist> %s\n\r" % (peer.account.player.equipment[_.WEAR_WAIST].get_name() \
       if peer.account.player.equipment[_.WEAR_WAIST] is not None else "Nothing")
    buf += "<worn around wrist> %s\n\r" % (peer.account.player.equipment[_.WEAR_WRIST].get_name() \
       if peer.account.player.equipment[_.WEAR_WRIST] is not None else "Nothing")
    buf += "<worn around wrist> %s\n\r" % (peer.account.player.equipment[_.WEAR_WRIST2].get_name() \
       if peer.account.player.equipment[_.WEAR_WRIST2] is not None else "Nothing")
    buf += "<wielded> %s\n\r" % (peer.account.player.equipment[_.WEAR_WEAPON].get_name() \
       if peer.account.player.equipment[_.WEAR_WEAPON] is not None else "Nothing")
    buf += "<held> %s\n\r" % (peer.account.player.equipment[_.WEAR_HELD].get_name() \
       if peer.account.player.equipment[_.WEAR_HELD] is not None else "Nothing")
    buf += "<floating nearby> %s\n\r" % (peer.account.player.equipment[_.WEAR_FLOAT].get_name() \
       if peer.account.player.equipment[_.WEAR_FLOAT] is not None else "Nothing")
    buf += "<orbiting nearby> %s\n\r" % (peer.account.player.equipment[_.WEAR_FLOAT2].get_name() \
       if peer.account.player.equipment[_.WEAR_FLOAT2] is not None else "Nothing")

    peer.account.player.send(buf)


def do_affects(peer, args):
    buf = "You are affected by the following:\n\r"
    if not peer.account.player.affects:
        buf += "None\n\r"
    else:
        for a in peer.account.player.affects:
            buf += "%s: %s for %s rounds\n\r" % (a.name, a.desc, int(a.duration / 4))
    buf += "\n\r"
    peer.account.player.send(buf)


def do_drop(peer, args):
    import item

    try:
        target = args.split()[0]
    except IndexError:
        peer.account.player.send("Drop what?\n\r")
        return
    try:
        temp_item = item.get_item_in_inventory(peer, target)
        peer.account.player.send("You drop %s.\n\r" % temp_item.get_name())
        _.send_to_room_except("%s drops %s.\n\r" % (peer.account.player.get_name(), temp_item.get_name()), peer.account.player.get_room(), [peer,])
        peer.account.player.get_room().add_item(temp_item)
        peer.account.player.remove_item(temp_item)
    except AttributeError:
        peer.account.player.send("You're not carrying that.\n\r")


def do_remove(peer, args):
    import item

    try:
        target = args.split()[0]
    except IndexError:
        peer.account.player.send("Remove what?\n\r")
        return
    try:
        temp_slot = item.get_item_slot_in_equipment(peer, target)
        peer.account.player.send("You stop using %s.\n\r" % peer.account.player.equipment[temp_slot].get_name())
        _.send_to_room_except("%s stops using %s.\n\r" % (peer.account.player.get_name(), peer.account.player.equipment[temp_slot].get_name()), \
                              peer.account.player.get_room(), [peer,])
        peer.account.player.add_item(peer.account.player.equipment[temp_slot])
        peer.account.player.equipment[temp_slot] = None
    except KeyError:
        peer.account.player.send("You're not wearing that.\n\r")


def do_kill(peer, args):
    import mobile
    import combat

    if peer.account.player.fighting is not None:
        peer.account.player.send("You are already fighting!\n\r")
        return
    try:
        target = args.split()[0]
    except IndexError:
        peer.account.player.send("Kill whom?\n\r")
        return
    temp_target = mobile.get_mobile_in_room(target, peer.account.player.get_room())
    if temp_target is None:
        peer.account.player.send("They aren't here.\n\r")
        return
    elif temp_target == peer.account.player:
        peer.account.player.send("Suicide is a mortal sin.\n\r")
        return
    combat.start_combat(peer.account.player, temp_target)
    temp_vector = temp_target.peer
    combat.start_combat_block()
    if temp_vector is not None:
        do_yell(temp_vector, "Help! I am being attacked by %s!" % peer.account.player.get_name())
    combat.do_one_round(peer.account.player)
    combat.end_combat_block()


def do_flee(peer, args):
    import combat
    if peer.account.player.fighting is None:
        peer.account.player.send("You aren't fighting anyone.\n\r")
        return
    if peer.account.player.get_room().random_exit() is None or random.randint(0,4) == 0:
        peer.account.player.send("PANIC! You couldn't escape!\n\r")
        return
    else:
        combat.start_combat_block()
        peer.account.player.send("You flee from combat!\n\r")  #  -Rework- to make you flee out of the room
        _.send_to_room_except("%s has fled!\n\r" % peer.account.player.get_name(), peer.account.player.get_room(), [peer,])
        peer.account.player.remove_from_combat()
        do_move(peer, peer.account.player.get_room().random_exit())
        combat.end_combat_block()


def do_sleep(peer, args):
    temp_position = peer.account.player.get_position()
    if temp_position == _.POS_SLEEPING:
        peer.account.player.send("You're already asleep!\n\r")
    elif temp_position == _.POS_RESTING or temp_position == _.POS_STANDING:
        peer.account.player.send("You go to sleep.\n\r")
        _.send_to_room_except("%s goes to sleep.\n\r" % peer.account.player.get_name(), peer.account.player.get_room(), [peer,])
        peer.account.player.set_position(_.POS_SLEEPING)
    elif temp_position == _.POS_FIGHTING:
        peer.account.player.send("You are still fighting!\n\r")


def do_stand(peer, args):
    temp_position = peer.account.player.get_position()
    if temp_position == _.POS_SLEEPING:
        peer.account.player.send("You wake and stand up.\n\r")
        _.send_to_room_except("%s wakes and stands up.\n\r" % peer.account.player.get_name(), peer.account.player.get_room(), [peer,])
        peer.account.player.set_position(_.POS_STANDING)
    elif temp_position == _.POS_RESTING:
        peer.account.player.send("You stand up.\n\r")
        _.send_to_room_except("%s stands up.\n\r" % peer.account.player.get_name(), peer.account.player.get_room(), [peer,])
        peer.account.player.set_position(_.POS_STANDING)
    elif temp_position == _.POS_FIGHTING or temp_position == _.POS_STANDING:
        peer.account.player.send("You are already standing.\n\r")


def do_wake(peer, args):
    import mobile
    temp_target = peer.account.player
    if len(args.split()) > 0:
        temp_target = mobile.get_mobile_in_room(args.split()[0], peer.account.player.get_room())
    if temp_target is None:
        peer.account.player.send("They aren't here.\n\r")
        return
    temp_position = temp_target.get_position()
    if temp_target.affected_by(_.affect_list["sap"]):
        if temp_target is peer.account.player:
            peer.account.player.send("You can't wake up!\n\r")
        else:
            peer.account.player.send("They won't wake up!\n\r")
        return
    temp_vector = temp_target.peer
    if temp_position == _.POS_SLEEPING:
        temp_vector.peer_send("You wake and stand up.\n\r", False)
        _.send_to_room_except("%s wakes and stands up.\n\r" % temp_target.get_name(), temp_target.get_room(), [temp_vector,])
        temp_target.set_position(_.POS_STANDING)
        do_look(temp_vector, "")
    elif temp_position == _.POS_RESTING and temp_target is peer.account.player:
        temp_vector.peer_send("You stand up.\n\r")
        _.send_to_room_except("%s stands up.\n\r" % temp_target.get_name(), temp_target.get_room(), [temp_vector,])
        temp_target.set_position(_.POS_STANDING)
    else:
        if temp_target is peer.account.player:
            peer.account.player.send("You aren't sleeping.\n\r")
        else:
            peer.account.player.send("They aren't sleeping.\n\r")


def do_rest(peer, args):
    temp_position = peer.account.player.get_position()
    if temp_position == _.POS_SLEEPING:
        peer.account.player.send("You wake up and start resting.\n\r", False)
        _.send_to_room_except("%s wakes up and starts resting.\n\r" % peer.account.player.get_name(), peer.account.player.get_room(),
                              [peer,])
        peer.account.player.set_position(_.POS_RESTING)
        do_look(peer, "")
    elif temp_position == _.POS_RESTING:
        peer.account.player.send("You are already resting.\n\r")
    elif temp_position == _.POS_STANDING:
        peer.account.player.send("You rest.\n\r")
        _.send_to_room_except("%s rests.\n\r" % peer.account.player.get_name(), peer.account.player.get_room(),
                              [peer,])
        peer.account.player.set_position(_.POS_RESTING)
    elif temp_position == _.POS_STANDING:
        peer.account.player.send("You are still fighting!\n\r")


def do_cast(peer, args):
    try:
        spell_name = args.split()[0]
    except IndexError:
        peer.account.player.send("What spell do you want to cast?\n\r")
        return
    for s in _.spell_list_sorted:
        if s not in peer.account.player.get_spells():
            continue
        if len(s) >= len(spell_name):
            if spell_name == s[:len(spell_name)]:
                _.spell_list[s].execute_spell(peer, "".join(args.split()[1:]))
                break
    else:
        peer.account.player.send("You don't know any spells by that name.\n\r")


def do_debug(peer, args):
    import inspect
    import player

    args = args.split(" ")
    if "peers" in args:
        print(str(_.peers))
    if "mobiles" in args:
        print(str(_.mobiles))


class Command():
    def __init__(self, function, position, lag, in_combat=True):
        self.function = function
        self.position = position
        self.lag = lag
        self.in_combat = in_combat

    def execute_command(self, peer, args):
        if peer.account.player.get_position() == _.POS_FIGHTING and not self.in_combat:
            peer.account.player.send("No way! You are already fighting!\n\r")
            return
        if peer.account.player.get_position() < self.position:
            if peer.account.player.get_position() == _.POS_SLEEPING:
                peer.account.player.send("You can't do that, you're sleeping!\n\r")
            elif peer.account.player.get_position() == _.POS_RESTING:
                peer.account.player.send("Nah...you're too relaxed.\n\r")
            elif peer.account.player.get_position() == _.POS_STANDING:
                peer.account.player.send("You aren't fighting anyone.\n\r")
            return
        self.function(peer, args)
        peer.account.player.add_lag(self.lag)


def initialize_commands():
    #  Movement
    _.command_list["north"] = Command(do_north, _.POS_STANDING, 0, False)
    _.command_list["east"] = Command(do_east, _.POS_STANDING, 0, False)
    _.command_list["south"] = Command(do_south, _.POS_STANDING, 0, False)
    _.command_list["west"] = Command(do_west, _.POS_STANDING, 0, False)
    _.command_list["up"] = Command(do_up, _.POS_STANDING, 0, False)
    _.command_list["down"] = Command(do_down, _.POS_STANDING, 0, False)
    _.command_list["n"] = Command(do_north, _.POS_STANDING, 0, False)
    _.command_list["e"] = Command(do_east, _.POS_STANDING, 0, False)
    _.command_list["s"] = Command(do_south, _.POS_STANDING, 0, False)
    _.command_list["w"] = Command(do_west, _.POS_STANDING, 0, False)
    _.command_list["u"] = Command(do_up, _.POS_STANDING, 0, False)
    _.command_list["d"] = Command(do_down, _.POS_STANDING, 0, False)
    #  Communication
    _.command_list["cgossip"] = Command(do_cgossip, _.POS_SLEEPING, 0)
    _.command_list["say"] = Command(do_say, _.POS_RESTING, 0)
    _.command_list["emote"] = Command(do_emote, _.POS_RESTING, 0)
    _.command_list["tell"] = Command(do_tell, _.POS_RESTING, 0)
    _.command_list["yell"] = Command(do_yell, _.POS_RESTING, 0)
    #  Info
    _.command_list["where"] = Command(do_where, _.POS_RESTING, 0)
    _.command_list["who"] = Command(do_who, _.POS_SLEEPING, 0)
    _.command_list["wh"] = Command(do_who, _.POS_SLEEPING, 0)
    _.command_list["commands"] = Command(do_commands, _.POS_SLEEPING, 0)
    _.command_list["look"] = Command(do_look, _.POS_RESTING, 0)
    _.command_list["peer"] = Command(do_peer, _.POS_RESTING, 0)
    _.command_list["inventory"] = Command(do_inventory, _.POS_SLEEPING, 0)
    _.command_list["affects"] = Command(do_affects, _.POS_SLEEPING, 0)
    _.command_list["equipment"] = Command(do_equipment, _.POS_SLEEPING, 0)
    _.command_list["score"] = Command(do_score, _.POS_SLEEPING, 0)
    _.command_list["skills"] = Command(do_skills, _.POS_SLEEPING, 0)
    _.command_list["spells"] = Command(do_spells, _.POS_SLEEPING, 0)
    _.command_list["prompt"] = Command(do_prompt, _.POS_SLEEPING, 0)
    #  Items
    _.command_list["get"] = Command(do_get, _.POS_RESTING, 0)
    _.command_list["take"] = Command(do_get, _.POS_RESTING, 0)
    _.command_list["drop"] = Command(do_drop, _.POS_RESTING, 0)
    _.command_list["wear"] = Command(do_wear, _.POS_RESTING, 0)
    _.command_list["remove"] = Command(do_remove, _.POS_RESTING, 0)
    #  Combat
    _.command_list["kill"] = Command(do_kill, _.POS_STANDING, 0, False)
    _.command_list["flee"] = Command(do_flee, _.POS_FIGHTING, 0)
    _.command_list["cast"] = Command(do_cast, _.POS_STANDING, 0)
    #  Misc
    _.command_list["color"] = Command(do_color, _.POS_SLEEPING, 0)
    _.command_list["quit"] = Command(do_quit, _.POS_SLEEPING, 0, False)
    _.command_list["qui"] = Command(do_qui, _.POS_SLEEPING, 0, False)
    _.command_list["shutdown"] = Command(do_shutdown, _.POS_SLEEPING, 0)
    _.command_list["shutdow"] = Command(do_shutdow, _.POS_SLEEPING, 0)
    #  Position
    _.command_list["stand"] = Command(do_stand, _.POS_SLEEPING, 0)
    _.command_list["wake"] = Command(do_wake, _.POS_SLEEPING, 0)
    _.command_list["rest"] = Command(do_rest, _.POS_SLEEPING, 0, False)
    _.command_list["sleep"] = Command(do_sleep, _.POS_SLEEPING, 0, False)

    #  Debug
    _.command_list["debug"] = Command(do_debug, _.POS_SLEEPING, 0, False)

    #  Populate sorted list
    _.command_list_sorted = sorted(_.command_list)