__author__ = 'ohell_000'


import globals as _


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
    if char.player.load(input_string):
        _.send_to_char(char, "\n\rPassword: ", False, True)
        char.login_state = _.LOGIN_PASSWORD
        return
    else:
        char.player.stats["name"] = input_string.capitalize()
        _.send_to_char(char, "\n\rDid I get that right, %s? (Y/N) " % char.player.stats["name"], False, True)
        char.login_state = _.LOGIN_NAME2
        return


def parse_password(peer, input_string):
    temp_password = input_string.split()[0].strip()
    if temp_password == peer.account.password:
        _.send_to_char(peer, ("You have %i gold and the following active players:\n\r" % peer.account.gold) +
                       str(peer.account.players)+ " ", False, True)
        peer.login_state = _.LOGIN_LIST_CHARS
        return
    else:
        peer.password_count += 1
        if peer.password_count >= _.MAX_PASSWORDS:
            _.send_to_char(peer, "\n\rIncorrect password.\n\r", False, True)
            peer.login_state = _.STATE_QUIT
            return
        else:
            _.send_to_char(peer, "\n\rIncorrect password. Password: ", False, True)
            return


def parse_new_password1(peer, input_string):
    peer.account.password = input_string.split()[0].strip()
    _.send_to_char(peer, "\n\rPlease retype password: ", False, True)
    peer.login_state = _.LOGIN_NEW_PASSWORD2


def parse_new_password2(peer, input_string):
    temp_password = input_string.split()[0].strip()
    if temp_password == peer.account.password:
        peer.account.save()
        _.send_to_char(peer, "New account.\n\You have the following active characters:\n\r" +
                       str(peer.account.players)+ " ", False, True)
        peer.login_state = _.LOGIN_LIST_CHARS
    else:
        _.send_to_char(peer, "\n\rPasswords don't match. Disconnecting.", False, True)
        peer.login_state = _.STATE_QUIT


def parse_name2(char, input_string):
    temp_answer = input_string[0].lower().strip()
    if temp_answer == "y":
        print("New character.")
        _.send_to_char(char, "New character.\n\rPlease choose a password: ", False, True)
        char.login_state = _.LOGIN_NEW_PASSWORD1

    elif temp_answer == "n":
        _.send_to_char(char, "\n\rAlright, what is it then? ", False, True)
        char.login_state = _.LOGIN_NAME1
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
            char.login_state = _.LOGIN_CLASS
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
            char.save()
            char.game_state = _.STATE_ONLINE
            _.mobiles.append(char.player)
            _.send_to_room_except("%s has entered the game.\n\r" % char.player.get_name(), char.player.get_room(),
                                  [char,])
            commands.do_look(char, "")
            break
    else:
        _.send_to_char(char, "\n\rThat's not a valid class. Choose from the following classes:\n\r" +
                             str(_.class_list) + " ", False, True)


def parse_account_name1(peer, input_string):
    try:
        input_string = input_string.split()[0].strip()
    except IndexError:
        _.send_to_char(peer, "Illegal account name.\n\rBy what name do you wish to be known? ", False, True)
        return
    if input_string != ''.join(c for c in input_string if c in _.VALID_CHARS):
        _.send_to_char(peer, "Illegal name.\n\rBy what name do you wish to be known? ", False, True)
        return

    #  See if player exists
    if peer.account.load(input_string):
        _.send_to_char(peer, "\n\rAccount found.\n\rPassword: \n\r", False, True)
        peer.login_state = _.LOGIN_PASSWORD
        return
    else:
        peer.account.name = input_string
        _.send_to_char(peer, "\n\rDid I get that right, %s? (Y/N) " % peer.temp_account_name, False, True)
        peer.login_state = _.LOGIN_ACCOUNT2
        return


def parse_account_name2(peer, input_string):
    temp_answer = input_string[0].lower().strip()
    if temp_answer == "y":
        print("New account.")
        _.send_to_char(peer, "New account.\n\rPlease choose a password: ", False, True)
        peer.login_state = _.LOGIN_NEW_PASSWORD1

    elif temp_answer == "n":
        _.send_to_char(peer, "\n\rAlright, what is it then? ", False, True)
        peer.login_state = _.LOGIN_ACCOUNT1
    else:
        _.send_to_char(peer, "\n\rPlease answer yes or no. ", False, True)


def parse_char(peer, input_string):
    import commands

    try:
        input_string = input_string.split()[0].lower()
    except IndexError:
        _.send_to_char(peer, "\n\rYou don't have a character by that name.\n\rYou have the following active \
                             characters:\n\r" + str(peer.account.players), False, True)
        return

    for c in peer.account.players:
        if c == input_string:
            if peer.account.player.load(input_string):
                print("Character found and loaded.")
                _.send_to_char(peer, "\n\rWelcome to Redemption!\n\rPlease don't feed the mobiles.\n\r\n\r", False, True)
                peer.game_state = _.STATE_ONLINE
                _.mobiles.append(peer.player)
                for p in [p for p in _.peers if p.player.get_room() == peer.player.get_room() and p is not peer]:
                    _.send_to_char(p, "%s has entered the game.\n\r" % peer.player.get_name(p.player).capitalize())
                commands.do_look(peer, "")
                break
            else:
                print("Character found but loading failed.")
    else:
        _.send_to_char(peer, "\n\rYou don't have a character by that name.\n\rYou have the following active \
                             characters:\n\r" + str(peer.account.players), False, True)


def handle_login(peer, input_string):
    if peer.login_state == _.LOGIN_ACCOUNT1:
        parse_account_name1(peer, peer.input_buffer)
    elif peer.login_state == _.LOGIN_ACCOUNT2:
        parse_account_name2(peer, peer.input_buffer)
    # Check state to handle login input_string
    elif peer.login_state == _.LOGIN_NAME1:
        parse_name1(peer, peer.input_buffer)
    elif peer.login_state == _.LOGIN_NAME2:
        parse_name2(peer, peer.input_buffer)
    elif peer.login_state == _.LOGIN_PASSWORD:
        parse_password(peer, peer.input_buffer)
    elif peer.login_state == _.LOGIN_NEW_PASSWORD1:
        parse_new_password1(peer, peer.input_buffer)
    elif peer.login_state == _.LOGIN_NEW_PASSWORD2:
        parse_new_password2(peer, peer.input_buffer)
    elif peer.login_state == _.LOGIN_RACE:
        parse_race(peer, peer.input_buffer)
    elif peer.login_state == _.LOGIN_CLASS:
        parse_class(peer, peer.input_buffer)
    elif peer.login_state == _.LOGIN_LIST_CHARS:
        parse_char(peer, peer.input_buffer)