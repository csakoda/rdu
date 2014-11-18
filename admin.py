__author__ = 'ohell_000'


import globals as _
import item
import copy
import update
import commands
import skills
import spells
import affects
import area
import random
import races
import classes
import mobile


def start_game():
    print("Loading mobiles...")
    mobile.initialize_mobiles()
    print("Loading areas...")
    area.initialize_area()
    print("Loading items...")
    item.initialize_items()
    print("Loading races...")
    races.initialize_races()
    print("Loading classes...")
    classes.initialize_classes()
    print("Initializing commands...")
    commands.initialize_commands()
    print("Initializing skills...")
    skills.initialize_skills()
    print("Initializing spells...")
    spells.initialize_spells()
    print("Initializing affects...")
    affects.initialize_affects()
    print("Seeding random...")
    random.seed()
    #  Sort dictionaries
    _.race_list = sorted(r.get_name() for r in _.races)
    _.class_list = sorted(c.get_name() for c in _.classes)
    #  Initialize combat loop
    update.UpdateLoop().start()

    for r in _.rooms:  # -Debug-
        temp_item = item.Item("", "", "", "", "")
        temp_item = copy.deepcopy(random.choice(_.items))
        r.add_item(temp_item)


def parse_command(char, input_string):
    if input_string != ''.join(c for c in input_string if c in _.VALID_CHARS):
        return True
    command = input_string.split()
    if len(command) > 0:
        command = command[0]
    args = input_string[len(command) + 1:]
    for c in _.command_list_sorted:
        #  First check commands
        if len(c) >= len(command):
            if command == c[:len(command)]:
                _.command_list[c].execute_command(char, args)
                break
    else:
        #  Then check skills
        for s in _.skill_list_sorted:
            if s not in char.player.get_skills():
                continue
            if len(s) >= len(command):
                if command == s[:len(command)]:
                    _.skill_list[s].execute_skill(char, args)
                    break
        else:
            return True  #  command not found


def save_char(char):
    import os
    if not os.path.exists('players'):
        os.makedirs('players')
    f = open("players/" + char.player.stats["name"] + ".dat","w")
    for s in char.player.stats:
        f.write("%s:^:%s%s\n" % (s, "" if type(char.player.stats[s]) is str else "(*int)", char.player.stats[s]))
    for i in char.player.inventory:
        f.write("item:^:%s\n" % i.vnum)
    for a in char.player.affects:
        f.write("affect:^:%s:^:%s\n" % (a.name, a.duration))
    for e in char.player.equipment:
        if char.player.equipment[e] is not None:
            f.write("equipment:^:%s:^:%s\n" % (char.player.equipment[e].vnum, e))
    f.close()


def load_char(char, input_string):
    import player
    try:
        f = open("players/" + input_string + ".dat", "r")
        print("File found, loading character.")
        char.player = player.Player()
        lines = f.readlines()
        for l in lines:
            temp_key = l.split(":^:")[0].strip()
            if temp_key == "item":
                temp_vnum = l.split(":^:")[1].strip()
                temp_item = copy.deepcopy(item.get_item_by_vnum(temp_vnum))
                if temp_item is not None:
                    char.player.inventory.append(temp_item)
            elif temp_key == "affect":
                temp_affect = l.split(":^:")[1].strip()
                temp_duration = int(float(l.split(":^:")[2].strip()))
                try:
                    _.affect_list[temp_affect].apply_affect(char.player,temp_duration)
                except KeyError:
                    print("Illegal affect found. Skipping.")
            elif temp_key == "equipment":
                try:
                    temp_vnum = l.split(":^:")[1].strip()
                    temp_item = copy.deepcopy(item.get_item_by_vnum(temp_vnum))
                    temp_slot = int(l.split(":^:")[2].strip())
                    if temp_item is not None:
                        char.player.equipment[temp_slot] = temp_item
                except IndexError:
                    print("Illegal equipment found. Skipping.")
            else:
                temp_key = l.split(":^:")[0].strip()
                temp_value = l.split(":^:")[1].strip()
                if "(*int)" in temp_value:
                    temp_value = temp_value[6:]
                    temp_value = int(temp_value)
                char.player.stats[temp_key] = temp_value
    except FileNotFoundError:
        print("File not found.")
        return False
    f.close()
    return True


