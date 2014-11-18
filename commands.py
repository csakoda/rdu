__author__ = 'ohell_000'


import globals as _
import random


def do_move(char, direction):
    temp_new_room_vnum = char.player.get_room().exits[direction]
    if temp_new_room_vnum is None:
        _.send_to_char(char, "You can't go that way.\n\r")
        return
    elif temp_new_room_vnum not in [x.vnum for x in _.rooms]:
        _.send_to_char(char, "Illegal room. Contact an immortal.\n\r")
        return

    dir_string = _.get_dir_string(direction)

    if "sneak" not in char.player.get_skills():
        _.send_to_room_except("%s leaves %s.\n\r" % (char.player.stats["name"], dir_string), char.player.get_room(), [char,])
    char.player.stats["room"] = temp_new_room_vnum
    do_look(char, "")
    if "sneak" not in char.player.get_skills():
        _.send_to_room_except("%s has arrived.\n\r" % char.player.stats["name"], char.player.get_room(), [char,])
    return


def do_north(char, args):
    do_move(char, _.DIR_NORTH)


def do_east(char, args):
    do_move(char, _.DIR_EAST)


def do_south(char, args):
    do_move(char, _.DIR_SOUTH)


def do_west(char, args):
    do_move(char, _.DIR_WEST)


def do_up(char, args):
    do_move(char, _.DIR_UP)


def do_down(char, args):
    do_move(char, _.DIR_DOWN)


def do_cgossip(char, args):
    if args == "":
        _.send_to_char(char, "What do you want to cgossip?\n\r")
        return
    _.send_to_char(char, "You cgossip '%s'\n\r" % args)
    _.send_to_all_except("%s cgossips '%s'\n\r" % (char.player.stats["name"], args), [char,])


def do_yell(char, args):
    if args == "":
        _.send_to_char(char, "Yell what?\n\r")
        return
    _.send_to_char(char, "You yell '%s'\n\r" % args)
    _.send_to_area_except("%s yells '%s'\n\r" % (char.player.stats["name"], args), char.player.get_area(), [char,])


def do_say(char, args):
    if args == "":
        _.send_to_char(char, "What do you want to say?\n\r")
        return
    _.send_to_char(char, "You say '%s'\n\r" % args)
    _.send_to_room_except("%s says '%s'\n\r" % (char.player.stats["name"], args), char.player.get_room(),[char,])


def do_tell(char, args):
    import player

    try:
        target = args.split()[0]
    except IndexError:
        _.send_to_char(char, "Who do you want to tell?\n\r")
        return
    target_player = player.get_player(target)
    if target_player is None:
        _.send_to_char(char, "You can't find them.\n\r")
        return
    try:
        message = args.split()[1]
    except IndexError:
        _.send_to_char(char, "What do you want to tell them?\n\r")
        return
    _.send_to_char(char, "You tell %s '%s'\n\r" % (target_player.get_name(), message))
    _.send_to_char(target_player.get_peer(), "%s tells you '%s'\n\r" % (char.player.get_name(), message))


def do_emote(char, args):
    _.send_to_room("%s %s\n\r" % (char.player.stats["name"], args), char.player.get_room())


def do_who(char, args):
    buf = ""
    for c in _.peers:
        if c.state == _.STATE_ONLINE:
            buf += "[51 %-7s %7s] [  Loner ] %s%s %s\n\r" % ( c.player.stats["race"].capitalize(), \
                c.player.stats["class"].capitalize(), "<LINKDEAD> " if c.linkdead else "", \
                c.player.stats["name"], c)
    _.send_to_char(char, buf)


def do_where(char, args):
    found = False
    myarea = char.player.get_area()
    buf = "Area: " + myarea.name + "\n\rPlayers near you:\n\r"
    for c in _.peers:
        buf += "%s  %s\n\r" % (c.player.stats["name"], c.player.get_room().get_name())
        found = True
    if not found:
        buf += "None\n\r"
    _.send_to_char(char, buf)


def do_score(char, args):
    buf = ""
    temp_player = char.player

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

    _.send_to_char(char, buf)


def do_commands(char, args):
    _.send_to_char(char, str(_.command_list_sorted) + "\n\r")


def do_skills(char, args):
    buf = str(char.player.get_skills()) + "\n\r"
    _.send_to_char(char, buf)


def do_spells(char, args):
    buf = str(char.player.get_spells()) + "\n\r"
    _.send_to_char(char, buf)


