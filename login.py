__author__ = 'ohell_000'


import globals as _


def parse_name1(peer, input_string):
    try:
        input_string = input_string.split()[0].strip()
    except IndexError:
        peer.peer_send("Illegal name.\n\rBy what name do you wish to be known? ", False, True)
        return
    if input_string != ''.join(c for c in input_string if c in _.VALID_CHARS):
        peer.peer_send("Illegal name.\n\rBy what name do you wish to be known? ", False, True)
        return

    #  See if player exists
    if peer.player.load(input_string):
        peer.peer_send("\n\rPassword: ", False, True)
        peer.login_state = _.LOGIN_PASSWORD
        return
    else:
        peer.player.stats["name"] = input_string.capitalize()
        peer.peer_send("\n\rDid I get that right, %s? (Y/N) " % peer.player.stats["name"], False, True)
        peer.login_state = _.LOGIN_NAME2
        return


def parse_password(peer, input_string):
    temp_password = input_string.split()[0].strip()
    if temp_password == peer.account.password:
        peer.peer_send(("You have %i gold and the following active players:\n\r" % peer.account.gold) +
                       str(peer.account.players)+ " ", False, True)
        peer.login_state = _.LOGIN_LIST_CHARS
        return
    else:
        peer.password_count += 1
        if peer.password_count >= _.MAX_PASSWORDS:
            peer.peer_send("\n\rIncorrect password.\n\r", False, True)
            peer.login_state = _.STATE_QUIT
            return
        else:
            peer.peer_send("\n\rIncorrect password. Password: ", False, True)
            return


def parse_new_password1(peer, input_string):
    peer.account.password = input_string.split()[0].strip()
    peer.peer_send("\n\rPlease retype password: ", False, True)
    peer.login_state = _.LOGIN_NEW_PASSWORD2


def parse_new_password2(peer, input_string):
    temp_password = input_string.split()[0].strip()
    if temp_password == peer.account.password:
        peer.account.save()
        peer.peer_send("New account.\n\You have the following active characters:\n\r" +
                       str(peer.account.players)+ " ", False, True)
        peer.login_state = _.LOGIN_LIST_CHARS
    else:
        peer.peer_send("\n\rPasswords don't match. Disconnecting.", False, True)
        peer.login_state = _.STATE_QUIT


def parse_name2(peer, input_string):
    temp_answer = input_string[0].lower().strip()
    if temp_answer == "y":
        print("New character.")
        peer.peer_send("New character.\n\rPlease choose a password: ", False, True)
        peer.login_state = _.LOGIN_NEW_PASSWORD1

    elif temp_answer == "n":
        peer.peer_send("\n\rAlright, what is it then? ", False, True)
        peer.login_state = _.LOGIN_NAME1
    else:
        peer.peer_send("\n\rPlease answer yes or no. ", False, True)


def parse_race(peer, input_string):
    try:
        input_string = input_string.split()[0]
    except IndexError:
        peer.peer_send("\n\rThat's not a valid race. Choose from the following races:\n\r" +
                             str(_.race_list) + " ", False, True)
        return

    for r in _.race_list:
        if len(input_string) > 0 and input_string == r[:min(len(r), len(input_string))]:
            peer.player.stats["race"] = r
            peer.peer_send("\n\rChoose from the following classes:\n\r" + str(_.class_list) + " ", False, True)
            peer.login_state = _.LOGIN_CLASS
            break
    else:
        peer.peer_send("\n\rThat's not a valid race. Choose from the following races:\n\r" +
                             str(_.race_list) + " ", False, True)


def parse_class(peer, input_string):
    import commands
    try:
        input_string = input_string.split()[0]
    except IndexError:
        peer.peer_send("\n\rThat's not a valid class. Choose from the following classes:\n\r" +
                             str(_.class_list) + " ", False, True)
        return

    for c in _.class_list:
        if len(input_string) > 0 and input_string == c[:min(len(c), len(input_string))]:
            peer.player.stats["class"] = c
            peer.peer_send("\n\rWelcome to Redemption!\n\rPlease don't feed the mobiles.\n\r\n\r", False, True)
            #  Save new character
            peer.save()
            peer.game_state = _.STATE_ONLINE
            _.mobiles.append(peer.player)
            _.send_to_room_except("%s has entered the game.\n\r" % peer.player.get_name(), peer.player.get_room(),
                                  [peer,])
            commands.do_look(peer, "")
            break
    else:
        peer.peer_send("\n\rThat's not a valid class. Choose from the following classes:\n\r" +
                             str(_.class_list) + " ", False, True)


def parse_account_name1(peer, input_string):
    try:
        input_string = input_string.split()[0].strip()
    except IndexError:
        peer.peer_send("Illegal account name.\n\rBy what name do you wish to be known? ", False, True)
        return
    if input_string != ''.join(c for c in input_string if c in _.VALID_CHARS):
        peer.peer_send("Illegal name.\n\rBy what name do you wish to be known? ", False, True)
        return

    #  See if player exists
    if peer.account.load(input_string):
        peer.peer_send("\n\rAccount found.\n\rPassword: \n\r", False, True)
        peer.login_state = _.LOGIN_PASSWORD
        return
    else:
        peer.account.name = input_string
        peer.peer_send("\n\rDid I get that right, %s? (Y/N) " % peer.temp_account_name, False, True)
        peer.login_state = _.LOGIN_ACCOUNT2
        return


def parse_account_name2(peer, input_string):
    temp_answer = input_string[0].lower().strip()
    if temp_answer == "y":
        print("New account.")
        peer.peer_send("New account.\n\rPlease choose a password: ", False, True)
        peer.login_state = _.LOGIN_NEW_PASSWORD1

    elif temp_answer == "n":
        peer.peer_send("\n\rAlright, what is it then? ", False, True)
        peer.login_state = _.LOGIN_ACCOUNT1
    else:
        peer.peer_send("\n\rPlease answer yes or no. ", False, True)


def parse_char(peer, input_string):
    import commands

    try:
        input_string = input_string.split()[0].lower()
    except IndexError:
        peer.peer_send("\n\rYou don't have a character by that name.\n\rYou have the following active \
                             characters:\n\r" + str(peer.account.players), False, True)
        return

    for c in peer.account.players:
        if c == input_string:
            if peer.account.player.load(input_string):
                print("Character found and loaded.")
                peer.peer_send("\n\rWelcome to Redemption!\n\rPlease don't feed the mobiles.\n\r\n\r", False, True)
                peer.game_state = _.STATE_ONLINE
                _.mobiles.append(peer.player)
                for p in [p for p in _.peers if p.player.get_room() == peer.player.get_room() and p is not peer]:
                    peer.peer_send(p, "%s has entered the game.\n\r" % peer.player.get_name(p.player).capitalize())
                commands.do_look(peer, "")
                break
            else:
                print("Character found but loading failed.")
    else:
        peer.peer_send("\n\rYou don't have a character by that name.\n\rYou have the following active \
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