def parse_name1(char, input_string):
    try:
        input_string = input_string.split()[0].strip()
    except IndexError:
        _.send_to_char(char, "Illegal name.\n\rBy what name do you wish to be known? ", False, True)
        return
    if input_string != ''.join(c for c in input_string if c in _.VALID_CHARS):
        _.send_to_char(char, "Illegal name.\n\rBy what name do you wish to be known? ", False, True)
        return

    #  See if player exists
    if load_char(char, input_string):
        _.send_to_char(char, "\n\rPassword: ", False, True)
        char.state = _.STATE_PASSWORD
        return
    else:
        char.player.stats["name"] = input_string.capitalize()
        _.send_to_char(char, "\n\rDid I get that right, %s? (Y/N) " % char.player.stats["name"], False, True)
        char.state = _.STATE_NAME2
        return


def parse_password(char, input_string):
    import commands
    import player
    temp_password = input_string.split()[0].strip()
    if temp_password == char.player.stats["password"]:
        #  Check if character is already connected
        temp_player = player.get_player(char.player.get_name())
        if temp_player is not None:
            char.player = temp_player
            temp_player.get_peer().quit()
            _.send_to_char(char, "\n\rReconnecting.", False, True)
        _.send_to_char(char, "\n\rWelcome to Redemption!\n\rPlease don't feed the mobiles.\n\r\n\r", False, True)
        char.state = _.STATE_ONLINE
        _.mobiles.append(char.player)
        for p in [p for p in _.peers if p.player.get_room() == char.player.get_room() and p is not char]:
            _.send_to_char(p, "%s has entered the game.\n\r" % char.player.get_name(p.player).capitalize())
        commands.do_look(char, "")
        return
    else:
        char.password_count += 1
        if char.password_count >= _.MAX_PASSWORDS:
            _.send_to_char(char, "\n\rIncorrect password.\n\r", False, True)
            char.state = _.STATE_QUIT
            return
        else:
            _.send_to_char(char, "\n\rIncorrect password. Password: ", False, True)
            return


def parse_new_password1(char, input_string):
    char.player.stats["password"] = input_string.split()[0].strip()
    _.send_to_char(char, "\n\rPlease retype password: ", False, True)
    char.state = _.STATE_NEW_PASSWORD2

def parse_new_password2(char, input_string):
    temp_password = input_string.split()[0].strip()
    if temp_password == char.player.stats["password"]:
        _.send_to_char(char, "New character.\n\rChoose from the following races:\n\r" + str(_.race_list)+ " ",
                       False, True)
        char.state = _.STATE_RACE
    else:
        _.send_to_char(char, "\n\rPasswords don't match. Disconnecting.", False, True)
        char.state = _.STATE_QUIT


def parse_name2(char, input_string):
    temp_answer = input_string[0].lower().strip()
    if temp_answer == "y":
        print("New character.")
        _.send_to_char(char, "New character.\n\rPlease choose a password: ", False, True)
        char.state = _.STATE_NEW_PASSWORD1

    elif temp_answer == "n":
        _.send_to_char(char, "\n\rAlright, what is it then? ", False, True)
        char.state = _.STATE_NAME1
    else:
        _.send_to_char(char, "\n\rPlease answer yes or no. ", False, True)


def parse_race(char, input_string):
    try:
        input_string = input_string.split()[0]
    except IndexError:
        _.send_to_char(char, "\n\rThat's not a valid race. Choose from the following races:\n\r" +
                             str(_.race_list) + " ", False, True)
        return

    for r in _.race_list:
        if len(input_string) > 0 and input_string == r[:min(len(r), len(input_string))]:
            char.player.stats["race"] = r
            _.send_to_char(char, "\n\rChoose from the following classes:\n\r" + str(_.class_list) + " ", False, True)
            char.state = _.STATE_CLASS
            break
    else:
        _.send_to_char(char, "\n\rThat's not a valid race. Choose from the following races:\n\r" +
                             str(_.race_list) + " ", False, True)


def parse_class(char, input_string):
    import commands
    try:
        input_string = input_string.split()[0]
    except IndexError:
        _.send_to_char(char, "\n\rThat's not a valid class. Choose from the following classes:\n\r" +
                             str(_.class_list) + " ", False, True)
        return

    for c in _.class_list:
        if len(input_string) > 0 and input_string == c[:min(len(c), len(input_string))]:
            char.player.stats["class"] = c
            _.send_to_char(char, "\n\rWelcome to Redemption!\n\rPlease don't feed the mobiles.\n\r\n\r", False, True)
            #  Save new character
            save_char(char)
            char.state = _.STATE_ONLINE
            _.mobiles.append(char.player)
            _.send_to_room_except("%s has entered the game.\n\r" % char.player.get_name(), char.player.get_room(),
                                  [char,])
            commands.do_look(char, "")
            break
    else:
        _.send_to_char(char, "\n\rThat's not a valid class. Choose from the following classes:\n\r" +
                             str(_.class_list) + " ", False, True)