def do_look(char, args):
    temp_room = char.player.get_room()

    if not char.player.can_see(None):
        _.send_to_char(char, "You can't see anything!\n\r")
        return

    #TODO: Look NORTH

    #Look AT something or someone
    if not args is None and not args is "":
        import mobile
        target = args.split()[0]

        #check mobiles
        temp_target = mobile.get_mobile_in_room(target, temp_room)

        if temp_target:
            _.send_to_char(char, temp_target.stats['desc'] + "\n\r")

        else:
            import item
            temp_target = item.get_item_in_room(temp_room, target)

            if temp_target:
                _.send_to_char(char, temp_target.stats['desc'] + "\n\r")
            elif item.get_item_in_inventory(char, target):
                _.send_to_char(char, item.get_item_in_inventory(char, target).stats['desc'] + "\n\r")
            else:
                _.send_to_char(char, "They aren't here.\n\r")

    else:
        #  Name and description
        buf = temp_room.get_name() + "\n\r\n\r"\
        + temp_room.get_desc() + "\n\r\n\rExits: [ "

        #  Exits
        noexit = True  # -Rework-
        for d in [x for x in sorted(temp_room.exits) if temp_room.exits[x] is not None]:
            buf += _.get_dir_string(d) + " "
            noexit = False

        if noexit:
            buf += "none "

        buf += "]\n\r\n\r"

        #  Items

        for r in temp_room.items:
            buf += "%s\n\r" % r.get_desc()
        if len(temp_room.items) > 0:
            buf += "\n\r"

        #  Characters

        other_players = [c.player for c in _.peers if c is not char and c.player.get_room() == char.player.get_room()
                                               and not c.linkdead and c.state == _.STATE_ONLINE]
        other_mobs = [m for m in _.mobiles if m.get_peer() is None and m.get_room() == char.player.get_room()]
        others = other_mobs + other_players

        for c in others:
            pos_string = ""
            pos_tag = ""
            if c.get_position() == _.POS_FIGHTING:
                pos_tag = ", fighting %s" % c.fighting.get_name() if c.fighting is not None else "null"
            elif c.get_position() == _.POS_RESTING:
                pos_string = "resting "
            elif c.get_position() == _.POS_SLEEPING:
                pos_string = "sleeping "
            buf += "%s%s is %shere%s.\n\r" % ("<LINKDEAD> " if c.get_peer() is not None and c.get_peer().linkdead else "",
                                              c.stats["name"].capitalize(), pos_string, pos_tag)
        if len(others) > 0:
            buf += "\n\r"

        _.send_to_char(char, buf)


def do_quit(char, args):  # -Rework- to avoid quitting while nervous
    from admin import save_char
    if char.nervous_count > 0:
        _.send_to_char(char, "You are too excited to quit!\n\r")
        return
    save_char(char)
    _.send_to_char(char, "Alas, all good things must come to an end.\n\r")
    char.quit()
    char.state = _.STATE_QUIT


def do_get(char, args):
    import item

    temp_room = char.player.get_room()
    try:
        target = args.split()[0]
    except IndexError:
        _.send_to_char(char, "Get what?\n\r")
        return
    if len(char.player.inventory) >= _.MAX_CARRY:
        _.send_to_char(char, "You can't carry any more.\n\r")
        return
    temp_item = item.get_item_in_room(temp_room, target)
    if temp_item is None:
        _.send_to_char(char, "You don't see that here.\n\r")
        return
    _.send_to_char(char, "You get %s.\n\r" % temp_item.get_name())
    _.send_to_room_except("%s gets %s.\n\r" % (char.player.get_name(), temp_item.get_name()), char.player.get_room(), [char,])
    temp_room.remove_item(temp_item)
    char.player.add_item(temp_item)


def do_wear(char, args):
    import item

    try:
        target = args.split()[0]
    except IndexError:
        _.send_to_char(char, "Wear what?\n\r")
        return
    if len(char.player.inventory) == 0:
        _.send_to_char(char, "You're not carrying that.\n\r")
        return
    temp_item = item.get_item_in_inventory(char, target)
    if temp_item is None:
        _.send_to_char(char, "You're not carrying that.\n\r")
        return
    char.player.wear_armor(temp_item)


def do_inventory(char, args):
    buf = "You are carrying:\n\r"
    if len(char.player.inventory) == 0:
        _.send_to_char(char, buf + "Nothing.\n\r")
        return
    for i in char.player.inventory:
        buf += "   " + i.get_name() + "\n\r"
    buf += "\n\r"
    _.send_to_char(char, buf)


def do_equipment(char, args):
    buf = "You are using:\n\r"
    buf += "<used as light> %s\n\r" % (char.player.equipment[_.WEAR_LIGHT].get_name() \
       if char.player.equipment[_.WEAR_LIGHT] is not None else "Nothing")
    buf += "<worn on finger> %s\n\r" % (char.player.equipment[_.WEAR_FINGER].get_name() \
       if char.player.equipment[_.WEAR_FINGER] is not None else "Nothing")
    buf += "<worn on finger> %s\n\r" % (char.player.equipment[_.WEAR_FINGER2].get_name() \
       if char.player.equipment[_.WEAR_FINGER2] is not None else "Nothing")
    buf += "<worn around neck> %s\n\r" % (char.player.equipment[_.WEAR_NECK].get_name() \
       if char.player.equipment[_.WEAR_NECK] is not None else "Nothing")
    buf += "<worn around neck> %s\n\r" % (char.player.equipment[_.WEAR_NECK2].get_name() \
       if char.player.equipment[_.WEAR_NECK2] is not None else "Nothing")
    buf += "<worn on torso> %s\n\r" % (char.player.equipment[_.WEAR_TORSO].get_name() \
       if char.player.equipment[_.WEAR_TORSO] is not None else "Nothing")
    buf += "<worn on head> %s\n\r" % (char.player.equipment[_.WEAR_HEAD].get_name() \
       if char.player.equipment[_.WEAR_HEAD] is not None else "Nothing")
    buf += "<worn on legs> %s\n\r" % (char.player.equipment[_.WEAR_LEGS].get_name() \
       if char.player.equipment[_.WEAR_LEGS] is not None else "Nothing")
    buf += "<worn on feet> %s\n\r" % (char.player.equipment[_.WEAR_FEET].get_name() \
       if char.player.equipment[_.WEAR_FEET] is not None else "Nothing")
    buf += "<worn on hands> %s\n\r" % (char.player.equipment[_.WEAR_HAND].get_name() \
       if char.player.equipment[_.WEAR_HAND] is not None else "Nothing")
    buf += "<worn on arms> %s\n\r" % (char.player.equipment[_.WEAR_ARMS].get_name() \
       if char.player.equipment[_.WEAR_ARMS] is not None else "Nothing")
    buf += "<worn as shield> %s\n\r" % (char.player.equipment[_.WEAR_OFFHAND].get_name() \
       if char.player.equipment[_.WEAR_OFFHAND] is not None else "Nothing")
    buf += "<worn about body> %s\n\r" % (char.player.equipment[_.WEAR_BODY].get_name() \
       if char.player.equipment[_.WEAR_BODY] is not None else "Nothing")
    buf += "<worn about waist> %s\n\r" % (char.player.equipment[_.WEAR_WAIST].get_name() \
       if char.player.equipment[_.WEAR_WAIST] is not None else "Nothing")
    buf += "<worn around wrist> %s\n\r" % (char.player.equipment[_.WEAR_WRIST].get_name() \
       if char.player.equipment[_.WEAR_WRIST] is not None else "Nothing")
    buf += "<worn around wrist> %s\n\r" % (char.player.equipment[_.WEAR_WRIST2].get_name() \
       if char.player.equipment[_.WEAR_WRIST2] is not None else "Nothing")
    buf += "<wielded> %s\n\r" % (char.player.equipment[_.WEAR_WEAPON].get_name() \
       if char.player.equipment[_.WEAR_WEAPON] is not None else "Nothing")
    buf += "<held> %s\n\r" % (char.player.equipment[_.WEAR_HELD].get_name() \
       if char.player.equipment[_.WEAR_HELD] is not None else "Nothing")
    buf += "<floating nearby> %s\n\r" % (char.player.equipment[_.WEAR_FLOAT].get_name() \
       if char.player.equipment[_.WEAR_FLOAT] is not None else "Nothing")
    buf += "<orbiting nearby> %s\n\r" % (char.player.equipment[_.WEAR_FLOAT2].get_name() \
       if char.player.equipment[_.WEAR_FLOAT2] is not None else "Nothing")

    _.send_to_char(char, buf)


def do_affects(char, args):
    buf = "You are affected by the following:\n\r"
    if not char.player.affects:
        buf += "None\n\r"
    else:
        for a in char.player.affects:
            buf += "%s: %s for %s rounds\n\r" % (a.name, a.desc, int(a.duration / 4))
    buf += "\n\r"
    _.send_to_char(char, buf)


def do_drop(char, args):
    import item

    try:
        target = args.split()[0]
    except IndexError:
        _.send_to_char(char, "Drop what?\n\r")
        return
    try:
        temp_item = item.get_item_in_inventory(char, target)
        _.send_to_char(char, "You drop %s.\n\r" % temp_item.get_name())
        _.send_to_room_except("%s drops %s.\n\r" % (char.player.get_name(), temp_item.get_name()), char.player.get_room(), [char,])
        char.player.get_room().add_item(temp_item)
        char.player.remove_item(temp_item)
    except AttributeError:
        _.send_to_char(char, "You're not carrying that.\n\r")


def do_remove(char, args):
    import item

    try:
        target = args.split()[0]
    except IndexError:
        _.send_to_char(char, "Remove what?\n\r")
        return
    try:
        temp_slot = item.get_item_slot_in_equipment(char, target)
        _.send_to_char(char, "You stop using %s.\n\r" % char.player.equipment[temp_slot].get_name())
        _.send_to_room_except("%s stops using %s.\n\r" % (char.player.get_name(), char.player.equipment[temp_slot].get_name()), \
                              char.player.get_room(), [char,])
        char.player.add_item(char.player.equipment[temp_slot])
        char.player.equipment[temp_slot] = None
    except KeyError:
        _.send_to_char(char, "You're not wearing that.\n\r")


def do_kill(char, args):
    import mobile
    import combat

    if char.player.fighting is not None:
        _.send_to_char(char, "You are already fighting!\n\r")
        return
    try:
        target = args.split()[0]
    except IndexError:
        _.send_to_char(char, "Kill whom?\n\r")
        return
    temp_target = mobile.get_mobile_in_room(target, char.player.get_room())
    if temp_target is None:
        _.send_to_char(char, "They aren't here.\n\r")
        return
    elif temp_target == char.player:
        _.send_to_char(char, "Suicide is a mortal sin.\n\r")
        return
    combat.start_combat(char.player, temp_target)
    temp_vector = temp_target.get_peer()
    combat.start_combat_block()
    if temp_vector is not None:
        do_yell(temp_vector, "Help! I am being attacked by %s!" % char.player.get_name())
    combat.do_one_round(char.player)
    combat.end_combat_block()


def do_flee(char, args):
    import combat
    if char.player.fighting is None:
        _.send_to_char(char, "You aren't fighting anyone.\n\r")
        return
    if char.player.get_room().random_exit() is None or random.randint(0,4) == 0:
        _.send_to_char(char, "PANIC! You couldn't escape!\n\r")
        return
    else:
        combat.start_combat_block()
        _.send_to_char(char, "You flee from combat!\n\r")  #  -Rework- to make you flee out of the room
        _.send_to_room_except("%s has fled!\n\r" % char.player.get_name(), char.player.get_room(), [char,])
        char.player.remove_from_combat()
        do_move(char, char.player.get_room().random_exit())
        combat.end_combat_block()


def do_sleep(char, args):
    temp_position = char.player.get_position()
    if temp_position == _.POS_SLEEPING:
        _.send_to_char(char, "You're already asleep!\n\r")
    elif temp_position == _.POS_RESTING or temp_position == _.POS_STANDING:
        _.send_to_char(char, "You go to sleep.\n\r")
        _.send_to_room_except("%s goes to sleep.\n\r" % char.player.get_name(), char.player.get_room(), [char,])
        char.player.set_position(_.POS_SLEEPING)
    elif temp_position == _.POS_FIGHTING:
        _.send_to_char(char, "You are still fighting!\n\r")


def do_stand(char, args):
    temp_position = char.player.get_position()
    if temp_position == _.POS_SLEEPING:
        _.send_to_char(char, "You wake and stand up.\n\r")
        _.send_to_room_except("%s wakes and stands up.\n\r" % char.player.get_name(), char.player.get_room(), [char,])
        char.player.set_position(_.POS_STANDING)
    elif temp_position == _.POS_RESTING:
        _.send_to_char(char, "You stand up.\n\r")
        _.send_to_room_except("%s stands up.\n\r" % char.player.get_name(), char.player.get_room(), [char,])
        char.player.set_position(_.POS_STANDING)
    elif temp_position == _.POS_FIGHTING or temp_position == _.POS_STANDING:
        _.send_to_char(char, "You are already standing.\n\r")


def do_wake(char, args):
    import mobile
    temp_target = char.player
    if len(args.split()) > 0:
        temp_target = mobile.get_mobile_in_room(args.split()[0], char.player.get_room())
    if temp_target is None:
        _.send_to_char(char, "They aren't here.\n\r")
        return
    temp_position = temp_target.get_position()
    if temp_target.affected_by(_.affect_list["sap"]):
        if temp_target is char.player:
            _.send_to_char(char, "You can't wake up!\n\r")
        else:
            _.send_to_char(char, "They won't wake up!\n\r")
        return
    temp_vector = temp_target.get_peer()
    if temp_position == _.POS_SLEEPING:
        _.send_to_char(temp_vector, "You wake and stand up.\n\r")
        _.send_to_room_except("%s wakes and stands up.\n\r" % temp_target.get_name(), temp_target.get_room(), [temp_vector,])
        temp_target.set_position(_.POS_STANDING)
        do_look(temp_vector, "")
    elif temp_position == _.POS_RESTING and temp_target is char.player:
        _.send_to_char(temp_vector, "You stand up.\n\r")
        _.send_to_room_except("%s stands up.\n\r" % temp_target.get_name(), temp_target.get_room(), [temp_vector,])
        temp_target.set_position(_.POS_STANDING)
    else:
        if temp_target is char.player:
            _.send_to_char(char, "You aren't sleeping.\n\r")
        else:
            _.send_to_char(char, "They aren't sleeping.\n\r")


def do_rest(char, args):
    temp_position = char.player.get_position()
    if temp_position == _.POS_SLEEPING:
        _.send_to_char(char, "You wake up and start resting.\n\r")
        _.send_to_room_except("%s wakes up and starts resting.\n\r" % char.player.get_name(), char.player.get_room(),
                              [char,])
        char.player.set_position(_.POS_RESTING)
    elif temp_position == _.POS_RESTING:
        _.send_to_char(char, "You are already resting.\n\r")
    elif temp_position == _.POS_STANDING:
        _.send_to_char(char, "You rest.\n\r")
        _.send_to_room_except("%s rests.\n\r" % char.player.get_name(), char.player.get_room(),
                              [char,])
        char.player.set_position(_.POS_RESTING)
    elif temp_position == _.POS_STANDING:
        _.send_to_char(char, "You are still fighting!\n\r")


def do_cast(char, args):
    try:
        spell_name = args.split()[0]
    except IndexError:
        _.send_to_char(char, "What spell do you want to cast?\n\r")
        return
    for s in _.spell_list_sorted:
        if s not in char.player.get_spells():
            continue
        if len(s) >= len(spell_name):
            if spell_name == s[:len(spell_name)]:
                _.spell_list[s].execute_spell(char, "".join(args.split()[1:]))
                break
    else:
        _.send_to_char(char, "You don't know any spells by that name.\n\r")


class Command():
    def __init__(self, function, position, lag, in_combat=True):
        self.function = function
        self.position = position
        self.lag = lag
        self.in_combat = in_combat

    def execute_command(self, char, args):
        if char.player.get_position() == _.POS_FIGHTING and not self.in_combat:
            _.send_to_char(char, "No way! You are already fighting!\n\r")
            return
        if char.player.get_position() < self.position:
            if char.player.get_position() == _.POS_SLEEPING:
                _.send_to_char(char, "You can't do that, you're sleeping!\n\r")
            elif char.player.get_position() == _.POS_RESTING:
                _.send_to_char(char, "Nah...you're too relaxed.\n\r")
            elif char.player.get_position() == _.POS_STANDING:
                _.send_to_char(char, "You aren't fighting anyone.\n\r")
            return
        self.function(char, args)
        char.player.add_lag(self.lag)


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
    _.command_list["inventory"] = Command(do_inventory, _.POS_SLEEPING, 0)
    _.command_list["affects"] = Command(do_affects, _.POS_SLEEPING, 0)
    _.command_list["equipment"] = Command(do_equipment, _.POS_SLEEPING, 0)
    _.command_list["score"] = Command(do_score, _.POS_SLEEPING, 0)
    _.command_list["skills"] = Command(do_skills, _.POS_SLEEPING, 0)
    _.command_list["spells"] = Command(do_spells, _.POS_SLEEPING, 0)
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
    _.command_list["quit"] = Command(do_quit, _.POS_SLEEPING, 0, False)
    #  Position
    _.command_list["stand"] = Command(do_stand, _.POS_SLEEPING, 0)
    _.command_list["wake"] = Command(do_wake, _.POS_SLEEPING, 0)
    _.command_list["rest"] = Command(do_rest, _.POS_SLEEPING, 0, False)
    _.command_list["sleep"] = Command(do_sleep, _.POS_SLEEPING, 0, False)

    #  Populate sorted list
    _.command_list_sorted = sorted(_.command_list)